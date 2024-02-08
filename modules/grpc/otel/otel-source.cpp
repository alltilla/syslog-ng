/*
 * Copyright (c) 2023 Attila Szakacs
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */

#include "otel-source.hpp"
#include "otel-source-services.hpp"
#include "credentials/grpc-credentials-builder.hpp"

#include "compat/cpp-start.h"
#include "messages.h"
#include "compat/cpp-end.h"

#include <string>

#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/ext/channelz_service_plugin.h>

#define get_SourceDriver(s) (((OtelSourceDriver *) s)->cpp)
#define get_SourceWorker(s) (((OtelSourceWorker *) s)->cpp)

using namespace syslogng::grpc::otel;

/* C++ Implementations */

syslogng::grpc::otel::SourceDriver::SourceDriver(OtelSourceDriver *s)
  : super(s)
{
  credentials_builder_wrapper.self = &credentials_builder;
}

void
syslogng::grpc::otel::SourceDriver::request_exit()
{
  if (server == nullptr)
    return;

  server->Shutdown();
  server = nullptr;
}

void
syslogng::grpc::otel::SourceDriver::format_stats_key(StatsClusterKeyBuilder *kb)
{
  stats_cluster_key_builder_add_legacy_label(kb, stats_cluster_label("driver", "opentelemetry"));

  gchar num[64];
  g_snprintf(num, sizeof(num), "%" G_GUINT64_FORMAT, port);
  stats_cluster_key_builder_add_legacy_label(kb, stats_cluster_label("port", num));
}

const char *
syslogng::grpc::otel::SourceDriver::generate_persist_name()
{
  static char persist_name[1024];

  if (super->super.super.super.super.persist_name)
    g_snprintf(persist_name, sizeof(persist_name), "opentelemetry.%s",
               super->super.super.super.super.persist_name);
  else
    g_snprintf(persist_name, sizeof(persist_name), "opentelemetry(%" G_GUINT64_FORMAT ")",
               port);

  return persist_name;
}

gboolean
syslogng::grpc::otel::SourceDriver::init()
{
  if (!credentials_builder.validate())
    return FALSE;

  std::string address = std::string("[::]:").append(std::to_string(port));

  ::grpc::EnableDefaultHealthCheckService(true);

  ::grpc::ServerBuilder builder;
  builder.AddListeningPort(address, credentials_builder.build());

  resource_quota.SetMaxThreads(32);
  builder.SetResourceQuota(resource_quota);

  for (auto nv : int_extra_channel_args)
    builder.AddChannelArgument(nv.first, nv.second);
  for (auto nv : string_extra_channel_args)
    builder.AddChannelArgument(nv.first, nv.second);

  if (enable_channelz)
    ::grpc::channelz::experimental::InitChannelzService();

  builder.RegisterService(&trace_service);
  builder.RegisterService(&logs_service);
  builder.RegisterService(&metrics_service);

  for (size_t i = 0; i < super->super.num_workers; i++)
    cqs.push_back(std::move(builder.AddCompletionQueue()));

  server = builder.BuildAndStart();
  if (!server)
    {
      msg_error("Failed to start OpenTelemetry server", evt_tag_int("port", port));
      return false;
    }

  msg_info("OpenTelemetry server accepting connections", evt_tag_int("port", port));

  super->super.worker_options.super.init_window_size /= super->super.num_workers;

  if (fetch_limit == -1)
    fetch_limit = super->super.worker_options.super.init_window_size;

  return log_threaded_source_driver_init_method(&super->super.super.super.super);
}

gboolean
syslogng::grpc::otel::SourceDriver::deinit()
{
  return log_threaded_source_driver_deinit_method(&super->super.super.super.super);
}

void
SourceDriver::add_extra_channel_arg(std::string name, long value)
{
  int_extra_channel_args.push_back(std::pair<std::string, long>{name, value});
}

void
SourceDriver::add_extra_channel_arg(std::string name, std::string value)
{
  string_extra_channel_args.push_back(std::pair<std::string, std::string>{name, value});
}

GrpcServerCredentialsBuilderW *
SourceDriver::get_credentials_builder_wrapper()
{
  return &credentials_builder_wrapper;
}

SourceWorker::SourceWorker(OtelSourceWorker *s, SourceDriver &d)
  : super(s), driver(d)
{
  cq = std::move(driver.cqs.front());
  driver.cqs.pop_front();
}

#include <chrono>
void
syslogng::grpc::otel::SourceWorker::run()
{
  /* Proceed() will immediately create a new ServiceCall,
   * so creating 1 ServiceCall here results in 2 concurrent requests.
   *
   * Because of this we should create (concurrent_requests - 1) ServiceCalls here.
   */
  for (size_t i = 0; i < driver.concurrent_requests - 1; i++)
    {
      new TraceServiceCall(*this, &driver.trace_service, cq.get());
      new LogsServiceCall(*this, &driver.logs_service, cq.get());
      new MetricsServiceCall(*this, &driver.metrics_service, cq.get());
    }

  void *tag;
  bool ok;

  auto last_next_returned_at = std::chrono::high_resolution_clock::now();

  while (cq->Next(&tag, &ok))
    {
      auto now = std::chrono::high_resolution_clock::now();
      msg_error("SourceWorker::run: Next() returned", evt_tag_int("worker_index", this->super->super.worker_index),
        evt_tag_int("was_blocked_for_ms", std::chrono::duration_cast<std::chrono::milliseconds>(now - last_next_returned_at).count()));
      last_next_returned_at = now;

      static_cast<AsyncServiceCallInterface *>(tag)->Proceed(ok);
    }
}

void
syslogng::grpc::otel::SourceWorker::request_exit()
{
  driver.request_exit();
  cq->Shutdown();
}

bool
SourceWorker::post(LogMessage *msg)
{
  log_threaded_source_worker_blocking_post(&super->super, msg);
  return true;
}

/* Config setters */

void
otel_sd_set_port(LogDriver *s, guint64 port)
{
  get_SourceDriver(s)->port = port;
}

void
otel_sd_set_fetch_limit(LogDriver *s, gint fetch_limit)
{
  get_SourceDriver(s)->fetch_limit = fetch_limit;
}

void
otel_sd_set_concurrent_requests(LogDriver *s, gint concurrent_requests)
{
  get_SourceDriver(s)->concurrent_requests = concurrent_requests;
}

void
otel_sd_add_int_channel_arg(LogDriver *s, const gchar *name, gint64 value)
{
  get_SourceDriver(s)->add_extra_channel_arg(name, value);
}

void
otel_sd_add_string_channel_arg(LogDriver *s, const gchar *name, const gchar *value)
{
  get_SourceDriver(s)->add_extra_channel_arg(name, value);
}

void
otel_sd_set_enable_channelz(LogDriver *s, gboolean enable)
{
  get_SourceDriver(s)->enable_channelz = enable;
}

GrpcServerCredentialsBuilderW *
otel_sd_get_credentials_builder(LogDriver *s)
{
  return get_SourceDriver(s)->get_credentials_builder_wrapper();
}

/* C Wrappers */

static void
_worker_free(LogPipe *s)
{
  delete get_SourceWorker(s);
  log_threaded_source_worker_free(s);
}

static void
_worker_run(LogThreadedSourceWorker *s)
{
  get_SourceWorker(s)->run();
}

static void
_worker_request_exit(LogThreadedSourceWorker *s)
{
  get_SourceWorker(s)->request_exit();
}

static LogThreadedSourceWorker *
_construct_worker(LogThreadedSourceDriver *s, gint worker_index)
{
  OtelSourceWorker *worker = g_new0(OtelSourceWorker, 1);
  log_threaded_source_worker_init_instance(&worker->super, s, worker_index);

  worker->cpp = new SourceWorker(worker, *get_SourceDriver(s));

  worker->super.run = _worker_run;
  worker->super.request_exit = _worker_request_exit;
  worker->super.super.super.free_fn = _worker_free;

  return &worker->super;
}

static void
_format_stats_key(LogThreadedSourceDriver *s, StatsClusterKeyBuilder *kb)
{
  get_SourceDriver(s)->format_stats_key(kb);
}

static const gchar *
_generate_persist_name(const LogPipe *s)
{
  return get_SourceDriver(s)->generate_persist_name();
}

static gboolean
_init(LogPipe *s)
{
  return get_SourceDriver(s)->init();
}

static gboolean
_deinit(LogPipe *s)
{
  return get_SourceDriver(s)->deinit();
}

static void
_free(LogPipe *s)
{
  delete get_SourceDriver(s);
  log_threaded_source_driver_free_method(s);
}

LogDriver *
otel_sd_new(GlobalConfig *cfg)
{
  OtelSourceDriver *s = g_new0(OtelSourceDriver, 1);
  log_threaded_source_driver_init_instance(&s->super, cfg);
  log_threaded_source_driver_set_transport_name(&s->super, "otlp");
  s->cpp = new syslogng::grpc::otel::SourceDriver(s);

  s->super.super.super.super.init = _init;
  s->super.super.super.super.deinit = _deinit;
  s->super.super.super.super.free_fn = _free;
  s->super.super.super.super.generate_persist_name = _generate_persist_name;

  s->super.worker_options.super.stats_source = stats_register_type("opentelemetry");
  s->super.format_stats_key = _format_stats_key;
  s->super.worker_construct = _construct_worker;

  s->super.auto_close_batches = FALSE;

  return &s->super.super.super;
}

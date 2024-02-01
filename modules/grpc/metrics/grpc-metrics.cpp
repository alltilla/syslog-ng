/*
 * Copyright (c) 2024 Attila Szakacs
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

#include "grpc-metrics.hpp"

using namespace syslogng::grpc;

void
DestDriverMetrics::create_grpc_request_counter(StatsClusterKeyBuilder *kb, int stats_level,
                                               const ::grpc::StatusCode &response_code,
                                               const std::string &response_code_label)
{
  stats_cluster_key_builder_push(kb);
  {
    stats_cluster_key_builder_set_name(kb, "output_grpc_requests_total");
    stats_cluster_key_builder_add_label(kb, stats_cluster_label("response_code", response_code_label.c_str()));
    StatsClusterKey *sc_key = stats_cluster_key_builder_build_single(kb);

    stats_lock();
    {
      StatsCounterItem *counter;
      grpc_request_clusters[response_code] = stats_register_counter(stats_level, sc_key, SC_TYPE_SINGLE_VALUE, &counter);
    }
    stats_unlock();
  }
  stats_cluster_key_builder_pop(kb);
}

void
DestDriverMetrics::create_grpc_request_counters(StatsClusterKeyBuilder *kb, int stats_level)
{
  static const std::pair<::grpc::StatusCode, std::string> status_code_name_mappings[] =
  {
    { ::grpc::StatusCode::OK, "ok" },
    { ::grpc::StatusCode::CANCELLED, "cancelled" },
    { ::grpc::StatusCode::UNKNOWN, "unknown" },
    { ::grpc::StatusCode::INVALID_ARGUMENT, "invalid_argument" },
    { ::grpc::StatusCode::DEADLINE_EXCEEDED, "deadline_exceeded" },
    { ::grpc::StatusCode::NOT_FOUND, "not_found" },
    { ::grpc::StatusCode::ALREADY_EXISTS, "already_exists" },
    { ::grpc::StatusCode::PERMISSION_DENIED, "permission_denied" },
    { ::grpc::StatusCode::UNAUTHENTICATED, "unauthenticated" },
    { ::grpc::StatusCode::RESOURCE_EXHAUSTED, "resource_exhausted" },
    { ::grpc::StatusCode::FAILED_PRECONDITION, "failed_precondition" },
    { ::grpc::StatusCode::ABORTED, "aborted" },
    { ::grpc::StatusCode::OUT_OF_RANGE, "out_of_range" },
    { ::grpc::StatusCode::UNIMPLEMENTED, "unimplemented" },
    { ::grpc::StatusCode::INTERNAL, "internal" },
    { ::grpc::StatusCode::UNAVAILABLE, "unavailable" },
    { ::grpc::StatusCode::DATA_LOSS, "data_loss" },
  };

  for (auto status_code_name_mapping : status_code_name_mappings)
    {
      create_grpc_request_counter(kb, stats_level, status_code_name_mapping.first, status_code_name_mapping.second);
    }
}

void
DestDriverMetrics::init(StatsClusterKeyBuilder *kb, int stats_level)
{
  create_grpc_request_counters(kb, stats_level);
}

void
DestDriverMetrics::deinit()
{
  stats_lock();
  {
    for (const auto &clusters : grpc_request_clusters)
      {
        StatsCounterItem *counter = stats_cluster_single_get_counter(clusters.second);
        stats_unregister_counter(&clusters.second->key, SC_TYPE_SINGLE_VALUE, &counter);
      }
  }
  stats_unlock();
}

void
DestDriverMetrics::insert_grpc_request_stats(const ::grpc::Status &response_status)
{
  StatsCounterItem *counter = stats_cluster_single_get_counter(grpc_request_clusters[response_status.error_code()]);
  stats_counter_inc(counter);
}

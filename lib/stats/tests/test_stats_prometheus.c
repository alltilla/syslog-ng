/*
 * Copyright (c) 2023 László Várady
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */

#include <criterion/criterion.h>

#include "syslog-ng.h"
#include "stats/stats.h"
#include "stats/stats-cluster.h"
#include "stats/stats-cluster-single.h"
#include "stats/stats-cluster-logpipe.h"
#include "stats/stats-prometheus.h"
#include "scratch-buffers.h"
#include "mainloop.h"

static void
setup(void)
{
  main_loop_thread_resource_init();
  stats_init();
  scratch_buffers_global_init();
  scratch_buffers_allocator_init();
}

static void
teardown(void)
{
  scratch_buffers_explicit_gc();
  scratch_buffers_allocator_deinit();
  scratch_buffers_global_deinit();
  stats_destroy();
  main_loop_thread_resource_deinit();
}

TestSuite(stats_prometheus, .init = setup, .fini = teardown, .timeout = 300);

static inline StatsCluster *
test_single_cluster(const gchar *name, StatsClusterLabel *labels, gsize labels_len)
{
  StatsClusterKey key;
  stats_cluster_single_key_set(&key, name, labels, labels_len);
  return stats_cluster_new(&key);
}

static inline StatsCluster *
test_logpipe_cluster(const gchar *name, StatsClusterLabel *labels, gsize labels_len)
{
  StatsClusterKey key;
  stats_cluster_logpipe_key_set(&key, name, labels, labels_len);
  return stats_cluster_new(&key);
}

static inline void
assert_prometheus_format(StatsCluster *cluster, gint type,  const gchar *expected_prom_record)
{
  cr_assert_str_eq(stats_prometheus_format_counter(cluster, type, stats_cluster_get_counter(cluster, type))->str,
                   expected_prom_record);
}

Test(stats_prometheus, test_prometheus_format_single)
{
  StatsCluster *cluster = test_single_cluster("test_name", NULL, 0);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_test_name 0\n");
  stats_cluster_free(cluster);

  StatsClusterLabel labels[] = { stats_cluster_label("app", "cisco") };
  cluster = test_single_cluster("test_name", labels, G_N_ELEMENTS(labels));
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_test_name{app=\"cisco\"} 0\n");
  stats_cluster_free(cluster);

  StatsClusterLabel labels2[] =
  {
    stats_cluster_label("app", "cisco"),
    stats_cluster_label("sourceip", "127.0.0.1"),
    stats_cluster_label("customlabel", "value"),
  };
  cluster = test_single_cluster("test_name", labels2, G_N_ELEMENTS(labels2));
  stats_counter_inc(stats_cluster_track_counter(cluster, SC_TYPE_SINGLE_VALUE));
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE,
                           "syslogng_test_name{app=\"cisco\",sourceip=\"127.0.0.1\",customlabel=\"value\"} 1\n");
  stats_cluster_free(cluster);
}

Test(stats_prometheus, test_prometheus_format_logpipe)
{
  StatsCluster *cluster = test_logpipe_cluster("test_name", NULL, 0);
  assert_prometheus_format(cluster, SC_TYPE_PROCESSED, "syslogng_test_name{result=\"processed\"} 0\n");
  stats_cluster_free(cluster);

  StatsClusterLabel labels[] = { stats_cluster_label("app", "cisco") };
  cluster = test_logpipe_cluster("test_name", labels, G_N_ELEMENTS(labels));
  assert_prometheus_format(cluster, SC_TYPE_DROPPED, "syslogng_test_name{app=\"cisco\",result=\"dropped\"} 0\n");
  stats_cluster_free(cluster);

  StatsClusterLabel labels2[] =
  {
    stats_cluster_label("app", "cisco"),
    stats_cluster_label("sourceip", "127.0.0.1"),
    stats_cluster_label("customlabel", "value"),
  };
  cluster = test_logpipe_cluster("test_name", labels2, G_N_ELEMENTS(labels2));
  stats_counter_inc(stats_cluster_track_counter(cluster, SC_TYPE_WRITTEN));
  assert_prometheus_format(cluster, SC_TYPE_WRITTEN,
                           "syslogng_test_name{app=\"cisco\",sourceip=\"127.0.0.1\",customlabel=\"value\","
                           "result=\"delivered\"} 1\n");
  stats_cluster_free(cluster);
}

Test(stats_prometheus, test_prometheus_format_empty_label_value)
{
  StatsClusterLabel labels[] =
  {
    stats_cluster_label("app", ""),
    stats_cluster_label("sourceip", NULL),
    stats_cluster_label("customlabel", "value"),
  };
  StatsCluster *cluster = test_single_cluster("test_name", labels, G_N_ELEMENTS(labels));
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_test_name{customlabel=\"value\"} 0\n");
  stats_cluster_free(cluster);

  StatsClusterLabel labels2[] =
  {
    stats_cluster_label("app", NULL),
    stats_cluster_label("sourceip", ""),
  };
  cluster = test_single_cluster("test_name", labels2, G_N_ELEMENTS(labels2));
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_test_name 0\n");
  stats_cluster_free(cluster);

  cluster = test_logpipe_cluster("test_name", labels2, G_N_ELEMENTS(labels2));
  assert_prometheus_format(cluster, SC_TYPE_PROCESSED, "syslogng_test_name{result=\"processed\"} 0\n");
  stats_cluster_free(cluster);
}

Test(stats_prometheus, test_prometheus_format_sanitize)
{
  StatsClusterLabel labels[] =
  {
    stats_cluster_label("app.name:", "a"),
    stats_cluster_label("//source-ip\n", "\"b\""),
    stats_cluster_label("laűúőbel", "c\n"),
  };
  StatsCluster *cluster = test_single_cluster("test.name-http://localhost/ű#", labels, G_N_ELEMENTS(labels));
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE,
                           "syslogng_test_name_httplocalhost{app_name=\"a\",source_ip=\"\\\"b\\\"\",label=\"c\\n\"} 0\n");
  stats_cluster_free(cluster);
}


Test(stats_prometheus, test_prometheus_format_legacy)
{
  StatsClusterKey key;
  stats_cluster_single_key_legacy_set_with_name(&key, SCS_GLOBAL, "id", NULL, "value");
  StatsCluster *cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_global_id 0\n");
  stats_cluster_free(cluster);

  stats_cluster_single_key_legacy_set_with_name(&key, SCS_GLOBAL, "id", NULL, "custom");
  cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_global_id_custom 0\n");
  stats_cluster_free(cluster);

  stats_cluster_single_key_legacy_set_with_name(&key, SCS_SOURCE | SCS_TAG, "", "instance", "custom");
  cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE,
                           "syslogng_src_tag_custom{stat_instance=\"instance\"} 0\n");
  stats_cluster_free(cluster);

  stats_cluster_single_key_legacy_set_with_name(&key, SCS_SOURCE | SCS_TAG, "id", "instance", "custom");
  cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE,
                           "syslogng_src_tag_custom{id=\"id\",stat_instance=\"instance\"} 0\n");
  stats_cluster_free(cluster);

  stats_cluster_logpipe_key_legacy_set(&key, SCS_SOURCE | SCS_TAG, "id", "instance");
  cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_PROCESSED,
                           "syslogng_src_tag_processed{id=\"id\",stat_instance=\"instance\"} 0\n");
  stats_cluster_free(cluster);
}

Test(stats_prometheus, test_prometheus_format_legacy_alias_is_ignored)
{
  StatsClusterKey key;
  stats_cluster_single_key_set(&key, "name", NULL, 0);
  stats_cluster_single_key_add_legacy_alias_with_name(&key, SCS_SOURCE | SCS_TAG, "", "instance", "custom");
  StatsCluster *cluster = stats_cluster_new(&key);
  assert_prometheus_format(cluster, SC_TYPE_SINGLE_VALUE, "syslogng_name 0\n");
  stats_cluster_free(cluster);
}

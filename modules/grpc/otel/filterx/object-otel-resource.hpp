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

#ifndef OBJECT_OTEL_RESOURCE_HPP
#define OBJECT_OTEL_RESOURCE_HPP

#include "syslog-ng.h"

#include "compat/cpp-start.h"
#include "filterx/filterx-object.h"
#include "object-otel.h"
#include "compat/cpp-end.h"

#include "opentelemetry/proto/resource/v1/resource.pb.h"

typedef struct FilterXOtelResource_ FilterXOtelResource;

FilterXObject *_filterx_otel_resource_clone(FilterXObject *s);

namespace syslogng {
namespace grpc {
namespace otel {
namespace filterx {

class Resource
{
public:
  Resource(FilterXOtelResource *s);
  Resource(FilterXOtelResource *s, FilterXObject *protobuf_object);
  Resource(Resource &o) = delete;
  Resource(Resource &&o) = delete;
  ~Resource();

  std::string marshal();
  bool set_field(const gchar *attribute, FilterXObject *value);
  FilterXObject *get_field(const gchar *attribute);
  const opentelemetry::proto::resource::v1::Resource &get_value() const;

private:
  Resource(const Resource &o, FilterXOtelResource *s);
  friend FilterXObject *::_filterx_otel_resource_clone(FilterXObject *s);
  bool set_schema_url(FilterXObject *value);

private:
  FilterXOtelResource *super;
  opentelemetry::proto::resource::v1::Resource resource;
  FilterXObject *schema_url;
};

}
}
}
}

struct FilterXOtelResource_
{
  FilterXObject super;
  syslogng::grpc::otel::filterx::Resource *cpp;
};

#endif

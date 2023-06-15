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

#include "otel-source-services.hpp"

grpc::Status
OtelSourceTraceService::Export(grpc::ServerContext *context, const ExportTraceServiceRequest *request,
                               ExportTraceServiceResponse *response)
{
  std::cout << "Trace received: " << request->ShortDebugString() << std::endl;
  return grpc::Status::OK;
}

grpc::Status
OtelSourceLogsService::Export(grpc::ServerContext *context, const ExportLogsServiceRequest *request,
                              ExportLogsServiceResponse *response)
{
  std::cout << "Logs received: " << request->ShortDebugString() << std::endl;
  return grpc::Status::OK;
}

grpc::Status
OtelSourceMetricsService::Export(grpc::ServerContext *context, const ExportMetricsServiceRequest *request,
                                 ExportMetricsServiceResponse *response)
{
  std::cout << "Metrics received: " << request->ShortDebugString() << std::endl;
  return grpc::Status::OK;
}

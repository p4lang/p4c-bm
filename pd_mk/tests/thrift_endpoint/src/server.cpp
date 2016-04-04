/* Copyright 2013-present Barefoot Networks, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Antonin Bas (antonin@barefootnetworks.com)
 *
 */

#include <thread>
#include <chrono>

#ifdef P4THRIFT
#include <p4thrift/protocol/TBinaryProtocol.h>
#include <p4thrift/server/TSimpleServer.h>
#include <p4thrift/server/TThreadedServer.h>
#include <p4thrift/transport/TServerSocket.h>
#include <p4thrift/transport/TBufferTransports.h>
#include <p4thrift/processor/TMultiplexedProcessor.h>

namespace thrift_provider = p4::thrift;
#else
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/processor/TMultiplexedProcessor.h>

namespace thrift_provider = apache::thrift;
#endif

#include "Standard_server.ipp"
#include "SimplePreLAG_server.ipp"
#include "SimpleSwitch_server.ipp"

using namespace ::thrift_provider;
using namespace ::thrift_provider::protocol;
using namespace ::thrift_provider::transport;
using namespace ::thrift_provider::server;

using boost::shared_ptr;

using ::bm_runtime::standard::StandardHandler;
using ::bm_runtime::standard::StandardProcessor;
using ::bm_runtime::simple_pre_lag::SimplePreLAGHandler;
using ::bm_runtime::simple_pre_lag::SimplePreLAGProcessor;
using ::sswitch_runtime::SimpleSwitchHandler;
using ::sswitch_runtime::SimpleSwitchProcessor;

void run_server(int port) {
  shared_ptr<StandardHandler> standard_handler(new StandardHandler());
  shared_ptr<SimplePreLAGHandler> simple_pre_lag_handler(new SimplePreLAGHandler());
  shared_ptr<SimpleSwitchHandler> simple_switch_handler(new SimpleSwitchHandler());

  shared_ptr<TMultiplexedProcessor> processor(new TMultiplexedProcessor());
  processor->registerProcessor(
    "standard",
    shared_ptr<TProcessor>(new StandardProcessor(standard_handler))
  );
  processor->registerProcessor(
    "simple_pre_lag",
    shared_ptr<TProcessor>(new SimplePreLAGProcessor(simple_pre_lag_handler))
  );
  processor->registerProcessor(
    "simple_switch",
    shared_ptr<TProcessor>(new SimpleSwitchProcessor(simple_switch_handler))
  );

  shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TThreadedServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
}

int start_server() {
  int port = 9090;
  std::thread t(run_server, port);
  t.detach();
  // I have discovered that on slower machine, the server does not have time to
  // start, and I try to connect to early.
  // It took me 3 hours to find this :(
  // TODO: replace sleep with cond var
  std::this_thread::sleep_for(std::chrono::seconds(2));
  return 0;
}

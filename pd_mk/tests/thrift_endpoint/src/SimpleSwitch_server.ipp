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

#include "SimpleSwitch.h"

#include <iostream>

namespace sswitch_runtime {

class SimpleSwitchHandler : virtual public SimpleSwitchIf {
 public:
  SimpleSwitchHandler() {
    // Your initialization goes here
  }

  int32_t mirroring_mapping_add(const int32_t mirror_id, const int32_t egress_port) {
    std::cout << "mirroring_mapping_add" << std::endl
	      << mirror_id << std::endl
	      << egress_port << std::endl;
  }

  int32_t mirroring_mapping_delete(const int32_t mirror_id) {
    // Your implementation goes here
    printf("mirroring_mapping_delete\n");
  }

  int32_t mirroring_mapping_get_egress_port(const int32_t mirror_id) {
    // Your implementation goes here
    printf("mirroring_mapping_get_egress_port\n");
  }

  int32_t set_egress_queue_depth(const int32_t depth_pkts) {
    // Your implementation goes here
    printf("set_egress_queue_depth\n");
  }

  int32_t set_egress_queue_rate(const int64_t rate_pps) {
    // Your implementation goes here
    printf("set_egress_queue_rate\n");
  }

};

}

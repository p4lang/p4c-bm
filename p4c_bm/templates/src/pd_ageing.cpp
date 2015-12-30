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

#include "pd/pd_learning.h"
#include "pd_conn_mgr.h"
#include <iostream>
#include <mutex>
#include <unordered_map>

#define NUM_DEVICES 256

extern pd_conn_mgr_t *conn_mgr_state;
extern int *my_devices;

namespace {

struct AgeingCb {
  p4_pd_notify_timeout_cb cb_fn;
  void *cb_cookie;
};

struct AgeingState {
  // maps table id to call back
  std::unordered_map<int, AgeingCb> cbs;
};


AgeingState *device_state[NUM_DEVICES];

typedef struct {
  char sub_topic[4];
  int switch_id;
  uint64_t buffer_id;
  int table_id;
  unsigned int num_entries;
  char _padding[8];
} __attribute__((packed)) ageing_hdr_t;

}  // namespace

extern "C" {

p4_pd_status_t ${pd_prefix}ageing_set_cb(int dev_id, int table_id,
					 p4_pd_notify_timeout_cb cb_fn,
					 void *cb_cookie) {
  AgeingState *state = device_state[dev_id];
  state->cbs[table_id] = {cb_fn, cb_cookie};
  return 0;
}

p4_pd_status_t ${pd_prefix}ageing_new_device(int dev_id) {
  device_state[dev_id] = new AgeingState();
  return 0;
}

p4_pd_status_t ${pd_prefix}ageing_remove_device(int dev_id) {
  assert(device_state[dev_id]);
  delete device_state[dev_id];
  return 0;
}

void ${pd_prefix}ageing_notification_cb(const char *hdr, const char *data) {
  const ageing_hdr_t *ageing_hdr = reinterpret_cast<const ageing_hdr_t *>(hdr);
  std::cout << "I received " << ageing_hdr->num_entries << " expired hanldes "
            << "for table " << ageing_hdr->table_id << std::endl;
    const AgeingState *state = device_state[ageing_hdr->switch_id];
    const AgeingCb &cb = state->cbs.find(ageing_hdr->table_id)->second;
    uint64_t *handles = (uint64_t *) &data;
    for(unsigned int i = 0; i < ageing_hdr->num_entries; i++) {
      cb.cb_fn(handles[i], cb.cb_cookie);
    }
}

}

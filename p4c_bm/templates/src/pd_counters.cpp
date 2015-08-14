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

#include "pd/pd_types.h"
#include "pd/pd_static.h"
#include "pd_conn_mgr.h"

extern pd_conn_mgr_t *conn_mgr_state;
extern int *my_devices;

extern "C" {

//:: for ca_name, ca in counter_arrays.items():
//::   params = ["p4_pd_sess_hdl_t sess_hdl",
//::             "p4_pd_dev_target_t dev_tgt"]
//::   if ca.is_direct:
//::     params += ["p4_pd_entry_hdl_t entry_hdl"]
//::   else:
//::     params += ["int index"]
//::   #endif
//::   params += ["int flags"]
//::   param_str = ",\n ".join(params)
//::   name = pd_prefix + "counter_read_" + ca_name
p4_pd_counter_value_t
${name}
(
 ${param_str}
) {
  assert(my_devices[dev_tgt.device_id]);
  (void) flags;
  p4_pd_counter_value_t counter_value;
  BmCounterValue value;

  // TODO: try / catch block
//::   if ca.is_direct:
  pd_conn_mgr_client(conn_mgr_state, dev_tgt.device_id)->bm_mt_read_counter(
      value,
      "${ca.table}",
      entry_hdl
  );
//::   else:
  pd_conn_mgr_client(conn_mgr_state, dev_tgt.device_id)->bm_counter_read(
      value,
      "${ca_name}",
      index
  );
//::   #endif

  counter_value.bytes = (uint64_t) value.bytes;
  counter_value.packets = (uint64_t) value.packets;
  return counter_value;
}

//::   params = ["p4_pd_sess_hdl_t sess_hdl",
//::             "p4_pd_dev_target_t dev_tgt"]
//::   if ca.is_direct:
//::     params += ["p4_pd_entry_hdl_t entry_hdl"]
//::   else:
//::     params += ["int index"]
//::   #endif
//::   params += ["p4_pd_counter_value_t counter_value"]
//::   param_str = ",\n ".join(params)
//::   name = pd_prefix + "counter_write_" + ca_name
p4_pd_status_t
${name}
(
 ${param_str}
) {
  assert(my_devices[dev_tgt.device_id]);
  BmCounterValue value;
  value.bytes = (int64_t) counter_value.bytes;
  value.packets = (int64_t) counter_value.packets;

  // TODO: try / catch block
//::   if ca.is_direct:
  pd_conn_mgr_client(conn_mgr_state, dev_tgt.device_id)->bm_mt_write_counter(
      "${ca.table}",
      entry_hdl,
      value
  );
//::   else:
  pd_conn_mgr_client(conn_mgr_state, dev_tgt.device_id)->bm_counter_write(
      "${ca_name}",
      index,
      value
  );
//::   #endif

  return 0;
}

//:: #endfor

}

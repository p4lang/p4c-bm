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

#include <vector>

#include "pd/pd_types.h"
#include "pd/pd_static.h"
#include "pd_conn_mgr.h"

extern pd_conn_mgr_t *conn_mgr_state;
extern int *my_devices;

extern "C" {

// TODO: remove
int ${pd_prefix}mirroring_mapping_add(p4_pd_mirror_id_t mirror_id,
                                      uint16_t egress_port) {
  (void) mirror_id; (void) egress_port;
  return 0;
}

int ${pd_prefix}mirror_session_create(p4_pd_sess_hdl_t shdl,
                                      p4_pd_dev_target_t dev_tgt,
                                      p4_pd_mirror_type_e type,
                                      p4_pd_direction_t dir,
                                      p4_pd_mirror_id_t id,
                                      uint16_t egr_port,
                                      uint16_t max_pkt_len,
                                      uint8_t cos,
                                      bool c2c) {
  (void) shdl; (void) type; (void) dir; (void) max_pkt_len; (void) cos; (void) c2c;
  SSwitchClient *client = pd_conn_mgr_sswitch_client(conn_mgr_state, dev_tgt.device_id);
  return client->mirroring_mapping_add(id, egr_port);
}

int ${pd_prefix}mirror_session_update(p4_pd_sess_hdl_t shdl,
                                      p4_pd_dev_target_t dev_tgt,
                                      p4_pd_mirror_type_e type,
                                      p4_pd_direction_t dir,
                                      p4_pd_mirror_id_t id,
                                      uint16_t egr_port,
                                      uint16_t max_pkt_len,
                                      uint8_t cos,
                                      bool c2c, bool enable) {
  (void) shdl; (void) type; (void) dir; (void) max_pkt_len; (void) cos; (void) c2c; (void) enable;
  SSwitchClient *client = pd_conn_mgr_sswitch_client(conn_mgr_state, dev_tgt.device_id);
  return client->mirroring_mapping_add(id, egr_port);
}

// TODO: remove
int ${pd_prefix}mirroring_mapping_delete(p4_pd_mirror_id_t mirror_id) {
  (void) mirror_id;
  return 0;
}

int ${pd_prefix}mirror_session_delete(p4_pd_sess_hdl_t shdl,
                                      p4_pd_dev_target_t dev_tgt,
                                      p4_pd_mirror_id_t mirror_id) {
  (void) shdl;
  SSwitchClient *client = pd_conn_mgr_sswitch_client(conn_mgr_state, dev_tgt.device_id);
  return client->mirroring_mapping_delete(mirror_id);
}

int ${pd_prefix}mirroring_mapping_get_egress_port(int mirror_id) {
  (void) mirror_id;
  return 0;
}

int ${pd_prefix}mirroring_add_coalescing_session(const int mirror_id,
                                                 const int egress_port,
                                                 const int8_t *header,
                                                 const int8_t header_length,
                                                 const int16_t min_pkt_size,
                                                 const int8_t timeout) {
  (void) mirror_id;
  (void) egress_port;
  (void) header;
  (void) header_length;
  (void) min_pkt_size;
  (void) timeout;
  return 0;
}

int ${pd_prefix}mirroring_set_coalescing_sessions_offset(const uint16_t offset) {
  (void) offset;
  return 0;
}

}

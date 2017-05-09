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

parser start { return ingress; }

@pragma dont_trim
register my_register {
    width : 16;
    direct : my_t;
}

action my_action(param) {
    // not defined for direct registers anyway...
    // register_write(my_register, param);
}

table my_t {
    reads { standard_metadata.egress_spec : exact; }
    actions { my_action; }
}

control ingress { apply(my_t); }

control egress { }

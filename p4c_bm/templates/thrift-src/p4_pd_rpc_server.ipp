//:: pd_prefix = "p4_pd_" + p4_prefix + "_"
//:: pd_static_prefix = "p4_pd_"
//:: api_prefix = p4_prefix + "_"

#include "p4_prefix.h"

#include <iostream>

#include <string.h>

extern "C" {
#include <pd/pd_static.h>
#include <pd/pd.h>
#include <pd/pd_mirroring.h>
}

#include <list>
#include <map>
#include <pthread.h>

using namespace  ::p4_pd_rpc;
using namespace  ::res_pd_rpc;

class ${p4_prefix}Handler : virtual public ${p4_prefix}If {
public:
    ${p4_prefix}Handler() {
//:: for lq_name, lq in learn_quantas.items():
//::   lq_name = get_c_name(lq_name)
      pthread_mutex_init(&${lq_name}_mutex, NULL);
//:: #endfor
    }

    // Table entry add functions

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type != TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   match_type = t.match_type
//::   has_match_spec = len(t.key) > 0
//::   for a_name, a in t.actions.items():
//::     a_name = get_c_name(a_name)
//::     has_action_spec = len(a.runtime_data) > 0
//::     params = ["const SessionHandle_t sess_hdl",
//::               "const DevTarget_t &dev_tgt"]
//::     if has_match_spec:
//::       params += ["const " + api_prefix + t_name + "_match_spec_t &match_spec"]
//::     #endif
//::     if match_type == MatchType.TERNARY:
//::       params += ["const int32_t priority"]
//::     #endif
//::     if has_action_spec:
//::       params += ["const " + api_prefix + a_name + "_action_spec_t &action_spec"]
//::     #endif
//::     if t.support_timeout:
//::       params += ["const int32_t ttl"]
//::     #endif
//::     param_str = ", ".join(params)
//::     name = t_name + "_table_add_with_" + a_name
//::     pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

//::     if has_match_spec:
        ${pd_prefix}${t_name}_match_spec_t pd_match_spec;
//::       match_params = gen_match_params(t.key)
//::       for name, width in match_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_match_spec.${name} = match_spec.${name};
//::         else:
	memcpy(pd_match_spec.${name}, match_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif
//::     if has_action_spec:
        ${pd_prefix}${a_name}_action_spec_t pd_action_spec;
//::       action_params = gen_action_params(a.runtime_data)
//::       for name, width in action_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_action_spec.${name} = action_spec.${name};
//::         else:
	memcpy(pd_action_spec.${name}, action_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif
        p4_pd_entry_hdl_t pd_entry;

//::     pd_params = ["sess_hdl", "pd_dev_tgt"]
//::     if has_match_spec:
//::       pd_params += ["&pd_match_spec"]
//::     #endif
//::     if match_type == MatchType.TERNARY:
//::       pd_params += ["priority"]
//::     #endif
//::     if has_action_spec:
//::       pd_params += ["&pd_action_spec"]
//::     #endif
//::     if t.support_timeout:
//::       pd_params += ["(uint32_t)ttl"]
//::     #endif
//::     pd_params += ["&pd_entry"]
//::     pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});
        return pd_entry;
    }

//::   #endfor
//:: #endfor


    // Table entry modify functions

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type != TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   for a_name, a in t.actions.items():
//::     a_name = get_c_name(a_name)
//::     has_action_spec = len(a.runtime_data) > 0
//::     params = ["const SessionHandle_t sess_hdl",
//::               "const int8_t dev_id",
//::               "const EntryHandle_t entry"]
//::     if has_action_spec:
//::       params += ["const " + api_prefix + a_name + "_action_spec_t &action_spec"]
//::     #endif
//::     param_str = ", ".join(params)
//::     name = t_name + "_table_modify_with_" + a_name
//::     pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

//::     if has_action_spec:
        ${pd_prefix}${a_name}_action_spec_t pd_action_spec;
//::       action_params = gen_action_params(a.runtime_data)
//::       for name, width in action_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_action_spec.${name} = action_spec.${name};
//::         else:
	memcpy(pd_action_spec.${name}, action_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif

//::     pd_params = ["sess_hdl", "dev_id", "entry"]
//::     if has_action_spec:
//::       pd_params += ["&pd_action_spec"]
//::     #endif
//::     pd_param_str = ", ".join(pd_params)
        return ${pd_name}(${pd_param_str});
    }

//::   #endfor
//:: #endfor


    // Table entry delete functions

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   t_name = get_c_name(t_name)
//::   name = t_name + "_table_delete"
//::   pd_name = pd_prefix + name
//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const EntryHandle_t entry"]
//::   param_str = ", ".join(params)
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return ${pd_name}(sess_hdl, dev_id, entry);
    }

//:: #endfor

    // set default action

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type != TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   for a_name, a in t.actions.items():
//::     a_name = get_c_name(a_name)
//::     has_action_spec = len(a.runtime_data) > 0
//::     params = ["const SessionHandle_t sess_hdl",
//::               "const DevTarget_t &dev_tgt"]
//::     if has_action_spec:
//::       params += ["const " + api_prefix + a_name + "_action_spec_t &action_spec"]
//::     #endif
//::     param_str = ", ".join(params)
//::     name = t_name + "_set_default_action_" + a_name
//::     pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

//::     if has_action_spec:
        ${pd_prefix}${a_name}_action_spec_t pd_action_spec;
//::       action_params = gen_action_params(a.runtime_data)
//::       for name, width in action_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_action_spec.${name} = action_spec.${name};
//::         else:
	memcpy(pd_action_spec.${name}, action_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif
        p4_pd_entry_hdl_t pd_entry;

//::     pd_params = ["sess_hdl", "pd_dev_tgt"]
//::     if has_action_spec:
//::       pd_params += ["&pd_action_spec"]
//::     #endif
//::     pd_params += ["&pd_entry"]
//::     pd_param_str = ", ".join(pd_params)
        return ${pd_name}(${pd_param_str});

        // return pd_entry;
    }

//::   #endfor
//:: #endfor

//:: name = "clean_all"
//:: pd_name = pd_prefix + name
  int32_t ${name}(const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      return ${pd_name}(sess_hdl, pd_dev_tgt);
  }

//:: name = "tables_clean_all"
//:: pd_name = pd_prefix + name
  int32_t ${name}(const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      assert(0);

      return 0;
  }

    // INDIRECT ACTION DATA AND MATCH SELECT

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type == TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   act_prof_name = get_c_name(t.act_prof)
//::   match_type = t.match_type
//::   has_match_spec = len(t.key) > 0
//::   for a_name, a in t.actions.items():
//::     a_name = get_c_name(a_name)
//::     has_action_spec = len(a.runtime_data) > 0
//::     params = ["const SessionHandle_t sess_hdl",
//::               "const DevTarget_t &dev_tgt"]
//::     if has_action_spec:
//::       params += ["const " + api_prefix + a_name + "_action_spec_t &action_spec"]
//::     #endif
//::     param_str = ", ".join(params)
//::     name = act_prof_name + "_add_member_with_" + a_name
//::     pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

//::     if has_action_spec:
        ${pd_prefix}${a_name}_action_spec_t pd_action_spec;
//::       action_params = gen_action_params(a.runtime_data)
//::       for name, width in action_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_action_spec.${name} = action_spec.${name};
//::         else:
	memcpy(pd_action_spec.${name}, action_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif
        p4_pd_mbr_hdl_t pd_mbr_hdl;

//::     pd_params = ["sess_hdl", "pd_dev_tgt"]
//::     if has_action_spec:
//::       pd_params += ["&pd_action_spec"]
//::     #endif
//::     pd_params += ["&pd_mbr_hdl"]
//::     pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});
        return pd_mbr_hdl;
    }

//::     params = ["const SessionHandle_t sess_hdl",
//::               "const int8_t dev_id",
//::               "const MemberHandle_t mbr"]
//::     if has_action_spec:
//::       params += ["const " + api_prefix + a_name + "_action_spec_t &action_spec"]
//::     #endif
//::     param_str = ", ".join(params)
//::     name = act_prof_name + "_modify_member_with_" + a_name
//::     pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

//::     if has_action_spec:
        ${pd_prefix}${a_name}_action_spec_t pd_action_spec;
//::       action_params = gen_action_params(a.runtime_data)
//::       for name, width in action_params:
//::         name = get_c_name(name)
//::         if width <= 4:
        pd_action_spec.${name} = action_spec.${name};
//::         else:
	memcpy(pd_action_spec.${name}, action_spec.${name}.c_str(), ${width});
//::         #endif
//::       #endfor

//::     #endif

//::     pd_params = ["sess_hdl", "dev_id", "mbr"]
//::     if has_action_spec:
//::       pd_params += ["&pd_action_spec"]
//::     #endif
//::     pd_param_str = ", ".join(pd_params)
        return ${pd_name}(${pd_param_str});
    }

//::   #endfor

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const MemberHandle_t mbr"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_del_member"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return ${pd_name}(sess_hdl, dev_id, mbr);	
    }

//::   if t.type_ != TableType.INDIRECT_WS: continue
//::
//::   params = ["const SessionHandle_t sess_hdl",
//::             "const DevTarget_t &dev_tgt",
//::             "const int16_t max_grp_size"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_create_group"
//::   pd_name = pd_prefix + name
    GroupHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

	p4_pd_grp_hdl_t pd_grp_hdl;

        ${pd_name}(sess_hdl, pd_dev_tgt, max_grp_size, &pd_grp_hdl);
	return pd_grp_hdl;
    }

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const GroupHandle_t grp"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_del_group"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return ${pd_name}(sess_hdl, dev_id, grp);
    }

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const GroupHandle_t grp",
//::             "const MemberHandle_t mbr"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_add_member_to_group"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return ${pd_name}(sess_hdl, dev_id, grp, mbr);	
    }

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const GroupHandle_t grp",
//::             "const MemberHandle_t mbr"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_del_member_from_group"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return ${pd_name}(sess_hdl, dev_id, grp, mbr);	
    }

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const GroupHandle_t grp",
//::             "const MemberHandle_t mbr"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_deactivate_group_member"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return 0;
    }

//::   params = ["const SessionHandle_t sess_hdl",
//::             "const int8_t dev_id",
//::             "const GroupHandle_t grp",
//::             "const MemberHandle_t mbr"]
//::   param_str = ", ".join(params)
//::   name = act_prof_name + "_reactivate_group_member"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        return 0;
    }

//:: #endfor

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type == TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   match_type = t.match_type
//::   has_match_spec = len(t.key) > 0
//::   params = ["const SessionHandle_t sess_hdl",
//::             "const DevTarget_t &dev_tgt"]
//::   if has_match_spec:
//::     params += ["const " + api_prefix + t_name + "_match_spec_t &match_spec"]
//::   #endif
//::   if match_type == MatchType.TERNARY:
//::     params += ["const int32_t priority"]
//::   #endif
//::   params_wo = params + ["const MemberHandle_t mbr"]
//::   param_str = ", ".join(params_wo)
//::   name = t_name + "_add_entry"
//::   pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

//::   if has_match_spec:
        ${pd_prefix}${t_name}_match_spec_t pd_match_spec;
//::     match_params = gen_match_params(t.key)
//::     for name, width in match_params:
//::       name = get_c_name(name)
//::       if width <= 4:
        pd_match_spec.${name} = match_spec.${name};
//::       else:
	memcpy(pd_match_spec.${name}, match_spec.${name}.c_str(), ${width});
//::       #endif
//::     #endfor

//::   #endif
        p4_pd_entry_hdl_t pd_entry;

//::   pd_params = ["sess_hdl", "pd_dev_tgt"]
//::   if has_match_spec:
//::     pd_params += ["&pd_match_spec"]
//::   #endif
//::   if match_type == MatchType.TERNARY:
//::     pd_params += ["priority"]
//::   #endif
//::   pd_params += ["mbr", "&pd_entry"]
//::   pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});
        return pd_entry;
    }

//::   if t_type != TableType.INDIRECT_WS: continue
//::   params_w = params + ["const GroupHandle_t grp"]
//::   param_str = ", ".join(params_w)
//::   name = t_name + "_add_entry_with_selector"
//::   pd_name = pd_prefix + name
    EntryHandle_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

//::   if has_match_spec:
        ${pd_prefix}${t_name}_match_spec_t pd_match_spec;
//::     match_params = gen_match_params(t.key)
//::     for name, width in match_params:
//::       name = get_c_name(name)
//::       if width <= 4:
        pd_match_spec.${name} = match_spec.${name};
//::       else:
	memcpy(pd_match_spec.${name}, match_spec.${name}.c_str(), ${width});
//::       #endif
//::     #endfor

//::   #endif
        p4_pd_entry_hdl_t pd_entry;

//::   pd_params = ["sess_hdl", "pd_dev_tgt"]
//::   if has_match_spec:
//::     pd_params += ["&pd_match_spec"]
//::   #endif
//::   if match_type == MatchType.TERNARY:
//::     pd_params += ["priority"]
//::   #endif
//::   pd_params += ["grp", "&pd_entry"]
//::   pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});
        return pd_entry;
    }

//:: #endfor

//:: for t_name, t in tables.items():
//::   t_type = t.type_
//::   if t_type == TableType.SIMPLE: continue
//::   t_name = get_c_name(t_name)
//::   params = ["const SessionHandle_t sess_hdl",
//::             "const DevTarget_t &dev_tgt"]
//::   params_wo = params + ["const MemberHandle_t mbr"]
//::   param_str = ", ".join(params_wo)
//::   name = t_name + "_set_default_entry"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

        p4_pd_entry_hdl_t pd_entry;

//::   pd_params = ["sess_hdl", "pd_dev_tgt"]
//::   pd_params += ["mbr", "&pd_entry"]
//::   pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});

        return pd_entry;
    }

//::   if t_type != TableType.INDIRECT_WS: continue
//::   params_w = params + ["const GroupHandle_t grp"]
//::   param_str = ", ".join(params_w)
//::   name = t_name + "_set_default_entry_with_selector"
//::   pd_name = pd_prefix + name
    int32_t ${name}(${param_str}) {
        std::cerr << "In ${name}\n";

        p4_pd_dev_target_t pd_dev_tgt;
        pd_dev_tgt.device_id = dev_tgt.dev_id;
        pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

        p4_pd_entry_hdl_t pd_entry;

//::   pd_params = ["sess_hdl", "pd_dev_tgt"]
//::   pd_params += ["grp", "&pd_entry"]
//::   pd_param_str = ", ".join(pd_params)
        ${pd_name}(${pd_param_str});

        return pd_entry;
    }
//:: #endfor

    // COUNTERS

//:: for ca_name, ca in counter_arrays.items():
//::   if ca.is_direct == "direct":
//::     name = "counter_read_" + ca_name
//::     pd_name = pd_prefix + name
    void ${name}(${api_prefix}counter_value_t &counter_value, const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt, const EntryHandle_t entry, const ${api_prefix}counter_flags_t &flags) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      int pd_flags = 0;
      // if(flags.read_hw_sync) pd_flags |= COUNTER_READ_HW_SYNC;

      p4_pd_counter_value_t value = ${pd_name}(sess_hdl, pd_dev_tgt, entry, pd_flags);
      counter_value.packets = value.packets;
      counter_value.bytes = value.bytes;
    }

//::     name = "counter_write_" + ca_name
//::     pd_name = pd_prefix + name
    int32_t ${name}(const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt, const EntryHandle_t entry, const ${api_prefix}counter_value_t &counter_value) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      p4_pd_counter_value_t value;
      value.packets = counter_value.packets;
      value.bytes = counter_value.bytes;

      return ${pd_name}(sess_hdl, pd_dev_tgt, entry, value);
    }

//::   else:
//::     name = "counter_read_" + ca_name
//::     pd_name = pd_prefix + name
    void ${name}(${api_prefix}counter_value_t &counter_value, const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt, const int32_t index, const ${api_prefix}counter_flags_t &flags) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      int pd_flags = 0;
      // if(flags.read_hw_sync) pd_flags |= COUNTER_READ_HW_SYNC;

      p4_pd_counter_value_t value = ${pd_name}(sess_hdl, pd_dev_tgt, index, pd_flags);
      counter_value.packets = value.packets;
      counter_value.bytes = value.bytes;
    }

//::     name = "counter_write_" + ca_name
//::     pd_name = pd_prefix + name
    int32_t ${name}(const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt, const int32_t index, const ${api_prefix}counter_value_t &counter_value) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      p4_pd_counter_value_t value;
      value.packets = counter_value.packets;
      value.bytes = counter_value.bytes;

      return ${pd_name}(sess_hdl, pd_dev_tgt, index, value);
    }

//::   #endif
//:: #endfor

//:: for ca_name, ca in counter_arrays.items():
//::   name = "counter_hw_sync_" + ca_name
//::   pd_name = pd_prefix + name
    int32_t ${name}(const SessionHandle_t sess_hdl, const DevTarget_t &dev_tgt) {
      return 0;
    }

//:: #endfor

  // METERS

//:: for ma_name, ma in meter_arrays.items():
//::   params = ["const SessionHandle_t sess_hdl",
//::             "const DevTarget_t &dev_tgt"]
//::   entry_or_index = "index";
//::   params += ["const int32_t index"]
//::   if ma.type_ == MeterType.PACKETS:
//::     params += ["const int32_t cir_pps", "const int32_t cburst_pkts",
//::                "const int32_t pir_pps", "const int32_t pburst_pkts"]
//::   else:
//::     params += ["const int32_t cir_kbps", "const int32_t cburst_kbits",
//::                "const int32_t pir_kbps", "const int32_t pburst_kbits"]
//::   #endif
//::   param_str = ", ".join(params)
//::
//::   pd_params = ["sess_hdl", "pd_dev_tgt", entry_or_index]
//::   if ma.type_ == MeterType.PACKETS:
//::     pd_params += ["cir_pps", "cburst_pkts", "pir_pps", "pburst_pkts"]
//::   else:
//::     pd_params += ["cir_kbps", "cburst_kbits", "pir_kbps", "pburst_kbits"]
//::   #endif
//::   pd_param_str = ", ".join(pd_params)
//::   
//::   name = "meter_configure_" + ma_name
//::   pd_name = pd_prefix + name
  int32_t ${name}(${param_str}) {
      std::cerr << "In ${name}\n";

      p4_pd_dev_target_t pd_dev_tgt;
      pd_dev_tgt.device_id = dev_tgt.dev_id;
      pd_dev_tgt.dev_pipe_id = dev_tgt.dev_pipe_id;

      return ${pd_name}(${pd_param_str});
  }

//:: #endfor

  // mirroring api

//:: name = "mirroring_mapping_add"
  int32_t ${name}(const int32_t mirror_id, const int32_t egress_port) {
      std::cerr << "In ${name}\n";
      return ${pd_prefix}${name}(mirror_id, egress_port);
  }

//:: name = "mirroring_mapping_delete"
  int32_t ${name}(const int32_t mirror_id) {
      std::cerr << "In ${name}\n";
      return ${pd_prefix}${name}(mirror_id);
  }

//:: name = "mirroring_mapping_get_egress_port"
  int32_t ${name}(int32_t mirror_id) {
      std::cerr << "In ${name}\n";
      return ${pd_prefix}${name}(mirror_id);
  }

  // coalescing api

//:: name = "mirroring_set_coalescing_sessions_offset"
  int32_t ${name}(const int16_t coalescing_sessions_offset) {
      std::cerr << "In ${name}\n";
      return ${pd_prefix}${name}(coalescing_sessions_offset);
  }

//:: name = "mirroring_add_coalescing_session"
  int32_t ${name}(const int32_t mirror_id, const int32_t egress_port, const std::vector<int8_t> &header, const int16_t min_pkt_size, const int8_t timeout){
      std::cerr << "In ${name}\n";
      return ${pd_prefix}${name}(mirror_id, egress_port, &header[0], (const int8_t)header.size(), min_pkt_size, timeout);
  }

  void set_learning_timeout(const SessionHandle_t sess_hdl, const int8_t dev_id, const int32_t msecs) {
      ${pd_prefix}set_learning_timeout(sess_hdl, (const uint8_t)dev_id, msecs);
  }

//:: for lq_name, lq in learn_quantas.items():
//::   lq_name = get_c_name(lq_name)
//::   rpc_msg_type = api_prefix + lq_name + "_digest_msg_t"
//::   rpc_entry_type = api_prefix + lq_name + "_digest_entry_t"
  std::map<SessionHandle_t, std::list<${rpc_msg_type}> > ${lq_name}_digest_queues;
  pthread_mutex_t ${lq_name}_mutex;

  p4_pd_status_t
  ${lq_name}_receive(const SessionHandle_t sess_hdl,
                        const ${rpc_msg_type} &msg) {
    pthread_mutex_lock(&${lq_name}_mutex);
    assert(${lq_name}_digest_queues.find(sess_hdl) != ${lq_name}_digest_queues.end());
    std::map<SessionHandle_t, std::list<${rpc_msg_type}> >::iterator digest_queue = ${lq_name}_digest_queues.find(sess_hdl);
    digest_queue->second.push_back(msg);
    pthread_mutex_unlock(&${lq_name}_mutex);

    return 0;
  }

  static p4_pd_status_t
  ${p4_prefix}_${lq_name}_cb(p4_pd_sess_hdl_t sess_hdl,
                             ${pd_prefix}${lq_name}_digest_msg_t *msg,
                             void *cookie) {
    ${pd_prefix}${lq_name}_digest_msg_t *msg_ = new ${pd_prefix}${lq_name}_digest_msg_t();
    *msg_ = *msg;
    ${rpc_msg_type} rpc_msg;
    rpc_msg.msg_ptr = (int64_t)msg_;
    rpc_msg.dev_tgt.dev_id = msg->dev_tgt.device_id;
    rpc_msg.dev_tgt.dev_pipe_id = msg->dev_tgt.dev_pipe_id;
    for (int i = 0; (msg != NULL) && (i < msg->num_entries); ++i) {
      ${rpc_entry_type} entry;
//::   for name, bit_width in lq.fields:
//::     c_name = get_c_name(name)
//::     width = (bit_width + 7) / 8
//::     if width > 4:
      entry.${c_name}.insert(entry.${c_name}.end(), msg->entries[i].${c_name}, msg->entries[i].${c_name} + ${width});
//::     else:
      entry.${c_name} = msg->entries[i].${c_name};
//::     #endif
//::   #endfor
      rpc_msg.msg.push_back(entry);
    }
    return ((${p4_prefix}Handler*)cookie)->${lq_name}_receive((SessionHandle_t)sess_hdl, rpc_msg);
  }

  void ${lq_name}_register( const SessionHandle_t sess_hdl, const int8_t dev_id) {
    ${pd_prefix}${lq_name}_register(sess_hdl, dev_id, ${p4_prefix}_${lq_name}_cb, this);
    pthread_mutex_lock(&${lq_name}_mutex);
    ${lq_name}_digest_queues.insert(std::pair<SessionHandle_t, std::list<${rpc_msg_type}> >(sess_hdl, std::list<${rpc_msg_type}>()));
    pthread_mutex_unlock(&${lq_name}_mutex);
  }

  void ${lq_name}_deregister(const SessionHandle_t sess_hdl, const int8_t dev_id) {
    ${pd_prefix}${lq_name}_deregister(sess_hdl, dev_id);
    pthread_mutex_lock(&${lq_name}_mutex);
    ${lq_name}_digest_queues.erase(sess_hdl);
    pthread_mutex_unlock(&${lq_name}_mutex);
  }

  void ${lq_name}_get_digest(${rpc_msg_type} &msg, const SessionHandle_t sess_hdl) {
    msg.msg_ptr = 0;
    msg.msg.clear();

    pthread_mutex_lock(&${lq_name}_mutex);
    std::map<SessionHandle_t, std::list<${rpc_msg_type}> >::iterator digest_queue = ${lq_name}_digest_queues.find(sess_hdl);
    if (digest_queue != ${lq_name}_digest_queues.end()) {
      if (digest_queue->second.size() > 0) {
        msg = digest_queue->second.front();
        digest_queue->second.pop_front();
      }
    }

    pthread_mutex_unlock(&${lq_name}_mutex);
  }

  void ${lq_name}_digest_notify_ack(const SessionHandle_t sess_hdl, const int64_t msg_ptr) {
    ${pd_prefix}${lq_name}_digest_msg_t *msg = (${pd_prefix}${lq_name}_digest_msg_t *) msg_ptr;
    ${pd_prefix}${lq_name}_notify_ack((p4_pd_sess_hdl_t)sess_hdl, msg);
    delete msg;
  }
//:: #endfor
};

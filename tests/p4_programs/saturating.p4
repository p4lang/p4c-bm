header_type my_meta_t {
    fields {
        f8 : 8 (saturating);
        f16 : 16;
        f32 : 32 (saturating);
    }
}

metadata my_meta_t my_meta;

parser start { return ingress; }

action my_add(param) { modify_field(my_meta.f8, my_meta.f8 + param); }

table my_t {
    actions { my_add; }
}

control ingress { apply(my_t); }

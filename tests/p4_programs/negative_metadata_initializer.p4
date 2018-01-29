header_type meta_t {
    fields {
        x : 16;
        y : 16;
        z : 16;
    }
}

@pragma dont_trim
metadata meta_t meta {
    x : 33;
    y : 44;
    z : 55;
};

parser start {
    return ingress;
}
control ingress { }

control egress { }

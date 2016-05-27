// this P4 program is not with the others because it requires an extra primitive
// declaration 

parser start {
    return ingress;
}

action a() {
    unknown_primitive();
}

table t {
    actions { a; }
}

control ingress {
    apply(t);
}

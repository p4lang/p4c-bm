parser start {
    return ingress;
}

action testA(src1) {
    shift_left(standard_metadata.egress_spec, 1, src1);
}

table test {
    actions {
	    testA;
    }
}

control ingress {
    apply(test);
}

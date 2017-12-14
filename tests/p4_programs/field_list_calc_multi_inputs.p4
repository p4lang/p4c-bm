header_type h_t { fields { f32 : 32; f16 : 16; } }

header h_t h;

parser start {
    return ingress;
}

field_list flist1 { h.f32; }
field_list flist2 { h.f16; }

@pragma dont_trim
field_list_calculation calc {
    input { flist1; flist2; }
    algorithm { csum16; crc16; }
    output_width : 16;
}

control ingress { }

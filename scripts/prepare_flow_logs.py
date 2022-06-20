# This script will parse the flow logs input 

import json

with open("logformat") as f:
    data = f.read()

js = json.loads(data)

fl_fields_list = js['FlowLogs'][0]['LogFormat'].replace("$","").replace("{","").replace("}","").replace("-","_").split(" ")

log_format_lookup = {
    "account_id"            : "string",
    "action"                : "string",
    "az_id"                 : "string",
    "bytes"                 : "bigint",
    "dstaddr"               : "string",
    "dstport"               : "int",
    "end"                   : "bigint",
    "flow_direction"        : "string",
    "instance_id"           : "string",
    "interface_id"          : "string",
    "log_status"            : "string",
    "packets"               : "bigint",
    "pkt_dst_aws_service"   : "string",
    "pkt_dstaddr"           : "string",
    "pkt_src_aws_service"   : "string",
    "pkt_srcaddr"           : "string",
    "protocol"              : "bigint",
    "region"                : "string",
    "srcaddr"               : "string",
    "srcport"               : "int",
    "start"                 : "bigint",
    "sublocation_id"        : "string",
    "sublocation_type"      : "string",
    "subnet_id"             : "string",
    "tcp_flags"             : "int",
    "traffic_path"          : "int",
    "type"                  : "string",
    "version"               : "int",
    "vpc_id"                : "string"
}

log_format = ""
c = 0
for i in fl_fields_list:
    log_format += "`" 
    log_format += i
    log_format += "` " 
    log_format += log_format_lookup[str(i)]
    if i == fl_fields_list[-1]:
        break
    log_format += ", "
    
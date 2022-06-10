
import argparse
import boto3
from io import StringIO

class StringBuilder:
    string = None
    
    def __init__(self):
        self.string = StringIO()
    
    def add(self, str):
        self.string.write(str)
        
    def __str__(self):
        return self.string.getvalue()
    
flow_log_format = {
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

def createTable(table_name="vpc_flow_logs_6", flow_logs_bucket_location="s3://sapphire-vpc-flow-logs-834539731159/", query_output_bucket_location="s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/", workgroup="primary"):
    
    client = boto3.client('athena')
    
    query_str = StringBuilder()
    query_str.add("CREATE EXTERNAL TABLE IF NOT EXISTS ")
    query_str.add("`" + table_name + "`")
    query_str.add(" ( `account_id` string, `action` string, `az_id` string, `bytes` bigint, `dstaddr` string, `dstport` int, `end` bigint, `flow_direction` string, `instance_id` string, `interface_id` string, `log_status` string, `packets` bigint, `pkt_dst_aws_service` string, `pkt_dstaddr` string, `pkt_src_aws_service` string, `pkt_srcaddr` string, `protocol` bigint, `region` string, `srcaddr` string, `srcport` int, `start` bigint, `sublocation_id` string, `sublocation_type` string, `subnet_id` string, `tcp_flags` int, `traffic_path` int, `type` string, `version` int, `vpc_id` string  ) \n")
    query_str.add("PARTITIONED BY (`date` date)\n")
    query_str.add("ROW FORMAT DELIMITED\n")
    query_str.add("FIELDS TERMINATED BY ' '\n")
    query_str.add("LOCATION ")
    query_str.add("'" + flow_logs_bucket_location + "'\n")
    query_str.add("TBLPROPERTIES (\"skip.header.line.count\"=\"1\")")
    
    response = client.start_query_execution(
        QueryString=str(query_str),
        
        # if the below block is commented out, the table will be created in the default db...
        # QueryExecutionContext={
        #     'Database': 'wbc'
        # },
        
        ResultConfiguration={
            'OutputLocation': query_output_bucket_location,
        },
        WorkGroup=workgroup
    )
    print(response)
    
def createPartition(table_name, account_id, region, date, flow_logs_bucket_location="s3://sapphire-vpc-flow-logs-834539731159/", query_output_bucket_location="s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/", workgroup="primary"):
    
    client = boto3.client('athena')
    #assuming date is of YYYY-MM-DD format
    date_components = date.split("-")
    
    query_str = StringBuilder()
    query_str.add("ALTER TABLE ")
    query_str.add(table_name + " \n")
    query_str.add("ADD PARTITION (`date`='")
    query_str.add(date + "')\n")
    query_str.add("LOCATION ")
    query_str.add("'" + flow_logs_bucket_location + "AWSLogs/")
    query_str.add(account_id + "/vpcflowlogs/")
    query_str.add(region + "/")
    query_str.add(date_components[0] + "/")
    query_str.add(date_components[1] + "/")
    query_str.add(date_components[2] + "';")
    
    response = client.start_query_execution(
        
        QueryString=str(query_str),
    
        # if the below block is commented out, the table will be created in the default db...
        # QueryExecutionContext={
        #     'Database': 'wbc'
        # },
        
        ResultConfiguration={
            'OutputLocation': query_output_bucket_location,
        },
        WorkGroup=workgroup
    )
    print(response)
    

def runQueryForAllFields(table_name, date, query_output_bucket_location="s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/", workgroup="primary"):
    
    client = boto3.client('athena')
    
    query_str = StringBuilder()
    query_str.add("SELECT * FROM ")
    query_str.add(table_name)
    query_str.add(" WHERE date = DATE('")
    query_str.add(date)
    query_str.add("');")
    
    response = client.start_query_execution(
        
        QueryString=str(query_str),
    
        # if the below block is commented out, the table will be created in the default db...
        # QueryExecutionContext={
        #     'Database': 'wbc'
        # },
        
        ResultConfiguration={
            'OutputLocation': query_output_bucket_location,
        },
        WorkGroup=workgroup
    )
    print(response)
    
def runCustomQuery(fields, table_name, date, query_output_bucket_location="s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/", workgroup="primary"):
    client = boto3.client('athena')
    
    # assuming fields is a list of fields to be queried
    query_fields_str = StringBuilder()
    for field in fields:
        query_fields_str.add(field)
        if field == fields[-1]:
            break
        query_fields_str.add(", ")

    query_str = StringBuilder()
    query_str.add("SELECT ")
    query_str.add(query_fields_str)
    query_str.add(" FROM ")
    query_str.add(table_name)
    query_str.add(" WHERE date = DATE('")
    query_str.add(date)
    query_str.add("');")
    
    response = client.start_query_execution(
        
        QueryString=str(query_str),
    
        # if the below block is commented out, the table will be created in the default db...
        # QueryExecutionContext={
        #     'Database': 'wbc'
        # },
        
        ResultConfiguration={
            'OutputLocation': query_output_bucket_location,
        },
        WorkGroup=workgroup
    )
    print(response)
    
def runOnPremConnectionCheckQuery(table_name, date, query_output_bucket_location="s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/", workgroup="primary"):
    
    client = boto3.client('athena')
    
    query_str = StringBuilder()
    query_str.add("SELECT account_id, flow_direction, srcaddr FROM ")
    query_str.add(table_name)
    query_str.add(" WHERE date = DATE('")
    query_str.add(date)
    query_str.add("') AND flow_direction = 'ingress';")

    response = client.start_query_execution(
        
        QueryString=str(query_str),
    
        # if the below block is commented out, the table will be created in the default db...
        # QueryExecutionContext={
        #     'Database': 'wbc'
        # },
        
        ResultConfiguration={
            'OutputLocation': query_output_bucket_location,
        },
        WorkGroup=workgroup
    )
    print(response)
    
def main(account_id, date, region, table):
    client = boto3.client('athena')
    
    createTable(table)
    createPartition(table, account_id, region, date)
    runQueryForAllFields(table, date)
    #runOnPremConnectionCheckQuery(table, date)
    
def parser():
    parser = argparse.ArgumentParser(description=['Parsing arguments'])
    parser.add_argument('-a','--account-id', help='Target account id', nargs='?', dest="account_id")
    parser.add_argument('-d','--date', help='Date', nargs='?', dest="date")
    parser.add_argument('-r','--region', help='Target region', nargs='?', dest="region")
    parser.add_argument('-t','--table', help='Target Athena table', nargs='?', dest="table")
    args = vars(parser.parse_args())
    
    account_id = args["account_id"]
    date = args["date"]
    region = args["region"]
    table = args["table"]

    return account_id, date, region, table

if __name__ == "__main__":
    account_id, date, region, table = parser()
    main(account_id, date, region, table)
    
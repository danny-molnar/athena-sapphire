# Athena deployment script

# This script will:
# - create an Athena table for the desired customer account in the specified region
# - create a partition for a desired date

# Usage: $ python[3] athena.py_setup -a ACCOUNT_NUMBER -d DATE{FORMAT: YYYY-MM-DD} -r REGION -t ATHENA_TABLE_NAME

import argparse
import boto3
from io import StringIO
from prepare_flow_logs import log_format

class StringBuilder:
    string = None
    
    def __init__(self):
        self.string = StringIO()
    
    def add(self, str):
        self.string.write(str)
        
    def __str__(self):
        return self.string.getvalue()
    

log_format2 = "`account_id` string, `action` string, `az_id` string, `bytes` bigint, `dstaddr` string, `dstport` int, `end` bigint, `flow_direction` string, `instance_id` string, `interface_id` string, `log_status` string, `packets` bigint, `pkt_src_aws_service` string, `pkt_dstaddr` string, `pkt_srcaddr` string, `protocol` bigint, `region` string, `srcaddr` string, `srcport` int, `start` bigint, `sublocation_id` string, `sublocation_type` string, `subnet_id` string, `tcp_flags` int, `traffic_path` int, `type` string, `version` int, `vpc_id` string"

def createTable(table_name, flow_logs_bucket_location, query_output_bucket_location, workgroup="primary"):
    
    client = boto3.client('athena')
    
    query_str = StringBuilder()
    query_str.add("CREATE EXTERNAL TABLE IF NOT EXISTS ")
    query_str.add("`" + table_name + "`")
    query_str.add(" ( " + log_format + " )\n")
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
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print("Table successfully created")
    
def createPartition(table_name, account_id, region, date, flow_logs_bucket_location, query_output_bucket_location, workgroup="primary"):
    
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
    #print(response)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print("Partition successfully created")
        
def main(account_id, date, region, table):
    client = boto3.client('athena')
    
    # the below variables will temporarily hold the flow logs and output buckets' as per a demo/sandbox account
    # these need changing once it is ready for release
    flow_logs_bucket = "s3://sapphire-vpc-flow-logs-834539731159/"
    query_output_bucket = "s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/"
    
    createTable(table, flow_logs_bucket, query_output_bucket)
    createPartition(table, account_id, region, date, flow_logs_bucket, query_output_bucket)
    
    athenaDate = date
    
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
    
# Query On-prem connectivity

# This script will:
# - create and run a query in Athena to check if there's any on-prem connectivity appearing in the flow logs
# - the query will check if the srcaddr field contains the on-prem cidr range 

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

def runOnPremConnectionCheckQuery(table_name, date, query_output_bucket_location, workgroup="primary"):
    
    client = boto3.client('athena')
    
    query_str = StringBuilder()
    query_str.add("SELECT ROW_NUMBER() OVER() AS num, flow_direction, srcaddr, dstaddr FROM ")
    query_str.add(table_name)
    query_str.add(" WHERE date = DATE('")
    query_str.add(date)
    query_str.add("') AND flow_direction = 'ingress'")
    #query_str.add("AND srcaddr LIKE '172.16%' OR srcaddr LIKE '172.28%'")

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
        print("Query sueccessfully created")
    
def main(date, table):
    client = boto3.client('athena')
    
    # the below variables will temporarily hold the flow logs and output buckets' 
    # this hardcoding of resources will have to be removed and parameterised with arguments coming from calling the script
    query_output_bucket = "s3://sapphire-vpc-flow-logs-athena-query-results-834539731159/"
    
    runOnPremConnectionCheckQuery(table, date, query_output_bucket)
        
def parser():
    parser = argparse.ArgumentParser(description=['Parsing arguments'])
    parser.add_argument('-d','--date', help='Target date', nargs='?', dest="date")
    parser.add_argument('-t','--table', help='Target Athena table', nargs='?', dest="table")
    args = vars(parser.parse_args())
    
    date = args["date"]
    table = args["table"]

    return date, table

if __name__ == "__main__":
    date, table = parser()
    main(date, table)
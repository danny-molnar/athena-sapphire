import boto3

#### Athena stuff

client = boto3.client('athena')

# create named query
response = client.create_named_query(
    Name='TestQuery',
    Database='sapphirelogsdatabase',
    QueryString="SELECT * FROM vpc_flow_logs_3 WHERE date = DATE('2022-05-25') LIMIT 100;",
)
print(response)

# list named queries
response = client.list_named_queries(
    MaxResults=10,
    WorkGroup='primary'
)
print(response)

# Actions to take:
    
# create new table for new queries
# create new partitioning for queires
# run query

# Creating new table 
# response = client.start_query_execution(
    
    
#     QueryString="""CREATE EXTERNAL TABLE IF NOT EXISTS `vpc_flow_logs_4` ( `account_id` string, `action` string, `az_id` string, `bytes` bigint, `dstaddr` string, `dstport` int, `end` bigint, `flow_direction` string, `instance_id` string, `interface_id` string, `log_status` string, `packets` bigint, `pkt_dst_aws_service` string, `pkt_dstaddr` string, `pkt_src_aws_service` string, `pkt_srcaddr` string, `protocol` bigint, `region` string, `srcaddr` string, `srcport` int, `start` bigint, `sublocation_id` string, `sublocation_type` string, `subnet_id` string, `tcp_flags` int, `traffic_path` int, `type` string, `version` int, `vpc_id` string  )
#                     PARTITIONED BY (`date` date)
#                     ROW FORMAT DELIMITED
#                     FIELDS TERMINATED BY ' '
#                     LOCATION 's3://sapphire-vpc-flow-logs-834539731159/'
#                     TBLPROPERTIES ("skip.header.line.count"="1")
#                 """,
    
#     # if the below block is commented out, the table will be created in the default db...
#     # QueryExecutionContext={
#     #     'Database': 'wbc'
#     # },
#     ResultConfiguration={
#         'OutputLocation': 's3://sapphire-vpc-flow-logs-athena-query-results-834539731159/',
#     },
#     WorkGroup='primary'
# )
# print(response)


# # Creating partition for previously created table
# response = client.start_query_execution(
    
    
#     QueryString=""" ALTER TABLE vpc_flow_logs_4
#                     ADD PARTITION (`date`='2022-05-25')
#                     LOCATION 's3://sapphire-vpc-flow-logs/AWSLogs/090402447788/vpcflowlogs/eu-west-2/2022/05/25';
#                 """,
    
#     # if the below block is commented out, the table will be created in the default db...
#     # QueryExecutionContext={
#     #     'Database': 'wbc'
#     # },
#     ResultConfiguration={
#         'OutputLocation': 's3://sapphire-vpc-flow-logs-athena-query-results-834539731159/',
#     },
#     WorkGroup='primary'
# )
# print(response)

# Running a sample query    
response = client.start_query_execution(
    
    QueryString=""" SELECT * FROM vpc_flow_logs_4 WHERE date = DATE('2022-05-25'); """,
    
    # if the below block is commented out, the table will be created in the default db...
    # QueryExecutionContext={
    #     'Database': 'wbc'
    # },
    ResultConfiguration={
        'OutputLocation': 's3://sapphire-vpc-flow-logs-athena-query-results-834539731159/',
    },
    WorkGroup='primary'
)
print(response)
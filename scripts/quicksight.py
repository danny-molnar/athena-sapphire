# TODO: follow the below list of actions to visualize data from an Athena table:

# create new analysis
# select new dataset
# select athena
# data source name: the one that matches the data source in Athena, by default it is "AwsDataCatalog"
# workgroup: as set/specified by the athena script, by default it is "workgroup"
# select database: as set/specified by the athena script, by default it is "default"
# select the athena table: as set/specified by the athena script

import boto3

client = boto3.client("quicksight")

# creating analysis
response = client.create_analysis(
    AwsAccountId ='834539731159',
    AnalysisId ='demo_analysis',
    Name ='Demo Analysis',
    SourceEntity = {}
)
print(response)

response = client.create_data_set()
print(response)


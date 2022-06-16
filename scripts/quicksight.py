# TODO: follow the below list of actions to visualize data from an Athena table:

# create new analysis
# select new dataset
# select athena
# data source name: the one that matches the data source in Athena, by default it is "AwsDataCatalog"
# workgroup: as set/specified by the athena script, by default it is "workgroup"
# select database: as set/specified by the athena script, by default it is "default"
# select the athena table: as set/specified by the athena script

import boto3
import pprint

account_id = "834539731159"
table_name = "spafax_migration_day"

client = boto3.client("quicksight")

# # listing datasets
# response = client.list_data_sets(
#     AwsAccountId=account_id,
# )
# print(response)

# create data source
# response = client.create_data_source(
#     AwsAccountId = account_id,
#     DataSourceId = "my_data_source_id",
#     Name = "Display Namer for the Data Source",
#     Type = "ATHENA",
#     DataSourceParameters={
#         'AthenaParameters': {
#             'WorkGroup': 'primary'
#         }
#     }
# )

response = client.list_analyses(
    AwsAccountId = account_id
)

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(response)

print("------------------------------------")
print("------------------------------------")
print("------------------------------------")

analysis_id = "2bdb41cc-7078-4fce-bd97-38cde5feab41"

response = client.describe_analysis(
    AwsAccountId = account_id,
    AnalysisId = analysis_id
)

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(response)

print("------------------------------------")
print("------------------------------------")
print("------------------------------------")

dataset_id = "341f7396-6f97-45ba-a8c4-f42625955340"

response = client.describe_data_set(
    AwsAccountId = account_id,
    DataSetId = dataset_id
)

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(response)

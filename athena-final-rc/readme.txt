To use these scripts, please do the following steps in order:

1. Assume into the customer's account by using AWSume
2. Run the flow_logs.sh bash script. If needed, add the executing permission by chmod +x flow_logs.sh
3. Run the prepare_flow_logs.py Python script in order to have the correct flow log format.
4. Assume into the account that has the flow logs set up in S3.
 - a. for DEMO purposes I will be using my pdev account
 - b. to make it usable for other accounts, change the athena_setup.py file with the correct options.
5. Run the athena_setup.py Python script as follows:
 - python[3] athena.py_setup -a ACCOUNT_NUMBER -d DATE{FORMAT: YYYY-MM-DD} -r REGION -t ATHENA_TABLE_NAME
 - make sure all parameters are provided and they are all correct
6. Once complete, run the desired queries, as follows:
 - python[3] query_{all_fields, onprem_connectivity, rejected_packets}.py -t ATHENA_TABLE_NAME, where
 - - query_all_fields.py: creates and runs a query that outputs all fields in the VPC flow logs in Athena
 - - query_onprem_connectivity.py: creates and runs a query that will check if the srcaddr field contains the on-prem cidr range 
 - - query_rejected_packets.py: creates and runs a query that will list the scraddr, flow_direction fields where a rejected action happened

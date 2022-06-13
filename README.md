## README ##

Last update: 13/06/2022

This repository contains the following:

- **scripts/athena.py:** this boto3 script deploys an Athena table, sets up a partition for a desired day and customer account, and creates SQL-like queries in Athena that can be viewed in the Athena console.
Usage: 
*$ python[3] athena.py -a ACCOUNT_NUMBER -d DATE{FORMAT: YYYY-MM-DD} -r REGION -t ATHENA_TABLE_NAME,*
where
  - ACCOUNT_NUMBER - the account number Athena will be using for VPC flow log quieries
  - DATE - the date for the query, required format: YYYY-MM-DD
  - REGION - the region in which the customer account has resources in
  - ATHENA_TABLE_NAME - the name of the desired Athena table

Once the script is run, the table then can be used for analysing VPC flow logs.

- **scripts/quicksight.py:** WIP, a script that will create a dashboard in Quicksight for a given Athena table.

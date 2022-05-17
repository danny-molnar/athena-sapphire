## README ##

*Last update: 17/05/2022.*

This README contains my solution thoughts on Amazon Athena for Sapphire Systems.
This README references files in the terraform folder.

Referenced resources:
https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html


### Pre-existing infrastructure

In my lab account using the console, I have set up a basic infrastructure consisting of a VPC, some subnets, routing, and an instance. 

I have enabled VPC flow logs to go into an S3 bucket, with default settings. 

### Athena in the console

Following the above documentation I have setup Athena with the following:
	1.  I have created an S3 bucket for Athena query results.
	2. Created a database with the SQL statement provided, and have set it up so that it can be partitioned by a date which will be provided in a later step. This SQL statement also makes sure Athena queries will use the bucket containing the VPC flow logs.
	3. With a second SQL statement, I have created a partition of the previous database for a specified date. 
	4. In the Athena console one can directly write SQL statements to query results from the flow logs.

### Athena in Terraform

With Terraform I was able to 

 - Deploy an Athena database
 - Deploy a named query that contains the SQL statement to create the table for Athena
 - Deploy a named query that contains the SQL statement to create the partition for a certain day.

### Personal thoughts and questions

1. With Terraform, Athena can be set up, and some sample queries can be created.
2. With the resources created with Terraform, what scripted approach would be appropriate for the queries to be run? 
3. Console vs Terraform - how much would the Athena Console be used, if at all?
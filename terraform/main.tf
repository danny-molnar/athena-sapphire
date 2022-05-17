# deploying Athena database
resource "aws_athena_database" "example" {
  name   = "athenaexample"
  bucket = "athena-query-results-tf-834539731159"
}

# named queries resources for setting up Athena - creating table
resource "aws_athena_named_query" "create_athena_table" {
  name      = "creating athena table"
  database  = aws_athena_database.example.name
  query     = <<EOF
    CREATE EXTERNAL TABLE IF NOT EXISTS `vpc_flow_logs` (
  `version` int, 
  `account_id` string, 
  `interface_id` string, 
  `srcaddr` string, 
  `dstaddr` string, 
  `srcport` int, 
  `dstport` int, 
  `protocol` bigint, 
  `packets` bigint, 
  `bytes` bigint, 
  `start` bigint, 
  `end` bigint, 
  `action` string, 
  `log_status` string
)
PARTITIONED BY (`date` date)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://vpc-flow-logs-834539731159/prefix/AWSLogs/834539731159/vpcflowlogs/eu-west-2/'
TBLPROPERTIES ("skip.header.line.count"="1");
    EOF
}

# named queries resources for setting up Athena - creating partition of table for a specified date
resource "aws_athena_named_query" "create_partition" {
  name      = "creating partition"
  database  = aws_athena_database.example.name
  query     = <<EOF
    ALTER TABLE vpc_flow_logs
ADD PARTITION (`date`='2022-05-17')
LOCATION 's3://vpc-flow-logs-834539731159/prefix/AWSLogs/834539731159/vpcflowlogs/eu-west-2/2022/05/17';
    EOF
}

# named queries resources for setting up Athena - sample query
resource "aws_athena_named_query" "sample" {
  name      = "sample query"
  database  = aws_athena_database.example.name
  query     = <<EOF
    SELECT * 
FROM vpc_flow_logs 
WHERE date = DATE('2020-05-04') 
LIMIT 100;
EOF
}
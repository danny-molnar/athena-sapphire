#!/bin/bash

# Assuming user has awsumed into the customer account
echo Getting VPC flow logs format from customer account
aws ec2 describe-flow-logs > logformat

echo File created: logformat
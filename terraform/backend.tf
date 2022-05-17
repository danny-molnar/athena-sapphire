terraform {
  backend "s3" {
    bucket = "834539731159-tfstates"
    key    = "834539731159.tfstate"
    dynamodb_table = "tf-state-lock-834539731159"
  }
}


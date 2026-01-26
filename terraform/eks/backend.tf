terraform {
  backend "s3" {
    bucket         = "cloudfinops-tf-state-bucket"       # <-- change this
    key            = "eks/${terraform.workspace}/terraform.tfstate"       # <-- change folder/key if desired
    region         = "us-east-1"                       # <-- match your AWS region
    dynamodb_table = "terraform-lock-table"                 # <-- enable state locking (recommended)
    encrypt        = true
  }
}
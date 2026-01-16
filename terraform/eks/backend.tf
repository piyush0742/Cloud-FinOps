terraform {
  backend "s3" {
    bucket         = "devops-project-tf-state-bucket"       # <-- change this
    key            = "eks-lbc/terraform.tfstate"       # <-- change folder/key if desired
    region         = "us-east-1"                       # <-- match your AWS region
    dynamodb_table = "terraform-lock-table"                 # <-- enable state locking (recommended)
    encrypt        = true
  }
}
provider "aws" {
  region = var.REGION
}

#remote state
terraform {
  backend "s3" {
    bucket = "terraform-bucket-t3"
    region = "us-east-1"
    key    = "backend/terraform.tfstate"
  }
}

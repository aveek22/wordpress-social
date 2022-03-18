module "social_integration__linkedin" {
    source  = "../terraform/social_integration__linkedin"
}

module "social_integration__twitter" {
    source  = "../terraform/social_integration__twitter"
}

module "parameter_store" {
    source  = "../terraform/parameter_store"
}

terraform {
  backend "s3" {
      bucket    = "wordpress-social"
      key       = "terraform-state/terraform.tfstate"
      region    = "eu-west-1"
  }
}
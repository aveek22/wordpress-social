module "social_integration__linkedin" {
    source  = "../terraform/social_integration__linkedin"
}

module "social_integration__twitter" {
    source  = "../terraform/social_integration__twitter"
}

module "social_integration__facebook" {
    source  = "../terraform/social_integration__facebook"
}

module "social_integration__instagram" {
    source  = "../terraform/social_integration__instagram"
}

module "parameter_store" {
    source  = "../terraform/parameter_store"
}

terraform {
  backend "s3" {
      bucket    = "wordpress-social-001"
      key       = "terraform-state/terraform.tfstate"
      region    = "eu-west-1"
      profile   = "aveek2021"
  }
}
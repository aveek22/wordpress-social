module "social_integration__linkedin" {
    source  = "../terraform/social_integration__linkedin"
    lambda_layer_arn = "${module.wordpress_social_lambda_layer.wordpress_social_lambda_layer_arn}"
}

module "social_integration__twitter" {
    source  = "../terraform/social_integration__twitter"
    lambda_layer_arn = "${module.wordpress_social_lambda_layer.wordpress_social_lambda_layer_arn}"
}

module "social_integration__facebook" {
    source  = "../terraform/social_integration__facebook"
    lambda_layer_arn = "${module.wordpress_social_lambda_layer.wordpress_social_lambda_layer_arn}"
}

module "social_integration__instagram" {
    source  = "../terraform/social_integration__instagram"
    lambda_layer_arn = "${module.wordpress_social_lambda_layer.wordpress_social_lambda_layer_arn}"
}

module "parameter_store" {
    source  = "../terraform/parameter_store"
}

module "wordpress_social_lambda_layer" {
    source  = "../terraform/wordpress_social_lambda_layer"
}

terraform {
  backend "s3" {
      bucket    = "wordpress-social-001"
      key       = "terraform-state/terraform.tfstate"
      region    = "eu-west-1"
      profile   = "aveek2021"
  }
}
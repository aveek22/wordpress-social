resource "aws_ssm_parameter" "facebook_page_access_token" {
  name  = "/social_integration/facebook/page_access_token"
  type  = "String"
  value = "${var.facebook_page_access_token}"
}

resource "aws_ssm_parameter" "facebook_user_access_token" {
  name  = "/social_integration/facebook/user_access_token"
  type  = "String"
  value = "${var.facebook_user_access_token}"
}

resource "aws_ssm_parameter" "instagram_app_id" {
  name  = "/social_integration/instagram/app_id"
  type  = "String"
  value = "${var.instagram_app_id}"
}

resource "aws_ssm_parameter" "instagram_app_secret" {
  name  = "/social_integration/instagram/app_secret"
  type  = "String"
  value = "${var.instagram_app_secret}"
}

resource "aws_ssm_parameter" "instagram_business_account_id" {
  name  = "/social_integration/instagram/business_account_id"
  type  = "String"
  value = "${var.instagram_business_account_id}"
}
resource "aws_ssm_parameter" "facebook_page_access_token" {
  name  = "/social_integration/facebook/page_access_token"
  type  = "String"
  value = "${var.facebook_page_access_token}"
}
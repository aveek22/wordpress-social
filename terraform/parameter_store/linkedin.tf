resource "aws_ssm_parameter" "linkedin_access_token" {
  name  = "/social_integration/linkedin/access_token"
  type  = "String"
  value = "${var.linkedin_access_token}"
}
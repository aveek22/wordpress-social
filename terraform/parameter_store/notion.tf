resource "aws_ssm_parameter" "notion_access_token" {
  name  = "/notion_automator/datacloudmag/access_token"
  type  = "String"
  value = "${var.notion_access_token}"
}
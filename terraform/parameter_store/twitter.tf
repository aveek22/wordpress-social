resource "aws_ssm_parameter" "twitter_consumer_key" {
  name  = "/social_integration/twitter/consumer_key"
  type  = "String"
  value = "${var.twitter_consumer_key}"
}

resource "aws_ssm_parameter" "twitter_consumer_key_secret" {
  name  = "/social_integration/twitter/consumer_key_secret"
  type  = "String"
  value = "${var.twitter_consumer_key_secret}"
}

resource "aws_ssm_parameter" "twitter_access_token" {
  name  = "/social_integration/twitter/access_token"
  type  = "String"
  value = "${var.twitter_access_token}"
}

resource "aws_ssm_parameter" "twitter_access_token_secret" {
  name  = "/social_integration/twitter/access_token_secret"
  type  = "String"
  value = "${var.twitter_access_token_secret}"
}
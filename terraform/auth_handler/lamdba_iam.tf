resource "aws_iam_role_policy" "wordpress_social_auth_handler_policy" {
  name = "wordpress_social_auth_handler_policy"
  role = aws_iam_role.wordpress_social_auth_handler_role.id

  policy = file("../terraform/auth_handler/iam-role/lambda-policy.json")
}

resource "aws_iam_role" "wordpress_social_auth_handler_role" {
  name = "wordpress_social_auth_handler_role"
  assume_role_policy = file("../terraform/auth_handler/iam-role/lambda-assume-policy.json")

  tags = {
    Application = "wordpress-social"
    Environment = "production"
  }
}
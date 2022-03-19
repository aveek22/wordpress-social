resource "aws_iam_role_policy" "wordpress_social_instagram_policy" {
  name = "wordpress_social_instagram_policy"
  role = aws_iam_role.wordpress_social_instagram_role.id

  policy = file("../terraform/social_integration__twitter/iam-role/lambda-policy.json")
}

resource "aws_iam_role" "wordpress_social_instagram_role" {
  name = "wordpress_social_instagram_role"
  assume_role_policy = file("../terraform/social_integration__twitter/iam-role/lambda-assume-policy.json")

  tags = {
    Application = "wordpress-social"
    Environment = "production"
  }
}
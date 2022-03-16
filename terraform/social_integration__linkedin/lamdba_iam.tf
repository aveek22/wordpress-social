resource "aws_iam_role_policy" "wordpress_social_linkedin_policy" {
  name = "wordpress_social_linkedin_policy"
  role = aws_iam_role.wordpress_social_linkedin_role.id

  policy = file("../terraform/social_integration__linkedin/iam-role/lambda-policy.json")
}

resource "aws_iam_role" "wordpress_social_linkedin_role" {
  name = "wordpress_social_linkedin_role"
  assume_role_policy = file("../terraform/social_integration__linkedin/iam-role/lambda-assume-policy.json")

  tags = {
    Application = "wordpress-social"
    Environment = "production"
  }
}
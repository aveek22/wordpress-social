locals {
  lambda-zip-location = "../build/lambda/social_integration/linkedin.zip"
}

data "archive_file" "wordpress_social_linkedin" {
  type = "zip"
  source_dir = "../app/lambda/functions/social_integration/linkedin/"
  output_path = local.lambda-zip-location
}

resource "aws_lambda_function" "wordpress_social_linkedin" {
  filename = local.lambda-zip-location
  function_name = "wordpress_social_linkedin"
  role = aws_iam_role.wordpress_social_linkedin_role.arn
  handler = "app.main"
  layers = [
    aws_lambda_layer_version.wordpress_social_lambda_layer.arn
  ]

  runtime = "python3.9"

  tags = {
    Environment = "production"
    Application = "wordpress-social"
  }

  # environment {
  #   variables = {
  #       foo = "bar"
  #       application_environment = "${var.environment}"
  #   }
  # }
}

output "wordpress_social_linkedin_arn" {
  description = "The ARN of the Lambda function: wordpress_social_linkedin"
  value       = join("", aws_lambda_function.wordpress_social_linkedin.*.arn)
}
locals {
  lambda-zip-location = "../build/aws_lambda/social_integration/linkedin.zip"
}

data "archive_file" "wordpress_social_linkedin" {
  type = "zip"
  source_dir = "../app/lambda_functions/social_integration/linkedin/"
  output_path = local.lambda-zip-location
  excludes = [
    "event.json",
    "lambda_event.py"
  ]
}

resource "aws_lambda_function" "wordpress_social_linkedin" {
  filename = local.lambda-zip-location
  function_name = "wordpress_social_linkedin"
  role = aws_iam_role.wordpress_social_linkedin_role.arn
  handler = "app.main"
  source_code_hash = "${data.archive_file.wordpress_social_linkedin.output_base64sha256}"
  runtime          = "python3.9"
  timeout          =  90
  layers = [
    aws_lambda_layer_version.wordpress_social_lambda_layer.arn
  ]

  tags = {
    Environment = "production"
    Application = "wordpress-social"
  }

  environment {
    variables = {
        WORDPRESS_SOCIAL_LOG_LEVEL = "INFO"
    }
  }
}

output "wordpress_social_linkedin_arn" {
  description = "The ARN of the Lambda function: wordpress_social_linkedin"
  value       = join("", aws_lambda_function.wordpress_social_linkedin.*.arn)
}
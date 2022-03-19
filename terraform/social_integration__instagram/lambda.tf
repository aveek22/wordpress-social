locals {
  lambda-zip-location = "../build/aws_lambda/social_integration/instagram.zip"
}

module "wordpress_social_lambda_layer" {
    source  = "../../terraform/wordpress_social_lambda_layer"
}

data "archive_file" "wordpress_social_instagram" {
  type = "zip"
  source_dir = "../app/lambda_functions/social_integration/instagram/"
  output_path = local.lambda-zip-location
  # excludes = [
  #   "event.json",
  #   "lambda_event.py"
  # ]
}

resource "aws_lambda_function" "wordpress_social_instagram" {
  filename = local.lambda-zip-location
  function_name = "wordpress_social_instagram"
  role = aws_iam_role.wordpress_social_instagram_role.arn
  handler = "app.main"
  source_code_hash = "${data.archive_file.wordpress_social_instagram.output_base64sha256}"
  runtime          = "python3.9"
  timeout          =  90
  layers = [
    module.wordpress_social_lambda_layer.wordpress_social_lambda_layer_arn
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

output "wordpress_social_instagram_arn" {
  description = "The ARN of the Lambda function: wordpress_social_instagram"
  value       = join("", aws_lambda_function.wordpress_social_instagram.*.arn)
}
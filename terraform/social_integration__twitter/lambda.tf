locals {
  lambda-zip-location = "../build/aws_lambda/social_integration/twitter.zip"
}

# module "wordpress_social_lambda_layer" {
#     source  = "../../terraform/wordpress_social_lambda_layer"
# }

data "archive_file" "wordpress_social_twitter" {
  type = "zip"
  source_dir = "../app/lambda_functions/social_integration/twitter/"
  output_path = local.lambda-zip-location
  excludes = [
    "event.json",
    "lambda_event.py"
  ]
}

resource "aws_lambda_function" "wordpress_social_twitter" {
  filename = local.lambda-zip-location
  function_name = "wordpress_social_twitter"
  role = aws_iam_role.wordpress_social_twitter_role.arn
  handler = "app.main"
  source_code_hash = "${data.archive_file.wordpress_social_twitter.output_base64sha256}"
  runtime          = "python3.9"
  timeout          =  90
  layers = [
    "${var.lambda_layer_arn}"
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

output "wordpress_social_twitter_arn" {
  description = "The ARN of the Lambda function: wordpress_social_twitter"
  value       = join("", aws_lambda_function.wordpress_social_twitter.*.arn)
}
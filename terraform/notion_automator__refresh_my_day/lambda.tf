locals {
  lambda-zip-location = "../build/aws_lambda/notion/refresh_my_day.zip"
}

data "archive_file" "notion_refresh_my_day" {
  type = "zip"
  source_dir = "../app/lambda_functions/notion_automator/refresh_my_day/"
  output_path = local.lambda-zip-location
  excludes = [
    "event.json",
    "lambda_event.py"
  ]
}

resource "aws_lambda_function" "notion_refresh_my_day" {
  filename = local.lambda-zip-location
  function_name = "notion_refresh_my_day"
  role = aws_iam_role.notion_refresh_my_day_role.arn
  handler = "app.main"
  source_code_hash = "${data.archive_file.notion_refresh_my_day.output_base64sha256}"
  runtime          = "python3.9"
  timeout          =  90
  layers = [
    "${var.lambda_layer_arn}"
  ]

  tags = {
    Environment = "production"
    Application = "notion-automator"
  }

  environment {
    variables = {
        WORDPRESS_SOCIAL_LOG_LEVEL = "INFO"
    }
  }
}

output "notion_refresh_my_day_arn" {
  description = "The ARN of the Lambda function: notion_refresh_my_day"
  value       = join("", aws_lambda_function.notion_refresh_my_day.*.arn)
}
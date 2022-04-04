locals {
  lambda-zip-location = "../build/aws_lambda/auth_handler.zip"
}

data "archive_file" "wordpress_social_auth_handler" {
  type = "zip"
  source_dir = "../app/lambda_functions/auth_handler/"
  output_path = local.lambda-zip-location
  # excludes = [
  #   "event.json",
  #   "lambda_event.py"
  # ]
}

resource "aws_lambda_function" "wordpress_social_auth_handler" {
  filename = local.lambda-zip-location
  function_name = "wordpress_social_auth_handler"
  role = aws_iam_role.wordpress_social_auth_handler_role.arn
  handler = "app.main"
  source_code_hash = "${data.archive_file.wordpress_social_auth_handler.output_base64sha256}"
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

resource "aws_lambda_permission" "apigw" {
   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = aws_lambda_function.wordpress_social_auth_handler.function_name
   principal     = "apigateway.amazonaws.com"
   source_arn = "${aws_api_gateway_rest_api.auth_handler.execution_arn}/*/*"
}

output "wordpress_social_auth_handler_arn" {
  description = "The ARN of the Lambda function: wordpress_social_auth_handler"
  value       = join("", aws_lambda_function.wordpress_social_auth_handler.*.arn)
}
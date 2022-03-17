resource "aws_lambda_layer_version" "wordpress_social_lambda_layer" {
  filename   = "../app/lambda_layers/packages/python.zip"
  layer_name = "wordpress_social_lambda_layer"

  compatible_runtimes = ["python3.6","python3.7","python3.8","python3.9"]
}

output "wordpress_social_lambda_layer_aarn" {
  description = "The ARN of the Lambda Layer"
  value       = join("", aws_lambda_layer_version.wordpress_social_lambda_layer.*.arn)
}
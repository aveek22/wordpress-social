resource "aws_api_gateway_rest_api" "auth_handler" {
  name        = "auth_handler_api_gateway"
  description = "API Gateway to handle OAuth requests."
}

resource "aws_api_gateway_resource" "proxy" {
   rest_api_id = aws_api_gateway_rest_api.auth_handler.id
   parent_id   = aws_api_gateway_rest_api.auth_handler.root_resource_id
   path_part   = "{proxy+}"
}
resource "aws_api_gateway_method" "proxy" {
   rest_api_id   = aws_api_gateway_rest_api.auth_handler.id
   resource_id   = aws_api_gateway_resource.proxy.id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
   rest_api_id = aws_api_gateway_rest_api.auth_handler.id
   resource_id = aws_api_gateway_method.proxy.resource_id
   http_method = aws_api_gateway_method.proxy.http_method
   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.wordpress_social_auth_handler.invoke_arn
}

resource "aws_api_gateway_method" "proxy_root" {
   rest_api_id   = aws_api_gateway_rest_api.auth_handler.id
   resource_id   = aws_api_gateway_rest_api.auth_handler.root_resource_id
   http_method   = "ANY"
   authorization = "NONE"
}
resource "aws_api_gateway_integration" "lambda_root" {
   rest_api_id = aws_api_gateway_rest_api.auth_handler.id
   resource_id = aws_api_gateway_method.proxy_root.resource_id
   http_method = aws_api_gateway_method.proxy_root.http_method
   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.wordpress_social_auth_handler.invoke_arn
}

resource "aws_api_gateway_deployment" "auth_handler_deployment" {
   depends_on = [
     aws_api_gateway_integration.lambda,
     aws_api_gateway_integration.lambda_root,
   ]
   rest_api_id = aws_api_gateway_rest_api.auth_handler.id
   stage_name  = "dev"
}

output "base_url" {
  value = aws_api_gateway_deployment.auth_handler_deployment.invoke_url
}
resource "aws_sqs_queue" "wordpress_social_linkedin_sqs_queue" {
  name                      = "wordpress_social_linkedin_sqs_queue"
  delay_seconds             = 20
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Application = "wordpress-social"
    Environment = "production"
  }
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.wordpress_social_linkedin_sqs_queue.arn
  function_name    = aws_lambda_function.wordpress_social_linkedin.arn
  enabled = true

  depends_on = [
    aws_lambda_function.wordpress_social_linkedin,
    aws_sqs_queue.wordpress_social_linkedin_sqs_queue
  ]
}
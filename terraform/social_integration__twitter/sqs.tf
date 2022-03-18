resource "aws_sqs_queue" "wordpress_social_twitter_sqs_queue" {
  name                      = "wordpress_social_twitter_sqs_queue"
  delay_seconds             = 2
  max_message_size          = 2048
  message_retention_seconds = 60
  receive_wait_time_seconds = 2
  visibility_timeout_seconds = 90

  tags = {
    Application = "wordpress-social"
    Environment = "production"
  }
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.wordpress_social_twitter_sqs_queue.arn
  function_name    = aws_lambda_function.wordpress_social_twitter.arn
  enabled = true

  depends_on = [
    aws_lambda_function.wordpress_social_twitter,
    aws_sqs_queue.wordpress_social_twitter_sqs_queue
  ]
}
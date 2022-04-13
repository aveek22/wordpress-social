resource "aws_cloudwatch_event_rule" "notion_refresh_myday_event_rule" {
  name = "notion_refresh_myday_event_rule"
  description = "Trigger Lambda at midnight everyday."
  schedule_expression = "cron(00 00 * * ? *)"
}

resource "aws_cloudwatch_event_target" "notion_refresh_myday_lambda_target" {
  arn = aws_lambda_function.notion_refresh_my_day.arn
  rule = aws_cloudwatch_event_rule.notion_refresh_myday_event_rule.name
  input = file("../terraform/notion_automator__refresh_my_day/eventbridge_input.json")
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notion_refresh_my_day.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.notion_refresh_myday_event_rule.arn
}

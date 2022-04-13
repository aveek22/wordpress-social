resource "aws_iam_role_policy" "notion_refresh_my_day_policy" {
  name = "notion_refresh_my_day_policy"
  role = aws_iam_role.notion_refresh_my_day_role.id

  policy = file("../terraform/notion_automator__refresh_my_day/iam-role/lambda-policy.json")
}

resource "aws_iam_role" "notion_refresh_my_day_role" {
  name = "notion_refresh_my_day_role"
  assume_role_policy = file("../terraform/notion_automator__refresh_my_day/iam-role/lambda-assume-policy.json")

  tags = {
    Application = "notion-automator"
    Environment = "production"
  }
}
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_lambda_function" "scraper" {
  function_name = "scraper-fn"
  role          = aws_iam_role.lambda_exec.arn
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  filename      = "lambda_scraper.zip"
  source_code_hash = filebase64sha256("lambda_scraper.zip")
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

output "lambda_arn" {
  value = aws_lambda_function.scraper.arn
}

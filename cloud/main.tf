# ===================================================================
# Meta WhatsApp Catalog API Gateway Infrastructure
# ===================================================================

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# ===================================================================
# Provider Configuration
# ===================================================================

provider "aws" {
  region = var.aws_region
}

# ===================================================================
# Variables
# ===================================================================

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "meta-catalog-api"
}

variable "resource_prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "real-estate"
}

variable "api_key_value" {
  description = "API key for authentication"
  type        = string
  sensitive   = true
}

variable "meta_access_token" {
  description = "Meta API access token"
  type        = string
  sensitive   = true
}

variable "meta_catalog_id" {
  description = "Meta catalog ID"
  type        = string
  sensitive   = true
}

variable "meta_business_id" {
  description = "Meta business ID"
  type        = string
  sensitive   = true
}

variable "meta_app_id" {
  description = "Meta app ID"
  type        = string
  sensitive   = true
}

variable "meta_app_secret" {
  description = "Meta app secret"
  type        = string
  sensitive   = true
}

# ===================================================================
# Data Sources
# ===================================================================

data "aws_caller_identity" "current" {}

# ===================================================================
# Lambda Function
# ===================================================================

# Lambda Layer per dipendenze Python
resource "aws_lambda_layer_version" "python_dependencies" {
  filename         = "${path.module}/lambda_layer.zip"
  layer_name       = "${var.resource_prefix}-${var.project_name}-dependencies"
  description      = "Python dependencies layer (requests, etc.)"
  
  compatible_runtimes = ["python3.9", "python3.10", "python3.11"]
  
  source_code_hash = filebase64sha256("${path.module}/lambda_layer.zip")
}

# Zip the Lambda function code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda_function.zip"
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.resource_prefix}-${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach basic execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_execution_role.name
}

# Lambda function
resource "aws_lambda_function" "catalog_function" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.resource_prefix}-${var.project_name}-function"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 256

  # Aggiungi il layer con le dipendenze
  layers = [aws_lambda_layer_version.python_dependencies.arn]

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      META_ACCESS_TOKEN = var.meta_access_token
      META_CATALOG_ID   = var.meta_catalog_id
      META_BUSINESS_ID  = var.meta_business_id
      META_APP_ID       = var.meta_app_id
      META_APP_SECRET   = var.meta_app_secret
      META_BASE_URL     = "https://graph.facebook.com/v18.0"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_cloudwatch_log_group.lambda_logs
  ]
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.resource_prefix}-${var.project_name}-function"
  retention_in_days = 7
}

# ===================================================================
# API Gateway
# ===================================================================

# API Gateway REST API
resource "aws_api_gateway_rest_api" "catalog_api" {
  name        = "${var.resource_prefix}-${var.project_name}-gateway"
  description = "API Gateway for Meta WhatsApp Catalog management"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "catalog_resource" {
  rest_api_id = aws_api_gateway_rest_api.catalog_api.id
  parent_id   = aws_api_gateway_rest_api.catalog_api.root_resource_id
  path_part   = "catalog"
}

# API Gateway Method
resource "aws_api_gateway_method" "catalog_post" {
  rest_api_id   = aws_api_gateway_rest_api.catalog_api.id
  resource_id   = aws_api_gateway_resource.catalog_resource.id
  http_method   = "POST"
  authorization = "NONE"
  
  api_key_required = true

  request_parameters = {
    "method.request.header.x-api-key" = true
  }
}

# API Gateway Integration
resource "aws_api_gateway_integration" "catalog_integration" {
  rest_api_id = aws_api_gateway_rest_api.catalog_api.id
  resource_id = aws_api_gateway_resource.catalog_resource.id
  http_method = aws_api_gateway_method.catalog_post.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.catalog_function.invoke_arn
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway_invoke" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.catalog_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.catalog_api.execution_arn}/*/*"
}

# ===================================================================
# API Gateway Deployment
# ===================================================================

resource "aws_api_gateway_deployment" "catalog_deployment" {
  depends_on = [
    aws_api_gateway_method.catalog_post,
    aws_api_gateway_integration.catalog_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.catalog_api.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "catalog_stage" {
  deployment_id = aws_api_gateway_deployment.catalog_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.catalog_api.id
  stage_name    = "prod"
}

# ===================================================================
# API Key and Usage Plan
# ===================================================================

resource "aws_api_gateway_api_key" "catalog_api_key" {
  name  = "${var.resource_prefix}-${var.project_name}-api-key"
  value = var.api_key_value
}

resource "aws_api_gateway_usage_plan" "catalog_usage_plan" {
  name         = "${var.resource_prefix}-${var.project_name}-usage-plan"
  description  = "Usage plan for Meta Catalog API"

  api_stages {
    api_id = aws_api_gateway_rest_api.catalog_api.id
    stage  = aws_api_gateway_stage.catalog_stage.stage_name
  }

  quota_settings {
    limit  = 1000
    period = "DAY"
  }

  throttle_settings {
    rate_limit  = 10
    burst_limit = 20
  }
}

resource "aws_api_gateway_usage_plan_key" "catalog_usage_plan_key" {
  key_id        = aws_api_gateway_api_key.catalog_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.catalog_usage_plan.id
}

# ===================================================================
# Outputs
# ===================================================================

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_stage.catalog_stage.invoke_url}/catalog"
}

output "api_key_id" {
  description = "API Key ID"
  value       = aws_api_gateway_api_key.catalog_api_key.id
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.catalog_function.function_name
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}
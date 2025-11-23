# Terraform Outputs

# VPC
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

# Load Balancer
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

# Application URLs
output "streamlit_url" {
  description = "Streamlit application URL"
  value       = "http://${aws_lb.main.dns_name}/"
}

output "jupyter_url" {
  description = "Jupyter Lab URL"
  value       = "http://${aws_lb.main.dns_name}/jupyter/"
}

output "metabase_url" {
  description = "Metabase URL"
  value       = "http://${aws_lb.main.dns_name}/metabase/"
}

# ECS
output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.analytics_lab.name
}

# ECR
output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.analytics_lab.repository_url
}

# RDS
output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "rds_address" {
  description = "RDS PostgreSQL address"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.postgres.port
}

output "database_name" {
  description = "Database name"
  value       = aws_db_instance.postgres.db_name
}

# Deployment Instructions
output "deployment_instructions" {
  description = "Instructions for deploying the application"
  value = <<-EOT
    
    🚀 Deployment Instructions:
    
    1. Build and push Docker image:
       aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.analytics_lab.repository_url}
       docker build -t ${aws_ecr_repository.analytics_lab.repository_url}:latest .
       docker push ${aws_ecr_repository.analytics_lab.repository_url}:latest
    
    2. Update ECS service:
       aws ecs update-service --cluster ${aws_ecs_cluster.main.name} --service ${aws_ecs_service.analytics_lab.name} --force-new-deployment --region ${var.aws_region}
    
    3. Access your applications:
       - Streamlit: http://${aws_lb.main.dns_name}/
       - Jupyter:   http://${aws_lb.main.dns_name}/jupyter/
       - Metabase:  http://${aws_lb.main.dns_name}/metabase/
    
    4. Database connection:
       Host: ${aws_db_instance.postgres.address}
       Port: ${aws_db_instance.postgres.port}
       Database: ${aws_db_instance.postgres.db_name}
       User: ${var.db_username}
  EOT
}

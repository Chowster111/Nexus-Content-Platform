resource "aws_ecr_repository" "backend" {
  name = "backend-repo"
}

resource "aws_ecr_repository" "frontend" {
  name = "frontend-repo"
}

resource "aws_ecr_repository" "scraper" {
  name = "scraper-repo"
}

output "backend_repo_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "frontend_repo_url" {
  value = aws_ecr_repository.frontend.repository_url
}

output "scraper_repo_url" {
  value = aws_ecr_repository.scraper.repository_url
}

I’ve completed the infrastructure and CI milestone of my Azure cloud engineering portfolio project.

The project brings together Terraform, Azure Container Apps, Azure Container Registry, Docker, PostgreSQL, and GitHub Actions around a small Flask API.

My focus was the cloud engineering work:
• Defining Azure resources in separate Terraform files
• Designing separate application and database subnets with private PostgreSQL DNS
• Configuring managed identity and AcrPull for container image access
• Connecting Container Apps environment logging to Log Analytics
• Automating database migrations, six application/database tests, Docker builds, and Terraform validation in CI
• Documenting architecture, troubleshooting, deployment sequencing, and cost controls

All CI checks are passing. Live Azure deployment verification remains a separate step, and automated paid deployment is disabled.

One practical takeaway: a healthy application endpoint does not guarantee a healthy database connection. Separating /health from /db-health makes troubleshooting much clearer.

Repository: https://github.com/davidandrelee1-vader/azure-production-deployment

I’m looking for Cloud Engineer, DevOps, Cloud Support, and Solutions Architect opportunities where I can keep building and troubleshooting infrastructure.

#Azure #Terraform #DevOps #CloudEngineering #Docker #GitHubActions

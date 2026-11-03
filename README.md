# Azure Production Deployment | Terraform, Docker, PostgreSQL & CI/CD

![CI Pipeline](https://github.com/davidandrelee1-vader/azure-production-deployment/actions/workflows/ci.yml/badge.svg)

## Project Overview

A production-oriented cloud engineering portfolio project demonstrating infrastructure as code, containerized application deployment, database persistence, schema migrations, and automated CI testing.

The project uses Microsoft Azure, Terraform, Docker, Flask, PostgreSQL, and GitHub Actions to demonstrate repeatable infrastructure provisioning and application delivery.

**Repository:** https://github.com/davidandrelee1-vader/azure-production-deployment

## Architecture

```text
                     Developer
                         |
                         v
                    GitHub Repo
                         |
                         v
                   GitHub Actions
                    /          \
                   v            v
              pytest Tests   Docker Build
                   |
                   v
             Validated Code

              Azure Environment
  +-----------------------------------------+
  | Resource Group: rg-azure-production-dev |
  |                                         |
  | Azure Container Registry                |
  |          |                              |
  |          v                              |
  | Azure Container Apps Environment        |
  |          |                              |
  |          v                              |
  | Containerized Flask REST API            |
  |          |                              |
  |          v                              |
  | PostgreSQL (local Docker development)   |
  +-----------------------------------------+
```

The Flask application has been deployed and health-checked in Azure Container Apps. PostgreSQL currently runs locally through Docker Compose; Azure Database for PostgreSQL Flexible Server is not yet deployed.

The CI pipeline validates application tests and Docker image builds. Automated deployment to Azure is planned.

## Technology Stack

| Technology | Purpose |
|---|---|
| Microsoft Azure | Cloud infrastructure |
| Terraform | Infrastructure as code |
| Azure Container Apps | Containerized application hosting |
| Azure Container Registry | Docker image storage |
| Docker / Docker Compose | Container packaging and local orchestration |
| Python / Flask | REST API |
| PostgreSQL | Relational database |
| psycopg | Python database connectivity |
| pytest | Automated API testing |
| GitHub Actions | Continuous integration |
| Azure Managed Identity / RBAC | Identity-based access to Azure Container Registry |

## Infrastructure as Code

Terraform manages the Azure development environment, including:

- Resource group
- Virtual network and delegated subnets
- Network security configuration
- Private DNS zone for PostgreSQL
- Azure Container Registry
- Azure Container Apps environment
- Container application
- User-assigned managed identity
- Azure role assignment for container registry image pulls

Terraform state is configured to use an Azure Storage backend.

Infrastructure can be provisioned, validated, reviewed, and destroyed using standard Terraform commands.

## Flask REST API

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Application information |
| `/health` | GET | Application health check |
| `/db-health` | GET | PostgreSQL connectivity check |
| `/transactions` | POST | Create a transaction |
| `/transactions` | GET | Retrieve recent transactions |

Example transaction:

```json
{
  "description": "Test cloud transaction",
  "amount": "125.50"
}
```

The API validates incoming transaction data before inserting records into PostgreSQL.

## Local Development

### Requirements

- Docker Desktop
- Docker Compose
- Git
- Azure CLI and Terraform for infrastructure deployment

### Environment configuration

Create a local `.env` file containing:

```dotenv
POSTGRES_PASSWORD=replace-with-a-strong-local-password
```

Do not commit this file to Git.

### Start the application

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Test the API:

```bash
curl http://localhost:5001/health
curl http://localhost:5001/db-health
curl http://localhost:5001/transactions
```

### Stop the application

```bash
docker compose down
```

Docker named volumes preserve database data across normal container recreation.

**Warning:** `docker compose down -v` removes associated named volumes and can delete local database data.

## Database Migrations

Version-controlled SQL migrations are stored in:

```text
database/migrations/
    001_create_transactions.sql
```

The Python migration runner:

```text
database/migrate.py
```

tracks applied migrations using PostgreSQL's `schema_migrations` table.

Run migrations from the project root:

```powershell
docker compose run --rm --no-deps `
  -v "${PWD}\database:/database:ro" `
  -w /database `
  --entrypoint python `
  api migrate.py
```

The runner skips previously applied migration versions and executes new migrations transactionally.

This is a learning implementation; production hardening should include migration checksums, concurrency control, and schema verification.

## Automated Testing

Four Flask tests currently validate:

1. Application home endpoint
2. Application health endpoint
3. Rejection of missing transaction descriptions
4. Rejection of invalid transaction amounts

Run tests locally:

```powershell
docker compose run --rm --no-deps `
  -v "${PWD}\app:/app" `
  -w /app `
  -e PYTHONPATH=/app `
  --entrypoint python `
  api -m pytest -v -p no:cacheprovider tests/
```

**Verified local result:** 4 tests passed.

Database integration testing is planned as a separate improvement.

## GitHub Actions CI Pipeline

Workflow file:

```text
.github/workflows/ci.yml
```

The pipeline performs two jobs:

**1. Test Flask Application**
- Check out source code
- Configure Python 3.12
- Install development dependencies
- Execute pytest

**2. Validate Docker Build**
- Runs after the testing job succeeds
- Builds the application Docker image

The workflow runs on pushes and pull requests targeting `main`, and supports manual execution.

**Verified GitHub Actions result:** Both jobs passed successfully.

## Security Practices

- Git ignores `.env`, Terraform state, and sensitive variable files.
- PostgreSQL credentials are supplied through environment variables for local development.
- Terraform defines Azure networking and subnet separation.
- Azure Container Registry access uses managed identity and RBAC.
- Automated tests validate selected API behaviors.

Additional production security controls, including comprehensive secret scanning, private database connectivity, least-privilege reviews, and deployment approvals, remain future work.

## Project Structure

```text
azure-production-deployment/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── tests/
│       └── test_app.py
├── database/
│   ├── migrate.py
│   └── migrations/
│       └── 001_create_transactions.sql
├── docs/
├── terraform/
│   ├── backend.tf
│   ├── container-app.tf
│   ├── container-apps.tf
│   ├── container-registry.tf
│   ├── identity.tf
│   ├── network.tf
│   ├── private-dns.tf
│   ├── providers.tf
│   ├── resource-groups.tf
│   ├── variables.tf
│   └── versions.tf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Next Improvements

- Add PostgreSQL integration tests in CI
- Automate container image publishing to Azure Container Registry
- Implement deployment automation with GitHub Actions and Azure identity federation
- Complete managed PostgreSQL deployment when subscription and regional restrictions permit
- Add monitoring, alerts, and operational dashboards
- Implement environment-specific deployment controls
- Add architecture diagrams and cost documentation

## Project Status

**Completed:** Terraform Azure infrastructure deployment, Azure Container Apps API health verification, local PostgreSQL persistence, SQL migration automation, Flask tests, Docker builds, and GitHub Actions continuous integration.

**In progress:** Production hardening, database integration testing, and continuous deployment automation.

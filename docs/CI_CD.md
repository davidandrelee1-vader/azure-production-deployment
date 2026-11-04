# CI/CD behavior and deployment boundary

## Workflows

| Workflow | Trigger | Work performed | Azure impact |
|---|---|---|---|
| `ci.yml` | Push to main, PR targeting main, manual | PostgreSQL 16 service, migrations, six pytest tests, Docker build, Terraform format/init/validate | No Azure authentication, plan, apply or image push |
| `validate-workflows.yml` | Workflow file changes or manual | actionlint with release checksum verification | None |
| `azure-deploy.yml` | Manual only | With default false input, test and build deployment image | Deploy job unconditionally disabled |
| `azure-login-test.yml` | Manual only | Azure OIDC login and account display | Authenticates only; not executed for this work |

The application test job runs migrations before pytest. Docker build waits for the tests. Terraform validation runs independently, initializes with `-backend=false` and uses the committed provider lockfile without updating it. These checks do not contact the configured Azure state backend or provision resources. Validation confirms configuration/schema consistency, not quotas, DNS reachability or subscription readiness.

## Deployment safeguards

The deployment workflow has no push trigger. Its boolean `execute_deployment` input defaults to false. The `deploy` job contains `if: ${{ false }}` and only a disabled-message placeholder. Setting the input true skips preparation and does not enable deployment. There are no active image-push or deployment steps.

The named `production` environment is referenced by the disabled job; this alone is not evidence that GitHub environment approval rules are configured. CI has `contents: read` only. OIDC write permission exists in the manual Azure workflows; CI does not receive it.

## Future approved rollout

Follow [DEPLOYMENT_HANDOFF.md](DEPLOYMENT_HANDOFF.md) after explicit Azure cost authorization. Review the Terraform plan, bootstrap ACR and publish the expected image, apply infrastructure in a reviewed order, run migrations from a network location able to reach the private database, and verify runtime health, logs and rollback. CI's temporary PostgreSQL service cannot validate Azure private-network connectivity.

No Azure deployment was enabled or executed by this documentation and monitoring update.

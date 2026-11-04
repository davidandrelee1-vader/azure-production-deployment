# Azure Deployment Handoff — Cost-Gated Work Only

The following tasks require the owner's explicit authorization and Azure credentials. None have been performed by this documentation package.

1. **Review cost and scope:** PostgreSQL Flexible Server, ACR Basic, Container Apps, Log Analytics, and Terraform backend storage may incur charges. Set a budget and decide a test window.
2. **Review Terraform:** Confirm Azure subscription, region, CIDRs, permissions, private DNS and provider compatibility. Run `terraform -chdir=terraform plan` only after confirming the state backend and credentials. Inspect the proposed creates, updates and replacements.
3. **Bootstrap registry and publish image:** Review a staged rollout because a new ACR must exist before it can receive an image. Do not expect a first full apply to build or publish the image. **Publish image to ACR:** The current GitHub CI image build does not publish. The Container App expects `azure-production-api:1.0` in the configured ACR. Confirm the tag exists before applying.
4. **Approve provisioning:** Run `terraform apply` only with explicit cost approval. Do not enable the currently disabled GitHub Actions deployment job automatically.
5. **Verify Azure runtime:** Confirm ACR managed identity pull, Container App revision health, PostgreSQL private DNS/TLS, `/health` and `/db-health`, logs and expected metrics. Perform migrations only as part of an approved database rollout.
6. **Capture evidence:** Save Terraform plan summary (without secrets), deployed resource screenshots, application endpoint, Log Analytics queries, and any troubleshooting/rollback notes.
7. **Cleanup:** Destroy test infrastructure after verification, confirm resources are gone, and separately review persistent backend storage and other non-Terraform resources. Never delete remote state casually.

## Current limitations

- CI has passed, but full Azure deployment has not been validated.
- The workflow `azure-deploy.yml` intentionally contains `if: false` for the deploy job.
- The Terraform monitoring configuration in this package is checked by credential-free CI using the repository provider lockfile; it has not been applied in Azure.
- The application currently uses PostgreSQL admin credentials; use a least-privilege account for actual production.

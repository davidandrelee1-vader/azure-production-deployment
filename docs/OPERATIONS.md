# Operations and Troubleshooting Quick Reference

| Symptom | Cloud engineer's first checks |
|---|---|
| Container App not starting | Revision status, container logs, image tag in ACR, managed identity/AcrPull |
| HTTP 503 from `/db-health` | Private DNS resolution, delegated subnet routing/NSG, PG host/port, TLS trust, database availability |
| No application logs | Container Apps environment logging destination, Log Analytics workspace, ingestion delay |
| Terraform plan fails | Azure CLI login/subscription, backend access, provider versions, resource quotas and policies |
| Deployment introduces errors | Compare revisions and configuration, roll back to known-good image/revision after impact review |
| Unexpected Azure charges | Azure Cost Management by resource group and service; confirm PostgreSQL, logs and backend storage |

## Log Analytics sample queries (after deployment)

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc
| take 50
```

```kusto
ContainerAppSystemLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc
| take 50
```

Table names and schemas should be verified against the actual workspace, as they may differ by collection configuration. Log ingestion may be delayed.

## Operational approach

Assess impact and dependencies, test changes when practical, plan rollback, make controlled changes, and validate service behavior afterward.

# Monitoring and Alerts

## Overview

Effective monitoring and alerting are critical for maintaining backup and disaster recovery health. Azure provides comprehensive tools to track backup jobs, replication status, and system health, enabling proactive management and rapid response to issues.

## Why Monitoring is Critical

**Key benefits:**
- **Early issue detection**: Identify problems before they impact recovery
- **Compliance verification**: Ensure backups meet policy requirements
- **Performance optimization**: Track and improve backup/restore times
- **Audit trail**: Maintain records for compliance and reporting
- **Proactive management**: Address issues before they become critical

## Monitoring Backup Jobs

### Viewing Backup Jobs

**From Recovery Services Vault:**
```
Recovery Services Vault → Backup Jobs
```

**Information displayed:**

| Column | Description |
|--------|-------------|
| **Job Type** | Backup, Restore, Configure Backup |
| **Status** | In Progress, Completed, Failed, Completed with Warnings |
| **Item Name** | VM or server being backed up |
| **Start Time** | When job began |
| **Duration** | How long job took/is taking |
| **Error Details** | Failure reason (if applicable) |

### Job Statuses

#### In Progress

**Meaning:** Backup job currently running

**What to monitor:**
- Duration (ensure within expected timeframe)
- Progress percentage (if available)
- No errors or warnings

**Action:** Wait for completion, monitor for timeouts

#### Completed

**Meaning:** Backup job finished successfully

**Verification:**
- Recovery point created
- Data transferred to vault
- No warnings

**Action:** None required

#### Completed with Warnings

**Meaning:** Backup succeeded but encountered minor issues

**Common warnings:**
- Some files were locked and couldn't be backed up
- Temporary network issues (but backup completed)
- Non-critical errors during snapshot

**Action:**
- Review warning details
- Determine if action needed
- Document for future reference

#### Failed

**Meaning:** Backup job did not complete successfully

**Common causes:**
- Network connectivity issues
- Insufficient permissions
- VM agent not responding
- Disk space issues
- Timeout

**Action:** **Immediate attention required**

### Backup Job Visibility

> [!IMPORTANT]
> Backup jobs appear in the Recovery Services Vault **as soon as they start**, providing real-time visibility into backup operations.

**Timeline:**
```
Backup Initiated → Immediately visible in Backup Jobs
Job Running → Status updates in real-time
Job Completes → Final status and details available
```

**Example from session:**
```
MARS Agent backup started on AWS VM
→ Job appears in Azure Recovery Services Vault immediately
→ Status: In Progress
→ Can monitor from Azure Portal in real-time
```

## Alert Configuration

### Types of Alerts

Azure Backup supports alerts for:
- **Backup failures**
- **Restore failures**
- **Replication health issues**
- **Configuration changes**
- **Security events**

### Configuring Backup Failure Alerts

**1. Navigate to Alerts**
```
Recovery Services Vault → Monitoring → Alerts
→ + New alert rule
```

**2. Define Scope**
- Select Recovery Services Vault
- Choose specific backup items (or all)

**3. Configure Condition**

**Signal type:** Backup Health Event

**Alert logic:**
```
Event level: Error
Status: Active
Event type: Backup failure
```

**4. Define Action Group**

**Action group components:**
- **Notifications**: Email, SMS, push notifications
- **Actions**: Webhook, Logic App, Azure Function, Runbook

**Example notification configuration:**
```
Email: backup-team@company.com
SMS: +1-555-0100 (on-call engineer)
```

**5. Configure Alert Details**

- **Alert rule name**: `Backup-Failure-Alert`
- **Description**: `Alert when any backup job fails`
- **Severity**: Error (Sev 2)
- **Enable upon creation**: Yes

**6. Review and Create**

### Alert Notification Example

**Email notification content:**
```
Subject: [ALERT] Backup Failure - prod-web-01

Alert Details:
- Resource: prod-web-01
- Vault: prod-backup-vault
- Job Type: Backup
- Status: Failed
- Time: 2024-01-15 02:30 AM UTC
- Error: VM agent not responding

Action Required:
1. Check VM agent status
2. Verify network connectivity
3. Re-run backup manually
4. Contact backup team if issue persists
```

## Manual Re-Run of Failed Backups

> [!NOTE]
> Engineers are expected to **manually re-run failed backups**. Automatic retry is not enabled by default to prevent repeated failures and allow for investigation.

### Re-Running a Failed VM Backup

**1. Investigate Failure**
```
Backup Jobs → Select failed job → View details
→ Review error message
→ Identify root cause
```

**2. Resolve Issue**

**Common issues and resolutions:**

| Issue | Resolution |
|-------|------------|
| **VM agent not responding** | Restart VM or reinstall agent |
| **Network timeout** | Check NSG rules, verify connectivity |
| **Insufficient permissions** | Verify backup service has required roles |
| **Disk space** | Free up space in cache location |
| **Snapshot timeout** | Reduce VM load, retry during off-hours |

**3. Trigger On-Demand Backup**
```
VM → Backup → Backup Now
→ Select retention period
→ Click OK
```

**4. Monitor New Job**
```
Recovery Services Vault → Backup Jobs
→ Verify new job completes successfully
```

**5. Document Resolution**
- Record issue and resolution
- Update runbooks if needed
- Share with team

### Re-Running a Failed MARS Agent Backup

**1. Check MARS Agent Console**
```
Microsoft Azure Backup → Jobs
→ Select failed job → View details
```

**2. Resolve Issue**

**Common issues:**
- Insufficient cache space
- Network connectivity
- Vault credentials expired
- Files locked by applications

**3. Trigger On-Demand Backup**
```
Microsoft Azure Backup → Back Up Now
→ Select retention
→ Click Back Up
```

**4. Verify Success**
- Monitor in MARS console
- Check Recovery Services Vault
- Verify recovery point created

## Monitoring Replication Health

### Viewing Replication Status

**From Recovery Services Vault:**
```
Site Recovery → Replicated Items
```

**Health indicators:**

| Status | Meaning | Action |
|--------|---------|--------|
| **Healthy** | Replication working normally | None |
| **Warning** | Minor issues detected | Investigate and resolve |
| **Critical** | Replication failing | Immediate action required |
| **Not Protected** | Replication not enabled | Enable if needed |

### Replication Metrics

**Key metrics to monitor:**

1. **RPO (Recovery Point Objective)**
   - Current lag between source and replica
   - Target: < 15 minutes
   - Alert if > 30 minutes

2. **Replication Health**
   - Percentage of healthy replicated items
   - Target: 100%
   - Alert if < 95%

3. **Test Failover Status**
   - Last successful test failover date
   - Target: Within last 90 days
   - Alert if > 90 days

4. **Synchronization Status**
   - Percentage synchronized
   - Target: 100%
   - Alert if < 100% for > 4 hours

### Replication Alerts

**Configure alerts for:**

**1. Replication Health Critical**
```
Signal: Site Recovery Health Event
Condition: Health status = Critical
Action: Email backup team, create incident
```

**2. RPO Threshold Exceeded**
```
Signal: RPO Exceeded
Condition: RPO > 30 minutes
Action: Email on-call engineer
```

**3. Test Failover Overdue**
```
Signal: Test Failover Not Performed
Condition: Last test > 90 days
Action: Email DR manager
```

## Monitoring Dashboard

### Creating a Custom Dashboard

**1. Navigate to Azure Portal Dashboard**
```
Azure Portal → Dashboard → + New dashboard
```

**2. Add Backup Tiles**

**Recommended tiles:**
- Backup Jobs (last 24 hours)
- Failed Backups (last 7 days)
- Protected Items count
- Storage consumed
- Replication health
- Upcoming scheduled backups

**3. Add Replication Tiles**
- Replicated items health
- RPO status
- Test failover status
- Replication jobs

**4. Add Alert Tiles**
- Active alerts
- Alert history
- Alert trends

**5. Save and Share**
- Name: `Backup and DR Monitoring`
- Share with backup team
- Set as default dashboard

### Dashboard Example Layout

```
┌─────────────────────────────────────────────────────┐
│  Backup and DR Monitoring Dashboard                 │
├─────────────────┬───────────────┬───────────────────┤
│ Backup Jobs     │ Failed Jobs   │ Protected Items   │
│ (Last 24h)      │ (Last 7d)     │                   │
│                 │               │                   │
│ ✓ 45 Completed  │ ✗ 2 Failed    │ 🛡️ 127 VMs        │
│ ⏳ 3 In Progress│ ⚠️ 1 Warning   │ 📁 15 File Shares │
├─────────────────┴───────────────┴───────────────────┤
│ Replication Health                                  │
│                                                     │
│ ✓ Healthy: 95 VMs                                  │
│ ⚠️ Warning: 3 VMs                                   │
│ ✗ Critical: 1 VM                                    │
├─────────────────────────────────────────────────────┤
│ Active Alerts                                       │
│                                                     │
│ • Backup failed: prod-db-02 (2 hours ago)          │
│ • RPO exceeded: prod-app-01 (30 minutes ago)       │
├─────────────────────────────────────────────────────┤
│ Storage Consumed                                    │
│                                                     │
│ Total: 15.2 TB                                     │
│ Trend: ↗️ +2.3 TB this month                        │
└─────────────────────────────────────────────────────┘
```

## Azure Monitor Integration

### Log Analytics Workspace

**Benefits:**
- Advanced querying with KQL
- Long-term log retention
- Custom visualizations
- Integration with other Azure services

**Setup:**
```
Recovery Services Vault → Diagnostic Settings
→ + Add diagnostic setting
→ Select logs to collect
→ Send to Log Analytics workspace
```

**Logs to enable:**
- Azure Backup Report Data
- Azure Site Recovery Jobs
- Azure Site Recovery Events
- Azure Site Recovery Replicated Items

### Sample KQL Queries

**Failed backups in last 7 days:**
```kusto
AzureDiagnostics
| where Category == "AzureBackupReport"
| where OperationName == "Backup"
| where Status_s == "Failed"
| where TimeGenerated > ago(7d)
| project TimeGenerated, BackupItemName_s, ErrorMessage_s
| order by TimeGenerated desc
```

**Replication health summary:**
```kusto
AzureDiagnostics
| where Category == "AzureSiteRecoveryReplicatedItems"
| summarize count() by ReplicationHealth_s
| render piechart
```

**Backup job duration trend:**
```kusto
AzureDiagnostics
| where Category == "AzureBackupReport"
| where OperationName == "Backup"
| where Status_s == "Completed"
| extend Duration = DurationInSeconds_s / 60
| summarize avg(Duration) by bin(TimeGenerated, 1d)
| render timechart
```

## Reporting

### Built-in Backup Reports

**Access reports:**
```
Recovery Services Vault → Backup Reports
```

**Available reports:**
- **Backup Items**: List of all protected items
- **Backup Jobs**: Job history and trends
- **Backup Policies**: Policy usage and compliance
- **Storage**: Storage consumption trends
- **Alerts**: Alert history and patterns

### Custom Reports

**Using Azure Workbooks:**

**1. Create Workbook**
```
Recovery Services Vault → Workbooks → + New
```

**2. Add Queries and Visualizations**
- Backup success rate
- Average backup duration
- Storage growth trend
- Failed backup analysis
- Replication health over time

**3. Schedule and Share**
- Save workbook
- Share with stakeholders
- Schedule automated delivery (via Logic App)

### Compliance Reporting

**Key metrics for compliance:**

| Metric | Target | Frequency |
|--------|--------|-----------|
| **Backup Success Rate** | > 98% | Daily |
| **Recovery Point Age** | < 24 hours | Daily |
| **Test Restore Success** | 100% | Quarterly |
| **DR Drill Completion** | 100% | Quarterly |
| **Policy Compliance** | 100% | Weekly |

## Proactive Monitoring Best Practices

### 1. Set Up Comprehensive Alerts

**Critical alerts:**
- Backup failures (immediate notification)
- Replication health critical (immediate)
- RPO exceeded (within 30 minutes)

**Warning alerts:**
- Backup completed with warnings (daily digest)
- Replication health warning (daily digest)
- Storage threshold exceeded (weekly)

**Informational alerts:**
- Test failover overdue (monthly)
- Policy changes (immediate)
- New protected items (daily digest)

### 2. Establish Monitoring Routines

**Daily:**
- Review backup job status
- Check for failed backups
- Verify replication health
- Address active alerts

**Weekly:**
- Review backup success rate
- Analyze storage consumption
- Check policy compliance
- Review warning trends

**Monthly:**
- Generate compliance reports
- Review and optimize policies
- Analyze cost trends
- Update documentation

**Quarterly:**
- Conduct DR drills
- Review and update alert thresholds
- Assess monitoring effectiveness
- Train team on new features

### 3. Automate Responses

**Use Azure Automation for:**
- Auto-remediation of common issues
- Automated backup retries (with limits)
- Notification escalation
- Report generation and distribution

**Example automation:**
```
Alert: Backup failed due to VM agent issue
→ Trigger runbook to restart VM agent
→ Wait 10 minutes
→ Trigger on-demand backup
→ If still fails, escalate to engineer
```

### 4. Maintain Documentation

**Document:**
- Alert response procedures
- Escalation paths
- Common issues and resolutions
- Monitoring dashboard access
- Report schedules

### 5. Regular Review and Optimization

**Quarterly review:**
- Alert effectiveness (false positives/negatives)
- Monitoring coverage (gaps)
- Response times (SLA compliance)
- Tool utilization (underused features)

**Continuous improvement:**
- Update alert thresholds based on trends
- Add monitoring for new workloads
- Optimize notification routing
- Enhance automation

## Monitoring Tools Comparison

| Tool | Use Case | Strengths | Limitations |
|------|----------|-----------|-------------|
| **Azure Portal** | Quick status checks | Easy to use, visual | Limited historical data |
| **Backup Reports** | Standard reporting | Pre-built, no setup | Limited customization |
| **Azure Monitor** | Advanced monitoring | Powerful querying, integration | Requires setup, learning curve |
| **Workbooks** | Custom dashboards | Highly customizable | Requires KQL knowledge |
| **MARS Console** | File-level backup monitoring | Local visibility | Only for MARS backups |

## Troubleshooting Monitoring Issues

### Alerts Not Firing

**Possible causes:**
- Alert rule misconfigured
- Action group not set up correctly
- Email blocked by spam filter

**Solutions:**
- Verify alert rule configuration
- Test action group
- Whitelist Azure email addresses

### Missing Backup Jobs

**Possible causes:**
- Backup not configured
- Backup schedule not reached
- VM deleted or stopped

**Solutions:**
- Verify backup configuration
- Check backup policy schedule
- Verify VM status

### Replication Status Not Updating

**Possible causes:**
- Replication agent issue
- Network connectivity problem
- Portal cache

**Solutions:**
- Check replication agent status
- Verify network connectivity
- Refresh portal (Ctrl+F5)

## Next Steps

- Review [Best Practices](./10-BestPractices.md) for comprehensive monitoring strategy
- Understand [Failover and Failback](./08-FailoverAndFailback.md) procedures
- Explore [Backup Policies](./05-BackupPolicies.md) for policy compliance monitoring

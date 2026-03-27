# Best Practices

## Overview

This guide consolidates best practices for Azure Backup and Disaster Recovery based on real-world experience, Microsoft recommendations, and lessons learned from the training session. Following these practices will help ensure robust data protection, efficient recovery, and cost-effective operations.

## Windows Server Recommendations

### Use Latest Windows Server Versions

> [!IMPORTANT]
> When provisioning new Windows VMs, use **Windows Server 2022** or **Windows Server 2024** for optimal performance, security, and support.

**Recommended versions:**
- ✅ **Windows Server 2024** (latest, best features)
- ✅ **Windows Server 2022** (stable, widely supported)
- ⚠️ **Windows Server 2019** (acceptable, but consider upgrading)
- ❌ **Windows Server 2016 or older** (avoid for new deployments)

**Benefits of latest versions:**
- Enhanced security features
- Better performance
- Longer support lifecycle
- Improved backup compatibility
- Modern management tools
- Better cloud integration

### VM Sizing for Windows

**Minimum recommended specifications:**

| Component | Minimum | Recommended | Use Case |
|-----------|---------|-------------|----------|
| **RAM** | 4 GB | **8 GB** | Standard workloads |
| **vCPUs** | 1 | **2** | Standard workloads |
| **OS Disk** | 127 GB | 256 GB | OS and applications |
| **Data Disk** | Varies | As needed | Application data |

**From session guidance:**
```
Ideal Windows VM Configuration:
- RAM: 8 GB minimum
- CPUs: 2 cores minimum
- OS Disk: 256 GB
- VM Size: Standard_D2s_v3 or better
```

**Why adequate resources matter:**
- Faster backup operations
- Better application performance
- Smoother failover/failback
- Reduced timeout issues
- Better user experience

### Remote Desktop Troubleshooting

**Common RDP connectivity issues:**

#### Issue: Cannot Connect via RDP

**Checklist:**

1. **Verify Port 3389 is Open**
   ```
   VM → Networking → Inbound port rules
   → Ensure RDP (3389) is allowed
   ```

2. **Check NSG Rules**
   - Verify Network Security Group allows port 3389
   - Check both NIC-level and subnet-level NSGs
   - Ensure source IP is allowed

3. **Verify VM is Running**
   ```
   VM → Overview → Status should be "Running"
   ```

4. **Check VM Memory**
   - Insufficient memory can cause RDP issues
   - Ensure VM has at least 8 GB RAM
   - Monitor memory usage in Azure Metrics

5. **Verify Public IP**
   - Ensure VM has public IP (if connecting from internet)
   - Or use Bastion for secure access

6. **Check Windows Firewall**
   - Use Run Command to check firewall status
   - Ensure RDP is allowed in Windows Firewall

**Quick fix commands:**
```powershell
# Enable RDP via Run Command
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

## Backup Strategy Best Practices

### 1. Implement Layered Protection

**Use multiple backup strategies:**

```
Layer 1: Daily VM Backups
  - Full VM protection
  - 30-day retention
  - Cross-region restore enabled

Layer 2: File-Level Backups (Critical Data)
  - MARS Agent for specific folders
  - 90-day retention
  - Faster granular recovery

Layer 3: Snapshots (Pre-Change)
  - Before major updates
  - Quick rollback capability
  - 7-day retention
```

### 2. Align Retention with Business Needs

**Don't over-retain:**
```
❌ Bad: Daily backups for 365 days (high cost, rarely needed)
✅ Good: Daily (30d) + Weekly (12w) + Monthly (12m) + Yearly (7y)
```

**Consider:**
- Regulatory requirements
- Business recovery needs
- Cost constraints
- Storage capacity

### 3. Enable Cross-Region Restore

**For all production vaults:**
```
Recovery Services Vault → Properties → Backup Configuration
→ Cross-region restore: Enabled
→ Storage redundancy: Geo-redundant (GRS)
```

**Why it's critical:**
- Protects against regional disasters
- Enables business continuity
- Meets compliance requirements
- Provides geographic redundancy

### 4. Test Backups Regularly

**Testing schedule:**
- **Monthly**: File-level restore test
- **Quarterly**: Full VM restore test
- **Annually**: Cross-region restore test

**What to test:**
- Restore completes successfully
- Data integrity verified
- Applications function correctly
- Recovery time meets RTO
- Documentation is accurate

### 5. Trigger Initial On-Demand Backup

> [!TIP]
> Always trigger an **on-demand backup immediately** after enabling backup for a VM. Don't wait for the scheduled time.

**Why:**
- Immediate protection
- Verify backup configuration works
- Identify issues early
- Establish baseline recovery point

**How:**
```
VM → Backup → Backup Now
→ Select retention period
→ Click OK
```

## Disaster Recovery Best Practices

### 1. Replicate All Critical VMs

**Identify critical workloads:**
- Production databases
- Application servers
- Domain controllers
- Critical business applications

**Enable replication:**
```
For each critical VM:
VM → Disaster Recovery → Enable replication
→ Configure target region
→ Monitor initial replication
```

### 2. Use Azure Paired Regions

**Recommended region pairs:**
- East US ↔ West US
- North Europe ↔ West Europe
- Southeast Asia ↔ East Asia

**Benefits:**
- Optimized network connectivity
- Coordinated platform updates
- Data residency compliance
- Priority recovery during outages

### 3. Create Recovery Plans

**Group related VMs:**
```
Recovery Plan: Production-Web-App
├── Group 1: Database Tier
│   ├── prod-db-01
│   └── prod-db-02
├── Group 2: Application Tier
│   ├── prod-app-01
│   └── prod-app-02
└── Group 3: Web Tier
    ├── prod-web-01
    └── prod-web-02
```

**Benefits:**
- Coordinated failover
- Proper startup order
- Automated scripts
- Consistent procedures

### 4. Perform Quarterly DR Drills

**DR drill schedule:**
```
Q1: Test failover for Tier 1 applications
Q2: Test failover for Tier 2 applications
Q3: Full production environment drill
Q4: Cross-region restore and failback drill
```

**Drill objectives:**
- Verify replication health
- Test failover procedures
- Train team members
- Validate RTO/RPO
- Update documentation

### 5. Monitor Replication Health Continuously

**Set up alerts for:**
- Replication health critical
- RPO exceeded (> 30 minutes)
- Synchronization issues
- Test failover overdue

**Daily monitoring:**
- Check replication status
- Verify synchronization percentage
- Review any warnings
- Address issues promptly

## Cost Optimization Best Practices

### 1. Right-Size Retention Policies

**Optimize retention:**
```
Before: Daily backups for 365 days
Cost: $X per month

After: Daily (30d) + Monthly (12m) + Yearly (7y)
Cost: $X * 0.6 per month (40% savings)
```

**Review quarterly:**
- Are all retention tiers needed?
- Can any be reduced?
- Are there unused protected items?

### 2. Clean Up Unused Vaults

> [!WARNING]
> Unused Recovery Services Vaults with retained backup data continue to incur storage charges. Always clean up properly.

**Quarterly review:**
```
For each vault:
1. Identify protected items
2. Determine if still needed
3. If not needed:
   - Stop backups
   - Delete backup data
   - Follow vault deletion procedure
   - Delete vault
```

**Vault deletion procedure:**
1. Stop all backups
2. Delete all backup data
3. Remove replication configurations
4. Download and run PowerShell script
5. Delete vault from portal

### 3. Use Appropriate Backup Types

**Cost comparison:**

| Backup Type | Cost | Use Case |
|-------------|------|----------|
| **Snapshot only** | Lowest | Dev/test, short-term |
| **File-level** | Low | Specific data, hybrid |
| **VM backup** | Medium | Production VMs |
| **VM backup + DR** | Highest | Critical workloads |

**Optimization:**
- Dev/test: Snapshots or weekly backups
- Standard prod: Daily VM backups
- Critical prod: Daily backups + DR replication

### 4. Optimize Instant Restore Retention

**Cost impact:**
```
Instant Restore 2 days: Standard cost
Instant Restore 5 days: +20% cost

Use 5 days only for critical VMs
Use 2 days for standard VMs
```

### 5. Monitor and Optimize Storage

**Storage optimization:**
- Review storage consumption trends
- Identify large backup items
- Optimize backup scope (exclude temp files)
- Clean up old recovery points
- Use appropriate storage tier

## Security Best Practices

### 1. Enable Soft Delete and Immutability

**For all vaults:**
```
Recovery Services Vault → Properties → Security Settings
→ Soft delete: Enabled (14 days)
→ Immutability: Enabled (optional, for critical data)
```

**Benefits:**
- Protection against accidental deletion
- Ransomware protection
- Compliance with retention policies
- Recovery from malicious deletion

### 2. Implement Proper RBAC

**Role assignments:**

| Role | Permissions | Assign To |
|------|-------------|-----------|
| **Backup Reader** | View only | Auditors, managers |
| **Backup Operator** | Backup and restore | Backup engineers |
| **Backup Contributor** | Manage policies | Backup admins |
| **Site Recovery Contributor** | Manage DR | DR team |

**Principle of least privilege:**
- Grant minimum necessary permissions
- Use Azure AD groups
- Regular access reviews
- Audit permission changes

### 3. Secure Encryption Passphrases

**For MARS Agent:**

> [!CAUTION]
> **Store encryption passphrases securely!** Without it, you cannot restore backup data. Microsoft cannot recover lost passphrases.

**Best practices:**
- Store in Azure Key Vault
- Use password manager (1Password, LastPass)
- Document location in runbooks
- Test passphrase works
- Maintain backup copy (separate location)

**Never:**
- Store in plain text files
- Email passphrases
- Share via unsecured channels
- Store only in one location

### 4. Monitor for Security Events

**Set up alerts for:**
- Backup deletion attempts
- Policy changes
- Vault configuration changes
- Unusual restore activity
- Failed authentication attempts

### 5. Regular Security Reviews

**Quarterly:**
- Review vault access logs
- Audit RBAC assignments
- Verify soft delete enabled
- Check for unauthorized changes
- Update security documentation

## Operational Best Practices

### 1. Document Everything

**Essential documentation:**

**Backup procedures:**
- How to enable backup
- How to configure policies
- How to trigger on-demand backup
- How to stop backups

**Recovery procedures:**
- File-level recovery steps
- VM recovery steps
- Cross-region restore steps
- MARS Agent recovery steps

**DR procedures:**
- Failover decision criteria
- Failover execution steps
- Failback execution steps
- Contact information

**Troubleshooting guides:**
- Common issues and resolutions
- Escalation paths
- Vendor support contacts

### 2. Maintain Current Runbooks

**Runbook requirements:**
- Step-by-step instructions
- Screenshots where helpful
- Expected outcomes
- Troubleshooting steps
- Last updated date

**Update triggers:**
- After each DR drill
- When procedures change
- When infrastructure changes
- Quarterly review

### 3. Establish Clear Ownership

**Define responsibilities:**

**Backup Team:**
- Vault management
- Policy configuration
- Backup monitoring
- Issue resolution
- Reporting

**DR Team:**
- Replication management
- DR drill coordination
- Failover/failback execution
- DR testing
- Documentation

**Application Teams:**
- Identify critical workloads
- Define RTO/RPO requirements
- Participate in DR drills
- Validate application functionality
- Provide application expertise

### 4. Implement Change Management

**For backup/DR changes:**
- Document proposed change
- Assess impact and risk
- Get approval
- Schedule maintenance window
- Execute change
- Verify success
- Update documentation

**Changes requiring approval:**
- Policy modifications
- Vault configuration changes
- Replication setup/removal
- Failover/failback operations

### 5. Continuous Improvement

**Regular reviews:**
- **Monthly**: Backup success rates, failed jobs
- **Quarterly**: Policies, costs, DR readiness
- **Annually**: Overall strategy, technology updates

**Improvement areas:**
- Automation opportunities
- Process optimization
- Cost reduction
- Performance enhancement
- Documentation updates

## Monitoring Best Practices

### 1. Set Up Comprehensive Alerts

**Critical (immediate notification):**
- Backup failures
- Replication health critical
- Vault deletion attempts

**Warning (daily digest):**
- Backup completed with warnings
- Replication health warning
- Storage threshold exceeded

**Informational (weekly digest):**
- Backup success summary
- Storage consumption trends
- Policy compliance status

### 2. Create Monitoring Dashboards

**Dashboard components:**
- Backup job status (last 24 hours)
- Failed backups (last 7 days)
- Protected items count
- Replication health
- Storage consumption
- Active alerts

**Share with:**
- Backup team (detailed dashboard)
- Management (summary dashboard)
- Application teams (their workloads)

### 3. Regular Health Checks

**Daily:**
- Review backup job status
- Check for failed backups
- Verify replication health
- Address active alerts

**Weekly:**
- Analyze backup success rate
- Review storage consumption
- Check policy compliance
- Review warning trends

**Monthly:**
- Generate compliance reports
- Review cost trends
- Analyze performance metrics
- Update stakeholders

### 4. Proactive Issue Resolution

**Don't wait for failures:**
- Monitor trends for degradation
- Address warnings promptly
- Investigate slow backups
- Resolve replication lag
- Update agents proactively

### 5. Maintain Audit Trail

**Log and track:**
- All backup operations
- All restore operations
- Policy changes
- Vault configuration changes
- Failover/failback events
- Access and permissions changes

## Compliance Best Practices

### 1. Meet Regulatory Requirements

**Understand requirements:**
- Data retention periods
- Geographic restrictions
- Encryption requirements
- Audit trail needs
- Recovery time requirements

**Implement controls:**
- Configure appropriate retention
- Use geo-redundancy where required
- Enable encryption (automatic in Azure)
- Maintain audit logs
- Document compliance

### 2. Regular Compliance Reporting

**Reports to generate:**
- Backup success rate
- Policy compliance
- Test restore results
- DR drill outcomes
- Security events

**Frequency:**
- Monthly: Operational reports
- Quarterly: Compliance reports
- Annually: Audit reports

### 3. Maintain Evidence

**Keep records of:**
- Backup configurations
- Policy definitions
- Test restore results
- DR drill reports
- Incident responses
- Change approvals

## Quick Reference Checklist

### New VM Backup Setup
- [ ] Use Windows Server 2022 or 2024
- [ ] Size VM appropriately (8 GB RAM, 2 CPUs minimum)
- [ ] Create or select Recovery Services Vault
- [ ] Enable cross-region restore
- [ ] Configure backup policy
- [ ] Enable backup
- [ ] Trigger initial on-demand backup
- [ ] Verify backup job completes
- [ ] Set up failure alerts
- [ ] Document configuration

### DR Setup for Critical VM
- [ ] Identify VM as critical workload
- [ ] Enable replication to paired region
- [ ] Monitor initial replication (may take 8+ hours)
- [ ] Verify replication status: Protected
- [ ] Create or add to recovery plan
- [ ] Configure network mapping
- [ ] Set up replication health alerts
- [ ] Schedule quarterly DR drill
- [ ] Document failover procedures
- [ ] Test failover (non-production)

### Monthly Maintenance
- [ ] Review backup success rate
- [ ] Investigate and resolve failed backups
- [ ] Check replication health
- [ ] Review storage consumption
- [ ] Verify policy compliance
- [ ] Update documentation as needed
- [ ] Review and address alerts
- [ ] Generate compliance reports

### Quarterly Tasks
- [ ] Conduct DR drill
- [ ] Review and optimize policies
- [ ] Review and optimize costs
- [ ] Test cross-region restore
- [ ] Review RBAC assignments
- [ ] Update runbooks
- [ ] Train team on procedures
- [ ] Review and update documentation

## Next Steps

- Review [Backup Strategies](./01-BackupStrategies.md) for implementation guidance
- Understand [Recovery Services Vault](./02-RecoveryServicesVault.md) setup
- Configure [VM Backup](./03-VMBackup.md) for your workloads
- Set up [MARS Agent](./04-MARSAgent.md) for hybrid scenarios
- Define [Backup Policies](./05-BackupPolicies.md) aligned with business needs
- Plan [Disaster Recovery](./07-DisasterRecovery.md) for critical workloads
- Implement [Monitoring and Alerts](./09-MonitoringAndAlerts.md) for proactive management

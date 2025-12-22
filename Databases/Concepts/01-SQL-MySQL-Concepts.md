# Azure SQL and MySQL Concepts

## Azure SQL Database

Azure SQL Database is a fully managed platform as a service (PaaS) database engine that handles most of the database management functions such as upgrading, patching, backups, and monitoring without user involvement.

### Service Tiers and Purchasing Models
- **DTU-based model**: Bundles compute and storage packages (Basic, Standard, Premium). Good for pre-configured resource options.
- **vCore-based model**: Allows you to choose compute (vCores) and storage independently. Offers more flexibility and control (General Purpose, Business Critical, Hyperscale).

### High Availability vs Disaster Recovery
- **High Availability (HA)**: Ensures your database is up and running within the same region (e.g., Zone Redundant storage).
- **Disaster Recovery (DR)**: Ensures your database can survive a region-wide outage.

#### Active Geo-Replication
- Creates a readable secondary database in the same or different region.
- You can manually failover to the secondary.
- Good for read-scale out (offloading read workloads).

#### Auto-Failover Groups
- Manages replication and failover of a group of databases to another region.
- complete abstraction: provides **Read-Write** and **Read-Only** listener endpoints.
    - You connects to `failover-group.database.windows.net` instead of `server-name.database.windows.net`.
    - If a failover happens, the DNS automatically points to the new primary. You don't need to change connection strings.

## Azure Database for MySQL

A fully managed service for MySQL Community Edition.

### Deployment Options
- **Single Server**: Deprecated model.
- **Flexible Server**: The recommended deployment option. It provides better control over high availability, maintenance windows, and cost optimization (burstable tier).

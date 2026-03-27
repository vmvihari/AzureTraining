# Log Analytics

## Log Analytics Workspace

A **Log Analytics Workspace** is the central repository for all log data collected from your Azure resources. It acts as a database where logs are stored, indexed, and queried.

### Key Functions
-   **Ingestion**: Receives logs from VMs, applications, and other Azure services.
-   **Storage**: Retains data based on configured retention policies (default is 30 days).
-   **Querying**: Allows deep analysis using KQL.

## Data Collection Rules (DCR)

Data Collection Rules define the specific data streams to capture.

### Linux Logs
-   **Syslog**: Standard logging protocol for Linux.
-   **Facilities**: auth, daemon, kern, syslog, user, etc.
-   **Severity Levels**: Error, Warning, Info, Debug.

### Windows Logs
-   **Event Logs**: Standard logging system for Windows.
-   **Categories**: Application, System, Security.
-   **Levels**: Critical, Error, Warning, Information.

> [!NOTE]
> Log data is not instantaneous. It typically takes around **one hour** for logs to appear in the workspace after initial configuration.

## Kusto Query Language (KQL)

KQL is the powerful query language used to retrieve and analyze data in Log Analytics.

### Basic Structure
A KQL query typically starts with a table name followed by a series of operators separated by pipes (`|`).

```kusto
// Example: Retrieve the last 10 heartbeat records for a specific computer
Heartbeat
| where Computer == "Linux-VM-01"
| top 10 by TimeGenerated desc
```

### Common Operators
-   `where`: Filters the data based on a condition.
-   `take` / `limit`: Returns a specific number of records.
-   `project`: Selects specific columns to display.
-   `summarize`: Aggregates data (e.g., count, average).
-   `render`: Visualizes the results (e.g., timechart, barchart).

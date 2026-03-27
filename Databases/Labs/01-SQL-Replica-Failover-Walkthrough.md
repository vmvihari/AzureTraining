# Walkthrough: SQL Replica & Failover Lab

This document provides step-by-step instructions to complete the [01-SQL-Replica-Failover-Lab.md](./01-SQL-Replica-Failover-Lab.md).

---

## Part 1: Azure SQL Primary Database Setup (Central US)

### 1. Create Resource Group
1. Sign in to the [Azure Portal](https://portal.azure.com).
2. Search for **Resource groups** and click **Create**.
3. **Subscription**: Select your subscription.
4. **Resource group**: `rg-sql-replica-hw`
5. **Region**: `Central US`
6. Click **Review + create**, then **Create**.

### 2. Create SQL Server (Primary)
1. Search for **SQL Servers** (not "SQL database" yet) and click **Create**.
2. **Resource Group**: `rg-sql-replica-hw`
3. **Server name**: `sql-central-hw-<yourname>-001` (Replace `<yourname>` with your name, e.g., `sql-central-hw-jane-001`).
4. **Location**: `Central US`
5. **Authentication**: Select **Use SQL authentication**.
    - **Admin login**: `sqladmin`
    - **Password**: Enter a strong password (e.g., `Pa$$w0rd1234`).
6. Click **Review + create**, then **Create**. Wait for deployment to finish.

### 3. Create SQL Database
1. Go to your new SQL Server resource (`sql-central-hw...`).
2. Click **Create database**.
3. **Database name**: `sqldb-central-hw-001`
4. **Workload environment**: Development.
5. **Compute + storage**: Click **Configure database**.
    - Select **Service tier**: **Basic** (for lowest cost) or **General Purpose**.
    - Click **Apply**.
6. Click **Review + create**, then **Create**.

### 4. Configure Firewall
1. On your SQL Server blade (`sql-central-hw...`), go to **Security** -> **Networking**.
2. Under **Public network access**, ensure **Selected networks** is selected.
3. Check **Add your client IPv4 address** (this adds your current IP).
4. (Optional) Check **Allow Azure services and resources to access this server** (useful for connecting from other Azure resources).
5. Click **Save**.

### 5. Create Table and Insert Data
1. Open **Azure Data Studio** or **SSMS** on your machine.
2. Create a **New Connection**:
    - **Server**: `sql-central-hw-<yourname>-001.database.windows.net`
    - **Authentication**: SQL Server Authentication
    - **User**: `sqladmin`
    - **Password**: (Your password)
    - **Database**: `sqldb-central-hw-001`
3. Connect and open a **New Query** window.
4. Run the following script:

```sql
CREATE TABLE dbo.Employees (
    EmpId INT IDENTITY(1,1) PRIMARY KEY,
    EmpName VARCHAR(100),
    Dept VARCHAR(50),
    CreatedAt DATETIME DEFAULT GETDATE()
);

INSERT INTO dbo.Employees (EmpName, Dept)
VALUES ('Asha','IT'), ('Rahul','HR'), ('Meena','Finance');

SELECT * FROM dbo.Employees;
```
5. **Take Screenshots**:
    - SQL Server + Database overview page in Portal.
    - Networking page showing your IP rule.
    - Query result showing 3 rows.

---

## Part 2: Create a Secondary Server (West US) + Geo-Replica

### 1. Configure Geo-Replication
1. In the Azure Portal, **ensure you are on the SQL Database page** (`sqldb-central-hw-001`), NOT the SQL Server page.
2. Search the left-hand menu for **"Replicas"** or **"Geo-Replication"**.
    - It is often under **Data management** or **Settings**.
    - If you don't see it, type "Repliacs" or "Geo" in the search box at the top left of the menu.
3. Click **Replicas** (or Geo-Replication).
4. Click **+ Create replica** or select the target region (e.g., **West US**) from the map or list.

### 2. Create Secondary Server
1. In the **Create replica** pane that opens:
2. **Server**: Click **Create new**.
    - **Server name**: `sql-west-hw-<yourname>-001`
    - **Location**: `West US` (should be auto-selected)
    - **Authentication**: Usage primary server's credentials.
    - Click **OK**.
3. **Compute + Storage**: Ensure it matches the primary (e.g., Basic).
4. Click **Create** (or **OK**).
5. Wait for the deployment to finish. The map will show a solid link between Central US and West US when seeding is 100% complete.

### 3. Verify Read-Only Replica
1. In Azure Data Studio, create a **new connection** to the **West US** server:
    - **Server**: `sql-west-hw-<yourname>-001.database.windows.net`
    - **User/Password**: Same as primary.
2. Connect to the database (`sqldb-central-hw-001`).
3. Run a `SELECT` query:
   ```sql
   SELECT * FROM dbo.Employees;
   ```
   (You should see the same data).
4. Try to delete a row:
   ```sql
   DELETE FROM dbo.Employees WHERE EmpName='Rahul';
   ```
5. **Take Screenshot**: Capture the error message. It should say roughly: *"Failed...(Read-only)"*.

---

## Part 3: Verify Sync from Primary to Replica

1. Switch back to your **Primary (Central US)** query window.
2. Run the delete command:
   ```sql
   DELETE FROM dbo.Employees WHERE EmpName='Rahul';
   SELECT * FROM dbo.Employees;
   ```
   (Row 'Rahul' should be gone).
3. Switch to your **Replica (West US)** query window.
4. Run:
   ```sql
   SELECT * FROM dbo.Employees;
   ```
   (Row 'Rahul' should be gone here too).
5. **Take Screenshots** of both outputs.

---

## Part 4: Create a Failover Group

### 1. Create Failover Group
1. Go to the **Primary Server** (`sql-central-hw...`) blade.
2. Under **Data management**, click **Failover groups**.
3. Click **Add group**.
4. **Failover group name**: `fog-hw-<yourname>-001` (must be globally unique).
5. **Server**: Click to select the secondary server (`sql-west-hw...`).
6. **Read/Write grace period**: Leave default (1 hour).
7. **Add databases**: Select `sqldb-central-hw-001`.
8. Click **Create**.

### 2. Connect via Listener Endpoint
1. Once created, look at the Failover group details.
2. Copy the **Read-write listener endpoint** (e.g., `fog-hw-<...>.database.windows.net`).
3. In Azure Data Studio, create a **New Connection**:
    - **Server**: Paste the listener endpoint.
    - **User/Password**: Same `sqladmin`.
4. Run:
   ```sql
   INSERT INTO dbo.Employees (EmpName, Dept) VALUES ('Kiran','Support');
   SELECT * FROM dbo.Employees;
   ```
5. **Take Screenshots**:
    - Failover group config page.
    - Successful INSERT output.

---

## Part 5: Azure Database for MySQL

### 1. Create MySQL Server
1. Search **Azure Database for MySQL** and click **Create**.
2. SQL database type: **Flexible Server**.
3. **Resource Group**: `rg-sql-replica-hw`.
4. **Server name**: `mysql-hw-<yourname>-001`.
5. **Region**: `Central US` (or any available).
6. **Workload type**: Development or Hobbyist (Burstable B1s is cheapest).
7. **Authentication**:
    - **Username**: `mysqladmin`
    - **Password**: (Enter password).
8. **Networking**:
    - **Connectivity method**: Public access (allowed IP addresses).
    - Checks **Allow public access from any Azure service...**
    - Click **Add current client IP address**.
9. Click **Review + create**, then **Create**. (This takes a few minutes).

### 2. Connect with MySQL Workbench
1. Open **MySQL Workbench**.
2. Click **+** to add a connection.
    - **Connection Name**: Azure MySQL
    - **Hostname**: `mysql-hw-<yourname>-001.mysql.database.azure.com`
    - **Username**: `mysqladmin`
    - Click **Store in Vault** to enter password.
3. Click **Test Application** then **OK**.
4. Open the connection.
5. Run the SQL:
   ```sql
   CREATE DATABASE trainingdb;
   USE trainingdb;
   CREATE TABLE students (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(100),
     course VARCHAR(100),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   INSERT INTO students (name, course)
   VALUES ('John','Azure'), ('Sara','SQL');
   SELECT * FROM students;
   ```
6. **Take Screenshots**:
    - MySQL Overview page in Portal.
    - Workbench output.

---

## Part 6: Cleanup
1. Go to **Resource groups**.
2. Click `rg-sql-replica-hw`.
3. Click **Delete resource group**.
4. Type the name to confirm and click **Delete**.
5. **Take Screenshot**: Showing the empty or deleted resource group.

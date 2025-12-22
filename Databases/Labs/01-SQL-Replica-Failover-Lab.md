# Homework: Azure SQL Database Replica, Failover Group (DR), and MySQL

## Part 1: Azure SQL Primary Database Setup (Central US)
**Resource Group**: `rg-sql-replica-hw`
**SQL Server**: `sql-central-hw-<yourname>-001`
**Database**: `sqldb-central-hw-001`

### Tasks
1. Create **SQL Server** + **SQL Database** (Basic/General Purpose is fine) in **Central US**.
2. Configure **SQL authentication** (admin user + password).
3. Set **Server-level firewall rule** to allow your client public IP.
4. Connect using **Azure Data Studio / SSMS** and run:

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

> **Submission proof**:
> - Screenshot of SQL Server + Database overview page
> - Screenshot of firewall rule page showing your IP rule
> - Screenshot of query output showing 3 rows

---

## Part 2: Create a Secondary Server (West US) + Geo-Replica (Read-Only)
**SQL Server**: `sql-west-hw-<yourname>-001` (in **West US**)

### Tasks
1. on the **Central US** database blade, click **Geo-Replication** (under Data management).
2. Add a replica in **West US**. You will need to create the new server (`sql-west-hw...`) during this step.
3. Wait for seeding to reach 100%.
4. Connect to the **Replica Database** (West US server).
5. Run:
   ```sql
   SELECT * FROM dbo.Employees;
   ```
6. Verify read-only behavior by attempting:
   ```sql
   DELETE FROM dbo.Employees WHERE EmpName='Rahul';
   ```
   *Expected result: Failed (Read-only).*

> **Submission proof**:
> - Screenshot showing geo-replication status (Central DB page)
> - Screenshot of SELECT output on replica
> - Screenshot of the error when trying DELETE on replica

---

## Part 3: Verify Sync from Primary to Replica

### Tasks
1. Connect to the **Primary** (Central US) database and run:
   ```sql
   DELETE FROM dbo.Employees WHERE EmpName='Rahul';
   SELECT * FROM dbo.Employees;
   ```
2. Connect back to the **Replica** (West US) and run:
   ```sql
   SELECT * FROM dbo.Employees;
   ```
   *Expected result: Replica should reflect the deletion.*

> **Submission proof**:
> - Screenshot of primary output after delete
> - Screenshot of replica output showing data synced

---

## Part 4: Create a Failover Group (Disaster Recovery Setup)

### Tasks
1. Go to the **Primary Server** (Central US) -> **Failover groups**.
2. Add a group:
   - **Failover Group Name**: `fog-hw-<yourname>-001` (must be globally unique)
   - **Servers**: Primary is Central, Secondary is West.
   - **Databases**: Add `sqldb-central-hw-001`.
3. Note down the endpoints:
   - **Read-write listener**: `fog-hw-<...>.database.windows.net`
4. Connect nicely using the **Read-write listener** endpoint and run:
   ```sql
   INSERT INTO dbo.Employees (EmpName, Dept) VALUES ('Kiran','Support');
   SELECT * FROM dbo.Employees;
   ```

> **Submission proof**:
> - Screenshot of failover group configuration page
> - Screenshot of successful INSERT via read-write listener

---

## Part 5: Azure Database for MySQL (Basic Setup + Workbench)

**Server name**: `mysql-hw-<yourname>-001` (Flexible Server recommended)

### Tasks
1. Create Azure Database for MySQL.
2. Allow your public IP in networking.
3. Connect using **MySQL Workbench**.
4. Run:
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

> **Submission proof**:
> - Screenshot of MySQL server overview page
> - Screenshot of Workbench connection + query output

---

## Part 6: Cost-Control (Mandatory Cleanup)
1. Delete the resource group `rg-sql-replica-hw`.
2. Delete MySQL resource group if different.

> **Submission proof**: Screenshot showing Resource Group deleted OR Empty.

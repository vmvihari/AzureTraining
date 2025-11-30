# App Service Overview

## What is Azure App Service?

Azure App Service is a **Platform as a Service (PaaS)** offering that enables you to build, deploy, and scale web apps, mobile backends, and RESTful APIs. It supports multiple languages and frameworks, including .NET, Java, Node.js, Python, and PHP.

### Key Benefits
-   **Fully Managed**: Azure handles OS patching, load balancing, and high availability.
-   **DevOps Integration**: Built-in support for GitHub, Azure DevOps, and Docker Hub.
-   **Global Scale**: High availability with SLA-backed uptime.

## Shared Responsibility Model

In a PaaS environment like App Service, the responsibility is shared between you and Microsoft:

| Responsibility | Managed By |
| :--- | :--- |
| Physical Datacenter | Microsoft |
| Network & Infrastructure | Microsoft |
| Operating System | Microsoft |
| Runtime & Middleware | Microsoft |
| **Application Code** | **You** |
| **Data & Content** | **You** |
| **Identity & Access** | **You** |

> [!IMPORTANT]
> While Azure manages the platform, **you are responsible for your data**. This includes configuring database backups, securing connection strings, and managing user access.

## Database Integration

App Service is often paired with a database to create full-stack applications.
-   **Cosmos DB**: A globally distributed, multi-model database service. It supports MongoDB API, making it easy to migrate existing Node.js/MongoDB apps.
-   **Azure Cache for Redis**: Can be added to improve performance by caching frequently accessed data, reducing load on the primary database.

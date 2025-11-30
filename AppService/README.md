# Azure App Service

## Overview

Azure App Service is a fully managed Platform as a Service (PaaS) for building, deploying, and scaling web apps. It allows you to focus on your application code without worrying about the underlying infrastructure (VMs, OS patching, etc.).

## Table of Contents

### Concepts

1. [App Service Overview](./Concepts/01-AppServiceOverview.md) - Introduction to PaaS and shared responsibilities
2. [Deployment and Scaling](./Concepts/02-DeploymentAndScaling.md) - Deployment options and scaling strategies
3. [Deployment Slots](./Concepts/03-DeploymentSlots.md) - Managing environments and zero-downtime swaps
4. [Custom Domains](./Concepts/04-CustomDomains.md) - Configuring custom domains for your apps

## Key Takeaways

- **PaaS Offering**: Azure manages the infrastructure; you manage the code and data.
- **Deployment Slots**: Essential for safe "Dev → Test → Prod" workflows with zero downtime.
- **Scaling**: Supports both Vertical (Scale Up) and Horizontal (Scale Out) scaling.
- **Integration**: Seamlessly integrates with GitHub and Azure DevOps for CI/CD.

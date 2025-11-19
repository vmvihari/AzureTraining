# Azure Projects

This directory contains hands-on Azure projects that demonstrate practical implementations of various Azure services and concepts.

## Projects Overview

### [Project 1: Azure Multi-Environment Custom Image Deployment with Packer](./Project1-Packer-Multi-Environment/README.md)

**Objective**: Build three isolated environments (Dev, Test, Prod) with custom VM images using Packer.

**Key Concepts Covered**:
- Service Principal creation and management
- Azure RBAC (Role-Based Access Control)
- Virtual Network configuration and peering
- Custom image creation with Packer
- Multi-environment infrastructure deployment

**Technologies Used**:
- Packer
- Azure CLI
- Microsoft Entra ID (Azure AD)
- Azure Virtual Networks
- Azure Virtual Machines

**Difficulty**: Intermediate

---

## Project Structure

Each project folder contains:
- **README.md** - Detailed step-by-step instructions
- **Configuration files** - Packer templates, scripts, etc. (where applicable)
- **Documentation** - Architecture diagrams, troubleshooting guides

## Getting Started

1. Choose a project from the list above
2. Navigate to the project folder
3. Follow the step-by-step instructions in the project's README
4. Complete the validation steps to ensure successful implementation

## Prerequisites

Most projects require:
- Active Azure subscription
- Azure CLI installed
- Basic understanding of cloud computing concepts
- Familiarity with command-line interfaces

Specific prerequisites are listed in each project's README.

## Contributing

When adding new projects:
1. Create a new folder with the naming convention: `ProjectX-Description`
2. Include a comprehensive README with step-by-step instructions
3. Update this README with project details
4. Include validation steps and troubleshooting sections

# Custom Domains

## Overview

By default, Azure App Service provides a domain like `myapp.azurewebsites.net`. For production applications, you typically want to use your own custom domain (e.g., `www.contoso.com`).

## Configuration Steps

1.  **Purchase Domain**: Buy a domain from a registrar (GoDaddy, Namecheap, etc.) or through Azure.
2.  **Verify Ownership**: Add a TXT record to your DNS configuration to prove you own the domain.
3.  **Add Binding**: In the App Service "Custom domains" blade, add your domain.
4.  **Configure DNS**:
    -   **A Record**: Maps the root domain (`contoso.com`) to the App Service IP address.
    -   **CNAME Record**: Maps a subdomain (`www.contoso.com`) to the default Azure domain (`myapp.azurewebsites.net`).

## Subdomains for Environments

You can map different subdomains to different deployment slots to create distinct access points for each environment.

-   `www.contoso.com` -> **Production Slot**
-   `dev.contoso.com` -> **Development Slot**
-   `test.contoso.com` -> **Staging Slot**

This allows stakeholders to access specific versions of the application using friendly URLs.

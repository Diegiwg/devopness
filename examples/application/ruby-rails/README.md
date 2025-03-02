# Ruby on Rails - Devopness Example

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://github.com/devopness/devopness/blob/main/LICENSE)

## Overview

This example demonstrates how to integrate a Ruby on Rails application with Devopness. It covers the process of adding an application, configuring environment variables, and deploying your application using the Devopness platform.

## 🚀 Getting Started

### Adding an Application

- Documentation: [Add an Application](https://www.devopness.com/docs/applications/add-application/)

To add your Ruby on Rails application to Devopness:

1. On Devopness, navigate to a **project** and select an **environment**
2. Locate the **Applications** card
3. Click **View** to see the list of existing applications
4. In the upper-right corner, click **ADD APPLICATION**
5. Select a **Source Provider**
6. Select a **Credential**
7. Choose the **Git Repository**: `devopness/devopness`
8. Choose the **Stack**: `Ruby`
9. Choose the **Engine Version**: `3.2.2`, then click **NEXT**
10. Choose the **Framework**: `Ruby on Rails`, then click **CONFIRM**
11. Once created, you can view the application details

## ⚙️ Configuring Environment Variables

Rails applications require specific environment variables, such as `RAILS_ENV`, `PORT`, and database credentials.

### Managing Environment Variables

1. Open the **Details** page of your application
2. Navigate to the **Variables** tab
3. In the upper-right corner, click **Add Variable**
4. Enter a name for the variable, such as `RAILS_ENV`
5. Enter the value for the variable, such as `production`
6. If needed, provide an optional description, such as `The environment in which the application runs`
7. Click **CONFIRM**

## 🚢 Deploying the Application

Deploying your application ensures that your latest code changes are applied with minimal downtime.

### Deployment Steps

1. Open the **Details** page of your application
2. Click **DEPLOY** on the application you want to deploy
3. Follow the prompts, then click **NEXT**
4. Review the deployment details, then click **CONFIRM**
5. A notification popup will confirm that the deployment has been triggered
6. Wait for the `Application Deploy` action to complete

## ✍️ Contributing

Contributions are highly encouraged! 🙏👊

See the [contributing guide](../../../CONTRIBUTING.md) for details on how to participate.

All communication and contributions to Devopness projects are subject to the [Devopness Code of Conduct](../../../CODE_OF_CONDUCT.md).

## 📜 License

All repository contents are licensed under the terms of the [MIT License](../../../LICENSE) unless otherwise specified.

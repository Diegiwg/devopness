# Ruby on Rails - Devopness Example

## Overview

This example demonstrates how to integrate a Ruby on Rails application with Devopness.

It covers adding an application, configuring environment variables, creating a daemon, setting up a virtual host, and deploying your application using the Devopness platform.

## 🚀 Getting Started

### Adding an Application

- Documentation: [Add an Application](https://www.devopness.com/docs/applications/add-application/)

To add your Ruby on Rails application to Devopness:

1. Navigate to a **project** on Devopness and select an **environment**.
2. Locate the **Applications** card.
3. Click **View** to see the list of existing applications.
4. In the upper-right corner, click **ADD APPLICATION**.
5. Select a **Source Provider**.
6. Select a **Credential**.
7. Choose the **Git Repository**: `devopness/devopness`.
8. Choose the **Stack**: `Ruby`.
9. Choose the **Engine Version**: `3.2.2`, then click **NEXT**.
10. Choose the **Framework**: `Ruby on Rails`.
11. Provide the **Root Directory**: `/examples/applications/ruby-rails`, then click **CONFIRM**.
12. Once created, you can view the application details.

## ⚙️ Configuring Environment Variables

Rails applications require specific environment variables, such as `RAILS_ENV`, `PORT`, and database credentials.

### Managing Environment Variables

1. Open the **Details** page of your application.
2. Navigate to the **Variables** tab.
3. Click **Add Variable** in the upper-right corner.
4. Enter a name for the variable, such as `RAILS_ENV`.
5. Enter the value for the variable, such as `production`.
6. Optionally, provide a description, such as `The environment in which the application runs`.
7. Click **CONFIRM**.

## 🛠️ Creating a Daemon for the Application

- Documentation: [Add a Daemon](https://www.devopness.com/docs/daemons/add-daemon)

To ensure your Rails application runs continuously as a background service, create a daemon:

1. Open the **Details** page of your application.
2. Click **ADD DAEMON** in the application details.
3. Provide a name for the daemon, such as `rails-server`.
4. Specify the command to start your application: `rails s`.
5. Click **CONFIRM** to create the daemon.

## 🌐 Creating a Virtual Host for the Application

- Documentation: [Add a Virtual Host](https://www.devopness.com/docs/virtual-hosts/add-virtual-host)

To make your application accessible via a domain or subdomain, set up a virtual host:

1. Open the **Details** page of your application.
2. Click **ADD VIRTUAL HOST** in the application details.
3. For a quick and simple test, select **Virtual Host Type**: `Server IP Address`.
4. Provide your **Server IP and port** (e.g., `127.0.0.1:9000`) as **Name**.
   - If you do not have a server, follow the [Add a Server](https://www.devopness.com/docs/servers/add-server) documentation before proceeding.
5. Specify the **Application Listen Address** as `http://localhost:{PORT}`.
   - If the `PORT` environment variable is not set, Rails defaults to `3000`.
6. Click **CONFIRM** to create the virtual host.

## 🚢 Deploying the Application

Deploying your application ensures that your latest code changes are applied with minimal downtime.

### Deployment Steps

1. Open the **Details** page of your application.
2. Click **DEPLOY** on the application you want to deploy.
3. Follow the prompts, then click **NEXT**.
4. Review the deployment details, then click **CONFIRM**.
5. A notification popup will confirm that the deployment has been triggered.
6. Wait for the `Application Deploy` action to complete.

## ✍️ Contributing

Contributions are highly encouraged! 🙏👊

See the [contributing guide](../../../CONTRIBUTING.md) for details on how to participate.

All communication and contributions to Devopness projects are subject to the [Devopness Code of Conduct](../../../CODE_OF_CONDUCT.md).

## 📜 License

All repository contents are licensed under the terms of the [MIT License](../../../LICENSE) unless otherwise specified.

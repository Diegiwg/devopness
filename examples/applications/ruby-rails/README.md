# Ruby on Rails - Devopness Example

## Overview

Integrate a Ruby on Rails application with Devopness for streamlined management and deployment.

This guide covers adding an application, configuring environment variables, creating a daemon, setting up a virtual host, and deploying your application using the Devopness platform.

## 🚀 Adding an Application

- Documentation: [Add an Application](https://www.devopness.com/docs/applications/add-application)

Add a Ruby on Rails application to your infrastructure environment so it can be managed and deployed through the Devopness web interface or automated workflows.

1. On Devopness, navigate to a project then select an environment
1. Find the **Applications** card
1. Click **View** in the Applications card to see a list of existing applications
1. On the upper-right corner of the list, click **ADD APPLICATION**
1. Select a **Source Provider**
1. Select a **Credential**
   - If no credential is listed or you want to use a different one, click **Create a new Credential** and follow the [Add a Credential](https://www.devopness.com/docs/credentials/add-credential) guide
1. Choose the **Git Repository**: `devopness/devopness`
1. Choose the **Stack**: `Ruby`
1. Choose the **Engine Version**: `3.4.2`, then click **NEXT**
1. Choose the **Framework**: `Ruby on Rails`
1. Provide the **Root Directory**: `/examples/applications/ruby-rails`, then click **CONFIRM**
1. In the Application details view, the newly created application details will be displayed

## ⚙️ Configuring Environment Variables

Rails applications require specific environment variables, such as `RAILS_ENV`, `PORT`, etc.

### Managing Environment Variables

1. On Devopness, navigate to the application's **Details** page
1. Open the **Variables** tab
1. Click **Add Variable** in the upper-right corner
1. Set the variable name to `RAILS_ENV`
1. Set the value to `development`
   - Optionally, add a description (e.g., *Defines the application's runtime environment*)
1. Click **CONFIRM** to save
1. Repeat the process for the `PORT` variable with a value of `9000`

## 🛠️ Creating a Daemon for the Application

- Documentation: [Add a Daemon](https://www.devopness.com/docs/daemons/add-daemon)

Ensure the Rails application runs continuously as a background service by adding a daemon.

1. On Devopness, navigate to the application's **Details** page
1. Click **ADD DAEMON** in the application details
1. Provide a **Name** for the daemon, such as `rails-server`
1. Specify the **Command** to start your application:

   ```sh
   bundle exec rails server
   ```

1. Click **CONFIRM** to create the daemon

## 🌐 Creating a Virtual Host for the Application

- Documentation: [Add a Virtual Host](https://www.devopness.com/docs/virtual-hosts/add-virtual-host)

Make your application accessible via a domain or server IP address by adding a virtual host.

1. On Devopness, navigate to a project then select an environment
1. Find the **Virtual Hosts** card
1. Click **View** in the Virtual Hosts card to see a list of existing Virtual Hosts
1. On the upper-right corner of the list, click **ADD VIRTUAL HOST**
1. Select **Virtual Host Type**: `Server IP Address`
1. Provide your **Server IP and Port** (e.g., `127.0.0.1:9200`)
   - If no server is available, follow the [Add a Server](https://www.devopness.com/docs/servers/add-server) guide before proceeding.
1. Specify the **Application Listen Address** as `http://localhost:{PORT}`
   - If the `PORT` environment variable is not set, Rails defaults to `3000`
1. Click **CONFIRM** to create the virtual host

## 🚢 Deploying the Application

- Documentation: [Deploy Application](https://www.devopness.com/docs/applications/deploy-application)

Deploy your application to apply the latest changes with minimal downtime.

1. On Devopness, navigate to the application's **Details** page
1. Click **DEPLOY** on the application you want to deploy
1. Follow the prompts, then click **NEXT**
1. Review the deployment details, then click **CONFIRM**
1. A notification popup will confirm that the deployment has been triggered
1. Wait for the `Application Deploy` action to complete

## ✍️ Contributing

Contributions are highly encouraged! 🙏👊

See the [contributing guide](../../../CONTRIBUTING.md) for details on how to participate.

All communication and contributions to Devopness projects are subject to the [Devopness Code of Conduct](../../../CODE_OF_CONDUCT.md).

## 📜 License

All repository contents are licensed under the terms of the [MIT License](../../../LICENSE) unless otherwise specified.

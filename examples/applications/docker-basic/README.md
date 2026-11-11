# Docker Application - Devopness Example

## Overview

Integrate a Docker-based application with Devopness for streamlined management and deployment.

This example uses a minimal Node.js HTTP server packaged in a Docker container. It listens on port `8080` and does not require any external services.

## 🚀 Adding an Application

Using the configuration below, follow the guide [Add an Application](https://www.devopness.com/docs/applications/add-application) to add your application to Devopness.

| Property       | Value                               |
| -------------- | ----------------------------------- |
| Repository     | `devopness/devopness`               |
| Stack          | `Docker`                            |
| Framework      | `No Framework`                     |
| Root Directory | `/examples/applications/docker-basic` |

## ⚙️ Configuring Environment Variables

Using the table below, follow the guide [Add an Environment Variable](https://www.devopness.com/docs/variables/add-variable) to configure the environment variables for your application.

| Variable Key | Variable Value |
| ------------ | -------------- |
| PORT         | `8080`         |
| HOST         | `0.0.0.0`      |

## 🛠️ Building and Running the Container

The Dockerfile builds the application image and starts the HTTP server with `npm start`.

| Property | Value |
| -------- | ----- |
| Build    | `docker build -t docker-basic .` |
| Run      | `docker run --rm -p 8080:8080 docker-basic` |

## 🌐 Creating a Virtual Host

Using the configuration below, follow the guide [Add a Virtual Host](https://www.devopness.com/docs/virtual-hosts/add-virtual-host) to create a virtual host for your application.

| Property       | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Type           | `Server IP Address`                                     |
| Name           | **Server IP and Port** using the format `{IP}:{PORT}`   |
| Application    | `Your Application`                                      |
| Listen Address | `http://127.0.0.1:8080`                                 |

## 🚢 Deploying the Application

Follow the guide [Deploy Application](https://www.devopness.com/docs/applications/deploy-application) to deploy your application.

## ✍️ Contributing

Contributions are highly encouraged! 🙏👊

See the [contributing guide](../../../CONTRIBUTING.md) for details on how to participate.

All communication and contributions to Devopness projects are subject to the [Devopness Code of Conduct](../../../CODE_OF_CONDUCT.md).

# Python FastAPI - Devopness Example

## Overview

Integrate a Python 3.13 FastAPI application with Devopness for streamlined management and deployment.

This example exposes two JSON endpoints and runs as a simple daemon using Uvicorn.

## 🚀 Adding an Application

| Property       | Value                                  |
| -------------- | -------------------------------------- |
| Repository     | `devopness/devopness`                  |
| Stack          | `Python`                               |
| Engine Version | `3.13`                                 |
| Framework      | `FastAPI`                              |
| Root Directory | `/examples/applications/python-fastapi` |

## 📦 Installing Dependencies

Install the required packages with:

```sh
python3.13 -m pip install -r requirements.txt
```

## ▶️ Running Locally

Start the API with:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🛠️ Creating a Daemon

| Property    | Value                                             |
| ----------- | ------------------------------------------------- |
| Name        | `python-fastapi-server`                           |
| Command     | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Application | `Your Application`                                |

## 🌐 Creating a Virtual Host

| Property       | Value                                                 |
| -------------- | ----------------------------------------------------- |
| Type           | `Server IP Address`                                   |
| Name           | **Server IP and Port** using the format `{IP}:{PORT}` |
| Application    | `Your Application`                                    |
| Listen Address | `http://localhost:8000`                               |

## 🔌 Endpoints

| Method | Path | Response |
| ------ | ---- | -------- |
| GET | `/` | `{"message": "Hello from Python and FastAPI!"}` |
| GET | `/health` | `{"status": "ok"}` |

## 🚢 Deploying the Application

Follow the guide [Deploy Application](https://www.devopness.com/docs/applications/deploy-application) to deploy your application.

## ✍️ Contributing

Contributions are highly encouraged! 🙏👊

See the [contributing guide](../../../CONTRIBUTING.md) for details on how to participate.

All communication and contributions to Devopness projects are subject to the [Devopness Code of Conduct](../../../CODE_OF_CONDUCT.md).

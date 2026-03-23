# Devopness Python SDK

[![PyPI version](https://img.shields.io/pypi/v/devopness.svg)](https://pypi.org/project/devopness/)
[![Python versions](https://img.shields.io/pypi/pyversions/devopness.svg)](https://pypi.org/project/devopness/)

Official Python client for the [Devopness API](https://www.devopness.com/). Use it to automate infrastructure, applications, environments, credentials, pipelines, and other Devopness resources from scripts, CLIs, background jobs, and web services.

## Why use this SDK?

- Typed request and response models powered by Pydantic.
- First-class sync and async clients with a consistent API.
- Structured exceptions for API and network failures.
- Thin, resource-oriented service surface that maps closely to the Devopness API.

## Installation

```bash
pip install devopness
```

Alternative package managers:

```bash
uv add devopness
poetry add devopness
```

## Quickstart

The SDK exposes two entry points:

- `DevopnessClient` for synchronous code.
- `DevopnessClientAsync` for asynchronous code.

### Synchronous quickstart

```python
import os

from devopness import DevopnessClient, DevopnessClientConfig

client = DevopnessClient(
    DevopnessClientConfig(
        api_token=os.environ["DEVOPNESS_API_TOKEN"],
    )
)

me = client.users.get_user_me()
print(me.status)
print(me.data.id)
```

### Asynchronous quickstart

```python
import asyncio
import os

from devopness import DevopnessClientAsync, DevopnessClientConfig


async def main() -> None:
    client = DevopnessClientAsync(
        DevopnessClientConfig(
            api_token=os.environ["DEVOPNESS_API_TOKEN"],
        )
    )

    me = await client.users.get_user_me()
    print(me.status)
    print(me.data.id)


if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication

Use a Devopness token and pass it through `DevopnessClientConfig(api_token=...)` or assign it later through `client.api_token`.

### Personal access token

```python
from devopness import DevopnessClient

client = DevopnessClient()
client.api_token = "your-personal-access-token"

current_user = client.users.get_user_me()
print(current_user.data.id)
```

Create a token in Devopness by following the official guide for personal access tokens:
https://www.devopness.com/docs/api-tokens/personal-access-tokens/add-personal-access-token

### Project API token

```python
from devopness import DevopnessClient, DevopnessClientConfig

client = DevopnessClient(
    DevopnessClientConfig(api_token="your-project-api-token")
)

project = client.projects.get_project(project_id=123)
print(project.data.name)
```

Create a token in Devopness by following the official guide for project API tokens:
https://www.devopness.com/docs/api-tokens/project-api-tokens/add-project-api-token

> Email/password login is deprecated and should not be used for new integrations.

## Configuration

`DevopnessClientConfig` controls how requests and responses are handled.

```python
from devopness import DevopnessClientConfig

config = DevopnessClientConfig(
    base_url="https://api.devopness.com",
    timeout=30,
    debug=False,
    validate_responses=True,
)
```

### Configuration reference

| Option | Default | Description |
| --- | --- | --- |
| `api_token` | `None` | Token used for authenticated requests. |
| `auto_refresh_token` | `False` | Deprecated legacy option. Automatically disabled when `api_token` is set. |
| `base_url` | `https://api.devopness.com` | Base URL for the Devopness API. |
| `debug` | `False` | Enables request/response debug logging. |
| `default_encoding` | `utf-8` | Default response encoding for `httpx`. |
| `headers` | SDK defaults | Base headers sent on every request. |
| `timeout` | `30` | Request timeout in seconds. |
| `validate_responses` | `True` | Parse API responses into Pydantic models. Set to `False` to receive raw decoded payloads instead. |

## Core concepts

### Clients

A client owns the SDK configuration and exposes services as attributes such as `users`, `projects`, `applications`, and `servers`.

### Services

Each service groups operations for one resource family. For example, `client.users.get_user_me()` and `client.projects.get_project(project_id=123)`.

### Responses

Most methods return `DevopnessResponse[T]` with:

- `status`: HTTP status code.
- `data`: Parsed model, list of models, primitive value, or raw decoded payload depending on the endpoint and configuration.
- `page_count`: Pagination metadata derived from the `Link` header.
- `action_id`: Action identifier from the `x-devopness-action-id` response header when present.

## Sync and async usage

The sync and async clients expose the same service names and method signatures.

```python
# Sync
project = client.projects.get_project(project_id=123)

# Async
project = await async_client.projects.get_project(project_id=123)
```

## Error handling

All SDK exceptions inherit from `DevopnessSdkError`.

- `DevopnessApiError`: The API returned a non-2xx response.
- `DevopnessNetworkError`: A transport-level failure occurred.

```python
from devopness import DevopnessClient
from devopness.core import DevopnessApiError, DevopnessNetworkError, DevopnessSdkError

client = DevopnessClient()
client.api_token = "your-token"

try:
    response = client.projects.get_project(project_id=123)
    print(response.data.name)
except DevopnessApiError as exc:
    print(exc.status_code)
    print(exc.message)
    print(exc.errors)
except DevopnessNetworkError as exc:
    print(f"Network error: {exc}")
except DevopnessSdkError as exc:
    print(f"Unexpected SDK error: {exc}")
```

## Disabling response validation

By default, the SDK validates API responses using Pydantic models. If you want maximum tolerance for partially malformed payloads, disable validation.

```python
from devopness import DevopnessClient, DevopnessClientConfig

client = DevopnessClient(
    DevopnessClientConfig(
        api_token="your-token",
        validate_responses=False,
    )
)

response = client.users.get_user_me()
print(type(response.data))
print(response.data)
```

With validation disabled, the SDK returns decoded JSON objects, lists, strings, integers, or floats when possible, instead of Pydantic models.

## More examples

```python
# List projects
projects = client.projects.list_projects()
for item in projects.data:
    print(item.id, item.name)

# Create or update resources using SDK models or plain dictionaries
created = client.projects.create_project({"name": "My project"})
updated = client.projects.update_project(project_id=created.data.id, data={"name": "Renamed"})
```

## Development

From the repository root:

```bash
cd packages/sdks/python
python -m unittest discover -s tests/unit
```

## License

MIT.

# Devopness SDK - Go

The official Devopness SDK for Go.

This first slice keeps the SDK intentionally small. It provides a core HTTP client, request transport, configuration, and Devopness PAT authentication using the Go standard library.

## Usage

```go
package main

import (
	"fmt"
	"os"

	devopness "github.com/Diegiwg/devopness/packages/sdks/go"
)

func main() {
	client, err := devopness.NewClient(
		devopness.WithAPIToken(os.Getenv("DEVOPNESS_API_TOKEN")),
	)
	if err != nil {
		panic(err)
	}

	fmt.Println(client.BaseURL())
}
```

## Notes

- The SDK uses only Go standard library packages for the first release slice.
- Service groups will be added later to match the JS and Python SDK surface.

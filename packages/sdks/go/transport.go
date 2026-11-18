package devopness

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

func newHTTPClient(timeout time.Duration) *http.Client {
	return &http.Client{Timeout: timeout}
}

func (client *Client) newRequest(ctx context.Context, method, path string, body any) (*http.Request, error) {
	config := client.Config()
	requestURL, err := resolveURL(config.BaseURL, path)
	if err != nil {
		return nil, err
	}

	var requestBody io.Reader
	if body != nil {
		if reader, ok := body.(io.Reader); ok {
			requestBody = reader
		} else {
			payload, marshalErr := json.Marshal(body)
			if marshalErr != nil {
				return nil, marshalErr
			}

			requestBody = bytes.NewReader(payload)
		}
	}

	request, err := http.NewRequestWithContext(ctx, method, requestURL, requestBody)
	if err != nil {
		return nil, err
	}

	for key, values := range config.Headers {
		for _, value := range values {
			request.Header.Add(key, value)
		}
	}

	if token := strings.TrimSpace(config.APIToken); token != "" {
		request.Header.Set("Authorization", bearerToken(token))
	}

	return request, nil
}

func resolveURL(baseURL, path string) (string, error) {
	base, err := url.Parse(strings.TrimRight(baseURL, "/"))
	if err != nil {
		return "", err
	}

	relative, err := url.Parse(strings.TrimLeft(path, "/"))
	if err != nil {
		return "", err
	}

	return base.ResolveReference(relative).String(), nil
}

func decodeResponse(response *http.Response, destination any) error {
	if destination == nil {
		return ErrNilResponse
	}

	if response.StatusCode == http.StatusNoContent {
		return nil
	}

	decoder := json.NewDecoder(response.Body)
	if err := decoder.Decode(destination); err != nil && err != io.EOF {
		return err
	}

	return nil
}

func readResponseBody(response *http.Response) []byte {
	if response == nil || response.Body == nil {
		return nil
	}

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return nil
	}

	return body
}

func closeQuietly(body io.Closer) {
	if body != nil {
		_ = body.Close()
	}
}

func statusError(method, requestURL string, response *http.Response) error {
	return &APIError{
		StatusCode: response.StatusCode,
		Method:     method,
		URL:        requestURL,
		Body:       readResponseBody(response),
	}
}


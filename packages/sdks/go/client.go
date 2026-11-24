package devopness

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	"time"
)

type Option func(*Client) error

type Client struct {
	config    *Config
	httpClient *http.Client
}

func NewClient(options ...Option) (*Client, error) {
	client := &Client{config: DefaultConfig()}

	for _, option := range options {
		if err := option(client); err != nil {
			return nil, err
		}
	}

	if err := client.config.Validate(); err != nil {
		return nil, err
	}

	if client.httpClient == nil {
		client.httpClient = newHTTPClient(client.config.Timeout)
	}

	return client, nil
}

func WithBaseURL(baseURL string) Option {
	return func(client *Client) error {
		client.config.BaseURL = baseURL
		return nil
	}
}

func WithTimeout(timeout time.Duration) Option {
	return func(client *Client) error {
		client.config.Timeout = timeout
		return nil
	}
}

func WithHeader(key, value string) Option {
	return func(client *Client) error {
		if client.config.Headers == nil {
			client.config.Headers = defaultHeaders()
		}

		client.config.Headers.Set(key, value)
		return nil
	}
}

func WithAPIToken(token string) Option {
	return func(client *Client) error {
		return client.SetAPIToken(token)
	}
}

func WithHTTPClient(httpClient *http.Client) Option {
	return func(client *Client) error {
		client.httpClient = httpClient
		return nil
	}
}

func (client *Client) Config() *Config {
	if client == nil || client.config == nil {
		return DefaultConfig()
	}

	return client.config.Clone()
}

func (client *Client) HTTPClient() *http.Client {
	if client == nil || client.httpClient == nil {
		return newHTTPClient(30 * time.Second)
	}

	return client.httpClient
}

func (client *Client) SetAPIToken(token string) error {
	if err := validateAPIToken(token); err != nil {
		return err
	}

	if client.config == nil {
		client.config = DefaultConfig()
	}

	client.config.APIToken = strings.TrimSpace(token)
	return nil
}

func (client *Client) SetBaseURL(baseURL string) error {
	if client.config == nil {
		client.config = DefaultConfig()
	}

	client.config.BaseURL = baseURL
	return client.config.Validate()
}

func (client *Client) SetHeader(key, value string) {
	if client.config == nil {
		client.config = DefaultConfig()
	}

	if client.config.Headers == nil {
		client.config.Headers = defaultHeaders()
	}

	client.config.Headers.Set(key, value)
}

func (client *Client) SetHTTPClient(httpClient *http.Client) {
	if client.config == nil {
		client.config = DefaultConfig()
	}

	client.httpClient = httpClient
}

func (client *Client) Do(ctx context.Context, method, path string, body any, destination any) (*http.Response, error) {
	request, err := client.newRequest(ctx, method, path, body)
	if err != nil {
		return nil, err
	}

	httpClient := client.httpClient
	if httpClient == nil {
		httpClient = newHTTPClient(client.Config().Timeout)
	}

	response, err := httpClient.Do(request)
	if err != nil {
		return nil, err
	}
	defer closeQuietly(response.Body)

	if response.StatusCode < http.StatusOK || response.StatusCode >= http.StatusMultipleChoices {
		return nil, statusError(method, request.URL.String(), response)
	}

	if destination != nil {
		if err := decodeResponse(response, destination); err != nil {
			return nil, err
		}
	}

	return response, nil
}

func (client *Client) Get(ctx context.Context, path string, destination any) (*http.Response, error) {
	return client.Do(ctx, http.MethodGet, path, nil, destination)
}

func (client *Client) Post(ctx context.Context, path string, body any, destination any) (*http.Response, error) {
	return client.Do(ctx, http.MethodPost, path, body, destination)
}

func (client *Client) Put(ctx context.Context, path string, body any, destination any) (*http.Response, error) {
	return client.Do(ctx, http.MethodPut, path, body, destination)
}

func (client *Client) Delete(ctx context.Context, path string, destination any) (*http.Response, error) {
	return client.Do(ctx, http.MethodDelete, path, nil, destination)
}

func (client *Client) BaseURL() string {
	if client == nil || client.config == nil {
		return DefaultBaseURL
	}

	return strings.TrimRight(client.config.BaseURL, "/")
}

func (client *Client) APIToken() string {
	if client == nil || client.config == nil {
		return ""
	}

	return client.config.APIToken
}

func (client *Client) String() string {
	return fmt.Sprintf("DevopnessClient{%s}", client.BaseURL())
}

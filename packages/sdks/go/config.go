package devopness

import (
	"net/http"
	"net/url"
	"strings"
	"time"
)

const DefaultBaseURL = "https://api.devopness.com"

type Config struct {
	BaseURL   string
	Timeout   time.Duration
	Headers   http.Header
	UserAgent string
	APIToken  string
}

func DefaultConfig() *Config {
	return &Config{
		BaseURL:   DefaultBaseURL,
		Timeout:   30 * time.Second,
		Headers:   defaultHeaders(),
		UserAgent: defaultUserAgent(),
	}
}

func (config *Config) Clone() *Config {
	if config == nil {
		return DefaultConfig()
	}

	clone := *config
	clone.Headers = cloneHeader(config.Headers)
	return &clone
}

func (config *Config) Validate() error {
	if config == nil {
		return ErrInvalidBaseURL
	}

	trimmedBaseURL := strings.TrimSpace(config.BaseURL)
	if trimmedBaseURL == "" {
		return ErrInvalidBaseURL
	}

	parsedURL, err := url.Parse(trimmedBaseURL)
	if err != nil {
		return ErrInvalidBaseURL
	}

	if parsedURL.Scheme != "http" && parsedURL.Scheme != "https" {
		return ErrInvalidBaseURL
	}

	if config.Timeout <= 0 {
		config.Timeout = 30 * time.Second
	}

	if config.Headers == nil {
		config.Headers = defaultHeaders()
	}

	if config.UserAgent == "" {
		config.UserAgent = defaultUserAgent()
	}

	if config.Headers.Get("Accept") == "" {
		config.Headers.Set("Accept", "application/json")
	}

	if config.Headers.Get("Content-Type") == "" {
		config.Headers.Set("Content-Type", "application/json")
	}

	if config.Headers.Get("User-Agent") == "" {
		config.Headers.Set("User-Agent", config.UserAgent)
	}

	return nil
}

func defaultHeaders() http.Header {
	headers := http.Header{}
	headers.Set("Accept", "application/json")
	headers.Set("Content-Type", "application/json")
	headers.Set("User-Agent", defaultUserAgent())
	return headers
}

func cloneHeader(headers http.Header) http.Header {
	if headers == nil {
		return nil
	}

	clone := make(http.Header, len(headers))
	for key, values := range headers {
		clone[key] = append([]string(nil), values...)
	}

	return clone
}

func defaultUserAgent() string {
	return "devopness-sdk-go/0.1.0 +https://github.com/Diegiwg/devopness (go/stdlib)"
}

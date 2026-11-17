package devopness

import (
	"testing"
	time"
)

func TestDefaultConfig(t *testing.T) {
	t.Parallel()

	config := DefaultConfig()

	if config.BaseURL != DefaultBaseURL {
		t.Fatalf("expected base url %q, got %q", DefaultBaseURL, config.BaseURL)
	}

	if config.Timeout != 30*time.Second {
		t.Fatalf("expected timeout %s, got %s", 30*time.Second, config.Timeout)
	}

	if err := config.Validate(); err != nil {
		t.Fatalf("expected config to be valid, got error %v", err)
	}
}

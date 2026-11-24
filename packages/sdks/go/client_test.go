package devopness

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
)

func TestClientSendsBearerToken(t *testing.T) {
	t.Parallel()

	var (
		requestMu          sync.Mutex
		authorizationHeader string
		acceptHeader       string
		contentTypeHeader  string
	)

	server := httptest.NewServer(http.HandlerFunc(func(responseWriter http.ResponseWriter, request *http.Request) {
		requestMu.Lock()
		authorizationHeader = request.Header.Get("Authorization")
		acceptHeader = request.Header.Get("Accept")
		contentTypeHeader = request.Header.Get("Content-Type")
		requestMu.Unlock()

		responseWriter.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(responseWriter).Encode(map[string]string{"status": "ok"})
	}))
	defer server.Close()

	client, err := NewClient(
		WithBaseURL(server.URL),
		WithAPIToken("test-token"),
	)
	if err != nil {
		t.Fatalf("expected client to initialize, got error %v", err)
	}

	var response struct {
		Status string `json:"status"`
	}

	_, err = client.Get(context.Background(), "/", &response)
	if err != nil {
		t.Fatalf("expected request to succeed, got error %v", err)
	}

	if response.Status != "ok" {
		t.Fatalf("expected response status %q, got %q", "ok", response.Status)
	}

	requestMu.Lock()
	defer requestMu.Unlock()

	if authorizationHeader != "Bearer test-token" {
		t.Fatalf("expected authorization header %q, got %q", "Bearer test-token", authorizationHeader)
	}

	if acceptHeader != "application/json" {
		t.Fatalf("expected accept header %q, got %q", "application/json", acceptHeader)
	}

	if contentTypeHeader != "application/json" {
		t.Fatalf("expected content-type header %q, got %q", "application/json", contentTypeHeader)
	}
}

func TestSetAPITokenAfterInitialization(t *testing.T) {
	t.Parallel()

	client, err := NewClient()
	if err != nil {
		t.Fatalf("expected client to initialize, got error %v", err)
	}

	if err := client.SetAPIToken("another-token"); err != nil {
		t.Fatalf("expected token update to succeed, got error %v", err)
	}

	if got := client.APIToken(); got != "another-token" {
		t.Fatalf("expected token %q, got %q", "another-token", got)
	}
}

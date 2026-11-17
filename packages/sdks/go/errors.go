package devopness

import (
	"errors"
	"net/http"
)

var (
	ErrInvalidBaseURL = errors.New("devopness: invalid base url")
	ErrEmptyAPIToken  = errors.New("devopness: api token is empty")
	ErrNilResponse    = errors.New("devopness: response destination is nil")
)

type APIError struct {
	StatusCode int
	Method     string
	URL        string
	Body       []byte
}

func (err *APIError) Error() string {
	if err == nil {
		return "devopness: api error"
	}

	if len(err.Body) == 0 {
		return err.Method + " " + err.URL + ": unexpected status " + http.StatusText(err.StatusCode)
	}

	return err.Method + " " + err.URL + ": unexpected status " + http.StatusText(err.StatusCode) + ": " + string(err.Body)
}

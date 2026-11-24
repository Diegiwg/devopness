package devopness

import "strings"

func validateAPIToken(token string) error {
	if strings.TrimSpace(token) == "" {
		return ErrEmptyAPIToken
	}

	return nil
}

func bearerToken(token string) string {
	return "Bearer " + token
}

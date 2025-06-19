package handlers

import (
	"encoding/json"
	"net/http"
)

// HealthHandler responds with a simple health status.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "OK"})
}

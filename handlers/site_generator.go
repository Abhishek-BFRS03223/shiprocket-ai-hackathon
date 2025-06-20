package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/gorilla/mux"
)

// GenerateSiteRequest represents the request to generate a website
type GenerateSiteRequest struct {
	ProductName string `json:"product_name"`
}

// GenerateSiteResponse represents the response from site generation
type GenerateSiteResponse struct {
	Success     bool   `json:"success"`
	ProductName string `json:"product_name"`
	SitePath    string `json:"site_path"`
	Message     string `json:"message"`
	GeneratedAt string `json:"generated_at"`
}

// ListSitesResponse represents the response for listing generated sites
type ListSitesResponse struct {
	Success bool     `json:"success"`
	Sites   []string `json:"sites"`
	Count   int      `json:"count"`
}

// Helper function to parse JSON from request
func parseJSON(r *http.Request, target interface{}) error {
	return json.NewDecoder(r.Body).Decode(target)
}

// Helper function to respond with JSON
func respondJSON(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

// GenerateSiteHandler handles website generation requests
func GenerateSiteHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse request body manually since we're dealing with form data potentially
	productName := r.FormValue("product_name")
	if productName == "" {
		// Try JSON parsing as fallback
		var req GenerateSiteRequest
		if err := parseJSON(r, &req); err != nil {
			http.Error(w, "Invalid request format", http.StatusBadRequest)
			return
		}
		productName = req.ProductName
	}

	if strings.TrimSpace(productName) == "" {
		http.Error(w, "Product name is required", http.StatusBadRequest)
		return
	}

	// Execute GPT Python script with AI-powered content generation
	pythonPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/langchain_env/bin/python3"
	scriptPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/gpt_site_generator.py"
	cmd := exec.Command(pythonPath, scriptPath, productName)

	output, err := cmd.CombinedOutput() // Use CombinedOutput to get both stdout and stderr
	if err != nil {
		fmt.Printf("Error executing Python script: %v\nOutput: %s\n", err, string(output))
		respondJSON(w, GenerateSiteResponse{
			Success:     false,
			ProductName: productName,
			Message:     fmt.Sprintf("Python execution failed: %v", err),
			GeneratedAt: time.Now().Format(time.RFC3339),
		})
		return
	}

	outputStr := strings.TrimSpace(string(output))
	fmt.Printf("Python script output: %s\n", outputStr) // Debug output

	// Look for SUCCESS or ERROR in the output (could be multiline)
	lines := strings.Split(outputStr, "\n")
	var resultLine string
	for _, line := range lines {
		if strings.HasPrefix(line, "SUCCESS:") || strings.HasPrefix(line, "ERROR:") {
			resultLine = line
			break
		}
	}

	if resultLine == "" {
		respondJSON(w, GenerateSiteResponse{
			Success:     false,
			ProductName: productName,
			Message:     "No valid result found in generator output",
			GeneratedAt: time.Now().Format(time.RFC3339),
		})
		return
	}

	if strings.HasPrefix(resultLine, "SUCCESS:") {
		sitePath := strings.TrimPrefix(resultLine, "SUCCESS:")

		respondJSON(w, GenerateSiteResponse{
			Success:     true,
			ProductName: productName,
			SitePath:    sitePath,
			Message:     "AI-powered website generated successfully with GPT content and real images",
			GeneratedAt: time.Now().Format(time.RFC3339),
		})
	} else if strings.HasPrefix(resultLine, "ERROR:") {
		errorMsg := strings.TrimPrefix(resultLine, "ERROR:")

		respondJSON(w, GenerateSiteResponse{
			Success:     false,
			ProductName: productName,
			Message:     fmt.Sprintf("Generation failed: %s", errorMsg),
			GeneratedAt: time.Now().Format(time.RFC3339),
		})
	}
}

// ListSitesHandler lists all generated websites
func ListSitesHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != "GET" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	sitesDir := "generated_sites"

	entries, err := os.ReadDir(sitesDir)
	if err != nil {
		respondJSON(w, ListSitesResponse{
			Success: false,
			Sites:   []string{},
			Count:   0,
		})
		return
	}

	var sites []string
	for _, entry := range entries {
		if entry.IsDir() {
			// Check if index.html exists
			indexPath := filepath.Join(sitesDir, entry.Name(), "index.html")
			if _, err := os.Stat(indexPath); err == nil {
				sites = append(sites, entry.Name())
			}
		}
	}

	respondJSON(w, ListSitesResponse{
		Success: true,
		Sites:   sites,
		Count:   len(sites),
	})
}

// ViewSiteHandler serves a specific generated website
func ViewSiteHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	vars := mux.Vars(r)
	siteName := vars["siteName"]

	if siteName == "" {
		http.Error(w, "Site name is required", http.StatusBadRequest)
		return
	}

	// Sanitize site name to prevent directory traversal
	re := regexp.MustCompile(`[^a-zA-Z0-9_-]`)
	safeSiteName := re.ReplaceAllString(siteName, "")

	indexPath := filepath.Join("generated_sites", safeSiteName, "index.html")

	if _, err := os.Stat(indexPath); os.IsNotExist(err) {
		http.Error(w, "Site not found", http.StatusNotFound)
		return
	}

	http.ServeFile(w, r, indexPath)
}

// DemoGenerateHandler generates 5 demo websites with images
func DemoGenerateHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Execute Enhanced Python script to generate demo sites with real images
	pythonPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/langchain_env/bin/python3"
	scriptPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/enhanced_site_generator.py"

	// Demo products representing different categories
	products := []string{"Smart Coffee Maker", "EcoFit Yoga Mat", "ProCode Text Editor", "Gourmet Pizza Restaurant", "Luxury Fashion Boutique"}

	results := []string{}
	for _, product := range products {
		cmd := exec.Command(pythonPath, scriptPath, product)
		output, err := cmd.Output()
		if err != nil {
			results = append(results, fmt.Sprintf("ERROR:%s:Failed to generate", product))
		} else {
			results = append(results, strings.TrimSpace(string(output)))
		}
	}

	// Combine all results into output string
	output := strings.Join(results, "\n")

	respondJSON(w, map[string]interface{}{
		"success":      true,
		"message":      "Enhanced demo sites generated successfully with real images",
		"output":       output,
		"generated_at": time.Now().Format(time.RFC3339),
	})
}

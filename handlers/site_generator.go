package handlers

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
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
	SiteContent string `json:"site_content"`
	SiteID      string `json:"site_id"`
	Message     string `json:"message"`
	GeneratedAt string `json:"generated_at"`
	Theme       string `json:"theme"`
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

// Enhanced GenerateSiteHandler handles website generation requests with new features
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

	// Parse request body
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

	// Clean product name for safety
	cleanedProductName := regexp.MustCompile(`[^a-zA-Z0-9\s\-_]`).ReplaceAllString(productName, "")
	if len(cleanedProductName) == 0 {
		http.Error(w, "Invalid product name", http.StatusBadRequest)
		return
	}

	// Execute Enhanced GPT Python script
	pythonPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/langchain_env/bin/python3"
	scriptPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/gpt_site_generator.py"
	cmd := exec.Command(pythonPath, scriptPath, cleanedProductName)

	// Set working directory and environment
	cmd.Dir = "/home/abhisheksoni/shiprocket-ai-hackathon-1"
	cmd.Env = append(os.Environ(),
		"PYTHONPATH=/home/abhisheksoni/shiprocket-ai-hackathon-1/langchain_env/lib/python3.11/site-packages",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error executing Python script: %v\nOutput: %s\n", err, string(output))
		respondJSON(w, GenerateSiteResponse{
			Success:     false,
			ProductName: productName,
			Message:     fmt.Sprintf("Site generation failed: %v", err),
			GeneratedAt: time.Now().Format(time.RFC3339),
		})
		return
	}

	outputStr := strings.TrimSpace(string(output))
	fmt.Printf("Enhanced generator output: %s\n", outputStr)

	// Look for SUCCESS or ERROR in the output
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
		tempFilePath := strings.TrimPrefix(resultLine, "SUCCESS:")

		// Read the temporary file content
		content, err := ioutil.ReadFile(tempFilePath)
		if err != nil {
			respondJSON(w, GenerateSiteResponse{
				Success:     false,
				ProductName: productName,
				Message:     fmt.Sprintf("Failed to read generated site: %v", err),
				GeneratedAt: time.Now().Format(time.RFC3339),
			})
			return
		}

		// Extract site ID from file path
		siteID := filepath.Base(tempFilePath)
		siteID = strings.TrimSuffix(siteID, ".html")

		// Clean up temporary file after reading
		go func() {
			time.Sleep(30 * time.Second) // Keep file for 30 seconds for any immediate requests
			os.Remove(tempFilePath)
		}()

		respondJSON(w, GenerateSiteResponse{
			Success:     true,
			ProductName: productName,
			SiteContent: string(content),
			SiteID:      siteID,
			Message:     "Enhanced AI-powered website generated successfully with dynamic themes and product images",
			GeneratedAt: time.Now().Format(time.RFC3339),
			Theme:       "dynamic", // Indicates theme was randomly selected
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

// ViewSiteHandler serves site content directly from memory/temporary storage
func ViewSiteHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != "GET" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	vars := mux.Vars(r)
	siteID := vars["siteId"]

	if siteID == "" {
		http.Error(w, "Site ID is required", http.StatusBadRequest)
		return
	}

	// For temporary sites, we'll serve a message indicating the site was temporary
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	html := `
<!DOCTYPE html>
<html>
<head>
    <title>Temporary Site Expired</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
        .message { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; }
        h1 { color: #e74c3c; margin-bottom: 20px; }
        p { color: #666; line-height: 1.6; margin-bottom: 20px; }
        button { background: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="message">
        <h1>⏰ Temporary Site Expired</h1>
        <p>This was a temporary demonstration site that has been automatically cleared for your privacy and to keep the system clean.</p>
        <p>Generate a new site to see the latest AI-powered designs with dynamic themes and enhanced features!</p>
        <button onclick="window.close()">Close</button>
    </div>
</body>
</html>`

	w.Write([]byte(html))
}

// DemoGenerateHandler generates multiple demo sites
func DemoGenerateHandler(w http.ResponseWriter, r *http.Request) {
	// Set CORS headers
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	// Demo products with diverse categories
	demoProducts := []string{
		"Smart AI Fitness Watch",
		"Artisanal Coffee Blend",
		"Luxury Designer Handbag",
		"Electric Sports Car",
		"Organic Yoga Mat",
		"Gaming Laptop Pro",
		"Wireless Noise-Canceling Headphones",
	}

	var results []GenerateSiteResponse
	successCount := 0

	for _, product := range demoProducts {
		// Create a new request for each demo product
		pythonPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/langchain_env/bin/python3"
		scriptPath := "/home/abhisheksoni/shiprocket-ai-hackathon-1/gpt_site_generator.py"
		cmd := exec.Command(pythonPath, scriptPath, product)
		cmd.Dir = "/home/abhisheksoni/shiprocket-ai-hackathon-1"

		output, err := cmd.CombinedOutput()

		if err == nil {
			outputStr := strings.TrimSpace(string(output))
			if strings.Contains(outputStr, "SUCCESS:") {
				successCount++
				results = append(results, GenerateSiteResponse{
					Success:     true,
					ProductName: product,
					Message:     "Demo site generated successfully",
					GeneratedAt: time.Now().Format(time.RFC3339),
				})
			}
		}
	}

	response := map[string]interface{}{
		"success":         true,
		"total_generated": successCount,
		"demo_results":    results,
		"message":         fmt.Sprintf("Generated %d demo sites with enhanced themes and features", successCount),
	}

	respondJSON(w, response)
}

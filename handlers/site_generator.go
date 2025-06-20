package handlers

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"time"

	"github.com/gorilla/mux"
)

// SiteGeneratorRequest represents the request to generate a site
type SiteGeneratorRequest struct {
	ProductName string `json:"product_name"`
	SaveToDisk  bool   `json:"save_to_disk,omitempty"`
}

// SiteGeneratorResponse represents the response from site generation
type SiteGeneratorResponse struct {
	Success          bool   `json:"success"`
	ProductName      string `json:"product_name"`
	Timestamp        string `json:"timestamp"`
	GenerationMethod string `json:"generation_method"`
	SavedTo          string `json:"saved_to,omitempty"`
	HTML             string `json:"html,omitempty"`
	Error            string `json:"error,omitempty"`
}

// GenerateWebsiteHandler handles website generation requests
func GenerateWebsiteHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
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

	var req SiteGeneratorRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		response := SiteGeneratorResponse{
			Success: false,
			Error:   "Invalid JSON request",
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	if req.ProductName == "" {
		response := SiteGeneratorResponse{
			Success: false,
			Error:   "Product name is required",
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	// Generate website using Python script
	result, err := generateWebsiteWithPython(req.ProductName, req.SaveToDisk)
	if err != nil {
		response := SiteGeneratorResponse{
			Success:     false,
			ProductName: req.ProductName,
			Error:       err.Error(),
			Timestamp:   time.Now().Format(time.RFC3339),
		}
		json.NewEncoder(w).Encode(response)
		return
	}

	json.NewEncoder(w).Encode(result)
}

// GetGeneratedSiteHandler serves generated HTML sites
func GetGeneratedSiteHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	siteName := vars["siteName"]

	if siteName == "" {
		http.Error(w, "Site name required", http.StatusBadRequest)
		return
	}

	// Construct path to generated site
	sitePath := filepath.Join("generated_sites", siteName, "index.html")

	// Check if file exists
	if _, err := os.Stat(sitePath); os.IsNotExist(err) {
		http.Error(w, "Site not found", http.StatusNotFound)
		return
	}

	// Read and serve the HTML file
	htmlContent, err := ioutil.ReadFile(sitePath)
	if err != nil {
		http.Error(w, "Error reading site file", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/html")
	w.Write(htmlContent)
}

// ListGeneratedSitesHandler lists all generated sites
func ListGeneratedSitesHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	sitesDir := "generated_sites"
	sites := []map[string]interface{}{}

	// Check if directory exists
	if _, err := os.Stat(sitesDir); os.IsNotExist(err) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"sites": sites,
			"total": 0,
		})
		return
	}

	// Read directory contents
	files, err := ioutil.ReadDir(sitesDir)
	if err != nil {
		http.Error(w, "Error reading sites directory", http.StatusInternalServerError)
		return
	}

	for _, file := range files {
		if file.IsDir() {
			siteInfo := map[string]interface{}{
				"name":     file.Name(),
				"created":  file.ModTime().Format(time.RFC3339),
				"url":      fmt.Sprintf("/api/sites/%s", file.Name()),
				"view_url": fmt.Sprintf("/generated/%s", file.Name()),
			}

			// Try to read metadata if it exists
			metadataPath := filepath.Join(sitesDir, file.Name(), "metadata.json")
			if metadataBytes, err := ioutil.ReadFile(metadataPath); err == nil {
				var metadata map[string]interface{}
				if json.Unmarshal(metadataBytes, &metadata) == nil {
					siteInfo["product_name"] = metadata["product_name"]
					siteInfo["generation_method"] = metadata["generation_method"]
				}
			}

			sites = append(sites, siteInfo)
		}
	}

	response := map[string]interface{}{
		"sites": sites,
		"total": len(sites),
	}

	json.NewEncoder(w).Encode(response)
}

// generateWebsiteWithPython calls the Python site generator
func generateWebsiteWithPython(productName string, saveToDisk bool) (SiteGeneratorResponse, error) {
	// Prepare Python script command
	pythonScript := `
import sys
import os
sys.path.insert(0, '/home/abhisheksoni/shiprocket-ai-hackathon-1/ai_agent')

try:
    from simple_site_generator import SimpleSiteGenerator
    import json
    
    product_name = sys.argv[1]
    save_to_disk = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'
    
    generator = SimpleSiteGenerator()
    result = generator.generate_website(product_name)
    
    if result["success"] and save_to_disk:
        site_dir = generator.save_website(result)
        result["saved_to"] = site_dir
    
    print(json.dumps(result))
    
except Exception as e:
    error_result = {
        "success": False,
        "error": str(e),
        "product_name": product_name if 'product_name' in locals() else "unknown"
    }
    print(json.dumps(error_result))
`

	// Write temporary Python script
	tmpFile, err := ioutil.TempFile("", "site_generator_*.py")
	if err != nil {
		return SiteGeneratorResponse{}, fmt.Errorf("failed to create temp file: %v", err)
	}
	defer os.Remove(tmpFile.Name())

	if _, err := tmpFile.WriteString(pythonScript); err != nil {
		return SiteGeneratorResponse{}, fmt.Errorf("failed to write temp script: %v", err)
	}
	tmpFile.Close()

	// Execute Python script
	saveFlag := "false"
	if saveToDisk {
		saveFlag = "true"
	}

	cmd := exec.Command("python3", tmpFile.Name(), productName, saveFlag)
	cmd.Dir = "/home/abhisheksoni/shiprocket-ai-hackathon-1"

	output, err := cmd.Output()
	if err != nil {
		return SiteGeneratorResponse{}, fmt.Errorf("python execution failed: %v", err)
	}

	// Parse Python output
	var result SiteGeneratorResponse
	if err := json.Unmarshal(output, &result); err != nil {
		return SiteGeneratorResponse{}, fmt.Errorf("failed to parse python output: %v", err)
	}

	return result, nil
}

// DemoSiteGeneratorHandler generates demo sites
func DemoSiteGeneratorHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	demoProducts := []string{
		"Smart Coffee Maker",
		"EcoFit Yoga Mat",
		"ProCode Text Editor",
		"Gourmet Pizza Restaurant",
		"Luxury Fashion Boutique",
	}

	results := []SiteGeneratorResponse{}

	for _, product := range demoProducts {
		result, err := generateWebsiteWithPython(product, true)
		if err != nil {
			result = SiteGeneratorResponse{
				Success:     false,
				ProductName: product,
				Error:       err.Error(),
				Timestamp:   time.Now().Format(time.RFC3339),
			}
		}
		results = append(results, result)
	}

	response := map[string]interface{}{
		"demo_results":    results,
		"total_generated": len(results),
		"timestamp":       time.Now().Format(time.RFC3339),
	}

	json.NewEncoder(w).Encode(response)
}

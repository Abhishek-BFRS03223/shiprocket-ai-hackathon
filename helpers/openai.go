package helpers

import (
	"log"
	"os"

	openai "github.com/sashabaranov/go-openai"
)

// OpenAIClient is a global client instance.
var OpenAIClient *openai.Client

// InitOpenAI initialises the OpenAI client using OPENAI_API_KEY.
func InitOpenAI() {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		log.Println("OPENAI_API_KEY not set, skipping OpenAI initialization")
		return
	}

	OpenAIClient = openai.NewClient(apiKey)
	log.Println("OpenAI client initialized")
}

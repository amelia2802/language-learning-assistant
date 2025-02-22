import requests
from typing import Optional, Dict, Any
import sys

# Default model
MODEL_ID = "tinyllama"

# Only import streamlit if we're running as a web app
if 'streamlit' in sys.modules:
    import streamlit as st

class OllamaChat:
    def __init__(self, model_id: str = MODEL_ID, base_url: str = "http://localhost:11434"):
        """Initialize Ollama chat client"""
        self.base_url = base_url
        self.model_id = model_id
        self.api_endpoint = f"{self.base_url}/api/generate"

    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a response using Ollama"""
        if inference_config is None:
            inference_config = {"temperature": 0.7, "max_tokens": 50}

        payload = {
            "model": self.model_id,
            "prompt": message,
            "stream": False,
            **inference_config
        }

        try:
            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            
            data = response.json()
            print("Debug Response:", data)  # Debugging output
            return data.get("response", "Error: No response received.")
            
        except requests.exceptions.RequestException as e:
            handle_error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            handle_error(f"Unexpected error: {str(e)}")
            return None

def handle_error(error_msg: str):
    """Handle errors based on running mode"""
    if 'streamlit' in sys.modules:
        st.error(error_msg)
    else:
        print(f"Error: {error_msg}")

if __name__ == "__main__":
    chat = OllamaChat()
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == '/exit':
                break
            response = chat.generate_response(user_input)
            if response:
                print("Bot:", response)
            else:
                print("Bot: Sorry, I couldn't generate a response. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

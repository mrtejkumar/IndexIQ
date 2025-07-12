import requests
import streamlit as st
from typing import Optional, Dict, Any

class OpenRouterAPI:
    """OpenRouter API client for stock market queries"""
    
    def __init__(self):
        self.api_key = st.secrets["openrouter"]["api_key"]
        self.model_id = "mistralai/mistral-7b-instruct:free"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _get_system_prompt(self) -> Dict[str, str]:
        """Get system prompt for stock market AI"""
        return {
            "role": "system",
            "content": (
                "You are an AI assistant with expert knowledge exclusively in the stock market. "
                "You must only respond to questions strictly related to stock market concepts, trading, "
                "investment strategies, IPOs, financial regulations, market indices, or terms used in share markets. "
                "If a user asks anything outside this scope, you must reply with only this message: "
                "'I'm sorry, I am specialized in stock market topics and cannot help with that.'"
            )
        }
    
    def _create_payload(self, question: str) -> Dict[str, Any]:
        """Create API payload"""
        return {
            "model": self.model_id,
            "messages": [
                self._get_system_prompt(),
                {"role": "user", "content": question}
            ]
        }
    
    def ask_stock_question(self, question: str) -> str:
        """
        Ask a stock market question to OpenRouter API
        
        Args:
            question (str): The stock market question to ask
            
        Returns:
            str: The AI response or error message
        """
        try:
            headers = self._get_headers()
            payload = self._create_payload(question)
            
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload,
                timeout=30  # Add timeout
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"❌ API Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "❌ Connection error. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            return f"❌ Request failed: {str(e)}"
        except KeyError as e:
            return f"❌ Invalid response format: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"

# Create a singleton instance
_openrouter_client = None

def get_openrouter_client() -> OpenRouterAPI:
    """Get or create OpenRouter client instance"""
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenRouterAPI()
    return _openrouter_client

# Legacy function for backward compatibility
def ask_openrouter_stock_ai(question: str) -> str:
    """
    Legacy function for backward compatibility
    
    Args:
        question (str): The stock market question to ask
        
    Returns:
        str: The AI response or error message
    """
    client = get_openrouter_client()
    return client.ask_stock_question(question)

# Async version for future use (optional)
async def ask_stock_question_async(question: str) -> str:
    """
    Async version of stock question API call
    Note: This is a placeholder for future async implementation
    """
    import asyncio
    # For now, just run the sync version in a thread
    loop = asyncio.get_event_loop()
    client = get_openrouter_client()
    return await loop.run_in_executor(None, client.ask_stock_question, question)
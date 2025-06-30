import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
    
    def get_llm(self, model: str = "gpt-4", temperature: float = 0.3):
        """Get configured LLM instance"""
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=self.api_key
        )

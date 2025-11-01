from langchain_core.language_models.llms import LLM
from typing import Optional, List
from litellm import completion
from dotenv import load_dotenv
from pydantic import Field
import os
import json

load_dotenv()

class LiteLLMWrapper(LLM):
    model: str = Field(default="gemini/gemini-2.5-flash")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        This wrapper allows CrewAI to talk to Gemini via LiteLLM.
        CrewAI sends prompt as ONE string → we wrap as user message.
        """

        # Structure messages for models that expect system+user messages
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Follow tool instructions strictly."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = completion(
                model=self.model,
                messages=messages
            )

            # Extract output
            content = response["choices"][0]["message"]["content"]
            return content

        except Exception as e:
            return f"[LiteLLMWrapper Error]: {str(e)}"

    def supports_stop_words(self) -> bool:
        return False

    @property
    def _llm_type(self) -> str:
        return "litellm-gemini-wrapper"

import os
from typing import Optional
import requests

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import Field

from lwe.core.provider import Provider, PresetValue

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_MODEL = "openai/gpt-3.5-turbo"


class ChatOpenRouter(ChatOpenAI):

    model_name: str = Field(default=OPENROUTER_DEFAULT_MODEL, alias="model")
    """Model name to use."""
    openai_api_base: Optional[str] = Field(default=OPENROUTER_API_BASE, alias="base_url")
    """Base URL path for API requests, leave blank if not using a proxy or service
        emulator."""

    @property
    def _llm_type(self):
        """Return type of llm."""
        return "openrouter"

    def __init__(self, **kwargs):
        if 'openai_api_key' in kwargs:
            openai_api_key = kwargs.pop('openai_api_key')
        else:
            openai_api_key = os.getenv('OPENROUTER_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        super().__init__(openai_api_key=openai_api_key, **kwargs)


class ProviderOpenrouter(Provider):
    """
    Access to OpenRouter chat models via the OpenAI API
    """

    def __init__(self, config=None):
        self.models = self.fetch_models()
        super().__init__(config)

    def fetch_models(self):
        models_url = f"{OPENROUTER_API_BASE}/models"
        try:
            response = requests.get(models_url)
            response.raise_for_status()
            models_data = response.json()
            models_list = models_data.get('data')
            if not models_list:
                raise ValueError('Could not retrieve models')
            models = {model['id']: {'max_tokens': model['context_length']} for model in models_list}
            return models
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': False,
            "models": self.models,
        }

    @property
    def default_model(self):
        return OPENROUTER_DEFAULT_MODEL

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return ChatOpenRouter

    def customization_config(self):
        return {
            "verbose": PresetValue(bool),
            "model_name": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "openai_api_base": PresetValue(str, include_none=True),
            "openai_api_key": PresetValue(str, include_none=True, private=True),
            "openai_organization": PresetValue(str, include_none=True, private=True),
            "request_timeout": PresetValue(int),
            "max_retries": PresetValue(int, 1, 10),
            "max_tokens": PresetValue(int, include_none=True),
            "model_kwargs": {
                "top_p": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "top_k": PresetValue(int, min_value=0, max_value=20, include_none=True),
                "min_p": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "top_a": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "frequency_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "presence_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "repitition_penalty": PresetValue(float, min_value=0, max_value=2.0),
                "logit_bias": dict,
                "logprobs": PresetValue(bool, include_none=True),
                "top_logprobs": PresetValue(int, min_value=0, max_value=20),
                "response_format": dict,
                "seed": PresetValue(int),
                "stop": PresetValue(str, include_none=True),
                "functions": None,
                "function_call": None,
            },
        }

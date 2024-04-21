import os
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import Field

from lwe.core.provider import Provider, PresetValue
from lwe.core import constants

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_DEFAULT_MODEL = "openai/gpt-3.5-turbo"


class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str = Field(default=OPENROUTER_DEFAULT_MODEL)
    """Model name to use."""

    @property
    def _llm_type(self):
        """Return type of llm."""
        return "chat_openrouter"

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = OPENROUTER_API_BASE,
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)


class ProviderOpenrouter(Provider):
    """
    Access to OpenAI chat models via the OpenAI API
    """

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': False,
            "models": {
                "openai/gpt-3.5-turbo": {
                    "max_tokens": 16384,
                },
            },
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

import os
from typing import Optional

from langchain_aws.chat_models import ChatBedrockConverse
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register


class BedrockLLM(object):
    def __init__(
        self,
        model: str,
        aws_profile_name: Optional[str] = None,
        aws_region: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024 * 4,
    ):
        PHOENIX_PROJECT_NAME = os.environ.get("PHOENIX_PROJECT_NAME", "default")
        PHOENIX_ENDPOINT = os.environ.get("PHOENIX_ENDPOINT", None)
        if PHOENIX_ENDPOINT:
            # initialize Phoenix tracer
            tracer_provider = register(
                project_name=PHOENIX_PROJECT_NAME,
                endpoint=PHOENIX_ENDPOINT,
            )
            LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

        self.model = ChatBedrockConverse(
            model=model,
            credentials_profile_name=aws_profile_name,
            region_name=aws_region,
            temperature=temperature,
            max_tokens=max_tokens,
        )

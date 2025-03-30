from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    # for lite LLM in CrewAI
    model_name: str = "gemini/gemini-2.0-flash-lite"
    # for other frameworks
    model_name_no_prefix: str = "gemini-2.0-flash-lite"
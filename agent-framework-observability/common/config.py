from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    model_name: str = "gemini/gemini-2.0-flash-lite"
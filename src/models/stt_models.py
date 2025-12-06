from pydantic import BaseModel, Field


class SttServiceConfig(BaseModel):
    """Configuration model for Speech to Text Service"""
    model_name: str = Field(
        ..., description="LLM model para el servicio Speech to Text"
    )
    language: str = Field(
        ..., description="Lenguaje para el servicio Speech to Text"
    )
    response_format: str = Field(
        ..., description="Formato de respuesta para el servicio Speech to Text"
    )


class SttServiceResponse(BaseModel):
    transcription: str = Field(..., description="Trancription of the input audio")
    language: str = Field(
        ..., description="Default language para el servicio Speech to Text"
    )

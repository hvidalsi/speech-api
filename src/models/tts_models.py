from pydantic import BaseModel, Field


class TtsServiceConfig(BaseModel):
    """Configuration model for Text to Speech Service"""

    model_name: str = Field(
        ..., description="LLM model para el servicio Text to Speech"
    )
    voice_type: str = Field(
        ..., description="Tipo de voz para el servicio Text to Speech"
    )
    speed: float = Field(
        ..., description="Velocidad de voz para el servicio Text to Speech"
    )
    response_format: str = Field(
        ..., description="Formato de respuesta para el servicio Text to Speech"
    )


class TtsRequest(BaseModel):
    message: str = Field(..., description="Mensaje de entrada para sintetizar a voz")
    lang: str = Field("es", description="Idioma del audio sintetizado")

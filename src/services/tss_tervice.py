import os
import uuid
import re
from typing import Optional

from openai import OpenAI

from core.config import settings
from core.logger import setup_logger
from models.tts_models import TtsServiceConfig

logger = setup_logger(__name__)


class TtsService:
    def __init__(self, config: Optional[TtsServiceConfig] = None):
        if config:
            self.config = config
        else:
            self.config = TtsServiceConfig(
                model_name=settings.tts_default_model,
                voice_type=settings.tts_default_voice_type,
                speed=settings.tts_default_speed,
                response_format=settings.tts_default_response_format,
            )
        self.client = OpenAI()

    def normalize_numbers_for_tts(self, text: str) -> str:
        """
        Convierte solo números largos (4+ dígitos) a dígitos separados.
        Ej: 19213 -> 1 9 2 1 3
        Mantiene números normales como 2024, 100, 25, etc.
        """

        def convert(match):
            num = match.group(0)

            # Reglas que puedes tunear:
            if len(num) >= 4:
                # Lo convertimos a dígito por dígito
                return " ".join(num)
            else:
                # Números pequeños se dejan intactos
                return num

        # Reemplaza secuencias de dígitos
        return re.sub(r"\d+", convert, text)

    def synthesize_speech(self, input_text: str):
        try:
            response = self.client.audio.speech.create(
                model=self.config.model_name,
                voice=self.config.voice_type,
                input=self.normalize_numbers_for_tts(input_text),
                speed=self.config.speed,
                instructions="Eres un experto en asistir a los clientes en sus consultas de tipo bancario.",
            )
            generated_filename = f"{str(uuid.uuid4())}.{self.config.response_format}"
            output_file = os.path.join(
                settings.root_path,
                "files",
                "generated",
                generated_filename,
            )
            response.stream_to_file(output_file)
            return {
                "file_path": output_file,
                "filename": generated_filename,
                "media_type": "audio/mpeg",
                "format": self.config.response_format,
            }
        except Exception as e:
            err_msg = f"Synthesize speech failed due: {str(e)}"
            logger.error(err_msg)
            raise Exception(err_msg)

import re
from typing import Optional

from openai import OpenAI

from core.config import settings
from core.logger import setup_logger
from models.stt_models import SttServiceConfig

logger = setup_logger(__name__)


class SttService:
    def __init__(self, config: Optional[SttServiceConfig] = None):
        if config:
            self.config = config
        else:
            self.config = SttServiceConfig(
                model_name=settings.stt_default_model,
                language=settings.stt_default_language,
                response_format=settings.stt_default_response_format,
            )
        self.client = OpenAI()

    def transcribe_audio(self, file_path: str):
        audio_file = open(file_path, "rb")
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.config.model_name,
                file=audio_file,
                response_format=self.config.response_format,
                language=self.config.language,
            )
            transcription = re.sub(r"(?<=\d)[\s\.,-]+(?=\d)", "", transcription)
            return {"transcription": transcription, "language": self.config.language}
        except Exception as e:
            err_msg = f"Transcription audio failed due: {str(e)}"
            logger.error(err_msg)
            raise Exception(err_msg)

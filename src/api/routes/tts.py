import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from core.config import settings
from core.logger import setup_logger
from models.tts_models import TtsRequest
from services.tss_tervice import TtsService

router = APIRouter(prefix=settings.api_prefix)

logger = setup_logger(__name__)


@router.post("/to/speech")
def synthesize_speech(req: TtsRequest):
    input_text = req.message
    try:
        tts_service = TtsService()
        audio_result = tts_service.synthesize_speech(input_text)
        return FileResponse(
            path=audio_result["file_path"],
            media_type=audio_result["media_type"],
            filename=f"output.{audio_result['format']}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

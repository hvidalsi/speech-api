import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from core.config import settings
from core.logger import setup_logger
from models.stt_models import SttServiceResponse
from services.stt_service import SttService

router = APIRouter(prefix=settings.api_prefix)

logger = setup_logger(__name__)


@router.post("/to/text", response_model=SttServiceResponse)
def transcribe(audioFile: UploadFile = File(...)) -> SttServiceResponse:
    """Transcribe audio file to text"""
    if not audioFile:
        raise HTTPException(status_code=400, detail="No se recibió archivo de audio.")

    if audioFile.content_type not in [
        "audio/mpeg",
        "audio/wav",
        "audio/mp3",
        "audio/x-wav",
        "audio/flac",
        "audio/webm",
    ]:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    try:
        # Guardar el archivo recibido
        save_path = os.path.join(
            settings.root_path, "files", "received", audioFile.filename
        )
        with open(save_path, "wb") as temp_file:
            temp_file.write(audioFile.file.read())

        stt_service = SttService()
        logger.info(f"Transcribiendo: {audioFile.filename}")
        transcription_result = stt_service.transcribe_audio(save_path)
        logger.info(f"Transcripción completada:\n{transcription_result['transcription']}")

        return SttServiceResponse(
            transcription=transcription_result["transcription"],
            language=transcription_result["language"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

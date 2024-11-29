import time
import os
from io import BytesIO
from fastapi import UploadFile

try:
    import azure.cognitiveservices.speech as speechsdk
    import azure.cognitiveservices.speech.audio as audiosdk
    ENABLE_AZURE_SPEECH = True
except ImportError:
    ENABLE_AZURE_SPEECH = False

from config import (
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_REGION,
)

SUPPORTED_AUDIO_EXTENSIONS = {
    "mp3", "wav", "wma", "aac", "ogg",
    "flac", "alaw", "ulaw", "mp4",
    "amr", "webm", "3gp", "3g2"
}


def is_audio(filename: str) -> bool:
    """Check if file is an audio file."""
    return filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg'))


def save_audio(file: UploadFile) -> str:
    name, suffix = file.filename.split(".")
    path = f"static/{name}_{int(time.time())}.{suffix}"
    with open(path, "wb") as buffer:
        buffer.write(file.file.read())
    return path


def process(file: UploadFile) -> str:
    """Process audio file and return text."""
    if not ENABLE_AZURE_SPEECH:
        raise ValueError("Azure Speech SDK not installed. Audio processing is disabled.")
    
    path = save_audio(file)
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('AZURE_SPEECH_KEY'),
        region=os.getenv('AZURE_SPEECH_REGION')
    )

    audio_config = audiosdk.AudioConfig(filename=path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    return result.text if result.text else ""

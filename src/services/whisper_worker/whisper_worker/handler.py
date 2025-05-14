import os
import json
from config.config import settings
from shared.util.logging import logger
from shared.clients.s3_client import s3
from shared.clients.redis_client import get_redis_client 
from services.whisper_worker.whisper_worker.pipeline import AudioPipeline

INPUT_AUDIO_FILE = "audio.mp3"
TRANSCRIPTION_STREAM = settings.redis.streams.transcription_complete
TRANSCRIPTION_STARTED = settings.redis.streams.transcription_started
IS_PUBLISH_ENABLED = settings.whisper_worker.redis_enabled

redis_client = get_redis_client()

def download_audio(s3_key):
    logger.info(f"⬇️ Downloading audio file from S3: {s3_key} to {INPUT_AUDIO_FILE}")
    s3.download_file(settings.s3.bucket_name, s3_key, INPUT_AUDIO_FILE)
    logger.info("✅ Audio download complete")

def upload_json_to_s3(base_key: str, suffix: str, data: dict):
    filename_without_ext = os.path.splitext(os.path.basename(base_key))[0]
    namespace = os.path.dirname(base_key)
    filename = f"{filename_without_ext}__{suffix}.json"
    s3_path = f"{namespace}/{filename}"
    logger.info(f"Uploading to {s3_path}")

    data_json = json.dumps(data)
    s3.put_object(
        Bucket=settings.s3.bucket_name,
        Key=s3_path,  
        Body=data_json, 
        ContentType='application/json' 
    )
    logger.info(f"Upload complete for {s3_path}")
    return s3_path

def publish_message(message, stream=TRANSCRIPTION_STREAM):
    logger.info(f"Publishing event to {TRANSCRIPTION_STREAM}. Message {message}")
    redis_client.xadd(stream, message)

def handler(event):
    """
    Pulls audio file from s3, transcribes it with whisperx, and uploads result to s3
    """
    try:
        publish_message({
            "id": event["input"]["id"],
            "status": "started",
        }, TRANSCRIPTION_STARTED)
        
        s3_key = event["input"]["key"]
        id = event["input"]["id"]
        recording_ended_at = event["input"]["recording_ended_at"]
        download_audio(s3_key)

        raw_result, merged_result = AudioPipeline(INPUT_AUDIO_FILE).run_pipeline()

        raw_s3_key = upload_json_to_s3(s3_key, "raw", raw_result)
        merged_s3_key = upload_json_to_s3(s3_key, "merged", merged_result)

        if IS_PUBLISH_ENABLED:
            publish_message({"id": id,
                            "key_raw": raw_s3_key,
                            "merged_key":  merged_s3_key,
                            "recording_ended_at": recording_ended_at,
                            "duration": raw_result["metadata"]["duration"]})

        return {"output": merged_result}
    except Exception as e:
        logger.exception("🔥 Error during transcription pipeline")
        return {"error": str(e)}
 
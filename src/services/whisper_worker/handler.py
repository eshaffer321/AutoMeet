import os
import traceback
import runpod
import runpod.serverless.worker as worker
import json
from config.config import settings
from shared.logging import logger
from shared.s3_client import s3
from shared.redis_client import redis_client
from main import AudioPipeline

model_dir = settings.whisper_worker.local_model_dir
output_file = "audio.mp3"
transcription_complete_stream = settings.redis.transcription_complete
is_publish_enabled = os.environ.get("REDIS_ENALBED", False)

def handler(event):
    """
    Pulls audio file from s3, transcribes it with whisperx, and uploads result to s3
    """
    try:
        s3_key = event["input"]["key"]
        # Download the audio file from the remote source
        logger.info(f'Downloading {s3_key} from s3')
        s3.download_file(settings.s3.bucket_name, s3_key, output_file)
        logger.info(f"Finished downloading {s3_key} from s3")

        result = AudioPipeline(output_file).run_pipeline()
        logger.info(result)

        filename_without_ext = os.path.splitext(os.path.basename(s3_key))[0]
        namespace = os.path.dirname(s3_key)

        transcript_name = f"{filename_without_ext}.json"

        result_json = json.dumps(result)
        logger.info(f'Uploading {transcript_name}')
        s3_path = f"{namespace}/{transcript_name}"
        s3.put_object(
            Bucket=settings.s3.bucket_name,
            Key=s3_path,  
            Body=result_json, 
            ContentType='application/json' 
        )

        if is_publish_enabled:
            logger.info(f"Signaling upload completion for {s3_path}")
            publish_message(s3_path)
        else:
            logger.info(f"Skipping publishing because message publishing disabled")

        return {"output": result_json}
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"🔥 Full traceback:\n{error_message}")  # Ensure it's printed
        logger.error(f"🔥 Full traceback:\n{error_message}")  # Log it properly
        # If there's an error, return it
        os._exit(1)  # This will terminate the process immediately
        return {"error": str(e)}
    
def publish_message(transcription_s3_path):
    message = {"key": transcription_s3_path}
    redis_client.xadd(transcription_complete_stream, message)
    logger.info(f"Publishing event to {transcription_complete_stream}. Message {message}")


# Start the serverless function
runpod.serverless.start({"handler": handler})
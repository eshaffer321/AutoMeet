import runpod
from config.config import settings
from shared.logging import logger
from main import AudioPipeline

model_dir = settings.whisper_worker.local_model_dir

def handler(event):
    """
    This is a sample handler function that echoes the input
    and adds a greeting.
    """
    try:
        # Extract the prompt from the input
        file = event["input"]["file"]
        logger.info(f'Recieved event {file}')

        # Download the audio file from the remote source

        #
        result = AudioPipeline().run_pipeline(file)

        # Return the result
        return {"output": 'Success'}
    except Exception as e:
        # If there's an error, return it
        return {"error": str(e)}


# Start the serverless function
runpod.serverless.start({"handler": handler})
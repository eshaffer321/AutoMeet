from services.whisper_worker.whisper_worker.handler import handler
import runpod.serverless

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
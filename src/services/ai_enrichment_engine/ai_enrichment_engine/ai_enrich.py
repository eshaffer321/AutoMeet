import json
from shared.database.client import SessionLocal
from shared.clients.redis_client import RedisStreamConsumer
from config.config import settings
from shared.util.logging import logger
from shared.clients.s3_client import s3
from shared.database.models import AIEnrichment, Recording
from openai import OpenAI

# Initialize the Redis stream consumer
consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.transcription_complete,
    consumer_group=settings.ai_enrichment.consumer_group,
    consumer_name="consumer_1"
)

client = OpenAI()

BUCKET = settings.s3.bucket_name
MODEL = settings.ai_enrichment.model_name

def analyze_transcription(transcription):

    response = client.responses.create(
        model="gpt-4o-2024-08-06",
        input=[
            {
                "role": "system",
                "content": (
                    "You are an expert meeting summarizer. "
                    "Given a raw meeting transcript, extract the following structured information: "
                    "1) A clear and concise meeting title, "
                    "2) A short 1–2 sentence summary of the discussion, and "
                    "3) A bullet list of the key points covered. "
                    "Ensure the output strictly matches the provided JSON Schema."
                )
            },
            {
                "role": "user",
                "content": f"Here is a transcript from a meeting:\n\n{transcription}"
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "meeting_overview_analysis",
                "description": "Extract key details from the meeting transcription.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "meeting_title": {"type": "string"},
                        "short_description": {"type": "string"},
                        "key_points": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                    },
                    "required": ["meeting_title", "short_description", "key_points"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    event = json.loads(response.output_text)
    logger.info(event)
    return event

def get_transcription(filename):
    try:
        # Attempt to fetch the transcription file from S3
        response = s3.get_object(Bucket=BUCKET, Key=filename)
        file_content = response['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)
        return json_data 
    except Exception as e:
        logger.error(f"Error fetching transcription for {filename}: {e}")
        raise e  # Optionally log the error as needed

def handler(data):
    s3_key_merged = data["merged_key"]
    recording_id = data["id"]
    
    session = SessionLocal()
    transcription = get_transcription(s3_key_merged)
    if not transcription:
        logger.error(f"❌ No transcription found for recording {recording_id} with merged key {s3_key_merged}")
        return
    
    enrichment_details = analyze_transcription(transcription)

    try:
        ai_enrichment = AIEnrichment(
            recording_id=recording_id,
            title=enrichment_details.get("meeting_title", "Untitled Meeting"),
            description=enrichment_details.get("short_description", ""),
            key_points=enrichment_details.get("key_points", [])
        ) 
        session.add( ai_enrichment)
        session.commit()
        logger.info(f"✅ Successfully inserted encrichment for recording {recording_id} into the database")
    except Exception as e:
        session.rollback()  
        logger.error(f"❌ Failed to insert recording enrichment for {recording_id} into the database. Error: {e}")
    finally:
        session.close()  

def consume_stream():
    consumer.process(handler_fn=handler)
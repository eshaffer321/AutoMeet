import json
from shared.clients.s3_client import s3
from shared.util.logging import logger
from config.config import settings

class TranscriptionService:
    def __init__(self, bucket=None):
        self.bucket = bucket or getattr(settings.s3, 'bucket_name', None)
    """
    Service class for handling transcription-related operations.
    """

    def get_transcription(self, filename):
        """
        Fetch the transcription for a given filename from S3.
        """
        try:
            # Attempt to fetch the transcription file from S3
            response = s3.get_object(Bucket=self.bucket, Key=filename)
            file_content = response['Body'].read().decode('utf-8')
            json_data = json.loads(file_content)
            return json_data 
        except Exception as e:
            logger.error(f"Error fetching transcription for {filename}: {e}")
            raise e  # Optionally log the error as needed
        
    def update_transcription(self, filename, transcription, speaker_map=None):
        """
        Update the transcription for a given filename in S3.
        """
        try:
            cleaned_json = json.loads(transcription)

            if speaker_map:
                print(speaker_map)
                # Apply the speaker mapping to the transcription
                for entry in cleaned_json['transcription']:
                    if entry['speaker'] in speaker_map:
                        entry['speaker'] = speaker_map[entry['speaker']]
            serialized_data = json.dumps(cleaned_json).encode('utf-8')
            s3.put_object(Bucket=self.bucket, Key=filename, Body=serialized_data)
        except Exception as e:
            logger.error(f"Error updating transcription for {filename}: {e}")
            logger.error(f"Transcription data: {transcription}")
            raise e
from datetime import date
from pprint import pprint
from notion_client import Client
from config.config import settings
from shared.clients.redis_client import RedisStreamConsumer
from shared.util.logging import logger

NOTION_SECRET = settings.notion.secret
MEETING_DATABASE_ID = settings.notion.meeting_database_id

notion = Client(auth=NOTION_SECRET)

consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.enrichment_complete,
    consumer_group=settings.notion.consumer_group,
    consumer_name="consumer_1"
)

def insert_new_recording_page(title="No Title", summary="No Summary", type="1:1"):

    new_page = notion.pages.create(
        parent={"database_id": MEETING_DATABASE_ID},
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Meeting Date": {
                "date": {
                    "start": str(date.today())
                }
            },
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary
                        }
                    }
                ]
            },
            "Type": {
                "select": {
                    "name": type  # or whatever other type you've defined
                }
            }
        }
    )

    logger.info("✅ Page created:", new_page["url"])

def handler(data):
    result = notion.databases.query(
        database_id=MEETING_DATABASE_ID
    )

    insert_new_recording_page(title=data['id'], summary=data['summary'], type=data['type'])
    

    

def consume_stream():
    handler({"key": "value"})
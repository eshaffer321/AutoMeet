from shared.database.models import db
from shared.util.logging import logger 
from config.config import settings
from pony.orm import sql_debug

def bind_and_generate():
    if db.provider:
        return

    db_config = settings.db
    if db_config.provider == 'sqlite':
        logger.info("Using sqlite ponyorm provider")
        db.bind(provider='sqlite', filename=':memory:', create_db=True)
    else:
        logger.info("Using postgres ponyorm provider")
        db.bind(
            provider=db_config.provider,
            user=db_config.user,
            password=db_config.password,
            host=db_config.host,
            database=db_config.database,
            port=db_config.port,
        )

    db.generate_mapping(create_tables=True)
    if settings.db.debug:
        logger.info("Enabling sql debug")
        sql_debug(True)


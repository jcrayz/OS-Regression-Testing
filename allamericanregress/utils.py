import shutil
from allamericanregress import database_engine
from allamericanregress import config
import logging

logger = logging.getLogger(__name__)


def uninstall():
    logger.close()
    database_engine.database_connection.close()
    shutil.rmtree(config.CONFIG_PATH)

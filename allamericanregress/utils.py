import shutil
from allamericanregress import database_engine
from allamericanregress import config
import logging

logger = logging.getLogger(__name__)


def uninstall():
    logging.shutdown()
    shutil.rmtree(config.CONFIG_PATH)

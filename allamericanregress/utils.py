"""Utility functions for AllAmericanRegress"""
import shutil
from allamericanregress import config
import logging

logger = logging.getLogger(__name__)


def uninstall():
    """Uninstalls AllAmericanRegress files"""
    # TODO: Uninstall the service
    logging.shutdown()
    shutil.rmtree(config.CONFIG_PATH)

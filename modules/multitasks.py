from loguru import logger
import utils

from utils.enums import PARAMETR


async def start_multitasks(settings):
    counter = 1
    for task in settings.TASKS:
        logger.info(f"START MODULE {counter}")
        module = task.get(PARAMETR.MODULE)
        settings_module = task.get(PARAMETR.SETTINGS)
        await module(settings=settings_module)

        logger.warning("SLEEP BETWEEN MODULES")
        await utils.time.sleep_view(settings.SLEEP_BETWEEN_MODULES)
        counter += 1

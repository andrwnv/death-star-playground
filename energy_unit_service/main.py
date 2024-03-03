import asyncio
import logging

from service.config import Config
from service import run


SUB_SERVICE_INFO = "Death-Star: Energy unit service (v1.0.0)"

SERVICE_INFO = f"""
    ______                                  __  __      _ __
   / ____/___  ___  _________ ___  __      / / / /___  (_) /_
  / __/ / __ \/ _ \/ ___/ __ `/ / / /_____/ / / / __ \/ / __/
 / /___/ / / /  __/ /  / /_/ / /_/ /_____/ /_/ / / / / / /_
/_____/_/ /_/\___/_/   \__, /\__, /      \____/_/ /_/_/\__/
                      /____//____/

{SUB_SERVICE_INFO}
"""


logger = logging.getLogger(__name__)

if __name__ == "__main__":

    def __parse_args():
        import argparse

        parser = argparse.ArgumentParser(SUB_SERVICE_INFO)

        parser.add_argument(
            "-c", "--config", nargs="?", type=str, help="Filepath to config file."
        )

        return parser.parse_args()

    args = __parse_args()

    logging.basicConfig(
        level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s"
    )

    cfg = Config()
    if args.config is not None:
        cfg.init_with_file(args.config)
    else:
        logger.error("Failed to start service! Config file doesn't set!")

        exit(-1)

    logger.info(SERVICE_INFO)

    asyncio.run(run(cfg))

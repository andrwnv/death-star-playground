import asyncio
import logging

from service.config import Config
from service import run


SUB_SERVICE_INFO = "Death-Star: Atmosphere unit service (v1.0.0)"

SERVICE_INFO = f"""
     ___   .___________..___  ___.   ______        _______..______    __    __   _______ .______       _______         __    __  .__   __.  __  .___________.
    /   \  |           ||   \/   |  /  __  \      /       ||   _  \  |  |  |  | |   ____||   _  \     |   ____|       |  |  |  | |  \ |  | |  | |           |
   /  ^  \ `---|  |----`|  \  /  | |  |  |  |    |   (----`|  |_)  | |  |__|  | |  |__   |  |_)  |    |  |__    ______|  |  |  | |   \|  | |  | `---|  |----`
  /  /_\  \    |  |     |  |\/|  | |  |  |  |     \   \    |   ___/  |   __   | |   __|  |      /     |   __|  |______|  |  |  | |  . `  | |  |     |  |     
 /  _____  \   |  |     |  |  |  | |  `--'  | .----)   |   |  |      |  |  |  | |  |____ |  |\  \----.|  |____        |  `--'  | |  |\   | |  |     |  |     
/__/     \__\  |__|     |__|  |__|  \______/  |_______/    | _|      |__|  |__| |_______|| _| `._____||_______|        \______/  |__| \__| |__|     |__|     
                                                                                                                                                            
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

from pathlib import Path

from sts_bot.runner.manual_runner import ManualRunner
from sts_bot.communication.communicator import Communicator
from sts_bot.sts.gamestate.player import PlayerClass
from sts_bot.logging.logger import STSLogger


def main():
    # intit logging
    basePath = Path(__file__).parent

    logger = STSLogger(basePath)

    fifoPath = basePath / "fifo"
    
    communicator = Communicator(
        logger=logger,
        input_path=fifoPath / "sts_input",
        output_path=fifoPath / "sts_output",
    )

    runner = ManualRunner(communicator, logger)
    runner.run(PlayerClass.IRONCLAD, 0, "LGZ12EEMFGUK")



if __name__ == "__main__":
    main()

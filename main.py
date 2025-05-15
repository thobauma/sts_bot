from pathlib import Path
import logging

# from smolagents import LiteLLMModel
from ollama import Client

from sts_bot.helper.constants import model_id, api_base
from sts_bot.runner.agentic_runner import AgenticRunner
from sts_bot.communication.communicator import Communicator
from sts_bot.sts.gamestate.player import PlayerClass
from sts_bot.logging.logger import STSLogger
from sts_bot.agent.agent import Agent


def main():
    # intit logging
    basePath = Path(__file__).parent

    logger = STSLogger(basePath)

    # # host model locally with ollama
    # model = LiteLLMModel(
    #     model_id=model_id,
    #     api_base=api_base,
    # )

    ollama_client = Client(host=api_base)
    agent = Agent(client=ollama_client, model=model_id, logger=logger)

    fifoPath = basePath / "fifo"

    communicator = Communicator(
        logger=logger,
        input_path=fifoPath / "sts_input",
        output_path=fifoPath / "sts_output",
    )

    runner = AgenticRunner(agent=agent, communicator=communicator, logger=logger)

    runner.run(PlayerClass.IRONCLAD, 0, "LGZ12EEMFGUK")


if __name__ == "__main__":
    main()

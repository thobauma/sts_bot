from abc import ABC, abstractmethod
from typing import List, Callable, Any, Optional
from pathlib import Path
import yaml

from sts_bot.logging.logger import STSLogger

prompts_path = Path(__file__).resolve().parent


class PromptGenerator:
    def __init__(
        self,
        examples: str | Path = prompts_path / "examples.yaml",
        general_prompts: str | Path = prompts_path / "general_prompt.yaml",
        dynamic_prompt: str | Path = prompts_path / "dynamic_prompts.yaml",
    ):
        with open(general_prompts, "r") as f:
            self.general_prompts = yaml.safe_load(f)
            self.system_prompt = self.general_prompts["system_prompt"]["Base"]
            self.sts_system_prompt = self.general_prompts["system_prompt"]["sts_system"]
            # self.general_user_prompt = self.general_prompts["user_prompt"]
        with open(examples, "r") as f:
            self.examples = yaml.safe_load(f)
        with open(dynamic_prompt, "r") as f:
            self.dynamic_prompt = yaml.safe_load(f)
        # for prompt_file_name in screentype_prompt_filenames:
        #     prompt_file_path = Path(prompts_path, prompt_file_name + ".yaml")
        #     with open(Path(prompt_file_path), "r") as f:
        #         self.screentype_prompts[prompt_file_name] = yaml.safe_load(f)

    def create_prompt(
        self,
        game_state: dict[str, Any],
        available_actions: str | list[str],
        example_key: str,
        dynamic_key: str = None,
        logger: Optional[STSLogger] = None,
    ):
        return self._create_prompt(
            system_prompt=self.system_prompt,
            static_prompt=self.sts_system_prompt,
            # general_user_prompt=self.general_user_prompt,
            game_state=game_state,
            available_actions=available_actions,
            examples=self.examples[example_key],
            dynamic_prompt=self.dynamic_prompt[dynamic_key],
            logger=logger,
        )

    def _create_prompt(
        self,
        system_prompt: str,
        static_prompt: str,
        # general_user_prompt: str,
        game_state: dict[str, Any],
        available_actions: str | list[str],
        examples: str | dict[str, Any],
        dynamic_prompt: Optional[str] = None,
        logger: Optional[STSLogger] = None,
        # format_type: str = "chat",
        # verbose_state: bool = False,
    ):
        system_message = {
            "role": "system",
            "content": (
                f"{system_prompt}\n\n"
                f"{static_prompt}\n\n"
                # f"<game_state>\n{game_state}\n</game_state>"
            ),
        }
        user_message = {
            "role": "user",
            "content": (
                f"{static_prompt}\n\n"
                f"<game_state>\n{game_state}\n</game_state>"
                # f"{general_user_prompt}\n\n"
                f"{dynamic_prompt}\n\n"
                f"<available_actions>\n{available_actions}\n</available_actions>\n\n"
                f"{examples}"
            ),
        }

        if logger is not None:
            logger.debug(system_message)
            logger.info(user_message)
        messages = [system_message, user_message]
        return messages

    # def generate_prompt(
    #     self, screen_type: str, serialized_state
    # ) -> list[dict[str, str]]:

    #     system_message = {"role": "system", "content": self.system_prompt}
    #     user_content = (
    #         self.sts_system_prompt + "\n\n" + self.screentype_prompts[screen_type]
    #     )
    #     user_message = {"role": "user", "content": user_content}
    #     messages = [system_message, user_message]

    #     return messages

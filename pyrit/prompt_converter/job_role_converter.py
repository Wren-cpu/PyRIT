# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import random
import re
# TODO: Fix imports as needed.

from pyrit.prompt_converter import PromptConverter, ConverterResult


logger = logging.getLogger(__name__)


class JobRoleGenerator(PromptConverter):
    """
    A PromptConverter that adds demographic groups to the job role.
    """

    def __init__(self, *, max_iterations: int = 20):
        """
        Initializes the JobRoleGenerator.

        Args:
            max_iterations (int): Maximum number of convert_async calls allowed. (TODO: add more details here)
        """
        super().__init__()
        self.max_iterations = max_iterations

        # TODO: Add any additional initialization logic here.

    def input_supported(self, input_type) -> bool:
        """
        Checks if the input type is supported by the converter.
        """
        return input_type == "text"

    async def convert_async(self, *, prompt: str, input_type="text") -> ConverterResult: # TODO: Needed.
        """
        Converts the given prompt by adding demographic groups to the job role.

        Args:
            prompt (str): The prompt to be converted.
            input_type (str): The type of input (should be "text").
        Returns:
            ConverterResult: The result containing the perturbed prompts.
        """
        # TODO: Implement the conversion logic here.
        pass
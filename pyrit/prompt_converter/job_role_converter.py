# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import random
from typing import Dict, List, Optional

from find_job_titles import Finder

from pyrit.prompt_converter import PromptConverter, ConverterResult


logger = logging.getLogger(__name__)


class JobRoleGenerator(PromptConverter):
    """
    A PromptConverter that adds demographic groups to the job role.
    """

    def __init__(self, *, 
                 max_iterations: int = 20, 
                 deterministic: bool = False,
                 custom_demographics: Optional[Dict[str, List[str]]] = None
    ) -> None:
        """
        Initializes the JobRoleGenerator.

        Args:
            max_iterations (int): Maximum number of convert_async calls allowed. (TODO: add more details here)
            deterministic (bool): If True, choose the demographic group deterministically. If False, choose randomly. Defaults to False.
            custom_demographics (Optional[Dict[str, List[str]]], optional): A dictionary of custom demographics
                                                                            to prepend the job roles. Defaults to None.
        """
        super().__init__()
        self.max_iterations = max_iterations

        default_demographics = [
            "European", "American", "African", "Hispanic", "Latino",  
            "White", "Black", "Caucasian", "Indigenous", "Native American",
            "South Asian", "East Asian", "French", "German", "Italian", "Spanish",
            "Chinese", "Japanese", "Korean", "Indian", "Filipino", "Vietnamese",
            "Mexican", "Puerto Rican", "Cuban", "Dominican", "Colombian", "Venezuelan",
            "Australian", "New Zealander", "British", "Irish", "Scottish", "Welsh",
            "Russian", "Ukrainian", "Polish", "Romanian", "Turkish", "Greek",
            "Arab", "Persian", "Israeli", "Egyptian", "Moroccan", "Nigerian"
        ]

        # Use custom demographics if provided, otherwise default to the standard ones
        self._demographics = custom_demographics if custom_demographics else default_demographics
        self._deterministic = deterministic

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
        if not self.input_supported(input_type):
            raise ValueError("Input type not supported")

        # Detect job role in the prompt
        finder = Finder()
        job_idxs = []
        for job_title, idx in finder.finditer(prompt, True):
            # Add demographic groups to the job role
            job_idxs.append(idx)

        job_idxs.sort(reverse=True)

        final_prompt = prompt
        # If job role is detected, add demographic groups to the job role
        for idx in job_idxs:
            # Add random demographic group to the job role
            if self._deterministic:
                d_idx = idx % len(self._demographics)
                final_prompt = final_prompt[:idx] + (self._demographics[d_idx]) + " " + final_prompt[idx:]
            else:
                final_prompt = final_prompt[:idx] + (random.choice(self._demographics)) + " " + final_prompt[idx:]
            pass

        pass
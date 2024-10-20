# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import re
import random
from typing import Dict, List, Optional

from pyrit.models import PromptDataType
from pyrit.prompt_converter import PromptConverter, ConverterResult


logger = logging.getLogger(__name__)


class JobRoleGenerator(PromptConverter):
    """
    A PromptConverter that adds demographic groups to the job role.
    """

    def __init__(self, *, 
                 max_iterations: int = 20, 
                 deterministic: bool = False,
                 custom_demographics: Optional[Dict[str, List[str]]] = None,
                 custom_jobs: Optional[Dict[str, List[str]]] = None
    ) -> None:
        """
        Initializes the JobRoleGenerator.

        Args:
            max_iterations (int): Maximum number of convert_async calls allowed. (TODO: add more details here)
            deterministic (bool): If True, choose the demographic group deterministically. If False, choose randomly. Defaults to False.
            custom_demographics (Optional[Dict[str, List[str]]], optional): A dictionary of custom demographics
                                                                            to prepend the job roles. Defaults to None.
            custom_jobs (Optional[Dict[str, List[str]]], optional): A dictionary of custom job roles. Defaults to None.
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

        default_jobs = [
            "accountant", "actor", "actress", "architect", "artist", "author", "baker", "banker", "barber", "bartender",
            "biologist", "blogger", "bookkeeper", "builder", "butcher", "carpenter", "cashier", "chef", "clerk", "coach",
            "comedian", "composer", "consultant", "contractor", "cook", "counselor", "dancer", "dentist", "designer",
            "developer", "dietician", "doctor", "driver", "editor", "electrician", "engineer", "farmer", "firefighter",
            "fisherman", "florist", "gardener", "hairdresser", "handyman", "instructor", "investor", "janitor", "jeweler",
            "journalist", "judge", "lawyer", "lecturer", "librarian", "lifeguard", "manager", "mechanic", "model", "nurse",
            "painter", "paramedic", "pharmacist", "photographer", "physician", "pilot", "plumber", "poet", "police officer",
            "politician", "professor", "psychologist", "receptionist", "reporter", "researcher", "salesperson", "scientist",
            "president", "senator", "sheriff", "singer", "soldier", "surgeon", "teacher", "technician", "therapist", "trainer",
        ]

        # Use custom lists if provided, otherwise default to the standard ones
        self._demographics = custom_demographics if custom_demographics else default_demographics
        self._jobs = custom_jobs if custom_jobs else default_jobs
        
        # Create a regex pattern to match job roles
        self._job_pattern = '|'.join(re.escape(title) for title in self._jobs)

        self._deterministic = deterministic

    def input_supported(self, input_type: PromptDataType) -> bool:
        """
        Checks if the input type is supported by the converter.
        """
        return input_type == "text"

        
    def _insert_demographic(self, prompt: str, demographic: str, idx: int) -> str:
        """
        Inserts a demographic group before the job role in the prompt.

        Args:
            prompt (str): The prompt to insert the demographic group into.
            demographic (str): The demographic group to insert.
            idx (int): The index of the job role in the prompt.
        Returns:
            str: The prompt with the demographic group inserted.
        """
        vowels = "aeiou"
    
        # Insert the new word at the specified index
        new_prompt = prompt[:idx] + demographic + " " + prompt[idx:]

        # Fix the previous article (a/an) if needed
        words_before = prompt[:idx].split()
        if len(words_before) > 0:
            prev_word = words_before[-1]
            if prev_word in ['a', 'an']:
                if demographic[0].lower() in vowels:
                    correct_article = "an"
                else:
                    correct_article = "a"
                
                # Ensure correct article is used
                prev_idx = len(prompt[:idx]) - len(prev_word) - 1
                new_prompt = new_prompt[:prev_idx] + correct_article + new_prompt[prev_idx + len(prev_word):]

        return new_prompt

    async def convert_async(self, *, prompt: str, input_type="text") -> ConverterResult:
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
        job_idxs = [(match.start()) for match in re.finditer(self._job_pattern, prompt, re.IGNORECASE)]

        job_idxs.sort(reverse=True)

        final_prompt = prompt
        # If job role is detected, add demographic groups to the job role
        for idx in job_idxs:
            # Add random demographic group to the job role
            if self._deterministic:
                d_idx = idx % len(self._demographics)
                final_prompt = self._insert_demographic(final_prompt, self._demographics[d_idx], idx)
            else:
                final_prompt = self._insert_demographic(final_prompt, random.choice(self._demographics), idx)
            pass

        return ConverterResult(final_prompt, "text")

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import asyncio
import pytest

from pyrit.prompt_converter.job_role_converter import JobRoleGenerator

# Test for input type not supported
def test_job_role_input_not_supported():
    converter = JobRoleGenerator()
    with pytest.raises(ValueError):
        asyncio.run(converter.convert_async(prompt="I'm not employed", input_type="image"))


# Test for deterministic substitution
@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("I'm not employed", "I'm not employed"),  # Zero job instances
        ("He is a janitor", "He is an Indigenous janitor"),  # One job instance
        ("My mother is a teacher and my father is a doctor", "My mother is a Spanish teacher and my father is an Israeli doctor"),  # Multiple job instances
        ("Artist, engineer, and scientist", "European Artist, Indigenous engineer, and Mexican scientist"),  # Punctuation handling
        ("APPLY NOW!!!!! CALLING FOR ALL LAWYER", "APPLY NOW!!!!! CALLING FOR ALL Irish LAWYER"),  # Special characters
        ("I have mostly seen comedians, actors, and some singers", "I have mostly seen Indian comedians, British actors, and some American singers"),  # Plural jobs
        ("dOcToR, SenatorBloggerbankerBAKER", "European dOcToR, SenatorBloggerbankerBAKER"),  # Merged words
    ],
)
def test_job_role_deterministic(input_text, expected_output):
    converter = JobRoleGenerator(deterministic=True)
    result = asyncio.run(converter.convert_async(prompt=input_text))
    assert result.output_text == expected_output


# Test for random substitution
@pytest.mark.parametrize(
    "input_text",
    [
        ("I'm not employed"),
        ("He is a janitor"),
        ("My mother is a teacher and my father is a doctor"),
        ("Artist, engineer, and scientist"),
        ("APPLY NOW!!!!! CALLING FOR ALL LAWYER"),
        ("I have mostly seen comedians, actors, and some singers"),
        ("dOcToR, SenatorBloggerbankerBAKER"),
    ],
)
def test_job_role_non_deterministic(input_text):
    converter = JobRoleGenerator(deterministic=True)
    result = asyncio.run(converter.convert_async(prompt=input_text))

    # Output text is at least as long as the input text
    assert len(result.output_text) >= len(input_text)

    input_words = set(input_text.split())
    output_words = set(result.output_text.split())
    
    for word in output_words:
        assert word in input_words or word in converter._demographics or word in ["a", "an"]


# Test for custom demographics
@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("I'm not employed", "I'm not employed"),
        ("He is a janitor", "He is a Demo1 janitor"),
        ("My mother is a teacher and my father is a doctor", "My mother is a Demo2 teacher and my father is a Demo1 doctor"),
    ],
)
def test_job_role_custom_demo(input_text, expected_output):
    converter = JobRoleGenerator(deterministic=True, custom_demographics=["Demo1", "Demo2"])
    result = asyncio.run(converter.convert_async(prompt=input_text))
    assert result.output_text == expected_output


# Test for custom jobs
@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("I'm not employed", "I'm not employed"),
        ("He is a janitor", "He is a janitor"),
        ("My mother is a teacher and my father is a doctor", "My mother is a Spanish teacher and my father is an Israeli doctor"),
        ("I am a TikToker", "I am a Caucasian TikToker")
    ],
)
def test_job_role_custom_jobs(input_text, expected_output):
    converter = JobRoleGenerator(deterministic=True, custom_jobs=["teacher", "doctor", "TikToker"]) # Exclude janitor
    result = asyncio.run(converter.convert_async(prompt=input_text))
    assert result.output_text == expected_output


# Test for short input text
@pytest.mark.parametrize(
    "input_text",
    [
        (""),  # Empty string
        ("I"),  # Single character
        ("&#"),  # Special characters
    ],
)
def test_job_role_short_input(input_text):
    converter = JobRoleGenerator(deterministic=True)
    result = asyncio.run(converter.convert_async(prompt=input_text))
    assert result.output_text == input_text
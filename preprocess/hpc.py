from .registry import register
from .utils import (
    process_templates_json,
    remove_brackets,
    split_on_punctuation,
)
import re
from functools import reduce


brackets_pattern = re.compile(r'\(([^\(\)]+)\)|\<([^\<\>]+)\>')
def subtract_brackets(line):
    result = re.findall(brackets_pattern, line)
    # as there is two two groups in the pattern we need to flatten the
    # extraction results
    result = [group for match in result for group in match]
    remaining = re.sub(brackets_pattern, '', line)
    if remaining:
        result.append(remaining)
    return result


# this case is a colon that's not followed by a variable
colon_for_details_pattern = re.compile(r':(?:(?!\s*VAR))')
def splitting_hpc(parts):
    """Takes care of specific preprocessing of this type of logs before
    rules or OpenIE is applied to extract triples."""
    result = []
    for part in parts:
        has_equals = "=" in part
        has_colon = ":" in part
        if has_equals and has_colon:
            subparts = part.strip(':').split(':')
            result.extend(subparts)
        elif has_colon and not has_equals:
            if re.search('VAR\d+\s*:\s*VAR', part):
                subparts = part.split(':')
            else:
                subparts = re.split(colon_for_details_pattern, part.strip(':'))
            result.extend(subparts)
        else:
            result.append(part)
    return result


def process_line(template):
    parts = subtract_brackets(template)
    parts = splitting_hpc(parts)
    parts = split_on_punctuation(parts)
    return parts  


@register("hpc")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    return process_templates_json(input_source, process_line)

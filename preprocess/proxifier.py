from .registry import register
from .utils import (
    process_templates_json,
    remove_brackets,
    split_on_punctuation,
)
import re


proxifier_tag_pattern = re.compile('^[^-]+-\s*')
def remove_log_type_tag(line):
    return re.sub(proxifier_tag_pattern, '', line)


def process_line(template):
    template = remove_log_type_tag(template)
    template = remove_brackets(template)
    parts = template.split(":")
    parts = split_on_punctuation(parts)
    return parts  


@register("proxifier")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    return process_templates_json(input_source, process_line)

from .registry import register
from .utils import (
    process_templates_json,
    Repl,
    remove_brackets,
    remove_underscores, underscores,
    split_on_punctuation,
)
import re


proxifier_tag_pattern = re.compile('^[^-]+-\s*')
def remove_log_type_tag(line):
    return re.sub(proxifier_tag_pattern, '', line)


def process_line(template):
    template = template.strip()
    template = remove_log_type_tag(template)
    template = remove_brackets(template)
    template = re.sub(underscores, remove_underscores, template)
    template = re.sub('\*', Repl(), template)
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

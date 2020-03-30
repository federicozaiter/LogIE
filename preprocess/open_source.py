from .registry import register
from .utils import (
    process_templates_json,
    Repl,
    remove_brackets,
    remove_underscores, underscores,
)
import re


def process_line(template):
    template = template.strip()
    template = remove_brackets(template)
    template = re.sub(underscores, remove_underscores, template)
    template = re.sub('\*', Repl(), template)
    return template  


@register("open_source")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    return process_templates_json(input_source, process_line)

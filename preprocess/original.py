from .registry import register
from .utils import (
    process_templates_json,
    Repl,
    remove_brackets,
    remove_underscores, underscores,
)
import re


# this step should be done before brackets are removed
log_type_tag_pattern = re.compile('^\[.+\]')
def remove_log_type_tag(line):
    return re.sub(log_type_tag_pattern, '', line)


def process_line(template):
    template = template.strip()
    template = remove_log_type_tag(template)
    template = remove_brackets(template)
    template = re.sub(underscores, remove_underscores, template)
    template = re.sub('\*', Repl(), template)
    return template  


@register("original")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    return process_templates_json(input_source, process_line)

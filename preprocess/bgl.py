from .registry import register
from .utils import (
    process_templates_json,
    Repl,
    remove_brackets,
    remove_underscores, underscores,
    split_on_punctuation,
)
import re


bgl_tag_pattern = re.compile(r'^([A-Z]+\s){2,}')
def remove_log_type_tag(line):
    return re.sub(bgl_tag_pattern, '', line)


colon_in_parentheses_pattern = re.compile(r'\(([^\(\)]+:[^\(\)]+)\)')
def subtract_parentheses_colon(line):
    result = re.findall(colon_in_parentheses_pattern, line)
    remaining = re.sub(colon_in_parentheses_pattern, '', line)
    if remaining:
        remaining = remaining.split(":")
        result.extend(remaining)
    return result


punctuation_split_pattern = re.compile(r'(?:\.|;)\s')
def split_on_punctuation(sentences):
    result = []
    for sentence in sentences:
        result.extend(re.split(punctuation_split_pattern, sentence))
    return result

def process_line(template):
    template = template.strip()
    template = remove_log_type_tag(template)
    template = re.sub(underscores, remove_underscores, template)
    template = re.sub('\*', Repl(), template)
    sentences = subtract_parentheses_colon(template)
    sentences = split_on_punctuation(sentences)
    return sentences  


@register("bgl")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    return process_templates_json(input_source, process_line)

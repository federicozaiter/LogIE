from .registry import register
from .utils import (
    remove_brackets,
    split_on_punctuation,
)
import re
from .preprocessor import BasePreprocessor
from .globalConfig import regL


bgl_tag_pattern = re.compile('^([A-Z]+\s)')
proxifier_tag_pattern = re.compile('^[^:]+:\s*')
def remove_log_type_tag(line):
    line = re.sub(bgl_tag_pattern, '', line)
    return re.sub(proxifier_tag_pattern, '', line)


def flatten(seq):
    return [elem for elems in seq for elem in elems]


curly_brackets_pattern = re.compile(r'\{([^\{\}]+)\}')
square_brackets_pattern = re.compile(r'\[([^\[\]]+)\]')
parentheses_pattern = re.compile(r'\(([^\(\)]+)\)')
def subtract_brackets(line, pattern=parentheses_pattern):
    result = re.findall(pattern, line)
    remaining = re.sub(pattern, '', line)
    if remaining:
        result.append(remaining)
    return result


colon_for_details_pattern = re.compile(r':(?:(?!\s*VAR))')
def splitting_spark(parts):
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


class Spark_Preprocessor(BasePreprocessor):
    
    def _process_template(self, template):
        template = remove_log_type_tag(template)
        parts = subtract_brackets(template, curly_brackets_pattern)
        parts = flatten(map(lambda x: subtract_brackets(x, square_brackets_pattern), parts))
        parts = flatten(map(lambda x: subtract_brackets(x, parentheses_pattern), parts))
        parts = map(lambda x: remove_brackets(x), parts)
        parts = splitting_spark(parts)
        parts = split_on_punctuation(parts)
        return parts     

    def _process_log(self, log):
        idx, log = log.strip().split('\t')
        regexes = regL[self.params['templates_type']]
        for regex in regexes:
            log = re.sub(regex, "", log)
        return log


@register("spark")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    return Spark_Preprocessor(params)

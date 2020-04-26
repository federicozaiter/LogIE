from .registry import register
from .utils import (
    remove_brackets,
    split_on_punctuation,
)
import re
from .preprocessor import BasePreprocessor
from .globalConfig import regL


bgl_tag_pattern = re.compile('^([A-Z]+\s)')
def remove_log_type_tag(line):
    return re.sub(bgl_tag_pattern, '', line)


# this case is a colon that's not followed by a variable
colon_for_details_pattern = re.compile(r':(?:(?!\s*VAR))')
def splitting_zookeeper(parts):
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


parentheses_pattern = re.compile(r'\(([^\(\)]+)\)')
def subtract_brackets(line, pattern=parentheses_pattern):
    result = re.findall(pattern, line)
    remaining = re.sub(pattern, '', line)
    if remaining:
        result.append(remaining)
    return result


class Zookeeper_Preprocessor(BasePreprocessor):
    
    def _process_template(self, template):
        template = remove_log_type_tag(template)
        parts = subtract_brackets(template)
        parts = splitting_zookeeper(parts)
        parts = split_on_punctuation(parts)
        return parts    

    def _process_log(self, log):
        idx, log = log.strip().split('\t')
        regexes = regL[self.params['templates_type']]
        for regex in regexes:
            log = re.sub(regex, "", log)
        return log


@register("zookeeper")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    return Zookeeper_Preprocessor(params)

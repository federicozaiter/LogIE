from .registry import register
from .utils import process_templates, Repl
import re


idx_re = re.compile(r'^\d+')
def is_template(line):
    match = idx_re.search(line)
    if match:
        return True
    return False

brackets = re.compile(r'[\[\]\{\}]') # \(\)
def remove_brackets(line):
    return re.sub(brackets, ' ', line).strip()


# this step should be done before brackets are removed
log_type_tag_pattern = re.compile('^\[.+\]')
def remove_log_type_tag(line):
    return re.sub(log_type_tag_pattern, '', line)

# Some variables use underscores which we want to keep so we only remove
# the ones from longer sentences
underscores = re.compile(r'([\w\d]+_[\w\d]+){3,}')
def remove_underscores(match):
    group = match.group()
    return group.replace('_', ' ')

def process_line(line):
    if is_template(line):
        idx, template = line.split('\t')
        template = template.strip()
        # template = template.lower()
        template = remove_log_type_tag(template)
        template = remove_brackets(template)
        template = re.sub(underscores, remove_underscores, template)
        template = re.sub('\*', Repl(), template)
        result = '\t'.join((idx, template))
        result = ''.join((result, '\n'))
        return result  
    else:
        return ''


@register("original")
def preprocess_dataset(params):
    """
    Runs template preprocessing executor.
    """
    input_source = params['templates']
    output = params['processed_templates']
    process_templates(input_source, output, process_line)

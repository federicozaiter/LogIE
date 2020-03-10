from .registry import register
import configparser
import os
import pathlib
from shutil import copy


def text_file_to_list(file_name):
    with open(file_name) as f:
        result = list(f)
    return result


def parse_triples_reverb_format(lines):
    result = {}
    for line in lines:
        line = line.strip().split('\t')
        idx = line[1]
        triple = (line[2], line[3], line[4])
        if idx in result:
            result[idx].append(triple)
        else:
            result[idx] = [triple]
    return result


def parse_remaining_reverb_format(lines, triples):
    remaining = {}
    # use count while the idx is not the ordinal of the template
    count = 0
    for line in lines:
        if str(count) not in triples:
            line = line.strip()#.split('\t')[1]
            remaining[count] = [line]
        count += 1
    return remaining



@register('stanford')
def extract_triples(source, output):
    config = configparser.ConfigParser()
    config_path = os.path.join(
        os.path.dirname(__file__),
        'openie.ini',
    )
    config.read(config_path)
    jars_dir = os.path.normpath(config['Stanford']['dir'])
    # the java app has an issue parsing the file name so it's easier to
    # create a temporary file and then remove it
    copy(source, './')
    source_file_name = os.path.basename(source)
    memory = config['Stanford']['memory']
    program = config['Stanford']['program']
    # checkout https://github.com/stanfordnlp/CoreNLP/issues/789
    # to see if they fixed how to use -resolve_coref true in the command
    command = f'java -{memory} -cp "{jars_dir}\\*" {program}\
        -threads 8\
        -ssplit.newlineIsSentenceBreak always\
        -triple.all_nominals true -format reverb "{source_file_name}"\
        > "{output}"'
    print(command)
    print("Extracting triples with StanfordNLP...")
    code = os.system(command)
    os.remove(os.path.join(
        './',
        source_file_name,
    ))
    if code == 0:
        stanford_triples = text_file_to_list(output)
        stanford_triples = parse_triples_reverb_format(stanford_triples)
        stanford_remaining = text_file_to_list(source)
        stanford_remaining = parse_remaining_reverb_format(stanford_remaining, stanford_triples)
        return stanford_triples, stanford_remaining
    else:
        print("Standford CoreNLP OpenIE FAILED")
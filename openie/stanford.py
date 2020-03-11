from .registry import register
import configparser
import os
import pathlib
from shutil import copyfile
from ..oie_extraction.extraction import Extraction


def text_file_to_list(file_name):
    with open(file_name) as f:
        result = list(f)
    return result


def parse_triples_reverb_format(lines):
# Reverb format https://github.com/knowitall/reverb/blob/master/README.md
    result = {}
    for line in lines:
        line = line.strip().split('\t')
        idx = line[1]
        triple = (line[2:5])
        extraction = Extraction.fromTuple(triple, sentence=line[12])
        if idx in result:
            result[idx].append(extraction)
        else:
            result[idx] = [extraction]
    return result


def parse_remaining_reverb_format(lines, triples):
    remaining = {}
    # use count while the idx is not the ordinal of the template
    # this is to see which templates didn't yield triples
    count = 0
    for line in lines:
        if str(count) not in triples:
            line = line.strip()#.split('\t')[1]
            remaining[count] = [line]
        count += 1
    return remaining


def clean_temp_file(file_name):
    lines = text_file_to_list(file_name)
    with open(file_name, 'w') as f:
        for line in lines:
            sentence = line.split('\t')[1]
            f.write(sentence)


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
    temp_file_name = './temp_source.txt'
    copyfile(source, temp_file_name)
    # We need to clean it so that Stanford CoreNLP has a clean sentence
    # per line in the input file
    clean_temp_file(temp_file_name)
    # parsing config
    memory = config['Stanford']['memory']
    program = config['Stanford']['program']
    # checkout https://github.com/stanfordnlp/CoreNLP/issues/789
    # to see if they fixed how to use -resolve_coref true in the command
    command = f'java -{memory} -cp "{jars_dir}\\*" {program}\
        -threads 8\
        -ssplit.newlineIsSentenceBreak always\
        -triple.all_nominals true -format reverb "{temp_file_name}"\
        > "{output}"'
    print(command)
    print("Extracting triples with StanfordNLP...")
    code = os.system(command)
    os.remove(temp_file_name)
    if code == 0:
        # parsing results into dicts
        stanford_triples = text_file_to_list(output)
        stanford_triples = parse_triples_reverb_format(stanford_triples)
        stanford_remaining = text_file_to_list(source)
        stanford_remaining = parse_remaining_reverb_format(stanford_remaining, stanford_triples)

        # obtaining a mapping of each line in the output triples from
        # reverb format to the original source template idx
        # note reverb outputs original line ordinal as the id instead
        stanford_to_idx = [line.strip().split('\t')[0] for line in text_file_to_list(source)]

        triples_output = {}
        remaining_output = {}
        for i in range(len(stanford_to_idx)):
            actual_idx = stanford_to_idx[i]
            triples_output[actual_idx] = stanford_triples.get(str(i), [])
            remaining_output[actual_idx] = stanford_remaining.get(str(i), [])
        return triples_output, remaining_output
    else:
        print("Standford CoreNLP OpenIE FAILED")
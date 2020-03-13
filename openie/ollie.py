from .registry import register
import configparser
from ..oie_extraction.extraction import Extraction
import subprocess
import os
from .utils import text_file_to_list


def save_remaining(remaining, output_file):
    text_to_idx = {}
    with open(output_file, 'w') as remaining_f:
        for idx in remaining:
            remaining_idx = remaining[idx]
            remaining_idx = [line for line in remaining_idx]
            remaining_f.writelines('\n'.join((*remaining_idx,'')))
            
            for line in remaining_idx:
                text_to_idx[line] = idx
    return text_to_idx


def parse_triples(lines, text_to_idx):
    result = {}
    for line in lines:
        line = line.strip().split('\t')
        text = line[6]
        idx = text_to_idx[text]
        triple = (line[1:4])
        extraction = Extraction.fromTuple(
            triple,
            sentence=text,
            confidence=float(line[0])
            )
        if idx in result:
            result[idx].append(extraction)
        else:
            result[idx] = [extraction]
    return result


def get_remaining(input_remaining, ollie_triples):
    result = {}
    for idx in input_remaining:
        if idx not in ollie_triples:
            if idx in result:
                result[idx].append(input_remaining[idx])
            else:
                result[idx] = input_remaining[idx]
    return result


@register('ollie')
def extract_triples(input_remaining, output):
    output = os.path.abspath(output)
    # the java app uses a file as an input so the remaining input is
    # saved into a temporary file 
    temp_source = os.path.abspath('./temp_remaining.txt')
    text_to_idx = save_remaining(input_remaining, temp_source)
    # parsing config
    config = configparser.ConfigParser()    
    config_path = os.path.join(
        os.path.dirname(__file__),
        'openie.ini',
    )
    config.read(config_path)
    jar_dir = os.path.normpath(config['Ollie']['dir'])
    jar = os.path.join(
        jar_dir,
        config['Ollie']['jar'],
        )
    memory = config['Ollie']['memory']
    command = ["java",
        f"-{memory}",
        "-jar", f"{jar}",
        "--output-format", "tabbed",
        '-o', output,
        temp_source,
        ]
    print(command)
    cp = subprocess.run(command, cwd=jar_dir)
    os.remove(temp_source)

    if cp.returncode == 0:
        triples = {}
        remaining = {}
        # parsing results into dicts
        ollie_output = text_file_to_list(output)[1:] # removing header
        ollie_triples = parse_triples(ollie_output, text_to_idx)
        ollie_remaining = get_remaining(input_remaining, ollie_triples)
        
        return ollie_triples, ollie_remaining
    else:
        raise RuntimeError("Ollie FAILED")

from .evaluation import registry as eval_registry
from .openie import registry as openie_registry
from .rules import registry as rules_registry
from .preprocess import registry as preprocess_registry
from .utils import (
    file_handling,
    print_params,
)
from .init_params import init_main_args, parse_main_args
from .utils import combine_extractions, unstructure_extractions
from .output_generator import OutputGenerator


def init_args():
    """Init command line args used for configuration."""

    parser = init_main_args()
    return parser.parse_args()


def parse_args(args):
    """Parse provided args for runtime configuration."""
    params = parse_main_args(args)
    return params


def main():
    # Init params
    params = parse_args(init_args())
    print_params(params)
    file_handling(params)
    # Load data: templates and ground truth for evaluation
    preprocessor_getter = preprocess_registry.get_preprocessor(params['templates_type'])
    preprocessor = preprocessor_getter(params)
    processed_templates, ground_truth, raw_templates = preprocessor.process_templates()
    # Run rules triples extraction
    if 'rules' in params:
        rules_extractor = rules_registry.get_extractor(params['rules'])
        rule_triples, rule_remaining = rules_extractor(processed_templates)
        remaining = rule_remaining
    else:
        rule_triples = {}
        remaining = {idx:templates for idx, templates in processed_templates.items()}
    # Run openie triples extraction
    openie_extractor = openie_registry.get_extractor(params['openie'])
    oie_triples, oie_remaining = openie_extractor(remaining, './triples.txt')
    global_result = combine_extractions(oie_triples, rule_triples)
    # Producing desired output for logs input
    if 'raw_logs' in params:
        processed_logs = preprocessor.process_logs()
        output_generator = OutputGenerator(raw_templates)
        desired_output = output_generator.generate_output(processed_logs, global_result)
    for i, log in enumerate(desired_output, 1):
        print(log)
        if i == 100:
            break
    exit()
    # PropS uses a different structure so we change it
    if params['openie'] == 'props' or 'lexical' in params['evaluation']:
        unstructure_extractions(ground_truth)
        unstructure_extractions(global_result)
    # Run evaluation
    for eval_metric in params['evaluation']:
        run_metric = eval_registry.get_eval_metric(eval_metric)
        run_metric(global_result, ground_truth)


if __name__ == "__main__":
    main()

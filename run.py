from .evaluation import registry as eval_registry
from .openie import registry as openie_registry
from .rules import registry as rules_registry
from .preprocess import registry as preprocess_registry
from .utils import (
    file_handling,
    print_params,
)
from .init_params import init_main_args, parse_main_args
from .utils import combine_extractions


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
    preprocess_data = preprocess_registry.get_preprocessor(params['templates_type'])
    processed_templates, ground_truth = preprocess_data(params)
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
    # Run evaluation
    for eval_metric in params['evaluation']:
        run_metric = eval_registry.get_eval_metric(eval_metric)
        run_metric(global_result, ground_truth)


if __name__ == "__main__":
    main()

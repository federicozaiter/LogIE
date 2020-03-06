from .rules import registry as rules_registry
from .preprocess import registry as preprocess_registry
from .preprocess.utils import load_processed_templates
from .utils import (
    file_handling,
    print_params,
)
from .init_params import init_main_args, parse_main_args


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
    file_handling(params)  # TODO: handle the case when the experiment ID already exists - this I think is the only one that matters
    # Preprocess templates
    if 'templates' in params:
        preprocess = preprocess_registry.get_preprocessor(params['templates_type'])
        preprocess(params)
    # Load preprocessed templates from file
    templates = load_processed_templates(params)
    # Run rules triples extraction
    rules_extractor = rules_registry.get_rules_extractor(params['rules'])
    rule_extractions = rules_extractor(templates)
    print(rule_extractions)
    # Run openie triples extraction

    # Run evaluation


if __name__ == "__main__":
    main()

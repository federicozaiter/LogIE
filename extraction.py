from .openie import registry as openie_registry
from .rules import registry as rules_registry
from .rules.utils import save_remaining
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
    rules_extractor = rules_registry.get_extractor(params['rules'])
    rule_triples, rule_remaining = rules_extractor(templates)
    remaining_dir = save_remaining(rule_remaining, params['base_dir'])
    # Run openie triples extraction
    openie_extractor = openie_registry.get_extractor(params['openie'])
    oie_triples, oie_remaining = openie_extractor(remaining_dir, 'triples.txt')
    print(len(oie_triples))
    print(oie_triples)
    print(len(oie_remaining))
    print(oie_remaining)
    # Run evaluation


if __name__ == "__main__":
    main()

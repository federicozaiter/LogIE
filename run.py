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
    if 'raw_logs' in params:
        # Producing desired output for logs input
        output_generator = OutputGenerator(raw_templates)
        for eval_metric in params['evaluation']:
            get_evaluator = eval_registry.get_eval_metric(eval_metric)
            evaluator = get_evaluator(params)
            processed_logs = preprocessor.process_logs()
            for i, log in enumerate(processed_logs, 1):
                online_output = output_generator.generate_output(log, global_result, tag=False)
                gt_output =  output_generator.generate_output(log, ground_truth, tag=False)
                evaluator.single_eval(online_output, gt_output)
                # print((log, online_output, gt_output))
                if i == 100:
                    print(f'ONLY CONSIDERING {i} LOGS IN THE EVALUATION')
                    break
            eval_result = evaluator.metrics()
            print(', '.join(f'{key}: {value}' for key, value in eval_result.items()))
    else:
        # Run template based evaluation
        for eval_metric in params['evaluation']:
            get_evaluator = eval_registry.get_eval_metric(eval_metric)
            evaluator = get_evaluator(params)
            evaluator.eval(global_result, ground_truth)
            eval_result = evaluator.metrics()
            print(', '.join(f'{key}: {value}' for key, value in eval_result.items()))

if __name__ == "__main__":
    main()

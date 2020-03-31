import os
import argparse
from uuid import uuid4
import sys


def init_main_args():
    """Init command line args used for configuration."""

    parser = argparse.ArgumentParser(
        description="Runs information extraction from logs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--templates",
        metavar="templates",
        type=str,
        nargs=1,
        help="input raw templates file path",
    )
    base_dir_default = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "output"
    )
    parser.add_argument(
        "--base_dir",
        metavar="base_dir",
        type=str,
        nargs=1,
        default=[base_dir_default],
        help="base output directory for output files",
    )
    parser.add_argument(
        "--templates_type",
        metavar="templates_type",
        type=str,
        nargs=1,
        default=["original"],
        choices=[
            "original",
            "open_source",
            ],
        help="Input type of templates.",
    )
    parser.add_argument(
        "--rules",
        metavar="rules",
        type=str,
        nargs=1,
        choices=["team",],
        help="Predefined rules to extract triples from templates.",
    )
    evaluation_choices = ["he",
                 "redundancy",
                 "counts",
                 ],
    parser.add_argument(
        "--evaluation",
        metavar="evaluation",
        type=str,
        nargs='+',
        default=[],
        choices=evaluation_choices,
        help=f"Triples extraction evaluation metrics. Choose from {evaluation_choices}.",
    )
    openie_choices = ["stanford", "openie5", "ollie", "predpatt", "clausie"]
    parser.add_argument(
        "--openie",
        metavar="openie",
        type=str,
        nargs=1,
        default=["stanford"],
        choices=openie_choices,
        help=f"OpenIE approach to be used for triple extraction. Choose from {openie_choices}.",
    )
    parser.add_argument(
        "--id",
        metavar="id",
        type=str,
        nargs=1,
        help="Experiment id. Automatically generated if not specified.",
    )

    return parser


def parse_main_args(args):
    """Parse provided args for runtime configuration."""
    params = {
        "evaluation": args.evaluation,
        "base_dir": args.base_dir[0],
        "templates_type": args.templates_type[0],
        "openie": args.openie[0],
    }
    if args.rules:
        params["rules"] = args.rules[0]
    if args.templates:
        params["templates"] = os.path.normpath(args.templates[0])
    if args.id:
        params['id'] = args.id[0]
    else:
        params['id'] = str(uuid4().time_low)
    print(f"\nExperiment ID: {params['id']}")
    # Creating experiments results folder with the format
    # {experiment_module_name}_{templates_type}_{id}
    experiment_name = os.path.basename(sys.argv[0]).split('.')[0]
    params['id_dir'] = os.path.join(
            params['base_dir'],
            '_'.join((
                experiment_name, params['templates_type'], params['id']
                ))
        )
    params['results_dir'] = os.path.join(params['id_dir'], "results")

    return params

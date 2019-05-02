"""Module to record AWS Chalice resources"""
import argparse
import json
import os

import boto3
from botocore import xform_name


def record_as_env_var(stack_name, stage):
    """Function to gather record resources"""
    cloudformation = boto3.client("cloudformation")
    response = cloudformation.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]
    with open(os.path.join(".chalice", "config.json")) as conf_file:
        d = json.load(conf_file)
        d["stages"].setdefault(stage, {}).setdefault("environment_vars", {})
        for output in outputs:
            d["stages"][stage]["environment_vars"][
                _to_env_var_name(output["OutputKey"])
            ] = output["OutputValue"]
    with open(os.path.join(".chalice", "config.json"), "w") as conf_file:
        serialized = json.dumps(d, indent=2, separators=(",", ": "))
        conf_file.write(serialized + "\n")
        d["stages"].setdefault(stage, {})
        d["stages"].setdefault("environment_variables", {})
        for output in outputs:
            d["stages"][stage]["environment_variables"][
                _to_env_var_name(output["OutputKey"])
            ] = output["OutputValue"]
    with open(os.path.join(".chalice", "config.json"), "w") as conf_file:
        serialized = json.dumps(d, indent=2, separators=(",", ": "))
        conf_file.write(serialized + "\n")


def _to_env_var_name(name):
    """To get appropriate environment variable names."""
    return xform_name(name).upper()


def main():
    """Main function to execute environment variable recordings."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stage", default="dev")
    parser.add_argument("--stack-name", required=True)
    args = parser.parse_args()
    record_as_env_var(stack_name=args.stack_name, stage=args.stage)


if __name__ == "__main__":
    main()

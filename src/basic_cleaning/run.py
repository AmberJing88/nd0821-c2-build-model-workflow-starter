#!/usr/bin/env python
"""
long_description [An example of a step using MLflow and Weights & Biases]: Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="job_type [my_step]: basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Fetching artifact")
    artifact - run.use_artifact(args.input_artifact)
    local_path = artifact.file()
    
    logger.info("Reading dataframe")
    df = pd.read_csv(local_path)
    
    # Pre-processing
    logger.info("Starting pre-processing")
    df = df.drop_duplicate().reset_index(drop=True)
    
    # need to modify with new feature in project
    df["title"].fillna(value='', inplace=True)
    df['song_name'].fillna(value='', inplace=True)
    df['text_feature'] = df['title'] + " " + df["song_name"]
    
    outfile = args.artifact_name
    df.to_csv(outfile)
    artifact = wandb.Artifact(
        name=args.artifact_name, 
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(outfile)
    
    run.log_artifact(artifact)
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="short_description [My step]: This steps cleans the data")


    parser.add_argument(
        "--parameters [parameter1", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--parameter2]: parameter1", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--parameter2", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--parameter3", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)

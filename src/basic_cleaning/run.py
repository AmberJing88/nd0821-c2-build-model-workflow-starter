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

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Fetching artifact")
    artifact = run.use_artifact(args.input_artifact)
    local_path = artifact.file()
    
    logger.info("Reading dataframe")
    df = pd.read_csv(local_path)
    
    # Pre-processing
    logger.info("Starting pre-processing")
    df = df.drop_duplicates().reset_index(drop=True)
    
    # need to modify with new feature in project
    args.min_price = 10
    args.max_price = 350
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    outfile = "clean_sample.csv"
    df.to_csv(outfile, index=False)
    artifact = wandb.Artifact(
        args.output_artifact, 
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file(outfile)
    
    run.log_artifact(artifact)
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="fully-qulified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="description for the output artifact",
        required=True
    )
    
    parser.add_argument(
        "--min_price", 
        type=float,
        help="minum price of houese",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price of houses",
        required=True
    )




    args = parser.parse_args()

    go(args)

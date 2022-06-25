#!/usr/bin/env python
"""
This script get rid of price outlier and convert last_review to dattime object
"""
import argparse
import logging
import pandas as pd
import os
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    try:
        run = wandb.init(job_type="clean_data")
        logger.info("wandb start")

        artifact = run.use_artifact(args.input_artifact)
        filepath = artifact.file()
        df = pd.read_csv(filepath)
        logger.info('use artifact success!')
    except:
        logger.error('there is some problem to use artifact')
        
    # process data
    # remove price outlier
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    #save datafrme as a csv file
    df.to_csv('clean_sample.csv', index=False)
    # put process dato into wandb as artifact
    artifact_p = wandb.Artifact(name=args.artifact_name, 
                                        type=args.artifact_type,
                                        description= args.artifact_description)
    artifact_p.add_file('clean_sample.csv')
    
    run.log_artifact(artifact_p)
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price", type=float, help="Minimum accepted price for a day", required=True
    )

    parser.add_argument(
        "--max_price", type=float, help="Maximum accepted price for a day", required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact",
        default="clean data",
        required=False
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        default="artifact for cleaned dataset",
        required=False
    )

    args = parser.parse_args()
    print(args)

    go(args)

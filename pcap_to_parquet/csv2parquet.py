#!/home/user/miniconda3/envs/spark/bin/python
import re
from functools import reduce
from pathlib import Path
from datetime import datetime
import argparse
import pyspark.sql.functions as F
import ipaddress
from collections import defaultdict

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StringType, IntegerType, ShortType, DoubleType, LongType, BooleanType, ByteType



@F.udf()
def ip_str_to_int(ip_str):
    try:
        return int(ipaddress.ip_address(ip_str))
    except ValueError:
        return None


def get_key2pathdict(all_csv_paths):
    return_dict = defaultdict(list)
    for k, csv_path in enumerate(all_csv_paths):
        return_dict[k].append(str(csv_path))
    return return_dict


def transform_and_store(ctx, base_store_path, key2pathdict):
    for k, csv_paths in key2pathdict.items():
        all_dfs = []
        for csv_path in csv_paths:
            df = ctx.read.options(header='true', delimiter='\t').csv(str(csv_path))
            df = df.withColumn("sIP", ip_str_to_int(df["sIP"]).cast(LongType()))
            df = df.withColumn("dIP", ip_str_to_int(df["dIP"]).cast(LongType()))
            all_dfs.append(df)
        df = reduce(DataFrame.unionByName, all_dfs)
        store_path = base_store_path / f'{k}.parquet'
        df.write.parquet(str(store_path))
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--base-path', default='.', type=str, help='The path to CSV files (Default: current dir)')
    arg_parser.add_argument('--store-path', type=str, required=True, help='The path to store the parquet files')
    arg_parser.add_argument('--merge', action='store_true', default=False, help='Whether to merge the input CSV files into one parquet file')
    args = arg_parser.parse_args()
    base_path = Path(args.base_path)
    all_csv_paths = list(base_path.glob('*.csv'))
    if len(all_csv_paths) == 0:
        raise ValueError(f"No CSVs files found at: {base_path}")
    if args.merge:
        key2pathdict = {0: [str(csv_path) for csv_path in all_csv_paths]}
    else:
        key2pathdict = {k: [str(csv_path)] for k, csv_path in enumerate(all_csv_paths)}

    ctx = SparkSession \
        .builder \
        .config("spark.driver.memory", '100G') \
        .config("spark.ui.killEnabled", False) \
        .getOrCreate()
    ctx.sparkContext.setLogLevel('OFF')

    base_store_path = Path(args.store_path)
    base_store_path.mkdir(parents=True, exist_ok=True)
    transform_and_store(ctx, base_store_path, key2pathdict)
    return


if __name__ == '__main__':
    main()

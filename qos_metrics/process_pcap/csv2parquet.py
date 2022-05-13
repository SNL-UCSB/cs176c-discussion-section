import re
from functools import reduce
from pathlib import Path
from datetime import datetime
import argparse
import pyspark.sql.functions as F
import ipaddress

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StringType, IntegerType, ShortType, DoubleType, LongType, BooleanType, ByteType


@F.udf()
def hex_to_int(hex_str):
    try:
        return int(hex_str, 16)
    except TypeError:
        return None


@F.udf()
def ip_str_to_int(ip_str):
    try:
        return int(ipaddress.ip_address(ip_str))
    except ValueError:
        return None

def tcp_change_column_names_and_project(df):
    df = df.select('ts', 'sIP', 'tcp_sPort', 'dIP', 'tcp_dPort', 'ip_len',
                   'ip_hdr_len', 'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                   'tcp_hdr_len', 'tcp_rwnd', 'tls_hostname',
                   'dns_hostname', 'dns_ip')
    df = df.toDF('ts', 'sIP', 'sPort', 'dIP', 'dPort', 'ip_len',
                 'ip_hdr_len', 'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                 'tcp_hdr_len', 'tcp_rwnd', 'tls_hostname',
                 'dns_hostname', 'dns_ip')
    df = df.filter(df['ip_proto'] == '6')
    df = df.withColumn("tcp_flags", hex_to_int(df["tcp_flags"]).cast(ShortType()))
    return df


def udp_change_column_names_and_project(df):
    df = df.select('ts', 'sIP', 'udp_sPort', 'dIP', 'udp_dPort', 'ip_len',
                   'ip_hdr_len', 'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                   'tcp_hdr_len', 'tcp_rwnd', 'tls_hostname',
                   'dns_hostname', 'dns_ip')
    df = df.toDF('ts', 'sIP', 'sPort', 'dIP', 'dPort', 'ip_len',
                 'ip_hdr_len', 'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                 'tcp_hdr_len', 'tcp_rwnd', 'tls_hostname',
                 'dns_hostname', 'dns_ip')
    df = df.filter(df['ip_proto'] == '17')
    return df


def transform_and_store(ctx, base_store_path, key2pathdict):
    for k, csv_paths in key2pathdict.items():
        all_dfs = []
        for csv_path in csv_paths:
            for is_tcp in [True, False]:
                df = ctx.read.options(header='true', delimiter='\t').csv(str(csv_path))
                if is_tcp:
                    df = tcp_change_column_names_and_project(df)
                else:
                    df = udp_change_column_names_and_project(df)
                df = df.withColumn("ts", df["ts"].cast(DoubleType()))
                df = df.withColumn("sIP", df["sIP"].cast(StringType()))
                df = df.withColumn("sPort", df["sPort"].cast(IntegerType()))
                df = df.withColumn("dIP", df["dIP"].cast(StringType()))
                df = df.withColumn("dPort", df["dPort"].cast(IntegerType()))
                df = df.withColumn("ip_len", df["ip_len"].cast(IntegerType()))
                df = df.withColumn("ip_hdr_len", (df["ip_hdr_len"]).cast(ByteType()))
                df = df.withColumn("ip_proto", df["ip_proto"].cast(ShortType()))
                df = df.withColumn("tcp_flags", df["tcp_flags"].cast(ShortType()))
                df = df.withColumn("tcp_seq", df["tcp_seq"].cast(LongType()))
                df = df.withColumn("tcp_ack", df["tcp_ack"].cast(LongType()))
                df = df.withColumn("tcp_hdr_len", (df["tcp_hdr_len"]).cast(ByteType()))
                df = df.withColumn("tcp_rwnd", df["tcp_rwnd"].cast(IntegerType()))
                df = df.withColumn("tls_hostname", df["tls_hostname"].cast(StringType()))
                df = df.withColumn("dns_hostname", df["dns_hostname"].cast(StringType()))
                df = df.withColumn("dns_ip", df["dns_ip"].cast(StringType()))
                
                all_dfs.append(df)
        df = reduce(DataFrame.unionByName, all_dfs)
        store_path = base_store_path / f'{k}.parquet'
        df.write.parquet(str(store_path))
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--base-path', default='.', type=str, help='The path to CSV files (Default: current dir)')
    arg_parser.add_argument('--store-path', type=str, required=True, help='The path to store the parquet files')
    args = arg_parser.parse_args()
    base_path = Path(args.base_path)
    all_csv_paths = list(base_path.glob('*.csv'))
    if len(all_csv_paths) == 0:
        raise ValueError(f"No CSVs files found at: {base_path}")
    key2pathdict = {k: [str(csv_path)] for k, csv_path in enumerate(all_csv_paths)}
    
    ctx = SparkSession \
        .builder \
        .config("spark.driver.memory", '4G') \
        .config("spark.ui.killEnabled", False) \
        .getOrCreate()
    ctx.sparkContext.setLogLevel('OFF')

    base_store_path = Path(args.store_path)
    base_store_path.mkdir(parents=True, exist_ok=True)
    transform_and_store(ctx, base_store_path, key2pathdict)
    return


if __name__ == '__main__':
    main()

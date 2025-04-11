import pandas as pd
from functools import reduce
from pathlib import Path
import argparse


def hex_to_int(hex_str):
    try:
        return int(hex_str, 16)
    except (TypeError, ValueError):
        return None


def ip_str_to_int(ip_str):
    try:
        return int(ipaddress.ip_address(ip_str))
    except ValueError:
        return None


def tcp_change_column_names_and_project(df):
    df = df[['ts', 'sIP', 'tcp_sPort', 'dIP', 'tcp_dPort', 'ip_len',
             'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
             'tls_hostname', 'dns_hostname', 'dns_ip']]
    df.columns = ['ts', 'sIP', 'sPort', 'dIP', 'dPort', 'ip_len',
                  'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                  'tls_hostname', 'dns_hostname', 'dns_ip']
    df = df[df['ip_proto'] == '6']
    df['tcp_flags'] = df['tcp_flags'].apply(hex_to_int).astype('Int16')
    return df


def udp_change_column_names_and_project(df):
    df = df[['ts', 'sIP', 'udp_sPort', 'dIP', 'udp_dPort', 'ip_len',
             'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
             'tls_hostname', 'dns_hostname', 'dns_ip']]
    df.columns = ['ts', 'sIP', 'sPort', 'dIP', 'dPort', 'ip_len',
                  'ip_proto', 'tcp_flags', 'tcp_seq', 'tcp_ack',
                  'tls_hostname', 'dns_hostname', 'dns_ip']
    df = df[df['ip_proto'] == '17']
    return df


def transform_and_store(base_store_path, output_filename, key2pathdict):
    all_dfs = []
    for csv_paths in key2pathdict.values():
        for csv_path in csv_paths:
            for is_tcp in [True, False]:
                df = pd.read_csv(csv_path, delimiter='\t')
                if is_tcp:
                    df = tcp_change_column_names_and_project(df)
                else:
                    df = udp_change_column_names_and_project(df)

                # Type conversion
                df['ts'] = df['ts'].astype(float)
                df['sIP'] = df['sIP'].astype(str)
                df['sPort'] = df['sPort'].astype('Int32')
                df['dIP'] = df['dIP'].astype(str)
                df['dPort'] = df['dPort'].astype('Int32')
                df['ip_len'] = df['ip_len'].astype('Int32')
                df['ip_proto'] = df['ip_proto'].astype('Int16')
                df['tcp_flags'] = df['tcp_flags'].astype('Int16')
                df['tcp_seq'] = df['tcp_seq'].astype('Int64')
                df['tcp_ack'] = df['tcp_ack'].astype('Int64')
                df['tls_hostname'] = df['tls_hostname'].astype(str)
                df['dns_hostname'] = df['dns_hostname'].astype(str)
                df['dns_ip'] = df['dns_ip'].astype(str)

                all_dfs.append(df)

    # Combine all dataframes using pd.concat
    df_combined = pd.concat(all_dfs, ignore_index=True)
    store_path = base_store_path / f'{output_filename}.csv'
    df_combined.to_csv(store_path, index=False,sep='\t')
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--base-path', default='.', type=str, help='The path to CSV files (Default: current dir)')
    arg_parser.add_argument('--store-path', type=str, required=True, help='The path to store the CSV files')
    arg_parser.add_argument('--output-filename', type=str, required=True, help='The name of the output CSV file')
    args = arg_parser.parse_args()

    base_path = Path(args.base_path)
    all_csv_paths = list(base_path.glob('*.csv'))
    if len(all_csv_paths) == 0:
        raise ValueError(f"No CSV files found at: {base_path}")
    key2pathdict = {k: [str(csv_path)] for k, csv_path in enumerate(all_csv_paths)}

    base_store_path = Path(args.store_path)
    base_store_path.mkdir(parents=True, exist_ok=True)

    transform_and_store(base_store_path, args.output_filename, key2pathdict)
    return


if __name__ == '__main__':
    main()

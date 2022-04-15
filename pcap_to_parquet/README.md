## Setup

### Setting up the conda environment
```bash
$ conda create -n spark
$ conda activate spark && conda install -y pyspark
```

### Converting PCAP to Parquet
```bash
$ ./split_pcaps.sh . data/split-pcaps 20 5
$ ./pcap2csv.sh data/split-pcaps data/csvs 5
$ conda activate spark
$ python csv2parquet.py --base-path data/csvs --store-path data/parquets --merge
```

## Acknowledgement
The `HTTP.pcap` file was taken from [packetlife.net][1]. The packet capture represents the download of a PNG image using the `wget` client. The download link for the file is: https://packetlife.net/media/captures/HTTP.cap

[1]: https://packetlife.net/captures/protocol/tcp/

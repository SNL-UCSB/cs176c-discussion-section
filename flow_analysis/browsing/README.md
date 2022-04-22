## Setup
1. Install Java (dependency for spark). [[LINK][1]]
2. Install parallel
   a. Linux: `sudo apt update && sudo apt install parallel`
   b. Mac: `brew install parallel`
3. Create the conda environment for this section.
```bash
$ conda create -n spark
$ conda activate spark && conda install -y pyspark
```

## Converting PCAP to Parquet
```bash
$ cd browsing
$ process_pcap/pcap2csv.sh . data/ 1
$ python process_pcap/csv2parquet.py --base-path data --store-path data
```

[1]: https://java.com/en/download/manual.jsp

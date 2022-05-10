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
4. Update `set_env.sh` script with your path to the python interpreter
```bash
$ conda activate spark
$ which python
# copy output of the above command and replace <PATH_TO_PYTHON_INTERPRETER>
# with the output in set_env.sh
```

## Converting PCAP to Parquet
```bash
$ conda activate spark
$ process_pcap/pcap2csv.sh . data/ 1
$ python process_pcap/csv2parquet.py --base-path data --store-path data
```

## Running notebook
```bash
$ conda activate spark
$ source set_env.sh
$ jupyter notebook
```

[1]: https://java.com/en/download/manual.jsp

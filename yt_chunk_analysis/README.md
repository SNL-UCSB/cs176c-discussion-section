## Setup
1. Install Java (dependency for spark). [[LINK][1]]
2. Install Miniconda [[LINK][2]]. Windows users would want to open the 'Anaconda Prompt (miniconda3)' from the start menu, to run the commands written below.
4. Create the conda environment for this section.
```bash
$ conda create -n spark
$ conda activate spark && conda install -y pyspark
$ conda install -y jupyter matplotlib numpy
```
5. [Windows Only] Install `m2-base` in your conda environment to be able to run bash commands in the 'Anaconda Prompt'
```bash
$ conda activate && conda install -y m2-base
$ conda activate spark && conda install -y m2-base
```
7.  Install parallel
   a. Linux: `sudo apt update && sudo apt install parallel`
   b. Mac: `brew install parallel`
   c. Windows: Use the script `process_pcap/pcap2csv_serial.sh` instead of `process_pcap/pcap2csv.sh` below. You don't have to install parallel
7. Update `set_env.sh` script with your path to the python interpreter
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
[2]: https://docs.conda.io/en/latest/miniconda.html

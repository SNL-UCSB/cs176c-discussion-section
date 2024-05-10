## Setup
1. Install Java (dependency for spark). [[LINK][1]] (Shortcut for MacOS:  "brew install java", subsequently use this command, "sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk")
2. Install Miniconda [[LINK][2]]. Windows users would want to open the 'Anaconda Prompt (miniconda3)' from the start menu, to run the commands written below. (if you already have a python virtual environment you can use the command, "pip3 install pyspark")
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

8. Download the yt.pcap from the link below and put it in the main directory in yt_chunk_analysis : https://drive.google.com/file/d/11D8yqprLbwHhfmWBS1nZL8wryvMcqVWS/view?usp=sharing

```

## Converting PCAP to CSV (you don't need to use parquet for this discussion section)
```bash
$ conda activate spark
$ process_pcap/pcap2csv.sh . data/ 1
$ python process_pcap/csvprocess.py --base-path data --store-path data --output-filename transform_data
```

## Running notebook
```bash
$ conda activate spark
$ source set_env.sh
$ jupyter notebook
```

## FAQs
1. I get a `tshark: command not found` even though I already have Wireshark installed

   You may have to create a symbolic link to the `tshark` executable as explained in this [SO post][3]. Alternatively, you can add the Wireshark directory to your PATH env variable like follows:
   ```bash
   $ export PATH=C:\Program Files\Wireshark:$PATH
   ```
   Note that you would have to execute the command above each time you open a new shell. Or, you can put it in your `.bashrc` file

[1]: https://java.com/en/download/manual.jsp
[2]: https://docs.conda.io/en/latest/miniconda.html
[3]: https://stackoverflow.com/a/63054234/7263373

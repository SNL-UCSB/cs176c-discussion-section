#!/bin/bash
if [ $# -ne 3 ]
then
    echo "Usage: $0 input_directory output_directory num_cores"
    exit 1
fi
export IN_DIR=$1
export OUT_DIR=$2
export NUM_CORES=$3
mkdir -p $OUT_DIR
ls $IN_DIR/*.pcap | parallel -j $NUM_CORES 'echo "sIP	dIP" > $OUT_DIR/$(basename {}).csv && tshark -r {} -Y "tcp" -T fields -E separator=/t -e ip.src -e ip.dst >> $OUT_DIR/$(basename {}).csv'

#!/bin/bash
if [ $# -ne 4 ]
then
    echo "Usage: $0 input_directory output_directory packets_per_file num_cores"
    exit 1
fi
export IN_DIR=$1
export OUT_DIR=$2
export PACKETS_PER_FILE=$3
export NUM_CORES=$4
mkdir -p $OUT_DIR
ls $IN_DIR/*.pcap | parallel -j $NUM_CORES 'editcap -c $PACKETS_PER_FILE {} $OUT_DIR/$(basename {})'

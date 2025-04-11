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
for pcap_file in $(ls $IN_DIR/*.pcap)
do
    echo "ts	sIP	tcp_sPort	udp_sPort	dIP	tcp_dPort	udp_dPort	ip_len	ip_proto	tcp_flags	tcp_seq	tcp_ack	tls_hostname	dns_hostname	dns_ip" > $OUT_DIR/$(basename $pcap_file .pcap).csv && tshark -r $pcap_file -T fields -E separator=/t -e frame.time_epoch -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport -e ip.len -e ip.proto -e tcp.flags -e tcp.seq_raw -e tcp.ack_raw -e tls.handshake.extensions_server_name -e dns.resp.name -e dns.a >> $OUT_DIR/$(basename $pcap_file .pcap).csv
done

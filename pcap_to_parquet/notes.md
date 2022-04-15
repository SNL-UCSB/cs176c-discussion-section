# Converting pcap to a readily analyzable format

![](https://i.imgur.com/AckQSED.png)

## Why?
* With Wireshark, we can analyze packets with filter expressions and dissection
* However, we can not perform more complex analysis that requires join or aggregation

## Converting PCAP to CSV
### tshark
* [tshark][1] is a popular protocol analyzer
* You can use it like Wireshark to apply filter to PCAP and display selected packets
* Similarly, you can also capture packets on a particular interface
* Finally, you can also use it to read a PCAP, apply a filter and write the corresponding packet as a row in a CSV file

```bash
tshark -r file.pcap -Y "tcp" -T fields -E separator=/t -e ip.src -e ip.dst >> file.csv
```

## Why do we need to split PCAP before conversion?
* Converting a PCAP to a CSV is very slow.
* However, it is an [embarrasingly parallel][2] process. But, tshark uses only a single core to process the pcap once it has been read. We can speed up this computation by using parallel processes running on separate cores.
* While processing a file, tshark takes up a lot of RAM and the RAM usage increases monotonically until the file has been processed. If the file is too large, the kernel kills the conversion because of an out of memory (OOM) error

## Splitting PCAP
### editcap
[editcap][3] is used for editing packet captures by truncating the packets, removing duplicates, etc. It can also be used to partition a PCAP file into multiple PCAP files based on the packet count or the duration of the capture.

```
editcap -c $PACKETS_PER_FILE file.pcap $OUTPUT_FILE_PREFIX
```

## Converting PCAP to CSV in parallel
We can use [GNU parallel][4] to spawn multiple processes each of which converts a pcap file to a CSV. `{}` denotes the input to the parallel command.

```
ls *.pcap | parallel -j $NUM_CORES 'tshark -r {} -Y "tcp" -T fields -E separator=/t -e ip.src -e ip.dst >> ((basename {}).csv)'
```

## Why Parquet?
[Apache Spark][5] is an open-source analytics engine for large-scale data processing. [Apache Parquet] is an efficient columnar data storage format designed to work well with Spark. It has the following benefits over CSVs:
* Since it's column oriented data-store, a query that requires a few columns would be able to read only the required subset of the data.
* Parquet is a compressed format, so you can store vast amounts of data on the disk.

## Converting CSV to Parquet
[PySpark][7] can be used to convert CSV files to parquet. The idea is to create a Spark dataframe by reading a CSV from the disk and then dumping the dataframe as a Parquet file.

[1]: https://www.wireshark.org/docs/man-pages/tshark.html
[2]: https://en.wikipedia.org/wiki/Embarrassingly_parallel
[3]: https://www.wireshark.org/docs/man-pages/editcap.html
[4]: https://www.gnu.org/software/parallel/
[5]: https://spark.apache.org/
[6]: https://parquet.apache.org/
[7]: https://spark.apache.org/docs/latest/api/python/
[8]: https://packetlife.net/media/captures/HTTP.cap

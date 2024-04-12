# Wireshark Introduction
Wireshark
* Open a pcap
    * Drag and drop a pcap or open from the file menu
* How to dissect a packet?
    * Click on a row and you can see the raw packet bits in the bottom-most pane
    * In the middle-pane, you can see the headers and their values organized by different layers in the packet. 
* How to compose filters?
    * We can construct flexible filters in wireshark using different headers
    * Examples of some filters:
        * "udp"
            * The filter above shows packets with a UDP header
        * "tcp.dstport == 80"
            * Filter out the outbound HTTP traffic 
        * "tcp.dstport == 80 and tcp.srcport == 4343"
            * Filter out the outbound HTTP traffic originating at port 4343
    * To construct filter with header fields, we need their wireshark names. The list of all protocols and their fields can be found at [this link][1]
    * You can also know the field name by opening up a packet, and clicking the header field in that packet. The field name will be visible in the bottom-left corner

802.11
* 802.11 Addressing
* Types of 802.11 frames (check out page 18 on [this tutorial][2])
* Management Frames
    * Beacon frames
        * AP sends them out periodically
    * Probe request/response
        * The client uses probe frames to scan the area for availability of APs
    * Association request/response, Auth, Deauth, Disassociation (check out this [link][3])

[1]: https://www.wireshark.org/docs/dfref/
[2]: http://www.sss-mag.com/pdf/802_11tut.pdf
[3]: https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/802.11_Association_Process_Explained

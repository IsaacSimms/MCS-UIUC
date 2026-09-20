## FastTrack
- Hybrid of Gnutella and Napster architectures
- "healthier" participants in the system are leveraged
- Tech under the hood: Kazaa, KazaaLite, Grokster
- proprietary
- Overlay graph with supernodes. 
    Supernodes store directory listings(contains file names, peer pointers).
    Any peer can become a supernode as long as it acquires enough *reputation*.
    more reputation by length of connection and number of uploads.
    peer searches overlay by contacting supernode.

## BitTorrent
- another overlay graph style P2P system
- This system produces incentives peers to contribute
    uses a tracker (one tracker per file or multiple files).
    When new peer joins the system, it finds torrents (trackers) by receiving heartbeats. 
- Files are split into blocks
    When a peer joins the group it begins to download blocks. Uses a "local rarest first" policy
- Tit for tat bandwidth usage. Peers provide blocks to neighbors that provide the best upload rates
- Chocking: limiting number of neighbors with concurrent uploads


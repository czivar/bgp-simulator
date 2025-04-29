# bgp-simulator
BGP Simulator with Dijkstra's Algorithm

## Overview

This simulator models a simplified Border Gateway Protocol (BGP) network using Dijkstra's algorithm to calculate the shortest paths between Autonomous Systems (AS). Each AS is represented as a node in the graph, and the edges represent the connections between AS with their respective weights (latencies).

## Explanation
We define an AutonomousSystem class to represent each AS, with attributes for its ASN, name, and peers.
The BGP class manages the AS graph and implements Dijkstra's algorithm to calculate the shortest paths.
The shortest_path method returns the shortest path and its distance between two given AS.
The print_routing_table method displays the routing table for a given AS, showing the shortest paths to all other AS.

## Run it and Output

To run this code:
```
python3 simulator.py
```

Will print something like:

```
Code
Shortest path from AS100 to AS400: ['ISP-A', 'ISP-B', 'ISP-C', 'ISP-D']
Distance: 35
Routing table for ISP-A (AS100):
  - ISP-B (AS200): ['ISP-A', 'ISP-B'] with latency 10
  - ISP-C (AS300): ['ISP-A', 'ISP-B', 'ISP-C'] with latency 15
  - ISP-D (AS400): ['ISP-A', 'ISP-B', 'ISP-C', 'ISP-D'] with latency 35
```

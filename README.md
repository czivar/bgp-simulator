# BGP simulator with MED
BGP Simulator with Dijkstra's Algorithm (with MED)

## Overview

This simulator models a simplified Border Gateway Protocol (BGP) network using Dijkstra's algorithm to calculate the shortest paths between Autonomous Systems (AS). Each AS is represented as a node in the graph, and the edges represent the connections between AS with their respective weights (latencies). In BGP, the MED attribute is used to indicate the preference of one exit point over another when there are multiple exit points to the same neighboring AS. Here's an updated version of the BGP simulator that models MED.

## Explanation
The code models a BGP network with Autonomous Systems (AS) and their peering relationships.
Each AS can advertise prefixes with MED values, and the best path to a prefix is selected based on the MED value.
The shortest_path method uses Dijkstra's algorithm to calculate the shortest path between two AS.
The best_path method selects the best path to a prefix based on MED values.
The print_routing_table method displays the routing table for a given AS.

## Run it and Output

To run this code:
```
python3 simulator.py
```

Will print something like:

```
Routing table for ISP-A (AS100):
Routing table for ISP-B (AS200):
  - 10.0.0.0/8: ['ISP-B', 'ISP-C'] with MED 5
Routing table for ISP-C (AS300):
  - 10.0.0.0/8: ['ISP-C', 'ISP-B'] with MED 10
```

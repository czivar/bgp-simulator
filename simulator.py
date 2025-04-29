import heapq

# Represents an Autonomous System (AS) in the BGP network
class AutonomousSystem:
    def __init__(self, asn, name):
        # ASN: Autonomous System Number, a unique identifier for the AS
        self.asn = asn
        # Name: a human-readable name for the AS
        self.name = name
        # Peers: a dictionary of neighboring AS with their corresponding latency
        self.peers = {}
        # Prefixes: a dictionary of prefixes advertised by this AS with their MED values
        self.prefixes = {}

    # Adds a peer to this AS with the specified latency
    def add_peer(self, asn, latency):
        self.peers[asn] = latency

    # Advertises a prefix with the specified MED value
    def advertise_prefix(self, prefix, med):
        self.prefixes[prefix] = med

# Represents the BGP network
class BGP:
    def __init__(self):
        # Autonomous systems in the network, keyed by ASN
        self.autonomous_systems = {}

    # Adds an Autonomous System to the network
    def add_autonomous_system(self, asn, name):
        self.autonomous_systems[asn] = AutonomousSystem(asn, name)

    # Establishes a peering relationship between two AS with the specified latency
    def add_peering(self, asn1, asn2, latency):
        if asn1 in self.autonomous_systems and asn2 in self.autonomous_systems:
            self.autonomous_systems[asn1].add_peer(asn2, latency)
            self.autonomous_systems[asn2].add_peer(asn1, latency)

    # Advertises a prefix with the specified MED value from the given AS
    def advertise_prefix(self, asn, prefix, med):
        if asn in self.autonomous_systems:
            self.autonomous_systems[asn].advertise_prefix(prefix, med)

    # Calculates the shortest path between two AS using Dijkstra's algorithm
    def shortest_path(self, start_asn, end_asn):
        # Initialize distances and previous nodes for all AS
        distances = {asn: float('infinity') for asn in self.autonomous_systems.keys()}
        distances[start_asn] = 0
        previous = {asn: None for asn in self.autonomous_systems.keys()}
        priority_queue = [(0, start_asn)]

        while priority_queue:
            # Extract the AS with the minimum distance from the priority queue
            current_distance, current_asn = heapq.heappop(priority_queue)

            # If the destination AS is reached, construct the path
            if current_asn == end_asn:
                path = []
                while current_asn is not None:
                    path.append(self.autonomous_systems[current_asn].name)
                    current_asn = previous[current_asn]
                path.reverse()
                return path, current_distance

            # Skip if the current distance is greater than the known distance
            if current_distance > distances[current_asn]:
                continue

            # Iterate over all peers of the current AS
            for neighbor_asn, weight in self.autonomous_systems[current_asn].peers.items():
                distance = current_distance + weight

                # Update the distance and previous node if a shorter path is found
                if distance < distances[neighbor_asn]:
                    distances[neighbor_asn] = distance
                    previous[neighbor_asn] = current_asn
                    heapq.heappush(priority_queue, (distance, neighbor_asn))

        # Return None if no path is found
        return None, None

    # Selects the best path to a prefix based on MED values
    def best_path(self, asn, prefix):
        best_path = None
        best_med = float('infinity')

        # Iterate over all peers of the given AS
        for peer_asn, latency in self.autonomous_systems[asn].peers.items():
            # Check if the peer AS advertises the prefix
            if prefix in self.autonomous_systems[peer_asn].prefixes:
                med = self.autonomous_systems[peer_asn].prefixes[prefix]
                path, distance = self.shortest_path(asn, peer_asn)
                # Update the best path if a lower MED value is found
                if med < best_med:
                    best_med = med
                    best_path = path

        return best_path, best_med

    # Prints the routing table for the given AS
    def print_routing_table(self, asn):
        print(f"Routing table for {self.autonomous_systems[asn].name} (AS{asn}):")
        for prefix in self.autonomous_systems[asn].prefixes:
            best_path, best_med = self.best_path(asn, prefix)
            print(f"  - {prefix}: {best_path} with MED {best_med}")

# Example usage
bgp = BGP()
bgp.add_autonomous_system(100, "ISP-A")
bgp.add_autonomous_system(200, "ISP-B")
bgp.add_autonomous_system(300, "ISP-C")

bgp.add_peering(100, 200, 10)
bgp.add_peering(100, 300, 20)
bgp.add_peering(200, 300, 5)

bgp.advertise_prefix(200, '10.0.0.0/8', 10)
bgp.advertise_prefix(300, '10.0.0.0/8', 5)

for asn in bgp.autonomous_systems:
    bgp.print_routing_table(asn)

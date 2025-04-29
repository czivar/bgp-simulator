import heapq

class AutonomousSystem:
    def __init__(self, asn, name):
        self.asn = asn
        self.name = name
        self.peers = {}

    def add_peer(self, asn, latency):
        self.peers[asn] = latency

class BGP:
    def __init__(self):
        self.autonomous_systems = {}

    def add_autonomous_system(self, asn, name):
        self.autonomous_systems[asn] = AutonomousSystem(asn, name)

    def add_peering(self, asn1, asn2, latency):
        if asn1 in self.autonomous_systems and asn2 in self.autonomous_systems:
            self.autonomous_systems[asn1].add_peer(asn2, latency)
            self.autonomous_systems[asn2].add_peer(asn1, latency)

    def shortest_path(self, start_asn, end_asn):
        distances = {asn: float('infinity') for asn in self.autonomous_systems.keys()}
        distances[start_asn] = 0
        previous = {asn: None for asn in self.autonomous_systems.keys()}
        priority_queue = [(0, start_asn)]

        while priority_queue:
            current_distance, current_asn = heapq.heappop(priority_queue)

            if current_asn == end_asn:
                path = []
                while current_asn is not None:
                    path.append(self.autonomous_systems[current_asn].name)
                    current_asn = previous[current_asn]
                path.reverse()
                return path, current_distance

            if current_distance > distances[current_asn]:
                continue

            for neighbor_asn, weight in self.autonomous_systems[current_asn].peers.items():
                distance = current_distance + weight

                if distance < distances[neighbor_asn]:
                    distances[neighbor_asn] = distance
                    previous[neighbor_asn] = current_asn
                    heapq.heappush(priority_queue, (distance, neighbor_asn))

        return None, None

    def print_routing_table(self, asn):
        print(f"Routing table for {self.autonomous_systems[asn].name} (AS{asn}):")
        for peer_asn in self.autonomous_systems.keys():
            if peer_asn != asn:
                path, distance = self.shortest_path(asn, peer_asn)
                print(f"  - {self.autonomous_systems[peer_asn].name} (AS{peer_asn}): {path} with latency {distance}")

# Example usage
bgp = BGP()
bgp.add_autonomous_system(100, "ISP-A")
bgp.add_autonomous_system(200, "ISP-B")
bgp.add_autonomous_system(300, "ISP-C")
bgp.add_autonomous_system(400, "ISP-D")

bgp.add_peering(100, 200, 10)
bgp.add_peering(100, 300, 20)
bgp.add_peering(200, 300, 5)
bgp.add_peering(200, 400, 15)
bgp.add_peering(300, 400, 10)

start_asn = 100
end_asn = 400

path, distance = bgp.shortest_path(start_asn, end_asn)
print(f"Shortest path from AS{start_asn} to AS{end_asn}: {path}")
print(f"Distance: {distance}")

bgp.print_routing_table(100)

import networkx as nx
import matplotlib.pyplot as plt
import csv

from switch import *

topology_file = 'C://Users//Rares//Desktop//Network Embededd Systems//Project//dtu-teaching//tsn-test-cases//simulation_output//topology.csv'
streams_file = 'C://Users//Rares//Desktop//Network Embededd Systems//Project//dtu-teaching//tsn-test-cases//simulation_output//streams.csv'

all_switches = []

def create_graph_from_csv(file_path):
    # Initialize a graph
    G = nx.Graph()

    # Open and read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by commas
            parts = line.strip().split(',')
            
            # Process nodes (SW and ES devices)
            if parts[0] == 'ES':
                device_type = parts[0]
                device_name = parts[1]
                ports = parts[2] if len(parts) > 2 else None
                domain = parts[3] if len(parts) > 3 else None
                
                # Add node to the graph with attributes
                G.add_node(device_name, DeviceType=device_type, Ports=ports, Domain=domain)
            

            if parts[0] == 'SW':
                device_type = parts[0]
                device_name = parts[1]
                ports = parts[2]
                domain = parts[3] if len(parts) > 3 else None
            
                switch = Switch(device_name, ports)

                G.add_node(switch)
                all_switches.append(switch)

            # Process links (LINK entries)
            elif parts[0] == 'LINK':
                link_id = parts[1]
                source_device = parts[2]
                source_port = parts[3]
                destination_device = parts[4]
                destination_port = parts[5]
                domain = parts[6] if len(parts) > 6 else None

                # Add edge between specified nodes with a label (link ID)
                if source_device.startswith('SW') and destination_device.startswith('ES'):
                    G.add_edge(Switch(source_device,source_port), destination_device, label=link_id, SourcePort=source_port, DestinationPort=destination_port, Domain=domain)
                if source_device.startswith('ES') and destination_device.startswith('SW'):
                    G.add_edge(source_device, Switch(destination_device, destination_port), label=link_id, SourcePort=source_port, DestinationPort=destination_port, Domain=domain)
                if source_device.startswith('SW') and destination_device.startswith('SW'):
                    G.add_edge(Switch(source_device, source_port), Switch(destination_device, destination_port), label=link_id, SourcePort=source_port, DestinationPort=destination_port, Domain=domain)

   # Draw the graph
   #
   #  plt.figure(figsize=(10, 8))
   #  pos = nx.spring_layout(G)  # Layout for better visualization
   #  nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=500, font_size=10)
   #  edge_labels = nx.get_edge_attributes(G, 'label')
   #  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
   #  plt.show()
   #
   #
    return G

# This function assumes that the graph is already created
def find_shortest_paths_for_streams(graph, streams_file_path):
    
    stream_paths = {};  # Dictionary to store the paths for each stream
    # Open the streams CSV file
    with open(streams_file_path, 'r') as file:
       for line in file:
        
        row = line.strip().split(',')
        # For each stream, find the shortest path and print it

        pcp = row[0]
        stream_name = row[1]
        stream_type = row[2]
        source_node = row[3]
        destination_node = row[4]
        size = row[5]
        period = row[6]
        deadline = row[7]

        try:
            # Find the shortest path between source and destination
            path = nx.shortest_path(graph, source=source_node, target=destination_node)
            # Store the stream and the corresponding shortest path in the dictionary
            stream_paths[stream_name] = path
            
        except nx.NetworkXNoPath:
            # If no path is found, store None or a message indicating no path found
            stream_paths[stream_name] = None

    return stream_paths

def get_streams_by_name(streams_file_path, name):
        with open(streams_file_path, 'r') as file:
            for line in file:
                
                row = line.strip().split(',')
                # For each stream, find the shortest path and print it

                pcp = row[0]
                stream_name = row[1]
                stream_type = row[2]
                source_node = row[3]
                destination_node = row[4]
                size = row[5]
                period = row[6]
                deadline = row[7]

                if name == stream_name:
                    return row

            return ''



# 1. First create the graph from topology CSV file
G = create_graph_from_csv(topology_file)  # Load network graph

# 2. function call to find paths for each stream
paths = find_shortest_paths_for_streams(G, streams_file)

for path in paths:
    for node in paths[path]:
        if type(node) is Switch:

            all_switches[all_switches.index(node)].add_frame(get_streams_by_name(streams_file, path), prev_node)

            node.add_frame(get_streams_by_name(streams_file, path), prev_node)
        prev_node=node

sums = []
f=open("output.csv",'w')

for path in paths:
    current_sums = 0
    current_path = ""
    for node in paths[path]:
        if type(node) is Switch:
            
            current_sums += all_switches[all_switches.index(node)].calculate_delay(get_streams_by_name(streams_file, path),prev_node)
            current_path += all_switches[all_switches.index(node)].id
        else:
            current_path += node
        current_path += "->"
        prev_node=node

    sums.append(current_sums)
    line = path + ', ' + str(current_sums) + ', ' + get_streams_by_name(streams_file, path)[7] + ", " + current_path[:-2] + "\n"
    f.write(line)

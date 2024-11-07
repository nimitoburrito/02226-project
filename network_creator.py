import networkx as nx
import matplotlib.pyplot as plt
import csv

def create_graph_from_csv(file_path):
    # Initialize a graph
    G = nx.Graph()

    # Open and read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by commas
            parts = line.strip().split(',')
            
            # Process nodes (SW and ES devices)
            if parts[0] in ['SW', 'ES']:
                device_type = parts[0]
                device_name = parts[1]
                ports = parts[2] if len(parts) > 2 else None
                domain = parts[3] if len(parts) > 3 else None
                
                # Add node to the graph with attributes
                G.add_node(device_name, DeviceType=device_type, Ports=ports, Domain=domain)
            
            # Process links (LINK entries)
            elif parts[0] == 'LINK':
                link_id = parts[1]
                source_device = parts[2]
                source_port = parts[3]
                destination_device = parts[4]
                destination_port = parts[5]
                domain = parts[6] if len(parts) > 6 else None
                
                # Add edge between specified nodes with a label (link ID)
                G.add_edge(source_device, destination_device, label=link_id, SourcePort=source_port, DestinationPort=destination_port, Domain=domain)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # Layout for better visualization
    nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.show()

    return G

# Example usage: call the function with your CSV file
# create_graph_from_csv('example_topology.csv')
#create_graph_from_csv('small-topology.csv')

# This function assumes that the graph is already created
def find_shortest_paths_for_streams(graph, streams_file_path):
    
    stream_paths = {};  # Dictionary to store the paths for each stream
    # Open the streams CSV file
    with open(streams_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        
        
        # For each stream, find the shortest path and print it
        for row in csv_reader:
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
                #print(f"Path for stream {stream_name}: {' -> '.join(path)}")
            except nx.NetworkXNoPath:
                # If no path is found, store None or a message indicating no path found
                stream_paths[stream_name] = None
                print(f"No path found for stream {stream_name} from {source_node} to {destination_node}")

    print(f"Stream Paths Dictionary: {stream_paths}")
    return stream_paths

# Example usage:
# 1. First create the graph from your topology CSV file
G = create_graph_from_csv('small-topology.csv')  # Load your network graph

# 2. Then, call the function to find paths for each stream
find_shortest_paths_for_streams(G, 'small-streams.csv')  # Replace 'streams.csv' with your streams file path
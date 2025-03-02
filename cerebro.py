import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def process_eeg(file_path):
    
    chunk_size = 2500
    chunks = []
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk)
    
    df = pd.concat(chunks, ignore_index=True)
    
    df.columns = df.columns.astype(str)
    

    mean_values = df.iloc[:, 1:].mean()
    mean_values.index = mean_values.index.astype(int)  
    
    top_channels = mean_values.nlargest(20).index.tolist()
    
    electrode_positions = {
        1: (-1, 3), 2: (0, 3), 3: (1, 3), 4: (-1.5, 2), 5: (-0.5, 2), 6: (0.5, 2), 7: (1.5, 2),
        8: (-2, 1), 9: (-1, 1), 10: (0, 1), 11: (1, 1), 12: (2, 1), 13: (-2, 0), 14: (-1, 0),
        15: (0, 0), 16: (1, 0), 17: (2, 0), 18: (-2, -1), 19: (-1, -1), 20: (0, -1), 21: (1, -1),
        22: (2, -1), 23: (-1.5, -2), 24: (-0.5, -2), 25: (0.5, -2), 26: (1.5, -2), 27: (-1, -3),
        28: (0, -3), 29: (1, -3), 30: (-2, -2), 31: (2, -2), 32: (0, 0), 33: (-3, 2), 34: (3, 2),
        35: (-3, 1), 36: (3, 1), 37: (-3, 0), 38: (3, 0), 39: (-3, -1), 40: (3, -1), 41: (-3, -2),
        42: (3, -2), 43: (-2, 3), 44: (2, 3), 45: (-2.5, 2.5), 46: (2.5, 2.5), 47: (-2.5, -2.5),
        48: (2.5, -2.5), 49: (-1.5, 3.5), 50: (1.5, 3.5), 51: (-3.5, 1.5), 52: (3.5, 1.5),
        53: (-3.5, -1.5), 54: (3.5, -1.5), 55: (-2.5, 1.5), 56: (2.5, 1.5), 57: (-2.5, -1.5),
        58: (2.5, -1.5), 59: (-1.5, -3.5), 60: (1.5, -3.5), 61: (-3.5, 0.5), 62: (3.5, 0.5),
        63: (-3.5, -0.5), 64: (3.5, -0.5)
    }
    
    G = nx.Graph()
    
    for channel in mean_values.index:
        if channel in electrode_positions:
            G.add_node(channel, weight=mean_values[channel])
    
    for channel in top_channels:
        if channel in electrode_positions:
            G.add_edge(32, channel, weight=mean_values[channel])
    
    pos = {node: electrode_positions[node] for node in G.nodes if node in electrode_positions}
   
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    
    plt.title("Conexões EEG - Canais com Maior Peso Médio (Layout 10-20)")
    plt.show()
    
    return mean_values, G

mean_values, G = process_eeg("S109R03_data.txt")

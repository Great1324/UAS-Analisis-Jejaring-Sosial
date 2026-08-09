import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# ==========================================
# 1. LOAD DATASET & REPRESENTASI GRAF (SOAL 1)
# ==========================================
# Membaca dataset Bitcoin Alpha dari file CSV
df = pd.read_csv('soc-sign-bitcoinalpha.csv', header=None, names=['SOURCE', 'TARGET', 'RATING', 'TIME'])

# Membuat Directed Weighted Graph
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(int(row['SOURCE']), int(row['TARGET']), weight=float(row['RATING']))

print("=== SOAL 1: INFORMASI DATASET & REPRESENTASI GRAF ===")
print("Jenis Graf         : Berarah (Directed) & Berbobot (Weighted)")
print(f"Total Node Jaringan: {G.number_of_nodes()}")
print(f"Total Edge Jaringan: {G.number_of_edges()}")

# Ambil sampel 5 node pertama yang ada di dataset
nodes_sample = list(G.nodes())[:5]
subG_5 = G.subgraph(nodes_sample)

# Cetak Matriks Adjacency (Berbobot) 5 Node Sampel
adj_matrix_5 = nx.adjacency_matrix(subG_5, nodelist=nodes_sample, weight='weight').toarray()
print(f"\nMatriks Adjacency Berbobot (5 Node Sampel: {nodes_sample}):")
print(adj_matrix_5)


# ==========================================
# 2. ANALISIS SENTRALITAS NODE (SOAL 2)
# ==========================================
print("\n=== SOAL 2: ANALISIS SENTRALITAS NODE ===")

in_degree = nx.in_degree_centrality(G)
out_degree = nx.out_degree_centrality(G)
betweenness = nx.betweenness_centrality(G, k=100, seed=42)
closeness = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=500)

print("Top 3 In-Degree Highest :", sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Out-Degree Highest:", sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Betweenness Highest:", sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Closeness Highest  :", sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Eigenvector Highest:", sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:3])


# ==========================================
# 3. STRUKTUR GLOBAL & DETEKSI KOMUNITAS (SOAL 3)
# ==========================================
print("\n=== SOAL 3: STRUKTUR GLOBAL & DETEKSI KOMUNITAS ===")

density = nx.density(G)
clustering_coef = nx.average_clustering(G)

# Hitung Diameter & Average Path Length pada Largest Strongly Connected Component (SCC)
sccs = list(nx.strongly_connected_components(G))
largest_scc = max(sccs, key=len)
G_scc = G.subgraph(largest_scc)

diameter = nx.diameter(G_scc)
avg_path_length = nx.average_shortest_path_length(G_scc)

# Deteksi Komunitas menggunakan Algoritma Louvain (Graf diubah ke Undirected)
G_undirected = G.to_undirected()
communities = nx.community.louvain_communities(G_undirected, seed=42)

print(f"Density Jaringan              : {density:.5f}")
print(f"Average Clustering Coefficient : {clustering_coef:.5f}")
print(f"Diameter (SCC Terbesar)       : {diameter}")
print(f"Average Path Length (SCC)     : {avg_path_length:.4f}")
print(f"Jumlah Komunitas (Louvain)    : {len(communities)}")


# ==========================================
# 4. SIMULASI PENYEBARAN INFORMASI (SOAL 4)
# ==========================================
print("\n=== SOAL 4: SIMULASI PENYEBARAN INFORMASI ===")

def simulate_propagation(graph, start_node, steps=5):
    infected = {start_node}
    history = [len(infected)]
    for _ in range(steps):
        new_infected = set()
        for node in infected:
            neighbors = set(graph.successors(node))
            new_infected.update(neighbors)
        infected.update(new_infected)
        history.append(len(infected))
    return history

top_out_node = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[0][0]
top_in_node = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[0][0]
random_node = list(G.nodes())[50]

print(f"Penyebaran dari Top Out-Degree (Node {top_out_node}):", simulate_propagation(G, top_out_node, steps=5))
print(f"Penyebaran dari Top In-Degree  (Node {top_in_node}):", simulate_propagation(G, top_in_node, steps=5))
print(f"Penyebaran dari Node Acak      (Node {random_node}):", simulate_propagation(G, random_node, steps=5))


# ==========================================
# 5. VISUALISASI JEJARING & EKSPOR GEPHI (SOAL 5)
# ==========================================
print("\n=== SOAL 5: VISUALISASI NETWORKX & EKSPOR CSV KE GEPHI ===")

# 1. Visualisasi Subgraf 200 Node
sub_nodes = list(G.nodes())[:200]
subG = G.subgraph(sub_nodes)

degrees = dict(subG.in_degree())
node_sizes = [v * 50 + 30 for v in degrees.values()]

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(subG, k=0.15, seed=42)

nx.draw_networkx_nodes(subG, pos, node_size=node_sizes, node_color='#2ecc71', alpha=0.8)
nx.draw_networkx_edges(subG, pos, alpha=0.2, edge_color='gray', arrows=True, arrowsize=8)

plt.title("Visualisasi Jaringan Bitcoin Alpha (Sampel 200 Node)")
plt.axis('off')

plt.savefig("visualisasi_bitcoinalpha.png", dpi=300, bbox_inches='tight')
print("Gambar NetworkX berhasil disimpan: 'visualisasi_bitcoinalpha.png'")

# 2. Buat file CSV khusus siap pakai untuk Gephi
df_gephi = df[['SOURCE', 'TARGET', 'RATING']].rename(columns={
    'SOURCE': 'Source',
    'TARGET': 'Target',
    'RATING': 'Weight'
})
df_gephi.to_csv("BitcoinAlpha_Gephi.csv", index=False)
print("File Gephi berhasil dibuat: 'BitcoinAlpha_Gephi.csv' (Siap di-import via File -> Import Spreadsheet)")

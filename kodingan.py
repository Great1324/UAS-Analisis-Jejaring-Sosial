import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD DATASET & REPRESENTASI GRAF (5 NODE)
# ==========================================
# Membaca dataset Wiki-Vote sebagai Directed Graph
G = nx.read_edgelist('wiki-Vote.txt.gz', create_using=nx.DiGraph(), nodetype=int)

print("=== SOAL 1: INFORMASI DATASET & 5 NODE ===")
print(f"Total Node Jaringan: {G.number_of_nodes()}")
print(f"Total Edge Jaringan: {G.number_of_edges()}")

# Ambil sampel 5 node khusus (30, 3, 1412, 3352, 5254)
nodes_sample = [30, 3, 1412, 3352, 5254]
subG_5 = G.subgraph(nodes_sample)

# Cetak Matriks Adjacency 5 Node
adj_matrix_5 = nx.adjacency_matrix(subG_5, nodelist=nodes_sample).toarray()
print("\nMatriks Adjacency (5 Node Sampel):")
print(adj_matrix_5)


# ==========================================
# 2. ANALISIS SENTRALITAS NODE (SOAL 2)
# ==========================================
print("\n=== SOAL 2: ANALISIS SENTRALITAS ===")

in_degree = nx.in_degree_centrality(G)
out_degree = nx.out_degree_centrality(G)
# Antara/betweenness dihitung dengan sampel k=100 agar proses cepat
betweenness = nx.betweenness_centrality(G, k=100, seed=42)
closeness = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=500)

print("Top 3 Node In-Degree Highest:", sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Node Out-Degree Highest:", sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Node Betweenness Highest:", sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Node Closeness Highest:", sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:3])
print("Top 3 Node Eigenvector Highest:", sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:3])


# ==========================================
# 3. STRUKTUR GLOBAL & DETEKSI KOMUNITAS (SOAL 3)
# ==========================================
print("=== SOAL 3: STRUKTUR GLOBAL & DETEKSI KOMUNITAS ===")

density = nx.density(G)
avg_clustering = nx.average_clustering(G)
sccs = list(nx.strongly_connected_components(G))
largest_scc = max(sccs, key=len)
G_scc = G.subgraph(largest_scc)
diameter = nx.diameter(G_scc)
avg_path_length = nx.average_shortest_path_length(G_scc)
G_undirected = G.to_undirected()
communities = nx.community.louvain_communities(G_undirected, seed=42)

print(f"Density                      : {density:.5f}")
print(f"Diameter (SCC Terbesar)      : {diameter}")
print(f"Average Path Length (SCC)    : {avg_path_length:.4f}")
print(f"Average Clustering Coeff.    : {avg_clustering:.4f}")
print(f"Jumlah Komunitas (Louvain)   : {len(communities)}")

# ==========================================
# 4. SIMULASI PENYEBARAN INFORMASI (SOAL 4)
# ==========================================
def simulate_propagation(graph, start_node, steps=5):
    infected = {start_node}
    history = [len(infected)]
    
    for _ in range(steps):
        new_infected = set()
        for node in infected:
            # Menginfeksi tetangga (out-edges)
            neighbors = set(graph.successors(node))
            new_infected.update(neighbors)
        infected.update(new_infected)
        history.append(len(infected))
    return history

top_node = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[0][0]
random_node = list(G.nodes())[100]

print("\n=== SOAL 4: SIMULASI PENYEBARAN INFORMASI ===")
print("Penyebaran dari Node Sentral (Top In-Degree):", simulate_propagation(G, top_node, steps=3))
print("Penyebaran dari Node Acak (Random Node):", simulate_propagation(G, random_node, steps=3))


# ==========================================
# 5. VISUALISASI JEJARING (SOAL 5)
# ==========================================
print("\n=== SOAL 5: MEMBUAT GAMBAR VISUALISASI ===")

# Ambil sampel subgraf 300 node agar gambar tidak menumpuk padat
sub_nodes = list(G.nodes())[:300]
subG = G.subgraph(sub_nodes)

degrees = dict(subG.in_degree())
node_sizes = [v * 40 + 20 for v in degrees.values()]

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(subG, k=0.15, seed=42)

nx.draw_networkx_nodes(subG, pos, node_size=node_sizes, node_color='#3498db', alpha=0.8)
nx.draw_networkx_edges(subG, pos, alpha=0.2, edge_color='gray', arrows=True)

plt.title("Visualisasi Jaringan Wiki-Vote (Sampel Subgraf)")
plt.axis('off')

# Simpan gambar untuk dipanggil di README.md
plt.savefig("visualisasi_wikivote.png", dpi=300, bbox_inches='tight')
print("Gambar berhasil disimpan dengan nama 'visualisasi_wikivote.png'")

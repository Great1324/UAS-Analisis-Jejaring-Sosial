# UAS-Analisis-Jejaring-Sosial
Tugas UAS Untara

## Biodata :
- Nama : Graciela Christy Nunuela
- NIM : 2211310028
- Prodi : Teknologi Informasi
- Dataset : `wiki-Vote.txt.gz`

## Deskripsi Repository
Repository ini berisi berkas analisis Social Network Analysis (SNA) menggunakan dataset Wiki-Vote dari Stanford SNAP.

## 1. Gambarkan dan jelaskan representasi graf dari jejaring yang digunakan. Tentukan jenis graf (berarah/tak berarah dan berbobot/tidak berbobot), kemudian buat contoh matriks adjacency dari minimal lima node.
- Gambar :
import networkx as nx
import matplotlib.pyplot as plt

# 1. Baca dataset
G = nx.read_edgelist('Wiki-Vote.txt', create_using=nx.DiGraph(), nodetype=int)

# 2. Ambil subgraf (misal 500 node pertama) agar gambar tidak terlalu padat & cepat dirender
sub_nodes = list(G.nodes())[:500]
subG = G.subgraph(sub_nodes)

# 3. Hitung in-degree untuk menentukan ukuran node
degrees = dict(subG.in_degree())
node_sizes = [v * 50 + 10 for v in degrees.values()]

# 4. Gambar jaringan
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(subG, k=0.15, seed=42)
nx.draw_networkx_nodes(subG, pos, node_size=node_sizes, node_color='skyblue', alpha=0.8)
nx.draw_networkx_edges(subG, pos, alpha=0.2, edge_color='gray', arrows=True)

plt.title("Visualisasi Sampel Jaringan Wiki-Vote")
plt.axis('off')

# 5. Simpan gambar
plt.savefig("visualisasi_wikivote.png", dpi=300, bbox_inches='tight')
plt.show()

- Jenis Graff :

## 2. Hitung dan analisis Degree Centrality, Betweenness Centrality, Closeness Centrality, dan Eigenvector Centrality. Jelaskan peran node yang memiliki nilai tertinggi pada masing-masing metrik.

## 3. Hitung Density, Diameter, Average Path Length, dan Clustering Coefficient. Selanjutnya lakukan deteksi komunitas menggunakan algoritma Louvain atau Girvan-Newman, kemudian interpretasikan hasilnya terhadap struktur jaringan.

## 4. Lakukan simulasi penyebaran informasi menggunakan konsep propagasi informasi atau model epidemi sederhana. Analisis pengaruh node penting terhadap kecepatan penyebaran informasi pada jaringan.

## 5. Visualisasikan jejaring menggunakan Gephi atau NetworkX, kemudian simpulkan karakteristik jaringan berdasarkan seluruh hasil analisis.

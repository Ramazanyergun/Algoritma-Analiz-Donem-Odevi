# Gerekli Kütüphanelerin kurulması:

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
import heapq

# ihtiyaç noktalarını ve önceliklerini içeren DataFrame oluşturma: 

needs = pd.DataFrame({
    'konumlar': [(37.78667666851529, 29.05490826216871),
                 (37.78848358993971, 29.072683250098766),
                 (37.781080760621016, 29.062947572062388),
                 (37.776009103129724, 29.07939496753293),
                 (37.77968171744668, 29.079099946986375),
                 (37.77670866278093, 29.058964794683867),
                 (37.77117030097405, 29.056530875174772),
                 (37.77373548854626, 29.062210020695993),
                 (37.77985659929157, 29.07393708742163),
                 (37.77402698150282, 29.04908160637421)],  
    'saglik':  [15, 20, 5,  10, 5,  10, 5,  15, 10, 5],
    'yemek':   [15, 25, 10, 5,  10, 5,  10, 0,  10, 10],
    'isinma':  [10, 5,  15, 0,  5,  0,  15, 5,  10, 5],
    'kiyafet': [5,  15, 5,  10, 5,  0,  10, 5,  15, 0]
})

oncelik = ['saglik', 'yemek', 'isinma', 'kiyafet']

# graf oluşturma
G = nx.Graph()

# konumları düğümlere ekleme
pos = {}
for i, location in enumerate(needs['konumlar']):
    G.add_node(i+1)
    pos[i+1] = location

# düğümleri ağırlıklara göre birleştirme
for j, p in enumerate(oncelik):
    for i in range(needs.shape[0]):
        if needs[p][i] != 0:
            G.add_edge(i+1, needs.shape[0]+j+1, weight=needs[p][i])


# her noktanın birbirine olan uzaklığını hesaplama

noktalar = [(37.78667666851529, 29.05490826216871),
            (37.78848358993971, 29.072683250098766),
            (37.781080760621016, 29.062947572062388),
            (37.776009103129724, 29.07939496753293),
            (37.77968171744668, 29.079099946986375),
            (37.77670866278093, 29.058964794683867),
            (37.77117030097405, 29.056530875174772),
            (37.77373548854626, 29.062210020695993),
            (37.77985659929157, 29.07393708742163),
            (37.77402698150282, 29.04908160637421)]

def prim_mst(G, start):

    # Başlangıç düğümüne kadar olan minimum ağaçları depolayacak set
    mst = set()
    # Başlangıç düğümüne olan tüm kenarların uzunluğunu ve hedef düğümünü tutan öncelikli kuyruk
    edges = [(weight, start, neighbor) for neighbor, weight in G[start].items()]
    # Öncelikli kuyrukta kenar yoksa, grafda ağaç yok demektir
    if not edges:
        return mst
    # Kuyruğu öncelikli olarak ayarla
    heapq.heapify(edges)
    # Zaten eklenen düğümleri izlemek için kullanılan küme
    connected_nodes = {start}
    # Ağaç, grafda n-1 kenar varsa tamamlandı kabul edilir
    while len(mst) < len(G) - 1:
        # Kenar önceliği, başlangıç düğümüne olan uzaklığı temel alınarak ayarlanır
        weight, node1, node2 = heapq.heappop(edges)
        if node2 not in connected_nodes:
            # Kenarı ağaç olarak kabul et ve düğümleri bağla
            mst.add((node1, node2, weight))
            connected_nodes.add(node2)
            # Yeni bağlantılar için öncelikli kuyruğa kenarları ekle
            for neighbor, weight in G[node2].items():
                if neighbor not in connected_nodes:
                    heapq.heappush(edges, (weight, node2, neighbor))
    return mst

# Grafiği çizdirme
pos = nx.spring_layout(G) # Grafı çizdirmek için düzenleme yapar
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'weight') # Kenarların etiketlerini alır
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Kenar etiketlerini çizdirir
plt.show()

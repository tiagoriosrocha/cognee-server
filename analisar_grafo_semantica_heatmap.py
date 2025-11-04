import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
from typing import Dict, Any, List, Tuple
from datetime import datetime
import json
import os

# =================== Criar grafo ===================
def criar_grafo(nodes, edges):
    G = nx.Graph()
    for node_id, node_data in nodes.items():
        G.add_node(node_id, **node_data)
        
    for edge_id, edge_data in edges.items():
        G.add_edge(edge_data["source"], edge_data["target"], **edge_data)
    return G

# =================== Gerar hash ===================
def gerar_hash(G: nx.Graph) -> Tuple[np.ndarray, List[str]]:
    """
    Gera um hash SHA-256 para cada nó do grafo, com base no ID do nó.
    """
    nodes = list(G.nodes())
    hashes = [hashlib.sha256(str(n).encode('utf-8')).hexdigest() for n in nodes]
    return np.array(hashes), nodes

# =================== Gera informações em um json ===================
def generate_node_list_json(graph1: Dict[str, Any], graph2: Dict[str, Any]) -> str:
    """
    Recebe dois grafos e retorna uma lista em formato JSON,
    classificando os nós em:
    - Exclusivos do Grafo 1
    - Exclusivos do Grafo 2
    - Comuns a ambos
    """
    nodes1 = set(graph1["nodes"].keys())
    nodes2 = set(graph2["nodes"].keys())

    common_nodes = sorted(list(nodes1.intersection(nodes2)))
    unique_nodes1 = sorted(list(nodes1 - nodes2))
    unique_nodes2 = sorted(list(nodes2 - nodes1))

    result = [
        {
            "unique_graph_1": unique_nodes1
        },
        {
            "common_nodes": common_nodes
        },
        {
            "unique_graph_2": unique_nodes2
        }
    ]

    return json.dumps(result, indent=4)

# =================== Heatmap de similaridade ===================
def heatmap_similaridade_grafos(graph1_data, graph2_data, save_path="heatmap.png"):
    """
    Recebe os dados completos de dois grafos e gera um heatmap de similaridade.
    A similaridade é baseada na igualdade dos IDs dos nós (hashing).
    Apenas salva a imagem, não mostra.
    """
    nodes_grafo1 = graph1_data.get("nodes", {})
    edges_grafo1 = graph1_data.get("edges", {})
    nodes_grafo2 = graph2_data.get("nodes", {})
    edges_grafo2 = graph2_data.get("edges", {})
    
    G1 = criar_grafo(nodes_grafo1, edges_grafo1)
    G2 = criar_grafo(nodes_grafo2, edges_grafo2)

    # Gerar hashes (substituindo os embeddings)
    hashes1, labels1 = gerar_hash(G1)
    hashes2, labels2 = gerar_hash(G2)
    
    # Calcular a "similaridade" binária baseada na igualdade dos hashes
    sim_matrix = np.zeros((len(hashes1), len(hashes2)))
    for i, h1 in enumerate(hashes1):
        for j, h2 in enumerate(hashes2):
            if labels1[i] == labels2[j]:
                sim_matrix[i, j] = 1

    # Plot heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(sim_matrix, xticklabels=labels2, yticklabels=labels1, cmap="viridis") #cmap="binary"
    plt.xlabel("Grafo 2")
    plt.ylabel("Grafo 1")
    plt.title("Heatmap de Similaridade por Hash (Igualdade dos IDs)")
    plt.tight_layout()
    plt.savefig(save_path, dpi=600)
    plt.close()
    print(f"Heatmap salvo em {save_path}")

# =================== Função principal para processamento ===================
def processar_grafos_e_gerar_saida(graph1: Dict[str, Any], graph2: Dict[str, Any]) -> str:
    """
    Função principal que orquestra a geração do heatmap e do JSON de nós.
    Retorna um JSON que contém a lista de nós e o nome do arquivo de imagem gerado.
    """
    # 1. Geração de nome de arquivo único com hash e timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_value = hashlib.sha256(timestamp.encode('utf-8')).hexdigest()[:8]
    image_filename = f"heatmap_{timestamp}_{hash_value}.png"
    
    # 2. Chama a função para gerar e salvar a imagem
    heatmap_similaridade_grafos(graph1, graph2, save_path=image_filename)
    
    # 3. Chama a função para gerar o JSON com a lista de nós
    nodes_json_string = generate_node_list_json(graph1, graph2)
    
    # 4. Combina os resultados em um único dicionário
    nodes_data = json.loads(nodes_json_string)
    final_output = {
        "status": "success",
        "image_file": os.path.abspath(image_filename),
        "node_categorization": nodes_data
    }
    
    # 5. Retorna o resultado final em formato JSON
    return json.dumps(final_output, indent=4)
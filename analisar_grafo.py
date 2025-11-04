# ================================================================
# Descrição das métricas calculadas no grafo
# ================================================================

# numero_nos
#   → Quantidade total de vértices (nós) presentes no grafo.
#   Exemplo: 3 nós no total.

# numero_arestas
#   → Quantidade total de conexões (arestas) entre os nós.
#   Exemplo: 3 arestas conectando os 3 nós.

# grau_medio
#   → Média do número de conexões que cada nó possui.
#   Fórmula: grau_medio = soma(grau(nó_i)) / número_total_de_nós
#   Exemplo: se todos os nós têm 2 conexões, o grau médio é 2.0

# distribuicao_graus
#   → Distribuição de quantos nós têm um certo número de conexões.
#   Exemplo: {"2": 3} significa que existem 3 nós com grau igual a 2.

# centralidade_media_grau
#   → Mede a importância de um nó com base no número de conexões diretas.
#   É o grau normalizado pelo máximo possível (n - 1).
#   Exemplo: para um grafo com 3 nós totalmente conectados, a média ≈ 0.67

# centralidade_media_betweenness
#   → Mede a frequência com que um nó aparece nos caminhos mais curtos
#     entre pares de outros nós.
#   Indica o quanto um nó “intermedeia” conexões no grafo.
#   Exemplo: média ≈ 0.167 significa baixa intermediação geral.

# diametro
#   → A maior distância (em número de arestas) entre quaisquer dois nós do grafo.
#   Exemplo: diametro = 1 significa que todos os nós estão diretamente conectados.

# densidade
#   → Proporção de arestas existentes em relação ao número máximo possível.
#   Fórmula: densidade = (2 * numero_arestas) / (n * (n - 1))
#   Exemplo: densidade = 1.0 indica grafo completamente conectado.

# numero_componentes_conexos
#   → Número de grupos de nós totalmente conectados entre si,
#     mas desconectados de outros grupos.
#   Exemplo: valor 1 indica que todo o grafo está conectado.
# ================================================================

import json
import networkx as nx
import statistics

def analisar_grafo(nodes_dict, edges_dict):
    """
    Recebe dois dicionários:
      - nodes_dict: dicionário de nós
      - edges_dict: dicionário de arestas
    Retorna um dicionário com métricas do grafo.
    """

    #print(type(nodes_dict))
    #print(nodes_dict)
    #print(type(edges_dict))
    #print(edges_dict)

    # Criação do grafo
    G = nx.Graph()

    # Adiciona nós
    for node_key, node_data in nodes_dict.items():
        G.add_node(node_key, **node_data)

    # Adiciona arestas
    for edge_key, edge_data in edges_dict.items():
        G.add_edge(edge_data["source"], edge_data["target"], label=edge_data.get("label", ""))

    # ---- Métricas ----
    num_nos = G.number_of_nodes()
    num_arestas = G.number_of_edges()
    graus = dict(G.degree())
    grau_medio = sum(graus.values()) / num_nos if num_nos > 0 else 0

    # Centralidades
    centralidade_grau = nx.degree_centrality(G)
    centralidade_betweenness = nx.betweenness_centrality(G)
    centralidade_grau_media = statistics.mean(centralidade_grau.values()) if centralidade_grau else 0
    centralidade_betweenness_media = statistics.mean(centralidade_betweenness.values()) if centralidade_betweenness else 0

    # Diâmetro (só se o grafo for conexo)
    diametro = nx.diameter(G) if nx.is_connected(G) else None

    # Densidade
    densidade = nx.density(G)

    # Componentes conexos
    componentes = list(nx.connected_components(G))
    num_componentes = len(componentes)

    # Distribuição de graus
    distribuicao_graus = {}
    for g in sorted(set(graus.values())):
        distribuicao_graus[g] = list(graus.values()).count(g)

    # ---- Resultado em JSON ----
    resultado = {
        "numero_nos": num_nos,
        "numero_arestas": num_arestas,
        "grau_medio": grau_medio,
        "distribuicao_graus": distribuicao_graus,
        "centralidade_media_grau": centralidade_grau_media,
        "centralidade_media_betweenness": centralidade_betweenness_media,
        "diametro": diametro,
        "densidade": densidade,
        "numero_componentes_conexos": num_componentes
    }

    resultado_agrupado = {
        "analise": resultado
    }

    #print("resultado da análise: ", resultado)

    return resultado_agrupado
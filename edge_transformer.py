import json
from typing import List, Tuple, Any, Dict

class EdgeTransformer:
    """
    Recebe uma LISTA DE TUPLAS de arestas e a transforma em um
    dicionário de arestas nomeadas ("edge1", "edge2", etc.).
    Formato da tupla de entrada: (source_id, target_id, label, {metadata})
    """
    def transform(self, edges_list: List[Tuple]) -> Dict[str, Any]:
        if not isinstance(edges_list, list):
            raise ValueError("A entrada de arestas deve ser uma lista de tuplas.")

        output_edges = {}
        for i, edge_tuple in enumerate(edges_list, start=1):
            if not isinstance(edge_tuple, tuple) or len(edge_tuple) < 3:
                print(f"Aviso (edges): Item de dados inválido, será ignorado: {edge_tuple}")
                continue

            edge_key = f"edge{i}"
            output_edges[edge_key] = {
                "target": edge_tuple[1],
                "source": edge_tuple[0],
                "label": edge_tuple[2]
            }
        return {"edges": output_edges}
    
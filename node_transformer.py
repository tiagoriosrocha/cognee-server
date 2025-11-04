import json
from typing import List, Tuple, Any, Dict

class NodeTransformer:
    """
    Recebe uma LISTA DE TUPLAS de nós e a transforma em um dicionário,
    usando o ID de cada nó como chave.
    Formato da tupla de entrada: (node_id, {properties})
    """
    def transform(self, nodes_list: List[Tuple[str, Dict]]) -> Dict[str, Any]:
        if not isinstance(nodes_list, list):
            raise ValueError("A entrada de nós deve ser uma lista de tuplas.")

        output_nodes: Dict[str, Any] = {}

        for node_record in nodes_list:
            if not isinstance(node_record, tuple) or len(node_record) != 2:
                print(f"Aviso: Registro de nó com formato inválido, será ignorado: {node_record}")
                continue

            node_id, node_properties = node_record
            output_nodes[node_id] = node_properties

        return {"nodes": output_nodes}


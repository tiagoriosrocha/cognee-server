import asyncio
import os
from cognee.shared.logging_utils import get_logger
import cognee
from cognee.infrastructure.databases.graph import get_graph_engine
from cognee.api.v1.search import SearchType
from deepeval.test_case import LLMTestCase
from deepeval_evaluator import DeepEvalEvaluator
from node_transformer import NodeTransformer
from edge_transformer import EdgeTransformer


class ProcessarCogneeBase:
    """
    Superclasse para processadores Cognee.
    Define o modelo LLM (Ollama), o logger e os métodos principais de execução.
    """

    def __init__(self, modelo: str):
        """
        Construtor base que define o modelo Ollama a ser usado.
        """
        self.modelo = modelo
        self.logger = get_logger(self.__class__.__name__)
        self.nodeTransformer = NodeTransformer()
        self.edgeTransformer = EdgeTransformer()

    async def _executar_cognee(self, question, context_texts, expected_output, ontology_path=None):
        """
        Executa o pipeline Cognee completo de forma genérica.
        """
        logger = self.logger

        # Limpeza e preparação
        logger.info("Reiniciando ambiente Cognee...")
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        # Adiciona dados e cria grafo
        await cognee.add(context_texts)
        await cognee.cognify(ontology_file_path=ontology_path)

        # Busca no grafo
        logger.info("Executando busca no grafo...")
        final_answer = await cognee.search(
            query_type=SearchType.GRAPH_COMPLETION,
            query_text=question,
        )

        # Carrega e transforma grafo
        graph_engine = await get_graph_engine()
        graph_data = await graph_engine.get_graph_data()
        transformed_nodes = self.nodeTransformer.transform(graph_data[0])
        transformed_edges = self.edgeTransformer.transform(graph_data[1])

        # Avaliação com DeepEval
        logger.info(f"Avaliando com DeepEval (modelo Ollama: {self.modelo})...")
        test_case = LLMTestCase(
            input=question,
            actual_output=str(final_answer).strip("[]'\""),
            expected_output=expected_output,
            retrieval_context=context_texts,
        )
        evaluator = DeepEvalEvaluator(modelo=self.modelo)
        evaluation_results = evaluator.evaluate_test_case(test_case)

        # Resultado final
        return {
            "final_answer": str(final_answer).strip("[]'\""),
            "nodes": transformed_nodes["nodes"],
            "edges": transformed_edges["edges"],
            "evaluation": evaluation_results,
        }

    def executar(self, dados_recebidos: dict) -> dict:
        """
        Método síncrono que gerencia o loop assíncrono de execução.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self._executar_processamento_assincrono(dados_recebidos), loop)
            return future.result()
        else:
            return loop.run_until_complete(self._executar_processamento_assincrono(dados_recebidos))

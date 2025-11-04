import json
from typing import List

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    BaseMetric
)


class DeepEvalEvaluator:
    def __init__(self, model_name: str = "phi4:latest", base_url: str = "http://localhost:11434", temperature: float = 0):
        #Inicializa o avaliador com as configurações do modelo Ollama.
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature

        #Instancia o modelo Ollama
        self.ollama_model = OllamaModel(
            model=self.model_name,
            base_url=self.base_url,
            temperature=self.temperature
        )

        #Define as métricas
        self.metrics: List[BaseMetric] = [
            #ContextualRelevancyMetric(threshold=0.7, model=self.ollama_model),
            #ContextualRecallMetric(threshold=0.7, model=self.ollama_model),
            #ContextualPrecisionMetric(threshold=0.7, model=self.ollama_model),
            AnswerRelevancyMetric(threshold=0.7, model=self.ollama_model),
            FaithfulnessMetric(threshold=0.7, model=self.ollama_model),
        ]


    def evaluate_test_case(self, test_case: LLMTestCase) -> str:
        #Executa a avaliação
        test_results = evaluate([test_case], metrics=self.metrics)
        #Pega o primeiro (e único) resultado
        test_result = test_results.test_results[0]
        #cria o json
        evaluation_results_json = {
            #"test_name": test_result.name,
            "success": test_result.success,
            "input": test_result.input,
            "actual_output": test_result.actual_output,
            "expected_output": test_result.expected_output,
            #"retrieval_context": test_result.retrieval_context,
            "metrics": []
        }
        #Navega pelas métricas e salva os dados no json
        for metric in test_result.metrics_data:
            evaluation_results_json["metrics"].append({
                "metric_name": metric.name,
                "score": metric.score,
                "passed": metric.success,
                "reasoning": metric.reason,
                #"threshold": metric.threshold,
                #"strict_mode": metric.strict_mode,
                #"evaluation_model": metric.evaluation_model,
                #"error": str(metric.error) if metric.error else None,
                #"evaluation_cost": metric.evaluation_cost,
                #"verbose_logs": metric.verbose_logs
            })

        #Converte o resultado para string JSON compacta
        #evaluation_results_json_str = json.dumps(evaluation_results_json, separators=(',', ':'))
        
        return evaluation_results_json




# # Preparando os dados de teste (exemplo)
# question = "Qual é a capital da França?"
# final_answer = "Paris é a capital da França e a maior cidade do país."
# expected_output = "Paris"
# retrieval_context = ["A capital da França é Paris.", "Paris é conhecida por sua arte e culinária."]

# # Cria o caso de teste
# test_case_example = LLMTestCase(
#     input=question,
#     actual_output=final_answer,
#     expected_output=expected_output,
#     retrieval_context=retrieval_context,
# )

# # Instancia a classe
#evaluator = DeepEvalEvaluator()

## Avalia e obtém o resultado em formato de dicionário
#evaluation_results = evaluator.evaluate_test_case(test_case_example)
#print(evaluation_results)
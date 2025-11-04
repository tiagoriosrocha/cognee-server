from processar_cognee_base import ProcessarCogneeBase
import os

class ProcessarCogneeQuestionOnto(ProcessarCogneeBase):
    async def _executar_processamento_assincrono(self, dados_recebidos: dict):
        question = dados_recebidos.get("question")
        expected_output = dados_recebidos.get("answer")
        context = [f"{title}: {' '.join(texts)}" for title, texts in dados_recebidos.get("context", [])]

        ontology_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "ontologias/ontologia_personagens_somente_classes.owl"
        )   

        return await self._executar_cognee(question, context, expected_output, ontology_path)

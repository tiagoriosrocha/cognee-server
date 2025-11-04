from processar_cognee_base import ProcessarCogneeBase
import os

class ProcessarCogneeSubquestionOnto(ProcessarCogneeBase):
    async def _executar_processamento_assincrono(self, dados_recebidos: dict):
        question = dados_recebidos.get("question")
        expected_output = dados_recebidos.get("answer")
        context = [title for title, _ in dados_recebidos.get("context", [])]

        for sub in dados_recebidos.get("question_decomposition", []):
            context.append(sub.get("question", ""))
            context.append(sub.get("answer", ""))

        ontology_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "ontologias/ontologia_personagens_somente_classes.owl"
        )
        return await self._executar_cognee(question, context, expected_output, ontology_path)

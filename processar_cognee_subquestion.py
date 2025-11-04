from processar_cognee_base import ProcessarCogneeBase

class ProcessarCogneeSubquestion(ProcessarCogneeBase):
    async def _executar_processamento_assincrono(self, dados_recebidos: dict):
        question = dados_recebidos.get("question")
        expected_output = dados_recebidos.get("answer")
        context = [f"{title}: {' '.join(texts)}" for title, texts in dados_recebidos.get("context", [])]

        subquestions = []
        for sub in dados_recebidos.get("question_decomposition", []):
            subquestions.append(sub.get("question", ""))

        return await self._executar_cognee(question, context, expected_output, subquestions)

from processar_cognee_base import ProcessarCogneeBase

class ProcessarCogneeQuestion(ProcessarCogneeBase):
    async def _executar_processamento_assincrono(self, dados_recebidos: dict):
        question = dados_recebidos.get("question")
        expected_output = dados_recebidos.get("answer")
        context = [title for title, _ in dados_recebidos.get("context", [])]

        return await self._executar_cognee(question, context, expected_output)

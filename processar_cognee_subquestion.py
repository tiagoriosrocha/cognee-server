from processar_cognee_base import ProcessarCogneeBase

class ProcessarCogneeSubquestion(ProcessarCogneeBase):
    async def _executar_processamento_assincrono(self, dados_recebidos: dict):
        question = dados_recebidos.get("question")
        expected_output = dados_recebidos.get("answer")
        context = [title for title, _ in dados_recebidos.get("context", [])]

        # Acrescenta sub-perguntas ao contexto
        for sub in dados_recebidos.get("question_decomposition", []):
            context.append(sub.get("question", ""))
            context.append(sub.get("answer", ""))
        return await self._executar_cognee(question, context, expected_output)

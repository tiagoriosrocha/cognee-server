# cognee-server

Repositório contendo ferramentas e scripts para processamento, análise e avaliação da base Cognee, tratamento de ontologias e experiementos com modelos.

## Descrição

Este projeto agrupa vários scripts Python usados para: processar a base Cognee, converter e manipular ontologias, gerar e analisar grafos semânticos, treinar/avaliar transformadores de nós e arestas, e executar um serviço/endpoint local (`app.py`). Ele é pensado para pesquisadores e desenvolvedores que trabalham com raciocínio, ontologias e avaliação automática de modelos.

## Conteúdo principal

- `app.py` — possível ponto de entrada (API/serviço Flask).
- `app_test.py` — testes/smoke tests para o `app.py`.
- `processar_cognee_base.py` — processamento principal da base Cognee.
- `processar_cognee_question.py` / `processar_cognee_subquestion.py` — scripts para processar perguntas e subperguntas.
- `processar_cognee_question_onto.py` / `processar_cognee_subquestion_onto.py` — processamento envolvendo ontologias para perguntas/subperguntas.
- `analisar_grafo.py` — análise de grafos gerados a partir de dados.
- `analisar_grafo_semantica_heatmap.py` — análises semânticas e heatmaps (visuais).
- `node_transformer.py` / `edge_transformer.py` — scripts relacionados a transformadores para nós/arestas.
- `deepeval_evaluator.py` — integração com a biblioteca DeepEval para avaliação automática.
- `ollama_model_manager.py` — integração/gerenciamento de modelos (ex.: Ollama ou similar).
- `requirements.txt` — dependências do projeto.
- `ontologias/` — pasta com arquivos OWL/RDF usados pelo projeto.

## Arquivos de ontologias

A pasta `ontologias/` contém diversos arquivos OWL/RDF usados pelos scripts. Exemplos:

- `bfo_classes_only.owl`
- `ontologia_personagens.owl`
- `schemaorg_complete_formato_cognee.owl`

Esses arquivos são inputs para os módulos que realizam análise semântica e geração de grafos.

## Requisitos

Recomendado: Python 3.10+ (os arquivos `.pyc` mostram uso de CPython 3.x). Dependências listadas em `requirements.txt` incluem:

```
Flask
cognee
flask_cors
matplotlib
seaborn
scikit-learn
deepeval
transformers
torch
sentencepiece
accelerate
safetensors
```

Observação: algumas dependências como `torch` e `transformers` podem exigir instruções específicas de instalação (GPU vs CPU). Se você estiver em macOS sem suporte nativo a CUDA, instale a versão CPU adequada do PyTorch seguindo as instruções oficiais (https://pytorch.org).

## Instalação (exemplo)

No macOS com zsh, execute:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Se a instalação de `torch` falhar, veja as instruções do PyTorch e instale a versão compatível com seu sistema.

## Como usar (exemplos)

Rodar o serviço/API (se aplicável):

```bash
python app.py
```

Executar um processamento da base Cognee:

```bash
python processar_cognee_base.py
```

Executar análise de grafo/heatmap:

```bash
python analisar_grafo.py
python analisar_grafo_semantica_heatmap.py
```

Rodar testes/smoke:

```bash
python app_test.py
```

## Boas práticas e notas de desenvolvimento

- Trabalhe em um ambiente virtual isolado.
- Para tarefas pesadas com modelos (`transformers`, `torch`), prefira uma máquina com GPU para speedups, caso contrário ajuste os parâmetros (batch size, device) para CPU.
- Se for versionar grandes pesos/artefatos, use um storage externo (não comitar modelos pesados no repositório).

## Próximos passos sugeridos

- Adicionar um `requirements.lock` ou `poetry`/`pip-tools` para controle de versões das dependências.
- Incluir um `Makefile` ou scripts em `./scripts` para tarefas recorrentes (instalação, lint, testes, execução).
- Adicionar exemplos de entrada/saída (sample data) e um notebook de demonstração.

## Licença

Nenhuma licença está explicitada neste repositório. Se desejar, adicione um arquivo `LICENSE` com a licença desejada (MIT, Apache-2.0, etc.).

## Contato

Se precisar de ajuda com o projeto, descreva o uso desejado e quaisquer erros que encontrar (logs/tracebacks).
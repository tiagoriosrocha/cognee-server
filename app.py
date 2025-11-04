import uuid
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analisar_grafo import analisar_grafo
import json
from analisar_grafo_semantica_heatmap import processar_grafos_e_gerar_saida, heatmap_similaridade_grafos, generate_node_list_json

from processar_cognee_question import ProcessarCogneeQuestion
from processar_cognee_question_onto import ProcessarCogneeQuestionOnto
from processar_cognee_subquestion import ProcessarCogneeSubquestion
from processar_cognee_subquestion_onto import ProcessarCogneeSubquestionOnto
from ollama_model_manager import OllamaModelManager
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
tasks = {}
comparisons = {}
cognee_lock = threading.Lock()
IMAGE_DIR = "/home/tiagoriosrocha/Documents/cognee/backend-flask-morehopqa"


###################################################################
###################################################################
###################################################################
###################################################################

def worker_processamento(task_id, dados_para_processar):
    """
    Função que executa o trabalho pesado em uma thread separada.
    """
    with cognee_lock:
        app.logger.info(f"Lock adquirido. Iniciando processamento para a tarefa: {task_id}")
        try:
            tasks[task_id]['status'] = 'PROCESSING'

            # Verifica o tipo de processamento solicitado na interface
            tipoProcessamento = dados_para_processar["processingType"]["value"]
            if not tipoProcessamento:
                tipoProcessamento = 1
            app.logger.info(f"Tipo de Processamento: {tipoProcessamento}.")
            
            # Verifica o modelo selecionado vindo da interface
            modeloOllama = dados_para_processar["ollamaModel"]
            if not modeloOllama:
                modeloOllama = "phi4:latest"
            app.logger.info(f"Modelo para o processamento: {modeloOllama}.")
            
            match tipoProcessamento:
                case 1:
                    processador = ProcessarCogneeQuestion(modeloOllama)
                case 2:
                    processador = ProcessarCogneeSubquestion(modeloOllama)    
                case 3:
                    processador = ProcessarCogneeQuestionOnto(modeloOllama)
                case 4:
                    processador = ProcessarCogneeSubquestionOnto(modeloOllama)    
            
            resultado_cognee = processador.executar(dados_para_processar["selectedQuestion"])
            resultado_analise = analisar_grafo(resultado_cognee["nodes"], resultado_cognee["edges"])
            tasks[task_id]['status'] = 'SUCCESS'
            tasks[task_id]['result'] = resultado_cognee | resultado_analise
            app.logger.info(f"Tarefa {task_id} concluída com sucesso.")

        except Exception as e:
            app.logger.error(f"Erro na tarefa {task_id}: {e}", exc_info=True)
            tasks[task_id]['status'] = 'FAILURE'
            tasks[task_id]['result'] = {"erro": "Um erro inesperado ocorreu durante o processamento.", "detalhes": str(e)}

    app.logger.info(f"Lock liberado para a tarefa: {task_id}")


@app.route('/runquestion', methods=['POST'])
def run_question_async():
    """
    Endpoint que INICIA uma tarefa de processamento em background.
    """
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'PENDING', 'result': None}
    
    thread = threading.Thread(target=worker_processamento, args=(task_id, dados_recebidos))
    thread.start()

    app.logger.info(f"Tarefa {task_id} criada e enfileirada para processamento.")
    return jsonify({"task_id": task_id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """
    Endpoint para verificar o status de uma tarefa.
    """
    task = tasks.get(task_id)
    
    if not task:
        app.logger.warning(f"Tentativa de acesso a uma tarefa inexistente: {task_id}")
        return jsonify({"erro": "ID da tarefa não encontrado."}), 404

    response_data = {
        "task_id": task_id,
        "status": task['status']
    }
    
    if task['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = task['result']
        
    return jsonify(response_data), 200


###################################################################
###################################################################
###################################################################
###################################################################


def processar_comparacoes(comparison_id, dados_para_processar):
    try:
        comparisons[comparison_id]['status'] = 'PROCESSING'
        
        idtask_grafo1 = dados_para_processar["idtask_grafo1"]
        idtask_grafo2 = dados_para_processar["idtask_grafo2"]

        grafo1 = tasks[idtask_grafo1]['result']
        grafo2 = tasks[idtask_grafo2]['result']
        #grafo1 = FIXED_RESULT1
        #grafo2 = FIXED_RESULT2

        resultado_analise = processar_grafos_e_gerar_saida(grafo1, grafo2) #analisar_grafo_heatmap(grafo1, grafo2)
        comparisons[comparison_id]['status'] = 'SUCCESS'
        comparisons[comparison_id]['result'] = json.loads(resultado_analise)            
    except Exception as e:
        app.logger.error(f"Erro na tarefa simulada {comparison_id}: {e}")
        comparisons[comparison_id]['status'] = 'FAILURE'
        comparisons[comparison_id]['result'] = {"erro": "Ocorreu um erro no processamento da comparacao.", "detalhes": str(e)}


@app.route('/runcomparison', methods=['POST'])
def run_comparasion():
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400
    
    comparison_id = str(uuid.uuid4())
    comparisons[comparison_id] = {'status': 'PENDING', 'result': None}
    thread = threading.Thread(target=processar_comparacoes, args=(comparison_id,dados_recebidos))
    thread.start()
    return jsonify({"comparison_id": comparison_id}), 202


@app.route('/getcomparison/<comparison_id>', methods=['GET'])
def get_comparasion(comparison_id):
    comp = comparisons.get(comparison_id)
    if not comp:
        return jsonify({"erro": "ID da comparação não encontrado."}), 404
    response_data = {
        "comparison_id": comparison_id,
        "status": comp['status']
    }
    if comp['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = comp['result']   
    return jsonify(response_data), 200


#######################################################################################################
#######################################################################################################
#######################################################################################################

@app.route('/static/<filename>')
def get_image(filename):
    """Serve o arquivo de imagem do diretório de imagens."""
    return send_from_directory(IMAGE_DIR, filename)

#######################################################################################################
#######################################################################################################
#######################################################################################################


@app.route('/modelos', methods=['GET'])
def obter_modelos():
    ollama_manager = OllamaModelManager()
    modelos = ollama_manager.listar_modelos()
    resposta = {"modelos": modelos}
    
    return jsonify(resposta), 200


###################################################################
###################################################################
###################################################################
###################################################################

if __name__ == '__main__':
    app.run(debug=False, port=5001)





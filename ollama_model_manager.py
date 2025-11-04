import subprocess

class OllamaModelManager:
    """
    Classe responsável por interagir com o Ollama
    e listar os modelos disponíveis localmente.
    """
    def __init__(self):
        pass

    def listar_modelos(self):
        """
        Retorna uma lista com os nomes dos modelos disponíveis no Ollama.
        """
        try:
            # Executa o comando `ollama list`
            resultado = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
            
            linhas = resultado.stdout.strip().split("\n")

            # Extrai os nomes dos modelos (ignorando o cabeçalho)
            modelos = []
            for linha in linhas[1:]:
                partes = linha.split()
                if partes:
                    modelos.append(partes[0])

            return modelos

        except subprocess.CalledProcessError as e:
            print("Erro ao listar modelos:", e)
            return []
        except FileNotFoundError:
            print("Ollama não encontrado. Verifique se está instalado e no PATH.")
            return []
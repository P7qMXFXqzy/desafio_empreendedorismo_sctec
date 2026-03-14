import json
import os

class Administrador_De_Dados:

    def inicializar(self, caminho_base):
        self.caminho_arquivo_json = os.path.join(caminho_base, "outros_arquivos", "dados.json")
        
    def carregar_json(self):
        if not os.path.exists(self.caminho_arquivo_json):
            return {}

        with open(self.caminho_arquivo_json, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)


    def salvar_json(self, dados):
        with open(self.caminho_arquivo_json, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def gerar_novo_id(self, dados):
        if not dados:
            return "00000"
        maior = max(int(i) for i in dados.keys())
        novo = maior + 1
        return str(novo).zfill(5)
    
    def salvar_registro(self, id_inserido, empreendimento, empreendedor, municipio, segmento, contato, status):
        dados = self.carregar_json()
        id_do_registro = 0
        #Se estiver editando um registro, movê-lo para a variável do registro alterado. Senão, criar um novo valor.
        if (id_inserido != None): id_do_registro = id_inserido
        else: id_do_registro = self.gerar_novo_id(dados)
        dados[id_do_registro] = {
            "empreendimento": empreendimento,
            "empreendedor": empreendedor,
            "municipio": municipio,
            "segmento": segmento,
            "contato": contato,
            "status": status
        }
        self.salvar_json(dados)
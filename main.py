from sys import argv, exit
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QLineEdit, QScrollArea, QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton, QButtonGroup, QMessageBox
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QTimer
from pyautogui import size as screen_size
from random import randrange, choice
import os
from time import sleep
import json
import sys
from outros_arquivos.administrar_dados_json import Administrador_De_Dados


class Janela(QMainWindow):
    def inicializar(self):
        #inicialização da janela
        self.administrador_de_dados_obj = Administrador_De_Dados()
        self.administrador_de_dados_obj.inicializar(self.encontrar_diretorio_base())
        self.id_em_edicao = None
        self.max_resolucao_x,  self.max_resolucao_y = screen_size()
        self.resize(self.max_resolucao_x,  self.max_resolucao_y)
        #botões para trocar de tela
        pos_x = 0
        comprimento_botao = int(self.width() / 2)
        self.botao_visualizar = QPushButton("visualizar", self)
        self.botao_visualizar.resize(comprimento_botao, 100)
        self.botao_visualizar.move(0,0)
        self.botao_visualizar.clicked.connect(lambda: (self.trocar_janela("visualizar", False)))
        self.botao_visualizar.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(60,60,60);
                                                font-size: 30px;
                                                color: red;
                                            }
                                            QPushButton:pressed {
                                                padding-top: 2px;
                                                padding-left: 2px;
                                            }
                                            """)
        pos_x += comprimento_botao
        self.botao_aed = QPushButton("Adicionar / editar/ deletar", self)
        self.botao_aed.resize(comprimento_botao, 100)
        self.botao_aed.move(pos_x,0)
        self.botao_aed.clicked.connect(lambda: (self.trocar_janela("editar", True)))
        self.botao_aed.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(60,60,60);
                                                font-size: 30px;
                                                color: orange;
                                            }
                                            QPushButton:pressed {
                                                padding-top: 2px;
                                                padding-left: 2px;
                                            }
                                            """)
        #widget de tela de visualização e de cadastro
        self.widget_lista = QWidget(self)
        self.widget_lista.resize(self.width(), self.height())
        self.widget_lista.move(0, 100)
        self.widget_lista.setStyleSheet("background-color: rgb(20,20,20)")
        self.widget_lista.showMaximized()
        self.widget_cadastro = QWidget(self)
        self.widget_cadastro.resize(self.width(), self.height())
        self.widget_cadastro.move(0, 100)
        self.widget_cadastro.setStyleSheet("background-color: rgb(20,20,20)")
        self.widget_cadastro.hide() #Iniciar com o widget de cadastro escondido e com a lista visível por padrão
        #grid para visualização dos dados
        # grid para visualização dos dados
        self.tabela = QTableWidget(self.widget_lista)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setStyleSheet("""
                                    QHeaderView::section {
                                        background-color: rgb(60,60,60);
                                        color: white;
                                        font-weight: bold;
                                        border: 1px solid rgb(90,90,90);
                                        padding: 4px;
                                    }

                                    QTableWidget {
                                        background-color: rgb(30,30,30);
                                        alternate-background-color: rgb(40,40,40);
                                        color: white;
                                        gridline-color: rgb(70,70,70);
                                    }

                                    QTableWidget::item:selected {
                                        background-color: rgb(0,120,215);
                                    }
                                    """
        )
        self.tabela.resize(self.width(), self.height())
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "Empreendimento",
            "Empreendedor",
            "Município",
            "Segmento de atuação",
            "E-mail / contato",
            "Status"
        ])
        self.tabela.setRowCount(100)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.cellDoubleClicked.connect(self.editar_empreendimento)
        self.carregar_dados_para_tabela()
        #elementos do widget de criação / edição / deleção de adados
        comprimento_campo = (int(self.width() / 3))
        pos_y = 30
        stylesheet_campos = "background-color: rgb(50,50,50); border-style: solid; border-width: 2px; border-color: red; font: 20px; color: white"
        stylesheet_labels = "color: white;  font: 35px"
        #campos e seus labels
        self.campo_empreendimento = QLineEdit(self.widget_cadastro)
        self.campo_empreendimento.move(400, pos_y)
        self.campo_empreendimento.resize(comprimento_campo, 50)
        self.campo_empreendimento.setStyleSheet(stylesheet_campos)
        self.label_empreendimento = QLabel("Empreendimento:", self.widget_cadastro)
        self.label_empreendimento.move(10, pos_y)
        self.label_empreendimento.setStyleSheet(stylesheet_labels)
        pos_y += 50 + 30
        self.campo_empreendedor = QLineEdit(self.widget_cadastro)
        self.campo_empreendedor.move(400, pos_y)
        self.campo_empreendedor.resize(comprimento_campo, 50)
        self.campo_empreendedor.setStyleSheet(stylesheet_campos)
        self.label_empreendedor = QLabel("Empreendedor:", self.widget_cadastro)
        self.label_empreendedor.move(10, pos_y)
        self.label_empreendedor.setStyleSheet(stylesheet_labels)
        pos_y += 50 + 30
        self.campo_municipio = QLineEdit(self.widget_cadastro)
        self.campo_municipio.move(400, pos_y)
        self.campo_municipio.resize(comprimento_campo, 50)
        self.campo_municipio.setStyleSheet(stylesheet_campos)
        self.label_municipio = QLabel("Município:", self.widget_cadastro)
        self.label_municipio.move(10, pos_y)
        self.label_municipio.setStyleSheet(stylesheet_labels)
        pos_y += 50 + 30
        self.campo_segmento = QLineEdit(self.widget_cadastro)
        self.campo_segmento.move(400, pos_y)
        self.campo_segmento.resize(comprimento_campo, 50)
        self.campo_segmento.setStyleSheet(stylesheet_campos)
        self.label_segmento = QLabel("Segmento:", self.widget_cadastro)
        self.label_segmento.move(10, pos_y)
        self.label_segmento.setStyleSheet(stylesheet_labels)
        pos_y += 50 + 30
        self.campo_contato = QLineEdit(self.widget_cadastro)
        self.campo_contato.move(400, pos_y)
        self.campo_contato.resize(comprimento_campo, 50)
        self.campo_contato.setStyleSheet(stylesheet_campos)
        self.label_contato = QLabel("Contato:", self.widget_cadastro)
        self.label_contato.move(10, pos_y)
        self.label_contato.setStyleSheet(stylesheet_labels)
        pos_y += 50 + 30
        #Botões de status do empreendimento
        self.label_status = QLabel("Status:", self.widget_cadastro)
        self.label_status.move(10, pos_y)
        self.label_status.setStyleSheet(stylesheet_labels)
        self.radio_ativo = QRadioButton("Ativo", self.widget_cadastro)
        self.radio_ativo.move(400, pos_y)
        self.radio_ativo.setStyleSheet("color: white; font: 35px")
        self.radio_inativo = QRadioButton("Inativo", self.widget_cadastro)
        self.radio_inativo.move(550, pos_y)
        self.radio_inativo.setStyleSheet("color: white; font: 35px")
        self.grupo_status = QButtonGroup(self)
        self.grupo_status.addButton(self.radio_ativo)
        self.grupo_status.addButton(self.radio_inativo)
        self.radio_ativo.setChecked(True)
        #botões da tela de edição
        pos_x_botoes = int(self.width() * 0.75)
        pos_y_botoes = 50
        altura_botao = 60
        largura_botao = 250

        stylesheet_botoes = """
                            QPushButton{
                                background-color: rgb(70,70,70);
                                color: white;
                                font-size: 22px;
                                border-style: solid; 
                                border-width: 2px; 
                                border-color: orange;
                            }
                            QPushButton:hover{
                                background-color: rgb(90,90,90);
                            }
                            QPushButton:pressed{
                                padding-top:2px;
                                padding-left:2px;
                            }
                            """

        self.botao_limpar = QPushButton("Limpar", self.widget_cadastro)
        self.botao_limpar.move(pos_x_botoes, pos_y_botoes)
        self.botao_limpar.resize(largura_botao, altura_botao)
        self.botao_limpar.setStyleSheet(stylesheet_botoes)
        self.botao_limpar.clicked.connect(self.limpar_tela_de_edicao)
        pos_y_botoes += altura_botao + 20

        self.botao_salvar = QPushButton("Salvar", self.widget_cadastro)
        self.botao_salvar.move(pos_x_botoes, pos_y_botoes)
        self.botao_salvar.resize(largura_botao, altura_botao)
        self.botao_salvar.setStyleSheet(stylesheet_botoes)
        self.botao_salvar.clicked.connect(self.salvar_registro)
        pos_y_botoes += altura_botao + 20

        self.botao_deletar = QPushButton("Deletar", self.widget_cadastro)
        self.botao_deletar.move(pos_x_botoes, pos_y_botoes)
        self.botao_deletar.resize(largura_botao, altura_botao)
        self.botao_deletar.setStyleSheet(stylesheet_botoes)
        self.botao_deletar.clicked.connect(self.deletar_registro)

    def encontrar_diretorio_base(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def carregar_dados_para_tabela(self):
        dados_carregados = self.administrador_de_dados_obj.carregar_json()
        self.tabela.setRowCount(len(dados_carregados))

        #adicionar dados à tabela após carregar dados salvos no json
        for linha, registro in enumerate(dados_carregados.values()):
            if registro["status"]:
                status = "Ativo"
            else:
                status = "Inativo"

            self.tabela.setItem(linha, 0, QTableWidgetItem(registro["empreendimento"]))
            self.tabela.setItem(linha, 1, QTableWidgetItem(registro["empreendedor"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(registro["municipio"]))
            self.tabela.setItem(linha, 3, QTableWidgetItem(registro["segmento"]))
            self.tabela.setItem(linha, 4, QTableWidgetItem(registro["contato"]))
            self.tabela.setItem(linha, 5, QTableWidgetItem(status))

        self.ids_registros = list(dados_carregados.keys())

    def trocar_janela(self, selecao, limpar_id):
        if (selecao == "visualizar"):
            self.widget_cadastro.hide()
            self.widget_lista.showMaximized()
            self.carregar_dados_para_tabela()
        else:
            self.widget_lista.hide()
            self.widget_cadastro.showMaximized()
            if (limpar_id == True): #Limpar campos caso a intenção seja salvar um novo registro
                self.limpar_tela_de_edicao()

    def limpar_tela_de_edicao(self):
        self.id_em_edicao = None
        self.campo_empreendimento.setText("")
        self.campo_empreendedor.setText("")
        self.campo_municipio.setText("")
        self.campo_segmento.setText("")
        self.campo_contato.setText("")

    def editar_empreendimento(self, linha): #Enviar dados da linha selecionada para a tela de edição
        dados_json = self.administrador_de_dados_obj.carregar_json()
        id_registro = self.ids_registros[linha]
        registro = dados_json[id_registro]

        self.campo_empreendimento.setText(registro["empreendimento"])
        self.campo_empreendedor.setText(registro["empreendedor"])
        self.campo_municipio.setText(registro["municipio"])
        self.campo_segmento.setText(registro["segmento"])
        self.campo_contato.setText(registro["contato"])
        self.radio_ativo.isChecked()
        if registro["status"]:
            self.radio_ativo.setChecked(True)
        else:
            self.radio_inativo.setChecked(True)

        self.id_em_edicao = id_registro
        self.trocar_janela("editar", False)

    def salvar_registro(self):
        #armazenar dados inseridos antes de salvar
        empreendimento = self.campo_empreendimento.text()
        empreendedor = self.campo_empreendedor.text()
        municipio = self.campo_municipio.text()
        segmento = self.campo_segmento.text()
        contato = self.campo_contato.text()
        status = self.radio_ativo.isChecked()
        if (empreendimento.strip() == "" or empreendedor.strip() == "" or municipio.strip() == "" or segmento.strip() == "" or contato.strip() == ""):
            return #Não permitir salvar caso um dos campos obrigatórios esteja vazio.
        
        self.administrador_de_dados_obj.salvar_registro(
            self.id_em_edicao,
            empreendimento,
            empreendedor,
            municipio,
            segmento,
            contato,
            status
        )
        resposta = QMessageBox.information(
                self,
                "Salvo",
                "Dados do registro salvos.",
                QMessageBox.Ok
            )

    def deletar_registro(self):
        if (self.id_em_edicao == None):
            QMessageBox.warning(self, "Aviso", "Nenhum registro carregado para deletar.")
            return
        else:
            resposta = QMessageBox.question(
                self,
                "Confirmar exclusão",
                "Tem certeza que deseja deletar este empreendimento?",
                QMessageBox.Yes | QMessageBox.No
            )

            if resposta == QMessageBox.No:
                return
            else:
                dados_json = self.administrador_de_dados_obj.carregar_json()
                if (self.id_em_edicao in dados_json):
                    del dados_json[self.id_em_edicao]
                self.administrador_de_dados_obj.salvar_json(dados_json)
                self.limpar_tela_de_edicao()
                QMessageBox.information(self, "Sucesso", "Registro deletado.")

app = QApplication(argv)
window = Janela()
window.setWindowTitle("Projeto de empreendedorismo da SCTEC")
window.inicializar()
window.showMaximized()
exit(app.exec_())

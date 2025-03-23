"""
Interface gráfica do Lilica Excel
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.core.processador import ProcessadorPlanilhas


class LilicaExcelGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lilica Excel - Processador de Planilhas")
        self.root.geometry("800x600")

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        self.style.configure("TLabel", padding=6, font=("Helvetica", 10))

        # Criar frames
        self.criar_frames()
        self.criar_widgets()

        # Inicializar variáveis
        self.arquivos_selecionados = []
        self.arquivo_telefones = None

    def criar_frames(self):
        """Cria os frames principais da interface"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Frame para arquivos
        self.files_frame = ttk.LabelFrame(self.main_frame, text="Arquivos", padding="5")
        self.files_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5
        )

        # Frame para ações
        self.actions_frame = ttk.Frame(self.main_frame, padding="5")
        self.actions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Frame para log
        self.log_frame = ttk.LabelFrame(
            self.main_frame, text="Log de Processamento", padding="5"
        )
        self.log_frame.grid(
            row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5
        )

    def criar_widgets(self):
        """Cria os widgets da interface"""
        # Botões para selecionar arquivos
        self.btn_selecionar_planilhas = ttk.Button(
            self.files_frame,
            text="Selecionar Planilhas de Clientes",
            command=self.selecionar_planilhas,
        )
        self.btn_selecionar_planilhas.grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5
        )

        self.btn_selecionar_telefones = ttk.Button(
            self.files_frame,
            text="Selecionar Planilha de Telefones",
            command=self.selecionar_telefones,
        )
        self.btn_selecionar_telefones.grid(
            row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5
        )

        # Labels para mostrar arquivos selecionados
        self.lbl_planilhas = ttk.Label(
            self.files_frame, text="Nenhuma planilha selecionada"
        )
        self.lbl_planilhas.grid(row=0, column=1, sticky=(tk.W), padx=5)

        self.lbl_telefones = ttk.Label(
            self.files_frame, text="Nenhuma planilha de telefones selecionada"
        )
        self.lbl_telefones.grid(row=1, column=1, sticky=(tk.W), padx=5)

        # Botão de processamento
        self.btn_processar = ttk.Button(
            self.actions_frame,
            text="Processar Planilhas",
            command=self.processar_planilhas,
        )
        self.btn_processar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=10)

        # Área de log
        self.text_log = tk.Text(self.log_frame, height=10, width=70)
        self.text_log.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5
        )

        # Scrollbar para o log
        self.scrollbar = ttk.Scrollbar(
            self.log_frame, orient=tk.VERTICAL, command=self.text_log.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_log["yscrollcommand"] = self.scrollbar.set

    def selecionar_planilhas(self):
        """Abre diálogo para selecionar múltiplas planilhas"""
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Planilhas de Clientes",
            filetypes=[("Planilhas Excel", "*.xlsx")],
        )
        if arquivos:
            self.arquivos_selecionados = arquivos
            self.lbl_planilhas.config(text=f"{len(arquivos)} planilhas selecionadas")
            self.log(
                f"Planilhas selecionadas: {', '.join(os.path.basename(f) for f in arquivos)}"
            )

    def selecionar_telefones(self):
        """Abre diálogo para selecionar planilha de telefones"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Planilha de Telefones",
            filetypes=[("Planilhas Excel", "*.xlsx")],
        )
        if arquivo:
            self.arquivo_telefones = arquivo
            self.lbl_telefones.config(text=os.path.basename(arquivo))
            self.log(f"Planilha de telefones selecionada: {os.path.basename(arquivo)}")

    def log(self, mensagem: str):
        """Adiciona mensagem ao log"""
        self.text_log.insert(tk.END, mensagem + "\n")
        self.text_log.see(tk.END)

    def processar_planilhas(self):
        """Processa as planilhas selecionadas"""
        if not self.arquivos_selecionados or not self.arquivo_telefones:
            messagebox.showerror(
                "Erro", "Selecione as planilhas de clientes e a planilha de telefones!"
            )
            return

        try:
            # Criar diretórios temporários
            os.makedirs("dados/entrada", exist_ok=True)
            os.makedirs("dados/saida", exist_ok=True)

            # Copiar arquivos para diretório de entrada
            self.log("Preparando arquivos para processamento...")

            # Iniciar processamento
            processador = ProcessadorPlanilhas()
            arquivos_cliente = [os.path.basename(f) for f in self.arquivos_selecionados]
            arquivo_telefones = os.path.basename(self.arquivo_telefones)

            self.log("Iniciando processamento...")
            resultado = processador.processar_planilhas(
                arquivos_cliente, arquivo_telefones
            )

            if resultado:
                messagebox.showinfo(
                    "Sucesso",
                    "Processamento concluído com sucesso!\nArquivo salvo em dados/saida/Clientes_Com_Telefones.xlsx",
                )
                self.log("Processamento concluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao processar planilhas!")
                self.log("Erro ao processar planilhas!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante o processamento: {str(e)}")
            self.log(f"Erro: {str(e)}")

    def executar(self):
        """Inicia a execução da interface gráfica"""
        self.root.mainloop()


def main():
    """Função principal para iniciar a interface gráfica"""
    app = LilicaExcelGUI()
    app.executar()


if __name__ == "__main__":
    main()

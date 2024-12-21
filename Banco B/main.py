import customtkinter as ctk

# Configurando o tema dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class BankApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.title("Aplicativo de Banco")
        self.geometry("600x400")

        # Inicializando o saldo
        self.saldo = 0.0

        # Frame esquerdo (Saldo e Histórico)
        self.frame_saldo = ctk.CTkFrame(self, width=300)
        self.frame_saldo.pack(side="left", fill="both", expand=True)

        self.label_saldo = ctk.CTkLabel(self.frame_saldo, text=f"Saldo Atual:\nR$ {self.saldo:.2f}", font=("Arial", 18), justify="left")
        self.label_saldo.pack(pady=20, padx=10)

        self.label_historico_titulo = ctk.CTkLabel(self.frame_saldo, text="Histórico de Transações", font=("Arial", 16))
        self.label_historico_titulo.pack(pady=10, padx=10)

        self.text_historico = ctk.CTkTextbox(self.frame_saldo, width=280, height=200, font=("Arial", 12))
        self.text_historico.pack(pady=10, padx=10)
        self.text_historico.configure(state="disabled")

        # Frame direito (Teclado e Entrada)
        self.frame_teclado = ctk.CTkFrame(self, width=300)
        self.frame_teclado.pack(side="right", fill="both", expand=True)

        self.entry_valor = ctk.CTkEntry(self.frame_teclado, placeholder_text="Insira um valor", font=("Arial", 14), justify="right")
        self.entry_valor.pack(pady=10, padx=10)

        # Adicionando botões numéricos
        self.teclado_frame = ctk.CTkFrame(self.frame_teclado)
        self.teclado_frame.pack(pady=10)

        self.botao_depositar = ctk.CTkButton(self.frame_teclado, text="Depositar", command=self.depositar)
        self.botao_depositar.pack(pady=5)

        self.botao_resgatar = ctk.CTkButton(self.frame_teclado, text="Resgatar", command=self.resgatar)
        self.botao_resgatar.pack(pady=5)

        self.criar_teclado()

    def criar_teclado(self):
        botoes = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("0", 3, 1), (",", 3, 2)
        ]

        for texto, linha, coluna in botoes:
            botao = ctk.CTkButton(self.teclado_frame, text=texto, width=60, command=lambda t=texto: self.adicionar_numero(t))
            botao.grid(row=linha, column=coluna, padx=5, pady=5)

        botao_corrigir = ctk.CTkButton(self.teclado_frame, text="Corrigir", width=60, command=self.corrigir)
        botao_corrigir.grid(row=3, column=0, padx=5, pady=5)

    def adicionar_numero(self, numero):
        self.entry_valor.insert(ctk.END, numero)

    def corrigir(self):
        self.entry_valor.delete(len(self.entry_valor.get()) - 1, ctk.END)

    def depositar(self):
        try:
            valor = self.entry_valor.get().replace(",", ".")
            valor = float(valor)
            if valor > 0:
                self.saldo += valor
                self.atualizar_saldo()
                self.adicionar_historico(f"Depósito: R$ {valor:.2f}", "green")
            else:
                self.mostrar_erro("Digite um valor positivo para depositar.")
        except ValueError:
            self.mostrar_erro("Digite um valor válido.")

    def resgatar(self):
        try:
            valor = self.entry_valor.get().replace(",", ".")
            valor = float(valor)
            if valor > 0:
                if valor <= self.saldo:
                    self.saldo -= valor
                    self.atualizar_saldo()
                    self.adicionar_historico(f"Resgate: R$ {valor:.2f}", "red")
                else:
                    self.mostrar_erro("Saldo insuficiente.")
            else:
                self.mostrar_erro("Digite um valor positivo para resgatar.")
        except ValueError:
            self.mostrar_erro("Digite um valor válido.")

    def atualizar_saldo(self):
        self.label_saldo.configure(text=f"Saldo Atual:\nR$ {self.saldo:.2f}")
        self.entry_valor.delete(0, ctk.END)

    def adicionar_historico(self, mensagem, cor):
        self.text_historico.configure(state="normal")
        self.text_historico.insert(ctk.END, mensagem + "\n")

        # Aplicar cor específica para a linha adicionada
        inicio = self.text_historico.index("end-2l")
        fim = self.text_historico.index("end-1l")
        self.text_historico.tag_add(mensagem, inicio, fim)
        if "Depósito" in mensagem:
            self.text_historico.tag_config(mensagem, foreground="#00f100")
        elif "Resgate" in mensagem:
            self.text_historico.tag_config(mensagem, foreground="#ff0000")

        self.text_historico.configure(state="disabled")

    def mostrar_erro(self, mensagem):
        erro = ctk.CTkLabel(self.frame_teclado, text=mensagem, font=("Arial", 12), text_color="red")
        erro.pack(pady=5)
        self.after(3000, erro.destroy)  # Remove a mensagem de erro após 3 segundos

if __name__ == "__main__":
    app = BankApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class NotaDeDevolucaoApp:
    def __init__(self, root):
        self.root = root
        root.title("Nota de Devolução")
        root.geometry("900x700")
        root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Accent.TButton", foreground="white", background="#0078D7")
        style.map("Accent.TButton",
                  foreground=[('active', 'white')],
                  background=[('active', '#005A9E')])

        main_frame = ttk.Frame(root, padding=18)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=0)

        # Dados do Cliente
        frame_cliente = ttk.LabelFrame(main_frame, text="Dados do Cliente", padding=12)
        frame_cliente.grid(row=0, column=0, sticky="ew", padx=0, pady=8)
        frame_cliente.columnconfigure((1,3), weight=1)

        ttk.Label(frame_cliente, text="Nome:").grid(row=0, column=0, sticky="e")
        self.nome = ttk.Entry(frame_cliente, width=35)
        self.nome.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(frame_cliente, text="Cód. Cliente:").grid(row=0, column=2, sticky="e")
        self.cod_cli = ttk.Entry(frame_cliente, width=15)
        self.cod_cli.grid(row=0, column=3, sticky="ew", padx=5)

        ttk.Label(frame_cliente, text="CPF:").grid(row=1, column=0, sticky="e")
        self.cpf = ttk.Entry(frame_cliente, width=20)
        self.cpf.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(frame_cliente, text="PDV:").grid(row=1, column=2, sticky="e")
        self.pdv = ttk.Entry(frame_cliente, width=10)
        self.pdv.grid(row=1, column=3, sticky="ew", padx=5)

        # Dados do Pedido
        frame_pedido = ttk.LabelFrame(main_frame, text="Dados do Pedido", padding=12)
        frame_pedido.grid(row=1, column=0, sticky="ew", pady=8)
        frame_pedido.columnconfigure((1,3), weight=1)

        ttk.Label(frame_pedido, text="Data:").grid(row=0, column=0, sticky="e")
        self.data = ttk.Entry(frame_pedido, width=15)
        self.data.grid(row=0, column=1, sticky="ew", padx=5)
        self.data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Label(frame_pedido, text="Nº Pedido:").grid(row=0, column=2, sticky="e")
        self.n_ped = ttk.Entry(frame_pedido, width=15)
        self.n_ped.grid(row=0, column=3, sticky="ew", padx=5)

        ttk.Label(frame_pedido, text="Data Pedido:").grid(row=1, column=0, sticky="e")
        self.data_pedido = ttk.Entry(frame_pedido, width=15)
        self.data_pedido.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(frame_pedido, text="Nº Cupom:").grid(row=1, column=2, sticky="e")
        self.n_cupom = ttk.Entry(frame_pedido, width=15)
        self.n_cupom.grid(row=1, column=3, sticky="ew", padx=5)

        # Produtos
        frame_produtos = ttk.LabelFrame(main_frame, text="Produtos Devolvidos", padding=12)
        frame_produtos.grid(row=2, column=0, sticky="ew", pady=8)
        for col in range(9):
            frame_produtos.columnconfigure(col, weight=1 if col != 8 else 0)

        self.produtos = []
        self.tree = ttk.Treeview(frame_produtos, columns=("cod", "quant", "desc", "unit", "total"), show="headings", height=5)
        for col, width in zip(("cod", "quant", "desc", "unit", "total"), (80, 80, 240, 100, 100)):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=width, anchor="center")
        self.tree.grid(row=0, column=0, columnspan=9, pady=4, sticky="ew")

        self.tree.bind("<<TreeviewSelect>>", self.carregar_produto_selecionado)

        ttk.Label(frame_produtos, text="Cód:").grid(row=1, column=0, sticky="e")
        self.cod_prod = ttk.Entry(frame_produtos, width=10)
        self.cod_prod.grid(row=1, column=1, padx=2, sticky="ew")

        ttk.Label(frame_produtos, text="Quant:").grid(row=1, column=2, sticky="e")
        self.quant_prod = ttk.Entry(frame_produtos, width=5)
        self.quant_prod.grid(row=1, column=3, padx=2, sticky="ew")

        ttk.Label(frame_produtos, text="Descrição:").grid(row=1, column=4, sticky="e")
        self.desc_prod = ttk.Entry(frame_produtos, width=25)
        self.desc_prod.grid(row=1, column=5, padx=2, sticky="ew")

        ttk.Label(frame_produtos, text="Unit:").grid(row=1, column=6, sticky="e")
        self.unit_prod = ttk.Entry(frame_produtos, width=10)
        self.unit_prod.grid(row=1, column=7, padx=2, sticky="ew")

        ttk.Button(frame_produtos, text="Adicionar Produto", command=self.add_produto, style="Accent.TButton").grid(row=1, column=8, padx=8, sticky="ew")
        ttk.Button(frame_produtos, text="Atualizar Produto", command=self.atualizar_produto).grid(row=2, column=8, padx=8, pady=4, sticky="ew")
        ttk.Button(frame_produtos, text="Excluir Produto", command=self.excluir_produto).grid(row=3, column=8, padx=8, pady=4, sticky="ew")

        # Valor Total e Assinatura
        frame_total = ttk.LabelFrame(main_frame, text="Finalização", padding=12)
        frame_total.grid(row=3, column=0, sticky="ew", pady=8)
        for col in range(6):
            frame_total.columnconfigure(col, weight=1 if col in (1,3) else 0)

        ttk.Label(frame_total, text="Valor Total:").grid(row=0, column=0, sticky="e")
        self.valor_total = ttk.Entry(frame_total, width=15)
        self.valor_total.grid(row=0, column=1, sticky="ew", padx=5)
        self.valor_total.configure(state='readonly')

        ttk.Label(frame_total, text="Ass. Responsável:").grid(row=0, column=2, sticky="e")
        self.ass_responsavel = ttk.Entry(frame_total, width=25)
        self.ass_responsavel.grid(row=0, column=3, padx=5, sticky="ew")

        ttk.Button(frame_total, text="Gerar Resumo", command=self.gerar_resumo).grid(row=0, column=4, padx=8, sticky="ew")
        ttk.Button(frame_total, text="Salvar em TXT", command=self.salvar_txt).grid(row=0, column=5, padx=8, sticky="ew")

        self.item_selecionado = None

    def add_produto(self):
        cod = self.cod_prod.get().strip()
        quant = self.quant_prod.get().strip()
        desc = self.desc_prod.get().strip()
        unit = self.unit_prod.get().strip()

        if not cod or not quant or not desc or not unit:
            messagebox.showwarning("Aviso", "Preencha todos os campos do produto.")
            return

        try:
            quant_float = float(quant.replace(',', '.'))
            unit_float = float(unit.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Unitário devem ser números válidos.")
            return

        total = quant_float * unit_float
        produto = {
            "cod": cod,
            "quant": quant_float,
            "desc": desc,
            "unit": unit_float,
            "total": total
        }

        self.produtos.append(produto)
        self.tree.insert("", "end", values=(cod, quant, desc, f"{unit_float:.2f}", f"{total:.2f}"))

        self.limpar_campos_produto()
        self.atualizar_valor_total()

    def carregar_produto_selecionado(self, event):
        selecionados = self.tree.selection()
        if not selecionados:
            return
        self.item_selecionado = selecionados[0]
        valores = self.tree.item(self.item_selecionado, "values")

        self.cod_prod.delete(0, tk.END)
        self.cod_prod.insert(0, valores[0])
        self.quant_prod.delete(0, tk.END)
        self.quant_prod.insert(0, valores[1])
        self.desc_prod.delete(0, tk.END)
        self.desc_prod.insert(0, valores[2])
        self.unit_prod.delete(0, tk.END)
        self.unit_prod.insert(0, valores[3])

    def atualizar_produto(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return

        cod = self.cod_prod.get().strip()
        quant = self.quant_prod.get().strip()
        desc = self.desc_prod.get().strip()
        unit = self.unit_prod.get().strip()

        if not cod or not quant or not desc or not unit:
            messagebox.showwarning("Aviso", "Preencha todos os campos do produto.")
            return

        try:
            quant_float = float(quant.replace(',', '.'))
            unit_float = float(unit.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Unitário devem ser números válidos.")
            return

        total = quant_float * unit_float

        self.tree.item(self.item_selecionado, values=(cod, quant, desc, f"{unit_float:.2f}", f"{total:.2f}"))

        index = self.tree.index(self.item_selecionado)
        self.produtos[index] = {
            "cod": cod,
            "quant": quant_float,
            "desc": desc,
            "unit": unit_float,
            "total": total
        }

        self.limpar_campos_produto()
        self.atualizar_valor_total()
        self.item_selecionado = None
        self.tree.selection_remove(self.tree.selection())

    def excluir_produto(self):
        selecionados = self.tree.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
        for item in selecionados:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.produtos[index]
        self.limpar_campos_produto()
        self.atualizar_valor_total()
        self.item_selecionado = None

    def limpar_campos_produto(self):
        self.cod_prod.delete(0, tk.END)
        self.quant_prod.delete(0, tk.END)
        self.desc_prod.delete(0, tk.END)
        self.unit_prod.delete(0, tk.END)

    def atualizar_valor_total(self):
        total_geral = sum(prod["total"] for prod in self.produtos)
        self.valor_total.configure(state='normal')
        self.valor_total.delete(0, tk.END)
        self.valor_total.insert(0, f"{total_geral:.2f}")
        self.valor_total.configure(state='readonly')

    def gerar_resumo(self):
        resumo = f"Nota de Devolução - Resumo\n\n"
        resumo += f"Cliente: {self.nome.get()}\n"
        resumo += f"Cód. Cliente: {self.cod_cli.get()}\n"
        resumo += f"CPF: {self.cpf.get()}\n"
        resumo += f"PDV: {self.pdv.get()}\n\n"
        resumo += f"Data: {self.data.get()}\n"
        resumo += f"Nº Pedido: {self.n_ped.get()}\n"
        resumo += f"Data Pedido: {self.data_pedido.get()}\n"
        resumo += f"Nº Cupom: {self.n_cupom.get()}\n\n"
        resumo += "Produtos Devolvidos:\n"
        resumo += f"{'Cód':<8}{'Quant':<8}{'Descrição':<30}{'Unit':<10}{'Total':<10}\n"
        resumo += "-"*70 + "\n"
        for p in self.produtos:
            resumo += f"{p['cod']:<8}{p['quant']:<8.2f}{p['desc']:<30}{p['unit']:<10.2f}{p['total']:<10.2f}\n"
        resumo += "-"*70 + "\n"
        resumo += f"Valor Total: {self.valor_total.get()}\n"
        resumo += f"Assinatura Responsável: {self.ass_responsavel.get()}\n"

        messagebox.showinfo("Resumo da Nota", resumo)

    def salvar_txt(self):
        nome = self.nome.get().strip()
        cod_cli = self.cod_cli.get().strip()
        data = self.data.get().strip()
        n_ped = self.n_ped.get().strip()
        cpf = self.cpf.get().strip()
        data_pedido = self.data_pedido.get().strip()
        pdv = self.pdv.get().strip()
        n_cupom = self.n_cupom.get().strip()
        assinatura = self.ass_responsavel.get().strip()
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M")

        if not nome or not data:
            messagebox.showwarning("Aviso", "Os campos 'Nome' e 'Data' são obrigatórios para salvar o arquivo.")
            return

        header = (
            "+" + "-"*80 + "+\n"
            "|{:^80}|\n".format("COMERCIAL ALLANE - ROMANEIO DE DEVOLUCAO") +
            "+" + "-"*80 + "+\n\n"
        )

        dados = (
            "CLIENTE : {:<35} COD CLIENTE : {:<10}\n".format(nome, cod_cli) +
            "DATA    : {:<35} N. PEDIDO   : {:<10}\n".format(data, n_ped) +
            "CPF     : {:<35} DATA PEDIDO\t: {:<10}\n".format(cpf, data_pedido) +
            "PDV     : {:<35} N. CUPOM  \t: {:<10}\n\n".format(pdv, n_cupom)
        )

        tabela = (
            "+" + "-"*8 + "+" + "-"*8 + "+" + "-"*42 + "+" + "-"*11 + "+" + "-"*11 + "+\n"
            "| {:^6} | {:^6} | {:^40} | {:^9} | {:^9} |\n".format("CODIGO", "QUANT.", "DESCRICAO", "UNITARIO", "TOTAL") +
            "+" + "-"*8 + "+" + "-"*8 + "+" + "-"*42 + "+" + "-"*11 + "+" + "-"*11 + "+\n"
        )

        valor_total = 0
        for p in self.produtos:
            valor_total += p["total"]
            tabela += "| {:>6} | {:>6} | {:<40} | R$ {:>7.2f} | R$ {:>7.2f} |\n".format(
                p["cod"], int(p["quant"]), p["desc"][:40], p["unit"], p["total"]
            )
            tabela += "+" + "-"*8 + "+" + "-"*8 + "+" + "-"*42 + "+" + "-"*11 + "+" + "-"*11 + "+\n"

        tabela += "|{:>70} ---->| R$ {:>7.2f} |\n".format("VALOR TOTAL", valor_total)
        tabela += "+" + "-"*8 + "+" + "-"*8 + "+" + "-"*42 + "+" + "-"*11 + "+" + "-"*11 + "+\n\n"

        assinatura_str = "ASSINATURA DO RESPONSAVEL:{:>36} [{}]\n\n".format("", data_hora)

        segunda_via = (
            "="*60 + "\n"
            "|{:^58}|\n".format("SEGUNDA VIA") +
            "="*60 + "\n\n"
            + header + dados + tabela + assinatura_str
        )

        texto = header + dados + tabela + assinatura_str + segunda_via

        try:
            nome_arquivo = f"{nome.replace(' ', '_').upper()}_{data.replace('/','-')}.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(texto)
            messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo}' salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotaDeDevolucaoApp(root)
    root.mainloop()

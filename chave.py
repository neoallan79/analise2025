import tkinter as tk
from tkinter import messagebox, filedialog

def calcular_dv(chave43):
    pesos = list(range(2, 10))
    soma = 0
    peso_index = 0

    for digito in reversed(chave43):
        soma += int(digito) * pesos[peso_index]
        peso_index = (peso_index + 1) % len(pesos)

    resto = soma % 11
    dv = 11 - resto
    if dv >= 10:
        dv = 0
    return str(dv)

def interpretar_chave(chave):
    if len(chave) != 44 or not chave.isdigit():
        return None, "Chave inválida! Deve conter 44 dígitos numéricos."

    chave43 = chave[:43]
    dv_informado = chave[43]
    dv_calculado = calcular_dv(chave43)

    partes = {
        "UF": chave[0:2],
        "Ano e Mês": chave[2:6],
        "CNPJ": chave[6:20],
        "Modelo": chave[20:22],
        "Série": chave[22:25],
        "Número NF": chave[25:34],
        "Código Numérico": chave[34:43],
        "Dígito Verificador": dv_informado,
        "DV Calculado": dv_calculado
    }

    if dv_informado != dv_calculado:
        return partes, f"⚠️ Dígito verificador inválido! Esperado: {dv_calculado}"
    return partes, "✅ Dígito verificador válido."

def formatar_resultado(partes, status):
    return (
        f"UF: {partes['UF']}\n"
        f"Ano e Mês: {partes['Ano e Mês']}\n"
        f"CNPJ: {partes['CNPJ']}\n"
        f"Modelo: {partes['Modelo']}\n"
        f"Série: {partes['Série']}\n"
        f"Número NF: {partes['Número NF']}\n"
        f"Código Numérico: {partes['Código Numérico']}\n"
        f"DV Informado: {partes['Dígito Verificador']}\n"
        f"DV Calculado: {partes['DV Calculado']}\n"
        f"\n{status}"
    )

def on_verificar():
    chave = entrada.get().strip()
    partes, status = interpretar_chave(chave)
    if not partes:
        messagebox.showerror("Erro", status)
        return

    resultado = formatar_resultado(partes, status)
    resultado_label.config(text=resultado)
    janela.resultado_atual = resultado
    janela.numero_nf_atual = partes['Número NF']

def on_exportar():
    if not hasattr(janela, 'resultado_atual') or not janela.resultado_atual:
        messagebox.showwarning("Aviso", "Nenhum resultado para exportar. Realize a verificação primeiro.")
        return

    numero_nf = getattr(janela, 'numero_nf_atual', 'NF')
    filename_sugerido = f"NF_{numero_nf}.txt"

    filepath = filedialog.asksaveasfilename(
        initialfile=filename_sugerido,
        defaultextension=".txt",
        filetypes=[("Arquivo de Texto", "*.txt")],
        title="Salvar resultado como..."
    )
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(janela.resultado_atual)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo.\n{e}")

# GUI
janela = tk.Tk()
janela.title("Validador de Chave de Acesso NF-e")
janela.geometry("500x450")

tk.Label(janela, text="Digite a chave de acesso (44 dígitos):").pack(pady=5)
entrada = tk.Entry(janela, width=60)
entrada.pack(pady=5)

tk.Button(janela, text="Verificar", command=on_verificar).pack(pady=10)
tk.Button(janela, text="Exportar para TXT", command=on_exportar).pack(pady=5)

resultado_label = tk.Label(janela, text="", justify="left", font=("Courier", 10))
resultado_label.pack(pady=10)

janela.resultado_atual = ""
janela.numero_nf_atual = "NF"

janela.mainloop()

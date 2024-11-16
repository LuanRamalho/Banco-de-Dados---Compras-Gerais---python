import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Nome do arquivo de banco de dados JSON
db_name = 'compras_loja.json'

# Carrega dados do banco de dados JSON
def load_data():
    if os.path.exists(db_name):
        with open(db_name, 'r') as file:
            return json.load(file)
    return []

# Salva dados no banco de dados JSON
def save_data():
    with open(db_name, 'w') as file:
        json.dump(product_list, file, indent=4)

# Função para atualizar a tabela
def update_table():
    for row in table.get_children():
        table.delete(row)
    
    total_price = 0
    for idx, product in enumerate(product_list, start=1):
        sub_total = product['quantidade'] * product['preco']
        total_price += sub_total
        table.insert('', 'end', values=(idx, product['codigo'], product['nome'], 
                                        product['quantidade'], f"R$ {product['preco']:.2f}", 
                                        f"R$ {sub_total:.2f}"))
    
    total_price_label.config(text=f"R$ {total_price:.2f}")
    calculate_change()
    save_data()

# Função para calcular o troco
def calculate_change():
    try:
        total_price = float(total_price_label.cget("text").replace("R$", "").strip())
        valor_pago = float(valor_pago_entry.get())
        if valor_pago >= total_price:
            troco = valor_pago - total_price
            troco_label.config(text=f"R$ {troco:.2f}")
        else:
            troco_label.config(text="R$ 0.00")
    except ValueError:
        troco_label.config(text="R$ 0.00")

# Função para adicionar produto
def add_product():
    try:
        codigo = codigo_entry.get()
        nome = nome_entry.get()
        quantidade = int(quantidade_entry.get())
        preco = float(preco_entry.get())

        if codigo and nome and quantidade > 0 and preco > 0:
            product_list.append({
                "codigo": codigo,
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco
            })
            update_table()
            clear_form()
        else:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")

# Função para limpar formulário
def clear_form():
    codigo_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)

# Função para buscar produtos
def search_product(event=None):
    query = search_entry.get().lower()
    for row in table.get_children():
        table.delete(row)

    for idx, product in enumerate(product_list, start=1):
        if query in product['codigo'].lower() or query in product['nome'].lower():
            sub_total = product['quantidade'] * product['preco']
            table.insert('', 'end', values=(idx, product['codigo'], product['nome'], 
                                            product['quantidade'], f"R$ {product['preco']:.2f}", 
                                            f"R$ {sub_total:.2f}"))

# Função para editar produto
def edit_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Erro", "Selecione um produto para editar.")
        return

    idx = table.index(selected_item[0])
    produto = product_list[idx]

    try:
        produto["codigo"] = codigo_entry.get()
        produto["nome"] = nome_entry.get()
        produto["quantidade"] = int(quantidade_entry.get())
        produto["preco"] = float(preco_entry.get())
        update_table()
        clear_form()
    except ValueError:
        messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")

# Função para excluir produto
def delete_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Erro", "Selecione um produto para excluir.")
        return

    idx = table.index(selected_item[0])
    product_list.pop(idx)
    update_table()

# Carregar dados ao iniciar
product_list = load_data()

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Sistema de Cadastro de Produtos")
root.geometry("800x600")
root.configure(bg="#74ebd5")

# Títulos e labels principais
tk.Label(root, text="Cadastro de Produtos", font=("Segoe UI", 20, "bold"), bg="#74ebd5", fg="white").pack(pady=10)

# Formulário de cadastro
form_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="sunken")
form_frame.pack(pady=10)

codigo_entry = ttk.Entry(form_frame)
nome_entry = ttk.Entry(form_frame)
quantidade_entry = ttk.Entry(form_frame)
preco_entry = ttk.Entry(form_frame)

for text, entry in zip(["Código do Produto", "Nome do Produto", "Quantidade", "Preço"], 
                       [codigo_entry, nome_entry, quantidade_entry, preco_entry]):
    ttk.Label(form_frame, text=text).pack(anchor="w", padx=5)
    entry.pack(pady=5, fill="x")

ttk.Button(form_frame, text="Adicionar Produto", command=add_product).pack(pady=5)

# Barra de busca
search_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="sunken")
search_frame.pack(pady=10)
search_entry = ttk.Entry(search_frame)
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", search_product)
ttk.Label(search_frame, text="Buscar Produto: ").pack(side="left")

# Exibição de preço total e troco
total_price_label = tk.Label(root, text="R$ 0.00", font=("Segoe UI", 14, "bold"), fg="#ff7043", bg="#74ebd5")
total_price_label.pack()
valor_pago_entry = ttk.Entry(root)
valor_pago_entry.pack(pady=5)
valor_pago_entry.bind("<KeyRelease>", lambda e: calculate_change())

tk.Label(root, text="Troco: ", font=("Segoe UI", 14), bg="#74ebd5").pack()
troco_label = tk.Label(root, text="R$ 0.00", font=("Segoe UI", 14, "bold"), fg="#ff7043", bg="#74ebd5")
troco_label.pack()

# Frame para os botões de edição e exclusão, agora posicionado acima da tabela
action_frame = tk.Frame(root, bg="#74ebd5")
action_frame.pack(pady=10)
ttk.Button(action_frame, text="Editar Produto", command=edit_product).grid(row=0, column=0, padx=5)
ttk.Button(action_frame, text="Excluir Produto", command=delete_product).grid(row=0, column=1, padx=5)

# Tabela de produtos com barra de rolagem horizontal
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

columns = ("ID", "Código", "Nome", "Quantidade", "Preço", "Sub-Total")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.pack(side="left", fill="both", expand=True)

for col in columns:
    table.heading(col, text=col)

# Inicializa a tabela
update_table()

root.mainloop()

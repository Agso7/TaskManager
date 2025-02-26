import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class TaskManager:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="22@Harrypotter22", 
                database="Task_manager",
                auth_plugin="mysql_native_password"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print("Erro ao conectar no MySQL:", e)
            self.conn = None
            self.cursor = None

    def add_user(self, name, email):
        if not self.cursor:
            messagebox.showerror("Erro", "Não está conectado ao banco de dados")
            return
        try:
            self.cursor.execute("INSERT INTO user_table (name, email) VALUES (%s, %s)", (name, email))
            self.conn.commit()
        except mysql.connector.Error as e:
            print("Erro ao adicionar usuário:", e)

    def add_task(self, title, description, status, user_id):
        if not self.cursor:
            messagebox.showerror("Erro", "Não está conectado ao banco de dados")
            return
        try:
            self.cursor.execute("INSERT INTO task_table (title, description, status, user_id) VALUES (%s, %s, %s, %s)",
                                (title, description, status, user_id))
            self.conn.commit()
        except mysql.connector.Error as e:
            print("Erro ao adicionar tarefa:", e)

    def get_users(self):
        if not self.cursor:
            return []
        self.cursor.execute("SELECT * FROM user_table")
        return self.cursor.fetchall()

    def get_tasks(self):
        if not self.cursor:
            return []
        self.cursor.execute("SELECT * FROM task_table")
        return self.cursor.fetchall()

    def tasks_to_json(self):
        if not self.cursor:
            messagebox.showerror("Erro", "Banco de dados não conectado")
            return
        
        self.cursor.execute("SELECT * FROM task_table")
        tasks = self.cursor.fetchall()

        data = []
        for row in tasks:
            task_data = {
                "task_id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "user_id": row[4]
            }
            data.append(task_data)

        with open("tasks.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        
        messagebox.showinfo("Exportação", "As tarefas foram exportadas pra tasks.json")

    def clear_users(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que quer apagar TODOS os usuários? Isso não pode ser desfeito!"):
            self.cursor.execute("DELETE FROM user_table")
            self.conn.commit()
            messagebox.showinfo("Sucesso!", "Todos os usuários foram apagados!")

    def clear_tasks(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que quer apagar TODAS as tarefas? Isso não pode ser desfeito!"):
            self.cursor.execute("DELETE FROM task_table")
            self.conn.commit()
            messagebox.showinfo("Sucesso!", "Todas as tarefas foram apagadas!")

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# Funções da interface
def add_user():
    name = simpledialog.askstring("Adicionar Usuário", "Digite o nome do usuário")
    email = simpledialog.askstring("Adicionar Usuário", "Digite o email do usuário")

    if name and email:
        manager.add_user(name=name,)
        messagebox.showinfo("Sucesso!", "Usuário adicionado!")
    else:
        messagebox.showerror("Erro", "Nome e email são obrigatórios!")

def add_task():
    title = simpledialog.askstring("Adicionar Tarefa", "Digite o título da tarefa")
    if not title:
        messagebox.showerror("Erro", "Título é obrigatório!")
        return
    
    description = simpledialog.askstring("Adicionar Tarefa", "Digite a descrição da tarefa")
    status = simpledialog.askstring("Adicionar Tarefa", "Digite o status (Pendente, Em Andamento, Concluído)")
    
    if status not in ["Pendente", "Em Andamento", "Concluído"]:
        messagebox.showerror("Erro", "O status deve ser 'Pendente', 'Em Andamento' ou 'Concluído'!")
        return
    
    user_id = simpledialog.askinteger("Adicionar Tarefa", "Digite o ID do usuário responsável")
    
    if not user_id:
        messagebox.showerror("Erro", "O ID do usuário é obrigatório!")
        return
    
    user_exists = manager.check_user_exists(user_id)
    if not user_exists:
        messagebox.showerror("Erro", f"O usuário com ID {user_id} não existe!")
        return
    
    try:
        manager.add_task(title, description, status, user_id)
        messagebox.showinfo("Sucesso!", "Tarefa adicionada!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao adicionar tarefa: {e}")



def view_users():
    top = tk.Toplevel(root)
    top.title("Usuários Cadastrados")
    tree = ttk.Treeview(top, columns=('ID', 'Nome', 'Email'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Email', text='Email')

    users = manager.get_users()
    if not users:
        messagebox.showerror("Erro", "Nenhum usuário encontrado")
    for user in users:
        tree.insert('', tk.END, values=user)

    tree.pack(expand=True, fill=tk.BOTH)

def view_tasks():
    top = tk.Toplevel(root)
    top.title("Tarefas Cadastradas")
    tree = ttk.Treeview(top, columns=('ID', 'Título', 'Descrição', 'Status', 'Usuário ID'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Título', text='Título')
    tree.heading('Descrição', text='Descrição')
    tree.heading('Status', text='Status')
    tree.heading('Usuário ID', text='Usuário ID')

    tasks = manager.get_tasks()
    if not tasks:
        messagebox.showerror("Erro", "Nenhuma tarefa encontrada")
    for task in tasks:
        tree.insert('', tk.END, values=task)

    tree.pack(expand=True, fill=tk.BOTH)


# Janela principal
manager = TaskManager()
root = tk.Tk()
root.title("TaskFlow - Gerenciador de Tarefas")

# Botões da interface
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Button(frame, text="Adicionar Usuário", command=add_user).grid(row=0, column=0, padx=10)
tk.Button(frame, text="Adicionar Tarefa", command=add_task).grid(row=0, column=1, padx=10)
tk.Button(frame, text="Ver Usuários", command=view_users).grid(row=1, column=0, padx=10, pady=5)
tk.Button(frame, text="Ver Tarefas", command=view_tasks).grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame, text="Exportar JSON", command=manager.tasks_to_json).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Limpar Usuários", command=manager.clear_users, fg="red").grid(row=3, column=0, pady=5)
tk.Button(frame, text="Limpar Tarefas", command=manager.clear_tasks, fg="red").grid(row=3, column=1, pady=5)



root.mainloop()

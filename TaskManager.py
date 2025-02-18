import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

# Classes de usuários e tarefas
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Task:
    def __init__(self, task_id, title, description, status, user):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.user = user

# Classe que manipula as tarefas
class TaskManager:
    def __init__(self):
        self.users = []
        self.tasks = []

    def add_user(self, user_id, name, email):
        for user in self.users:
            if user.user_id == user_id:
                raise Exception("ID já existe!")
        self.users.append(User(user_id, name, email))

    def add_task(self, task_id, title, description, status, user_id):
        user_found = None
        for user in self.users:
            if user.user_id == user_id:
                user_found = user
                break
        if user_found is None:
            raise Exception("Usuário não encontrado!")
        for task in self.tasks:
            if task.task_id == task_id:
                raise Exception("ID de tarefa já existe!")
        self.tasks.append(Task(task_id, title, description, status, user_found))

    def get_users(self):
        return self.users

    def get_tasks(self):
        return self.tasks

    def tasks_to_json(self, filename='tasks.json'):
        data = []
        for task in self.tasks:
            data.append({
                'task_id': task.task_id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'user_id': task.user.user_id
            })
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return "Tarefas exportadas para " + filename

# interface
def add_user():
    user_id = simpledialog.askinteger("Adicionar Usuário", "Digite o ID do usuário")
    name = simpledialog.askstring("Adicionar Usuário", "Digite o nome do usuário")
    email = simpledialog.askstring("Adicionar Usuário", "Digite o email do usuário")
    try:
        manager.add_user(user_id, name, email)
        messagebox.showinfo("Sucesso!", "Usuário adicionado!")
    except Exception as e:
        messagebox.showerror("Erro!", str(e))

def add_task():
    task_id = simpledialog.askinteger("Adicionar Tarefa", "Digite o ID da tarefa")
    title = simpledialog.askstring("Adicionar Tarefa", "Digite o título da tarefa")
    description = simpledialog.askstring("Adicionar Tarefa", "Digite a descrição")
    status = simpledialog.askstring("Adicionar Tarefa", "Digite o status")
    user_id = simpledialog.askinteger("Adicionar Tarefa", "Digite o ID do usuário")
    try:
        manager.add_task(task_id, title, description, status, user_id)
        messagebox.showinfo("Sucesso!", "Tarefa adicionada!")
    except Exception as e:
        messagebox.showerror("Erro!", str(e))

def view_users():
    top = tk.Toplevel(root)
    top.title("Ver Usuários")
    tree = ttk.Treeview(top, columns=('User ID', 'Name', 'Email'), show='headings')
    tree.heading('User ID', text='ID')
    tree.heading('Name', text='Nome')
    tree.heading('Email', text='Email')
    for user in manager.get_users():
        tree.insert('', tk.END, values=(user.user_id, user.name, user.email))
    tree.pack(expand=True, fill=tk.BOTH)

def view_tasks():
    top = tk.Toplevel(root)
    top.title("Ver Tarefas")
    tree = ttk.Treeview(top, columns=('Task ID', 'Title', 'Description', 'Status', 'User ID'), show='headings')
    tree.heading('Task ID', text='ID da Tarefa')
    tree.heading('Title', text='Título')
    tree.heading('Description', text='Descrição')
    tree.heading('Status', text='Status')
    tree.heading('User ID', text='ID do Usuário')
    for task in manager.get_tasks():
        tree.insert('', tk.END, values=(task.task_id, task.title, task.description, task.status, task.user.user_id))
    tree.pack(expand=True, fill=tk.BOTH)

def tasks_to_json():
    response = manager.tasks_to_json()
    messagebox.showinfo("Exportação", response)

root = tk.Tk()
root.title("Sistema de Gerenciamento de Tarefas")
manager = TaskManager()

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Adicionar Usuário", command=add_user)
file_menu.add_command(label="Adicionar Tarefa", command=add_task)
file_menu.add_command(label="Ver Usuários", command=view_users)
file_menu.add_command(label="Ver Tarefas", command=view_tasks)
file_menu.add_command(label="Exportar Tarefas para JSON", command=tasks_to_json)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=root.quit)

root.mainloop()

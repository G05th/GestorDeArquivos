import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import ttkbootstrap as tb
import subprocess

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Arquivos")
        self.root.geometry("800x500")
        self.style = tb.Style("darkly")
        
        self.frame_top = tb.Frame(self.root, padding=10)
        self.frame_top.pack(fill=tk.X)
        
        self.entry_path = tb.Entry(self.frame_top, width=50)
        self.entry_path.pack(side=tk.LEFT, padx=5)
        
        self.btn_browse = tb.Button(self.frame_top, text="Selecionar Pasta", command=self.browse_folder)
        self.btn_browse.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh = tb.Button(self.frame_top, text="Atualizar", command=self.load_files)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Nome", "Tamanho", "Tipo"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Tamanho", text="Tamanho")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frame_bottom = tb.Frame(self.root, padding=10)
        self.frame_bottom.pack(fill=tk.X)
        
        self.btn_open = tb.Button(self.frame_bottom, text="Abrir", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)
        
        self.btn_rename = tb.Button(self.frame_bottom, text="Renomear", command=self.rename_file)
        self.btn_rename.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = tb.Button(self.frame_bottom, text="Excluir", command=self.delete_file)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.btn_create_folder = tb.Button(self.frame_bottom, text="Criar Pasta", command=self.create_folder)
        self.btn_create_folder.pack(side=tk.LEFT, padx=5)
        
        self.btn_move = tb.Button(self.frame_bottom, text="Mover", command=self.move_file)
        self.btn_move.pack(side=tk.LEFT, padx=5)
        
        self.btn_copy = tb.Button(self.frame_bottom, text="Copiar", command=self.copy_file)
        self.btn_copy.pack(side=tk.LEFT, padx=5)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)
            self.load_files()
    
    def load_files(self):
        folder = self.entry_path.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Erro", "Pasta inválida!")
            return
        
        self.tree.delete(*self.tree.get_children())
        for item in os.listdir(folder):
            path = os.path.join(folder, item)
            size = os.path.getsize(path)
            tipo = "Pasta" if os.path.isdir(path) else "Arquivo"
            self.tree.insert("", tk.END, values=(item, f"{size} bytes", tipo))
    
    def delete_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um arquivo para excluir")
            return
        
        file_name = self.tree.item(selected_item, "values")[0]
        folder = self.entry_path.get()
        file_path = os.path.join(folder, file_name)
        
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            self.load_files()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")
    
    def create_folder(self):
        folder = self.entry_path.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Erro", "Pasta inválida!")
            return
        
        new_folder = simpledialog.askstring("Nova Pasta", "Digite o nome da nova pasta:")
        if new_folder:
            os.makedirs(os.path.join(folder, new_folder), exist_ok=True)
            self.load_files()
    
    def open_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um arquivo para abrir")
            return
        
        file_name = self.tree.item(selected_item, "values")[0]
        folder = self.entry_path.get()
        file_path = os.path.join(folder, file_name)
        
        if os.path.isdir(file_path):
            messagebox.showinfo("Aviso", "Não é possível abrir pastas diretamente")
        else:
            subprocess.run(["xdg-open", file_path], check=False)
    
    def rename_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um arquivo para renomear")
            return
        
        file_name = self.tree.item(selected_item, "values")[0]
        folder = self.entry_path.get()
        old_path = os.path.join(folder, file_name)
        
        new_name = simpledialog.askstring("Renomear", "Digite o novo nome:")
        if new_name:
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            self.load_files()
    
    def move_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um arquivo para mover")
            return
        
        file_name = self.tree.item(selected_item, "values")[0]
        folder = self.entry_path.get()
        old_path = os.path.join(folder, file_name)
        
        new_folder = filedialog.askdirectory()
        if new_folder:
            new_path = os.path.join(new_folder, file_name)
            shutil.move(old_path, new_path)
            self.load_files()
    
    def copy_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um arquivo para copiar")
            return
        
        file_name = self.tree.item(selected_item, "values")[0]
        folder = self.entry_path.get()
        old_path = os.path.join(folder, file_name)
        
        new_folder = filedialog.askdirectory()
        if new_folder:
            new_path = os.path.join(new_folder, file_name)
            shutil.copy2(old_path, new_path)
            self.load_files()

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = FileManagerApp(root)
    root.mainloop()

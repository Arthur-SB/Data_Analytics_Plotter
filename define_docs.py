import tkinter as tk
from tkinter import filedialog, Scrollbar, Canvas
from PIL import Image, ImageTk
from fpdf import FPDF

def select_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("PNG files", "*.png")])
    
    for path in file_paths:
        add_image_frame(path)

# Função para adicionar um frame de imagem com opções
def add_image_frame(image_path):
    img = Image.open(image_path)
    img.thumbnail((200, 200))  # Redimensiona a imagem para o preview
    img_tk = ImageTk.PhotoImage(img)
    
    # Frame para cada imagem e seu campo de texto
    frame = tk.Frame(preview_frame, bg="white", bd=2, relief="solid")
    frame.pack(anchor='w', pady=5)
#A ser implementado no futuro



# from tkinter import font as tkfont
# from tkinter import filedialog
# from tkinter import messagebox
# from tkinter import ttk
# from tkinter import *

# from datetime import datetime
# from fpdf import FPDF

# import matplotlib.pyplot as plt
# import pandas as pd
# import os

# def page_two():
#     page_two = Tk() #Starter window

#     width = 1100
#     height = 650

#     color_background = "#1f1f1f"
#     color_canva_main = "#181818"
#     color_canva_main_outline = "#181818"
#     color_line = "#FED700"
#     color_text="White"
#     color_text_light = "#404040"

#     text_top = "PDF"
#     text_open_button = "Abrir Imagens"
#     text_pdf_button = "Gerar PDF"

#     image_for_main_path = "resource/for_branco.png"
#     dir_res_icon = "resource/for_preto_icon.ico"

#     title_font = tkfont.Font(size=14, weight='bold')
#     button_font = tkfont.Font(family='Inter', size=14)
#     debug_font = tkfont.Font(family='Inter', size=12)

#     page_two.geometry(f'{width}x{height}+270+70')
#     page_two.resizable(False, False)
#     page_two.title(text_top)
#     page_two.iconbitmap(dir_res_icon)
#     page_two.configure(bg = color_background)

#     #região cinza escuro no topo
#     canvas_sidetop = Canvas(
#         page_two,
#         width=width,
#         height=90,
#         bg=color_canva_main,
#         highlightbackground=color_canva_main_outline,
#         borderwidth=0)
#     canvas_sidetop.place(x=0,y=0)

#     #Linha amarela do topo
#     line_top = Canvas(
#         page_two,
#         width=10000,
#         height=1,
#         bg=color_line,
#         highlightcolor=color_line,
#         highlightthickness=0,
#         highlightbackground=color_line,
#         borderwidth=0
#     )
#     line_top.place(x=0,y=94)

#     Debug = Text(
#         page_two,
#         bg=color_canva_main,
#         fg=color_text,
#         font=debug_font,
#         height=10,  # Ajuste a altura conforme necessário
#         width=80,  # Ajuste a largura conforme necessário
#         wrap=WORD,  # Define quebra automática de linha
#         state=NORMAL  # Permite edição (mude para DISABLED se não quiser permitir edição pelo usuário)
#     )
#     Debug.place(x=300, y=450)

#     #Botão abrir arquivo
#     button_open = Button(
#         page_two,
#         text=text_open_button,
#         font=button_font,
#         bg=color_canva_main,
#         fg=color_text,
#         activebackground=color_canva_main,
#         activeforeground=color_text,
#         relief="groove",
#         cursor='hand2',
#         width=18
#     )
#     button_open.place(x=35,y=30)

#     #Botão gerar pdf
#     button_image = Button(
#         page_two,
#         text=text_pdf_button,
#         font=button_font,
#         bg=color_canva_main,
#         fg=color_text,
#         activebackground=color_canva_main,
#         activeforeground=color_text,
#         relief="groove",
#         cursor='hand2',
#         width=18
#     )
#     button_image.place(x=270, y=30)

#     page_two.mainloop() #Finish window
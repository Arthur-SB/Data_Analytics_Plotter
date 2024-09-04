from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

import define
import docs

import matplotlib.pyplot as plt
import pandas as pd
import os


page_one = Tk() #Starter window

width = 1100
height = 650

color_background = "#1f1f1f"
color_canva_main = "#181818"
color_canva_main_outline = "#181818"
color_line = "#FED700"
color_text="White"
color_text_light = "#404040"

text_top = "Data Analyser Plotter"
text_open_button = "Abrir Arquivos"
text_imagem_button = "Gerar Imagem"
text_pdf_button = "PDF"
text_ia_button = "Machine Learn"
text_debug = "Esperando .CSV"

image_for_main_path = "resource/for_branco.png"
dir_res_icon = "resource/for_preto_icon.ico"

dir_folder_plotter = ['plotter/lap','plotter/laptime','plotter/logs']

title_font = tkfont.Font(size=14, weight='bold')
button_font = tkfont.Font(family='Inter', size=14)
debug_font = tkfont.Font(family='Inter', size=12)


#---------- Mensagem ----------#


df = []
df_org = []
col_index = []
axisx_lap = []
axisx_laptime = []
axisx_log = 0
var_axisy = StringVar()
var_axisx = StringVar()
var_axisy_all = IntVar(value=0)
var_axisx_all = IntVar(value=0)
var_max = IntVar(value=1)
var_min = IntVar(value=1)
var_avg = IntVar(value=1)
var_range = IntVar(value=1)
var_absmax = IntVar(value=1)


#---------- Funções ----------#


def def_open():    
    global axisx_log
    global dir_folder_plotter

    Debug['text'] = "Processando"

    for folder in dir_folder_plotter:
        define.clear_file(folder)

    df_, df_org_, col_index_, name_file_, tam_bytes_, axisx_lap_, axisx_laptime_, axisx_log_ = define.open_csv()

    df.clear()
    df.append(df_)

    df_org.clear()
    df_org.append(df_org_)

    col_index.clear()
    col_index.extend(col_index_)

    axisx_lap.clear()
    axisx_lap.extend(axisx_lap_)

    axisx_laptime.clear()
    axisx_laptime.extend(axisx_laptime_)

    axisx_log = axisx_log_

    combobox_data['values'] = col_index_
    text_2['text'] = name_file_
    text_3['text'] = f"{tam_bytes_}" + " Bytes"

    Debug['text'] = "Carregado"

def def_image():
    msg_tranm = [var_axisy.get(),var_axisx.get(),var_axisy_all.get(),var_axisx_all.get(),var_max.get(),var_min.get(),var_avg.get(),var_range.get(),var_absmax.get()]
    define.prepare_msg(msg_tranm, df, df_org, col_index, axisx_lap, axisx_laptime, axisx_log)
    Debug['text'] = "Imagem gerada"

def def_ia():
    Debug['text'] = "Visualização"

def def_pdf():
    docs.page_two()
    Debug['text'] = "PDF Gerado"


#---------- Code ----------#

page_one.geometry(f'{width}x{height}+250+50')
page_one.resizable(False, False)
page_one.title(text_top)
page_one.iconbitmap(dir_res_icon)
page_one.configure(bg = color_background)

#região cinza escuro no topo
canvas_sidetop = Canvas(
    page_one,
    width=width,
    height=90,
    bg=color_canva_main,
    highlightbackground=color_canva_main_outline,
    borderwidth=0)
canvas_sidetop.place(x=0,y=0)

#região cinza escuro do lado esquerdo
canvas_sideleft = Canvas(
    page_one,
    width=250,
    bg=color_canva_main,
    highlightbackground=color_canva_main_outline,
    borderwidth=2
)
canvas_sideleft.pack(fill='both',side='left')

#Linha amarela da esquerda
line_left = Canvas(
    page_one,
    width=1,
    height=10000,
    bg=color_line,
    highlightcolor=color_line,
    highlightthickness=0,
    highlightbackground=color_line,
    borderwidth=0
)
line_left.place(x=258,y=94)

#Linha amarela do topo
line_top = Canvas(
    page_one,
    width=10000,
    height=1,
    bg=color_line,
    highlightcolor=color_line,
    highlightthickness=0,
    highlightbackground=color_line,
    borderwidth=0
)
line_top.place(x=258,y=94)

#Texto do topo da janela
canvas_sidetop.create_text(
    670,
    50,
    text=text_top,
    font=title_font,
    fill=color_text,
    anchor='center'
)

#Imagem do formula
image_main = PhotoImage(file=image_for_main_path)
logo = Label(
    page_one,
    image=image_main,
    justify="center",
    anchor="center",
    bg=color_canva_main)
logo.place(x=40,y=2)

#Botão abrir arquivo
button_open = Button(
    page_one,
    text=text_open_button,
    font=button_font,
    bg=color_canva_main,
    fg=color_text,
    activebackground=color_canva_main,
    activeforeground=color_text,
    command=def_open,
    relief="groove",
    cursor='hand2',
    width=22
)
button_open.place(x=3,y= 200)

#Botão gerar imagem
button_image = Button(
    page_one,
    text=text_imagem_button,
    font=button_font,
    bg=color_canva_main,
    fg=color_text,
    activebackground=color_canva_main,
    activeforeground=color_text,
    command=def_image,
    relief="groove",
    cursor='hand2',
    width=22
)
button_image.place(x=3, y=270)

#A ser implementado no futuro

# #Botão visualização
# button_ia = Button(
#     page_one,
#     text=text_ia_button,
#     font=button_font,
#     bg=color_canva_main,
#     fg=color_text,
#     activebackground=color_canva_main,
#     activeforeground=color_text,
#     command=def_ia,
#     relief="groove",
#     cursor='hand2',
#     width=22
# )
# button_ia.place(x=3,y= 340)

# #Botão pdf
# button_pdf = Button(
#     page_one,
#     text=text_pdf_button,
#     font=button_font,
#     bg=color_canva_main,
#     fg=color_text,
#     activebackground=color_canva_main,
#     activeforeground=color_text,
#     command=def_pdf,
#     relief="groove",
#     cursor='hand2',
#     width=22
# )
# button_pdf.place(x=3,y= 410)

Debug = Label(
    page_one,
    text=text_debug,
    bg=color_canva_main,
    fg=color_text,
    font=debug_font,
    width=20,
    justify='center'
)
Debug.place(x=40,y=620)

text_1 = Label(
    page_one,
    text="Dado (Eixo y):",
    bg=color_background,
    fg=color_text,
    font=debug_font,
    width=15,
    justify='center'
)
text_1.place(x=305,y=188)

text_2 = Label(
    page_one,
    text="-",
    bg=color_canva_main,
    fg=color_text,
    font=debug_font,
    width=20,
    justify='center'
)
text_2.place(x=40,y=530)

text_3 = Label(
    page_one,
    text="-",
    bg=color_canva_main,
    fg=color_text,
    font=debug_font,
    width=20,
    justify='center'
)
text_3.place(x=40,y=560)

combobox_data = ttk.Combobox(
    page_one,
    justify='center',
    textvariable=var_axisy,
    height=5,
    values= [],
    width=50,
)
combobox_data.place(x=460,y=190)

text_4 = Label(
    page_one,
    text="Tempo (Eixo x):",
    bg=color_background,
    fg=color_text,
    font=debug_font, 
    width=15,
    justify='center'
)
text_4.place(x=305,y=278)

combobox_x = ttk.Combobox(
    page_one,
    justify='center',
    values=['Lap','Lap Time','Logs'],
    textvariable=var_axisx,
    height=5,
    width=50,
)
combobox_x.place(x=460,y=280)

check1 = Checkbutton(
    page_one,
    height=1,
    width=4,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Todos',
    font=debug_font,
    variable=var_axisy_all
)
check1.place(x=460,y=215)

check2 = Checkbutton(
    page_one,
    height=1,
    width=4,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Todos',
    font=debug_font,
    variable=var_axisx_all
)
check2.place(x=460,y=305)

canvas_units = Canvas(
    page_one,
    width=150,
    height=220,
    bg=color_background,
    highlightbackground="white",
    borderwidth=2
)
canvas_units.place(x=870,y=125)

text_5 = Label(
    page_one,
    text="Estatística",
    bg=color_background,
    fg=color_text,
    font=debug_font,
    width=15,
    justify='center'
)
text_5.place(x=880,y=148)

check_max = Checkbutton(
    page_one,
    height=1,
    width=8,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Max',
    font=debug_font,
    variable=var_max
)
check_max.place(x=900,y=180)

check_min = Checkbutton(
    page_one,
    height=1,
    width=8,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Min',
    font=debug_font,
    variable=var_min
)
check_min.place(x=900,y=210)

check_avg = Checkbutton(
    page_one,
    height=1,
    width=8,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Avg',
    font=debug_font,
    variable=var_avg
)
check_avg.place(x=900,y=240)

check_range = Checkbutton(
    page_one,
    height=1,
    width=8,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Range',
    font=debug_font,
    variable=var_range
)
check_range.place(x=900,y=270)

check_absmax = Checkbutton(
    page_one,
    height=1,
    width=8,
    bg=color_background,
    fg=color_text,
    activebackground=color_background,
    activeforeground=color_text,
    selectcolor=color_background,
    text='Abs Max',
    font=debug_font,
    variable=var_absmax
)
check_absmax.place(x=900,y=300)

page_one.mainloop() #Finish window
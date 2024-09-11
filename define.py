from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import matplotlib.pyplot as plt
import pandas as pd
import docs
import re
import os

frames = []
current_frame = 0
dict_docs = {}

def msg_warning():
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    messagebox.showwarning("Aviso", "Algo faltando ou incorreto")
    root.destroy()  # Fecha a janela principal

def clear_file(folder):
    if os.path.exists(folder):
        # Itera sobre todos os itens na folder
        for arquivo_ou_folder in os.listdir(folder):
            caminho_completo = os.path.join(folder, arquivo_ou_folder)
            # Remove arquivos
            if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                os.unlink(caminho_completo)

def prepare_df(df):
    # Acessar a primeira linha e criar novos nomes de colunas
    first_row = df.iloc[0]
    df.columns = [f'{first_row.iloc[i]}_{col}' for i, col in enumerate(df.columns)]
    
    # Remover a primeira linha que foi usada para renomear as colunas
    df = df.drop(0).reset_index(drop=True)
    
    # Limpar nomes de colunas, removendo sufixos desnecessários
    df.columns = df.columns.str.replace('.1', '', regex=False)
    df.columns = df.columns.str.replace('.2', '', regex=False)
    df.columns = df.columns.str.replace('.3', '', regex=False)
    df.columns = df.columns.str.replace('.4', '', regex=False)

    df.iloc[:, 2] = df.iloc[:, 2].str.replace(', ', '', regex=False)

    # Tratar valores na coluna específica
    if "nan_Unnamed: 3" in df.columns:
        df["nan_Unnamed: 3"] = df["nan_Unnamed: 3"].str.strip().apply(lambda x: x[:8])

    df["nan_Unnamed: 2"] = pd.to_datetime(df["nan_Unnamed: 2"], format='%d/%m/%Y')

    axisx_lap = df.iloc[:, 4]
    axisx_log = df.shape[0]

    df_org = df.sort_values(by='nan_Unnamed: 5')

    axisx_laptime = df_org.iloc[:, 5]

    df_org = df_org.drop(df_org.columns[:6], axis=1)
    df = df.drop(df.columns[:6], axis=1)

    return df, df_org, axisx_lap, axisx_laptime, axisx_log

def open_csv():
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file:
        return None, None, None, None
    
    df_complete = pd.read_csv(file)
    df_complete.to_csv('csv_backup/database_complete.csv', index=False)

    df, df_org, axisx_lap, axisx_laptime, axisx_log = prepare_df(df_complete)

    col_index = [col.split('_', 1)[-1] for col in df.columns]  # Mantém tudo após o primeiro "_"
    col_index = list(set(col_index))  # Remove duplicatas
    col_index.sort()

    name_file = os.path.basename(file)
    tam_bytes = os.path.getsize(file)

    df_org.to_csv('csv_backup/database_organized.csv', index=False)
    df.to_csv('csv_backup/database_main.csv', index=False)

    return df, df_org, col_index, name_file, tam_bytes, axisx_lap, axisx_laptime, axisx_log

#msg_tranm = [var_axisy.get(),var_axisx.get(),var_axisy_all.get(),var_axisx_all.get(),var_max.get(),var_min.get(),var_avg.get(),var_range.get(),var_absmax.get()]
# Nome do eixo y = 0
# Nome do eixo x = 1
# Check all eixo y = 2
# Check all eixo x = 3
# Check Max = 4
# Check Min = 5
# Check Avg = 6
# Check Range = 7
# Check AbsMax = 8

def prepare_msg(msg_tranm, df, df_org, col_index, axisx_lap, axisx_laptime, axisx_log):

    df = pd.DataFrame(df[0])
    df_org = pd.DataFrame(df_org[0])

    # if msg_tranm[0] == FALSE or msg_tranm[1] == FALSE or msg_tranm[2] == FALSE or msg_tranm[3] == FALSE:
    #     print(msg_tranm[0])
    #     print(msg_tranm[1])
    #     print(msg_tranm[2])
    #     print(msg_tranm[3])
    #     msg_warning()

    if msg_tranm[2]:
        axisy = col_index
    elif msg_tranm[0]:  # Verifica se msg_tranm[0] tem um valor
        axisy = msg_tranm[0]


    if msg_tranm[3]:
        axisx = axisx_lap
        num_lin = axisx_log
        gen_imagem_lap(axisx,axisy,num_lin,msg_tranm,df)

        axisx = axisx_laptime
        gen_imagem_laptime(axisx,axisy,msg_tranm,df_org)

        axisx = axisx_log
        gen_imagem_log(axisx,axisy,msg_tranm,df)

    elif msg_tranm[1] == 'Lap':
        axisx = axisx_lap
        num_lin = axisx_log
        gen_imagem_lap(axisx,axisy,num_lin,msg_tranm,df)

    elif msg_tranm[1] == 'Lap Time':
        axisx = axisx_laptime
        gen_imagem_laptime(axisx,axisy,msg_tranm,df_org)

    elif msg_tranm[1] == 'Logs':
        axisx = axisx_log
        gen_imagem_log(axisx,axisy,msg_tranm,df)

def gen_imagem_lap(axisx,axisy,num_lin,msg_tranm,df):

    axisx_num = list(range(0, num_lin))

    if not msg_tranm[2]:
        plt.figure(figsize=(28, 14))
        img = plt.imread('resource/marca.png')
        plt.figimage(img, xo=100, yo=730, alpha=0.4)

        if msg_tranm[4]:
            try:
                plt.plot(axisx, df[f"Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
            except KeyError:
                pass

        if msg_tranm[5]:
            try:
                plt.plot(axisx, df[f"Min_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
            except KeyError:
                pass

        if msg_tranm[6]:
            try:
                plt.plot(axisx, df[f"Avg_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
            except KeyError:
                pass

        if msg_tranm[7]:
            try:
                plt.plot(axisx, df[f"Range_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
            except KeyError:
                pass

        if msg_tranm[8]:
            try:
                plt.plot(axisx, df[f"Abs Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
            except KeyError:
                pass

        plt.xlabel("Lap", fontsize=22)
        plt.xticks(ticks=axisx_num, labels=axisx,fontsize=22, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=22)
        plt.yticks(fontsize=22)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Lap's X {axisy}", fontsize=24, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=22, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/lap/lap X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 14))
            img = plt.imread('resource/marca.png')
            plt.figimage(img, xo=100, yo=730, alpha=0.4)

            if msg_tranm[4]:
                try:
                    plt.plot(axisx, df[f"Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
                except KeyError:
                    pass

            if msg_tranm[5]:
                try:
                    plt.plot(axisx, df[f"Min_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
                except KeyError:
                    pass

            if msg_tranm[6]:
                try:
                    plt.plot(axisx, df[f"Avg_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
                except KeyError:
                    pass

            if msg_tranm[7]:
                try:
                    plt.plot(axisx, df[f"Range_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
                except KeyError:
                    pass

            if msg_tranm[8]:
                try:
                    plt.plot(axisx, df[f"Abs Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
                except KeyError:
                    pass

            plt.xlabel("Lap", fontsize=22)
            plt.xticks(ticks=axisx_num, labels=axisx,fontsize=22, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=22)
            plt.yticks(fontsize=22)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Lap's X {axisy_}", fontsize=24, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=22, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/lap/lap X {axisy_}.png")
            plt.close()

def gen_imagem_laptime(axisx,axisy,msg_tranm,df_org):

    if not msg_tranm[2]:
        plt.figure(figsize=(28, 14))
        img = plt.imread('resource/marca.png')
        plt.figimage(img, xo=100, yo=730, alpha=0.4)

        if msg_tranm[4]:
            try:
                plt.plot(axisx, df_org[f"Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
            except KeyError:
                pass

        if msg_tranm[5]:
            try:
                plt.plot(axisx, df_org[f"Min_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
            except KeyError:
                pass

        if msg_tranm[6]:
            try:
                plt.plot(axisx, df_org[f"Avg_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
            except KeyError:
                pass

        if msg_tranm[7]:
            try:
                plt.plot(axisx, df_org[f"Range_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
            except KeyError:
                pass

        if msg_tranm[8]:
            try:
                plt.plot(axisx, df_org[f"Abs Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
            except KeyError:
                pass

        plt.xlabel("Lap Time", fontsize=22)
        plt.xticks(ticks=axisx, labels=axisx,fontsize=22, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=22)
        plt.yticks(fontsize=22)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Lap Time [mm:ss] X {axisy}", fontsize=24, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=22, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/laptime/laptime X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 14))
            img = plt.imread('resource/marca.png')
            plt.figimage(img, xo=100, yo=730, alpha=0.4)

            if msg_tranm[4]:
                try:
                    plt.plot(axisx, df_org[f"Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
                except KeyError:
                    pass

            if msg_tranm[5]:
                try:
                    plt.plot(axisx, df_org[f"Min_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
                except KeyError:
                    pass

            if msg_tranm[6]:
                try:
                    plt.plot(axisx, df_org[f"Avg_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
                except KeyError:
                    pass

            if msg_tranm[7]:
                try:
                    plt.plot(axisx, df_org[f"Range_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
                except KeyError:
                    pass

            if msg_tranm[8]:
                try:
                    plt.plot(axisx, df_org[f"Abs Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
                except KeyError:
                    pass

            plt.xlabel("Lap Time", fontsize=22)
            plt.xticks(ticks=axisx, labels=axisx,fontsize=22, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=22)
            plt.yticks(fontsize=22)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Lap Time [mm:ss] X {axisy_}", fontsize=24, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=22, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/laptime/laptime X {axisy_}.png")
            plt.close()
    
def gen_imagem_log(axisx,axisy,msg_tranm,df):

    axisx = list(range(1, axisx+1))

    if not msg_tranm[2]:
        plt.figure(figsize=(28, 14))
        img = plt.imread('resource/marca.png')
        plt.figimage(img, xo=100, yo=730, alpha=0.4)

        if msg_tranm[4]:
            try:
                plt.plot(axisx, df[f"Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
            except KeyError:
                pass

        if msg_tranm[5]:
            try:
                plt.plot(axisx, df[f"Min_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
            except KeyError:
                pass

        if msg_tranm[6]:
            try:
                plt.plot(axisx, df[f"Avg_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
            except KeyError:
                pass

        if msg_tranm[7]:
            try:
                plt.plot(axisx, df[f"Range_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
            except KeyError:
                pass

        if msg_tranm[8]:
            try:
                plt.plot(axisx, df[f"Abs Max_{axisy}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
            except KeyError:
                pass

        plt.xlabel("Log", fontsize=22)
        plt.xticks(ticks=axisx, labels=axisx,fontsize=22, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=22)
        plt.yticks(fontsize=22)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Log's X {axisy}", fontsize=24, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=22, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/logs/logs X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 14))
            img = plt.imread('resource/marca.png')
            plt.figimage(img, xo=100, yo=730, alpha=0.4)

            if msg_tranm[4]:
                try:
                    plt.plot(axisx, df[f"Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Max')
                except KeyError:
                    pass

            if msg_tranm[5]:
                try:
                    plt.plot(axisx, df[f"Min_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Min')
                except KeyError:
                    pass

            if msg_tranm[6]:
                try:
                    plt.plot(axisx, df[f"Avg_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Avg')
                except KeyError:
                    pass

            if msg_tranm[7]:
                try:
                    plt.plot(axisx, df[f"Range_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='Range')
                except KeyError:
                    pass

            if msg_tranm[8]:
                try:
                    plt.plot(axisx, df[f"Abs Max_{axisy_}"].astype(str).str.replace(',', '.').apply(float), marker='o', linewidth=2, label='AbsMax')
                except KeyError:
                    pass

            plt.xlabel("Log", fontsize=22)
            plt.xticks(ticks=axisx, labels=axisx,fontsize=22, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=22)
            plt.yticks(fontsize=22)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Log's X {axisy_}", fontsize=24, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=22, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/logs/logs X {axisy_}.png")
            plt.close()

def page_two():
    page_two = Toplevel()  # Starter window

    width = 1100
    height = 650

    color_background = "#1f1f1f"
    color_canva_main = "#181818"
    color_canva_main_outline = "#181818"
    color_line = "#FED700"
    color_text = "White"
    color_text_light = "#404040"

    text_top = "PDF"
    text_open_button = "Abrir Imagens"
    text_pdf_button = "Gerar Docs"
    text_next_button = "Página"
    text_frame_intro = "Introdução"
    text_frame_subject = "Conteúdo"
    text_frame_end = "Conclusão"

    dir_for_main = "resource/for_branco.png"
    dir_res_icon = "resource/for_preto_icon.ico"

    title_font = tkfont.Font(size=14)
    button_font = tkfont.Font(family='Inter', size=14)
    debug_font = tkfont.Font(family='Inter', size=12)

    style = ttk.Style()
    style.configure("Default.TFrame", background=color_background)

    def show_frame(index):
        global current_frame
        frames[current_frame].place_forget()  # Esconder o frame atual
        current_frame = index % len(frames)   # Garantir que o índice seja cíclico
        frames[current_frame].place(x=5, y=120, width=1090, height=545)  # Mostrar o novo frame

    def show_next_frame():
        show_frame(current_frame + 1)  # Ir para o próximo frame

    def open_images():
        filenames = filedialog.askopenfilenames(
            title="Selecione as imagens",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        for i, filename in enumerate(filenames):
            image_frame = ttk.Frame(page_two, style="Default.TFrame")

            img = Image.open(filename)
            img.thumbnail((840, 300))
            img_tk = ImageTk.PhotoImage(img)

            # Adicionar imagem ao frame
            image_label = Label(image_frame, image=img_tk, bg=color_background)
            image_label.image = img_tk  # Manter referência da imagem para não ser coletada pelo garbage collector
            image_label.place(x=125, y=110)

            text_box = Text(
                image_frame,
                bg=color_canva_main,
                fg=color_text,
                font=debug_font,
                height=4,  # Ajuste a altura conforme necessário
                width=110,  # Ajuste a largura conforme necessário
                wrap=WORD,  # Define quebra automática de linha
                state=NORMAL  # Permite edição (mude para DISABLED se não quiser permitir edição pelo usuário)
            )
            text_box.place(x=50, y=430)

            title_text = Label(
                image_frame,
                text="Titulo:",
                font=title_font,
                bg=color_background,
                fg=color_text,
                anchor='center'
            )
            title_text.place(x=60, y=20)

            title = Text(
                image_frame,
                bg=color_canva_main,
                fg=color_text,
                font=debug_font,
                height=2,  # Ajuste a altura conforme necessário
                width=50,  # Ajuste a largura conforme necessário
                wrap=WORD,  # Define quebra automática de linha
                state=NORMAL  # Permite edição (mude para DISABLED se não quiser permitir edição pelo usuário)
            )
            title.place(x=60, y=50)

            font_text = Label(
                image_frame,
                text="Fonte:",
                font=title_font,
                bg=color_background,
                fg=color_text,
                anchor='center'
            )
            font_text.place(x=600, y=20)

            font = Text(
                image_frame,
                bg=color_canva_main,
                fg=color_text,
                font=debug_font,
                height=2,  # Ajuste a altura conforme necessário
                width=50,  # Ajuste a largura conforme necessário
                wrap=WORD,  # Define quebra automática de linha
                state=NORMAL  # Permite edição (mude para DISABLED se não quiser permitir edição pelo usuário)
            )
            font.place(x=600, y=50)

            frames.append(image_frame)

            # Adicionar o caminho da imagem e a referência ao campo de texto ao dicionário
            dict_docs[f"imagem {i+1}"] = [title,font,text_box,filename]


    def documentation():
        for image_key, widgets in dict_docs.items():
            # Extraindo os widgets da lista
            title_widget, font_widget, text_widget, filename = widgets

            # Pegando o texto de cada widget
            title_text = title_widget.get("1.0", END).strip()  # Texto do título
            font_text = font_widget.get("1.0", END).strip()  # Texto da fonte
            description_text = text_widget.get("1.0", END).strip()  # Texto da descrição

            # Atualizando o dicionário com os textos
            dict_docs[image_key] = {
                "title": title_text,
                "font": font_text,
                "description": description_text,
                "filename": filename
            }

        name_report = intro_teste_name.get("1.0", END).strip()
        objetivo = intro_teste_obj.get("1.0", END).strip()
        responsible = intro_teste_resp.get("1.0", END).strip()
        driver = intro_teste_driver.get("1.0", END).strip()
        date = intro_teste_date.get("1.0", END).strip()
        hour_in = intro_teste_hour_in.get("1.0", END).strip()
        hour_out = intro_teste_hour_out.get("1.0", END).strip()
        local = intro_teste_loc.get("1.0", END).strip()
        problem = end_problem.get("1.0", END).strip()
        conclusion = end_conclusion.get("1.0", END).strip()

        dict_docs["name_report"] = name_report
        dict_docs["objetivo"] = objetivo
        dict_docs["responsible"] = responsible
        dict_docs["driver"] = driver
        dict_docs["date"] = date
        dict_docs["hour_in"] = hour_in
        dict_docs["hour_out"] = hour_out
        dict_docs["local"] = local
        dict_docs["problem"] = problem
        dict_docs["conclusion"] = conclusion

        docs.report(dict_docs)

    page_two.geometry(f'{width}x{height}+270+70')
    page_two.resizable(False, False)
    page_two.title(text_top)
    page_two.iconbitmap(dir_res_icon)
    page_two.configure(bg=color_background)

    # Região cinza escuro no topo
    canvas_sidetop = Canvas(
        page_two,
        width=width,
        height=110,
        bg=color_canva_main,
        highlightbackground=color_canva_main_outline,
        borderwidth=0)
    canvas_sidetop.place(x=0, y=0)

    # Linha amarela do topo
    line_top = Canvas(
        page_two,
        width=10000,
        height=1,
        bg=color_line,
        highlightcolor=color_line,
        highlightthickness=0,
        highlightbackground=color_line,
        borderwidth=0
    )
    line_top.place(x=0, y=114)

    #Imagem do formula
    for_main = PhotoImage(file=dir_for_main)
    logo = Label(
        page_two,
        image=for_main,
        justify="center",
        anchor="center",
        bg=color_canva_main)
    logo.place(x=40,y=-5)

    # Botão abrir arquivo
    button_open = Button(
        page_two,
        text=text_open_button,
        font=button_font,
        bg=color_canva_main,
        fg=color_text,
        activebackground=color_canva_main,
        activeforeground=color_text,
        relief="groove",
        cursor='hand2',
        width=18,
        command=open_images
    )
    button_open.place(x=335, y=40)

    # Botão gerar pdf
    button_image = Button(
        page_two,
        text=text_pdf_button,
        font=button_font,
        bg=color_canva_main,
        fg=color_text,
        activebackground=color_canva_main,
        activeforeground=color_text,
        relief="groove",
        cursor='hand2',
        width=18,
        command=documentation
    )
    button_image.place(x=570, y=40)

    button_next = Button(
        page_two,
        text=text_next_button,
        font=button_font,
        bg=color_canva_main,
        fg=color_text,
        command=show_next_frame,
        activebackground=color_canva_main,
        activeforeground=color_text,
        relief="groove",
        cursor='hand2',
        width=10
    )
    button_next.place(x=870, y=40)

    intro = ttk.Frame(page_two, style="Default.TFrame")
    end = ttk.Frame(page_two, style="Default.TFrame")

    frames = [intro, end]

    intro_text1 = Label(
        intro,
        text="Nome do teste:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text1.place(x=60, y=10)

    intro_teste_name = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=110,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_name.place(x=60, y=45)

    intro_text2 = Label(
        intro,
        text="Objetivo do teste:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text2.place(x=60, y=110)

    intro_teste_obj = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=6,
        width=110,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_obj.place(x=60, y=145)

    intro_text7 = Label(
        intro,
        text="Responsável:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text7.place(x=60, y=290)

    intro_teste_resp = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=50,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_resp.place(x=60, y=325)

    intro_text8 = Label(
        intro,
        text="Pilotos:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text8.place(x=600, y=290)

    intro_teste_driver = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=50,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_driver.place(x=600, y=325)

    intro_text3 = Label(
        intro,
        text="Data:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text3.place(x=60, y=405)

    intro_teste_date = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=20,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_date.place(x=60, y=440)

    intro_text4 = Label(
        intro,
        text="Horario iniciado:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text4.place(x=330, y=405)

    intro_teste_hour_in = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=20,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_hour_in.place(x=330, y=440)

    intro_text5 = Label(
        intro,
        text="Horario finalizado:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text5.place(x=600, y=405)

    intro_teste_hour_out = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=20,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_hour_out.place(x=600, y=440)

    intro_text6 = Label(
        intro,
        text="Local:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    intro_text6.place(x=870, y=405)

    intro_teste_loc = Text(
        intro,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=2,
        width=20,
        wrap=WORD,
        state=NORMAL
    )
    intro_teste_loc.place(x=870, y=440)

    end_text1 = Label(
        end,
        text="Problemas e Soluções:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    end_text1.place(x=60, y=10)

    end_problem = Text(
        end,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=12,
        width=110,
        wrap=WORD,
        state=NORMAL
    )
    end_problem.place(x=60, y=45)

    end_text2 = Label(
        end,
        text="Conclusão:",
        font=title_font,
        bg=color_background,
        fg=color_text,
        anchor='center'
    )
    end_text2.place(x=60, y=285)

    end_conclusion = Text(
        end,
        bg=color_canva_main,
        fg=color_text,
        font=debug_font,
        height=8,
        width=110,
        wrap=WORD,
        state=NORMAL
    )
    end_conclusion.place(x=60, y=320)

    show_frame(0)
    page_two.mainloop()  # Finish window
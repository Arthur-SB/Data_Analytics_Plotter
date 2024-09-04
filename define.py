from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

import matplotlib.pyplot as plt
import pandas as pd
import re
import os

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
        plt.figure(figsize=(28, 10))
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

        plt.xlabel("Lap", fontsize=18)
        plt.xticks(ticks=axisx_num, labels=axisx,fontsize=12, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=18)
        plt.yticks(fontsize=12)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Lap's X {axisy}", fontsize=18, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=13, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/lap/lap X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 10))
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

            plt.xlabel("Lap", fontsize=18)
            plt.xticks(ticks=axisx_num, labels=axisx,fontsize=12, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=18)
            plt.yticks(fontsize=12)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Lap's X {axisy_}", fontsize=18, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=13, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/lap/lap X {axisy_}.png")
            plt.close()

def gen_imagem_laptime(axisx,axisy,msg_tranm,df_org):

    if not msg_tranm[2]:
        plt.figure(figsize=(28, 10))
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

        plt.xlabel("Lap Time", fontsize=18)
        plt.xticks(ticks=axisx, labels=axisx,fontsize=12, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=18)
        plt.yticks(fontsize=12)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Lap Time [mm:ss] X {axisy}", fontsize=18, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=13, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/laptime/laptime X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 10))
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

            plt.xlabel("Lap Time", fontsize=18)
            plt.xticks(ticks=axisx, labels=axisx,fontsize=12, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=18)
            plt.yticks(fontsize=12)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Lap Time [mm:ss] X {axisy_}", fontsize=18, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=13, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/laptime/laptime X {axisy_}.png")
            plt.close()
    
def gen_imagem_log(axisx,axisy,msg_tranm,df):

    axisx = list(range(1, axisx+1))

    if not msg_tranm[2]:
        plt.figure(figsize=(28, 10))
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

        plt.xlabel("Log", fontsize=18)
        plt.xticks(ticks=axisx, labels=axisx,fontsize=12, rotation=-15)
        plt.ylabel(f"{axisy}", fontsize=18)
        plt.yticks(fontsize=12)
        plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

        plt.title(f"Log's X {axisy}", fontsize=18, loc='left', pad=20, verticalalignment='center')
        plt.tight_layout()
        plt.legend(fontsize=13, loc='upper right', frameon=True)
        plt.grid(True)

        axisy = re.sub(r'[^\w\s]','', axisy)

        plt.savefig(f"plotter/logs/logs X {axisy}.png")
        plt.close()

    elif msg_tranm[2]:
        for axisy_ in axisy:

            plt.figure(figsize=(28, 10))
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

            plt.xlabel("Log", fontsize=18)
            plt.xticks(ticks=axisx, labels=axisx,fontsize=12, rotation=-15)
            plt.ylabel(f"{axisy_}", fontsize=18)
            plt.yticks(fontsize=12)
            plt.grid(True, color='black', linestyle='--', linewidth=0.4)  # Mudando a cor e estilo da grade

            plt.title(f"Log's X {axisy_}", fontsize=18, loc='left', pad=20, verticalalignment='center')
            plt.tight_layout()
            plt.legend(fontsize=13, loc='upper right', frameon=True)
            plt.grid(True)

            axisy_ = re.sub(r'[^\w\s]','', axisy_)

            plt.savefig(f"plotter/logs/logs X {axisy_}.png")
            plt.close()

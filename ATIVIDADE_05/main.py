from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).parents[0]
DATA_DIR = ROOT_DIR.joinpath( 'data/' )

def main():
    df_transacoes = load_transacoes()
    df_transacoes = tratar_data_transacoes( df_transacoes )
    df_transacoes = tratar_valores_transacoes( df_transacoes )
    df_transacoes = filtrar_transacoes( df_transacoes )
    df_transacoes = gerar_risco( df_transacoes )
    df_transacoes = calcular_z_score( df_transacoes )
    df_transacoes = filtrar_por_z_score( df_transacoes )

    pivot_table = gerar_pivot_table( df_transacoes )

    transacoes_diarias = df_transacoes.groupby('dia')['valor'].sum().to_dict()
    media_movel = calcular_media_movel( df_transacoes )

    display_graph( transacoes_diarias, media_movel )

def load_transacoes() -> pd.DataFrame:
    df = pd.read_csv( DATA_DIR.joinpath( 'transacoes.csv' ), encoding='latin1' )    
    df["plataforma"] = "mobile" 
    return df.drop_duplicates()

def tratar_data_transacoes( df:pd.DataFrame ) -> pd.DataFrame:
    df = df.astype( {"data_transacao":"datetime64[ns]"} ) 
    df["data_transacao"] = df["data_transacao"].dt.tz_localize( 'America/Sao_Paulo' ) 
    df["dia"] = df["data_transacao"].dt.weekday
    df["mes"] = df["data_transacao"].dt.month
    return df

def tratar_valores_transacoes( df:pd.DataFrame ) -> pd.DataFrame:
    df_medias = df.groupby("estado_cliente")["valor"].median()
    df["valor"] = df["valor"].fillna( value=df["estado_cliente"].map( df_medias ) )
    return df

def filtrar_transacoes( df:pd.DataFrame ) -> pd.DataFrame:
    filtro_estado_sp = df["estado_cliente"]  == "SP"
    filtro_estado_mg = df["estado_cliente"]  == "MG"
    filtro_valor = df["valor"] > 5000
    df_filtrado = df[(( filtro_estado_mg | filtro_estado_sp ) & filtro_valor)]
    return df_filtrado

def gerar_risco( df:pd.DataFrame ) -> pd.DataFrame:
    clientes = df.groupby("id_cliente")["id_cliente"].all().to_dict()    
    for key in clientes.keys():
        clientes[key] = str(np.random.choice(['Baixo', 'Medio', 'Alto']))
    df["risco"] = df["id_cliente"].map(clientes) 
    return df

def gerar_pivot_table( df:pd.DataFrame ) -> pd.DataFrame:
    return df.pivot_table(values='valor', index=['mes'], columns=['risco'], aggfunc="sum", margins=True )
    
def calcular_z_score( df:pd.DataFrame ) -> pd.DataFrame:
    # https://medium.com/@amit25173/understanding-groupby-transform-in-pandas-b59954153907
    df['z-score'] = df.groupby('estado_cliente')['valor'].transform( lambda x: (x - x.mean()) / x.std() )
    return df    

def filtrar_por_z_score( df:pd.DataFrame ) -> pd.DataFrame:
    return df[abs(df["z-score"]) <= 2.25]

def calcular_media_movel( df:pd.DataFrame ) -> dict:
    media_movel = pd.DataFrame( df['valor'].rolling(7, min_periods=1).mean() )
    media_movel = pd.concat( [media_movel, df["data_transacao"]], axis=1 ).set_index("data_transacao").sort_index()
    return media_movel.to_dict()['valor']

def display_graph( transacoes_diarias:dict, media_movel:dict ) -> None:
    fig, (ax_top, ax_bottom) = plt.subplots(2,1)

    ax_top.plot(transacoes_diarias.keys(), transacoes_diarias.values())
    ax_bottom.plot(media_movel.keys(), media_movel.values())

    ax_top.set_title('Transações Diarias')
    ax_bottom.set_title('Media Movel')
    
    plt.show()

if __name__ == "__main__": main()

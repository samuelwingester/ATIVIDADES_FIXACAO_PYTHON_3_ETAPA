import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from pathlib import Path 

ROOT_DIR = Path(__file__).parents[0]
DATA_DIR = ROOT_DIR.joinpath('DADOS/')

def main():
    sns.set_palette( sns.color_palette("deep") )

    fig, axs = plt.subplots( 3, 3, figsize=( 20, 10 ) )

    plot_gf_barras( axs[0,0] )
    plot_gf_boxplot( axs[0,1] )
    plot_gf_dispersao( axs[0,2] )
    plot_gf_distribuicao( axs[1,0] )
    plot_gf_frequencia( axs[1,1] )
    plot_gf_heatmap( axs[1,2] )
    plot_gf_linhas( axs[2,0] )
    plot_gf_pizza( axs[2,1] )
    plot_gf_regressao( axs[2,2] )

    plt.tight_layout()
    plt.show()

def load_csv( name:str ) -> pd.DataFrame:
    return pd.read_csv( DATA_DIR.joinpath( 'dados_' + name + '.csv' ) )

def plot_gf_barras( ax ): 
    sns.barplot( 
        data=load_csv( 'barras' ), x='regiao', y='vendas_medias', 
        hue='categoria', ax=ax 
    )

    ax.set_title("Média de Vendas por Região", fontsize=14, fontweight="bold")
    ax.set_xlabel("Região", fontsize=11)
    ax.set_ylabel("Media Vendas ($)", fontsize=11)
    ax.legend(title="Categorias", frameon=True)

def plot_gf_boxplot( ax ):
    sns.barplot( data=load_csv( 'boxplot' ), x='departamento', y='salario', ax=ax )

    ax.set_title("Salario por Deparatamento", fontsize=14, fontweight="bold")
    ax.set_xlabel("departamento", fontsize=11)
    ax.set_ylabel("salario", fontsize=11)

def plot_gf_dispersao( ax ):
    df = load_csv( 'dispersao' )

    sns.regplot( 
        data=df[ df['sexo'] == 'Masculino' ], x="altura_cm", y="peso_kg", 
        scatter=True, color="red", ax=ax
    )

    sns.regplot( 
        data=df[ df['sexo'] == 'Feminino' ], x="altura_cm", y="peso_kg", 
        scatter=True, color="blue", ax=ax
    )

    ax.set_title("Disperção de pesos e alturas por sexo", fontsize=14, fontweight="bold")
    ax.set_xlabel("Altura (CM)", fontsize=11)
    ax.set_ylabel("Peso (KG)", fontsize=11)

def plot_gf_distribuicao( ax ):
    sns.histplot( data=load_csv( 'distribuicao' ), x='idade', bins=20, kde=True, stat='percent', ax=ax  )

    ax.set_title("Distribuição de idades", fontsize=14, fontweight="bold")
    ax.set_xlabel("idade", fontsize=11)

def plot_gf_frequencia( ax ):
    sns.countplot( 
        data=load_csv( 'frequencia' ), x='tipo_atendimento', stat='count', 
        hue='tipo_atendimento', ax=ax
    )

    ax.set_title("Frequencia de Atendimentos", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tipo de Atendimento", fontsize=11)

def plot_gf_heatmap( ax ):
    df = load_csv( 'heatmap' )
    
    df = df.pivot( index='dia_semana', columns='horario', values='movimento_clientes'  )

    sns.heatmap( data=df, ax=ax, cmap='coolwarm' )

    ax.set_title("Movimento na semana", fontsize=14, fontweight="bold")
    ax.set_xlabel("Dia", fontsize=11)
    ax.set_ylabel("Horario", fontsize=11)

def plot_gf_linhas( ax ):
    sns.lineplot( data=load_csv( 'linhas' ), x='data', y='vendas', hue='loja', ax=ax )
    
    ax.set_title("Vendas", fontsize=14, fontweight="bold")
    ax.set_xlabel("Data", fontsize=11)
    ax.set_ylabel("Valor", fontsize=11)

def plot_gf_pizza( ax ):
    df = load_csv( 'pizza' )

    ax.pie( x=df['faturamento'].tolist(), labels=df['canal_venda'].tolist() )
    
    ax.set_title("Faturamento por canal", fontsize=14, fontweight="bold")

def plot_gf_regressao( ax ):
    sns.regplot( data=load_csv( 'regressao' ), x='renda_mensal', y='gasto_mensal', scatter=True, ax=ax )

    ax.set_title("Renda e Gasto Mensais", fontsize=14, fontweight="bold")
    ax.set_xlabel("Renda Mensal", fontsize=11)
    ax.set_ylabel("Gasto Mensal", fontsize=11)

if __name__ == '__main__': main()
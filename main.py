import pandas as pd
import streamlit as st
import io

pd.set_option("display.precision", 19)


def make_excel(table):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        table.to_excel(writer, index=False)

    return buffer


# --- Page Config
st.set_page_config(page_title='Filtrar Metabolitos', layout='wide')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title('Filtrar os Metabólitos')

arquivo = st.file_uploader('Insira a tabela dos Metabólitos', accept_multiple_files=False)

if arquivo:
    tabela = pd.read_excel(arquivo)
    tabela['Query.Mass'] = tabela['Query.Mass'].map(lambda x: '{0:.6f}'.format(x))

    gp = tabela.groupby('Query.Mass')

    df = pd.DataFrame(columns=['Query.Mass', 'Matched.Compound', 'Matched.Form', 'Mass.Diff'])

    for nome, tab in gp:
        minimo = tab['Mass.Diff'].min()

        df_temp = tab[tab['Mass.Diff'] == minimo]

        df = pd.merge(df, df_temp, how='outer')

    st.write(df)

    excel_gliri = make_excel(df)

    st.download_button(label=f'Download dos metabólitos filtrados',
                       data=excel_gliri,
                       file_name=f'Metabólitos_Filtrados.xlsx',
                       mime="application/vnd.ms-excel")

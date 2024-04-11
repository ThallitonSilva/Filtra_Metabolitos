import pandas as pd
import streamlit as st
import io

pd.set_option("display.precision", 20)
pd.set_option('display.float_format', '{:.20f}'.format)


def make_excel(tb1, tb2, tb3, tb4):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        tb1.to_excel(writer, sheet_name=f'Raw_Data', index=False)
        tb2.to_excel(writer, sheet_name=f'Filter_QueryMass', index=False)
        tb3.to_excel(writer, sheet_name=f'Filter_MatchedCompound', index=False)
        tb4.to_excel(writer, sheet_name=f'Final_Result', index=False)

    return buffer


def filtro1(tabela):
    gp = tabela.groupby('Query.Mass')

    dff = pd.DataFrame(columns=['ID', 'Query.Mass', 'Matched.Compound', 'Matched.Form', 'Mass.Diff'])

    for nome, tab in gp:
        minimo = tab['Mass.Diff'].min()

        df_temp = tab[tab['Mass.Diff'] == minimo]

        dff = pd.merge(dff, df_temp, how='outer')

    return dff


def filtro2(tabela):
    gp = tabela.groupby('Matched.Compound')

    dff = pd.DataFrame(columns=['Query.Mass', 'Matched.Compound', 'Matched.Form', 'Mass.Diff'])

    for nome, tab in gp:
        minimo = tab['Mass.Diff'].min()

        df_temp = tab[tab['Mass.Diff'] == minimo]

        dff = pd.merge(dff, df_temp, how='outer')

    dff.sort_values('Query.Mass', inplace=True)

    return dff


def filtro3(tabela):
    dff = tabela.drop_duplicates('Query.Mass', keep=False)

    return dff


# --- Page Config
st.set_page_config(page_title='Horario dos Funcionários', layout='wide')

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
    to_filter = pd.read_excel(arquivo)
    to_filter['Query.Mass'] = to_filter['Query.Mass'].map(lambda x: '{0:.6f}'.format(x))

    df = filtro1(to_filter)
    df2 = filtro2(df)
    df3 = filtro3(df2)

    st.write(df3)

    excel = make_excel(to_filter, df, df2, df3)

    st.download_button(label=f'Download dos metabólitos filtrados',
                       data=excel,
                       file_name=f'Metabólitos_Filtrados.xlsx',
                       mime="application/vnd.ms-excel")

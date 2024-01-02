import pandas as pd
import streamlit as st

from functions import *

tab1, tab2 = st.tabs(["Recherche", "Affichage des Données"])

with tab1:
    st.header("Recherche d'Articles")
    keyword = st.text_input("Entrez le mot-clé pour la recherche")
    search_button = st.button("Rechercher")

    if search_button and keyword:
        keyword = keyword.replace(' ', '+')
        data_page_1 = scraping_bdm(keyword, page=1)
        data_page_2 = scraping_bdm(keyword, page=2)

        data = {**data_page_1, **data_page_2}
        df = pd.DataFrame.from_dict(data, orient='index')

        st.session_state['data'] = df

        st.dataframe(df)

        st.download_button(
            label="Télécharger les données en CSV",
            data=st.session_state['data'].to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
            file_name='bdm_articles.csv',
            mime='text/csv',
        )

        st.write(f"Nombre d'articles : {len(df)}")

with tab2:
    st.header("Articles du Blog du Modérateur")

    if 'data' in st.session_state:

        for _, row in st.session_state['data'].iterrows():
            st.subheader(row['title'])
            st.image(row['image'], width=300)
            st.write(f"Date de publication : {row['time']}")
            st.markdown(f"[Lire l'article]({row['link']})", unsafe_allow_html=True)
            st.write("---")
    else:
        st.write("Aucune donnée à afficher. Veuillez effectuer une recherche.")

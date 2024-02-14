# importation de packages
import time

import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs


# caching des données
@st.cache_data
def srappe_terrain_a_vendre(nbr_pages=10):
    df = pd.DataFrame()
    for p in range(1, nbr_pages + 1):
        url = f'https://www.expat-dakar.com/terrains-a-vendre?page={p}'
        resp = get(url)
        soup = bs(resp.text, 'html.parser')
        links_a = soup.find_all('a', class_='listing-card__inner')
        links = [link['href'] for link in links_a]
        data = []
        for link in links:
            res = get(link)
            Soup = bs(res.text, 'html.parser')
            try:
                adresse = Soup.find('span', class_='listing-item__address-location').text.strip()
                prix = (Soup.find('span', class_='listing-card__price__value 1').text.strip()
                        .replace('\u202f', '')
                        .replace(' F Cfa', ''))
                detail = Soup.find('div', class_='listing-item__description').text
                lien_image = soup.find("img", class_="listing-card__image__resource").get("src")
                try:
                    inf = Soup.find_all('dd', class_='listing-item__properties__description')
                    superficie = inf[0].text.strip().replace(' m²', '')
                except:
                    superficie = ''

                obj = {
                    'Détail': detail,
                    'Superficie': superficie,
                    'Adresse': adresse,
                    'Prix': prix,
                    'Lien vers image': lien_image
                }
                data.append(obj)
            except:
                pass

        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
        time.sleep(2)
    return df

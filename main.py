import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import os

URL_BASE = "HIDED_URL"
headers = {'Cookie': 'HIDED_COOKIES',
           'Referer': 'HIDED_URL'}
CHEMIN_DLL = "videos/HIDE/"
HEBERGEUR = "vimeo"


def download_mp3(chemin, dossier, title, bouton):
    print("MP3 detecté : téléchargement...")
    for chiffre, btn in enumerate(bouton):
        if numb >= 1:
            if numb >= 2:
                title = title[:6]
            title += "_part" + str(chiffre + 1)
        with open(chemin + dossier + '/' + title, 'wb') as x:
            x.write(session.get(btn['href']).content)


with requests.Session() as session:
    r = session.get(URL_BASE, headers=headers)
    print(r)
    if r.ok:
        # print("demarrage du telechagement...")
        soup = BeautifulSoup(r.text, 'html.parser')
        navbar = soup.find("nav", {"class": "navbar"})
        liens_videos = navbar.findAll('a')
        # nb_dossier = 1
        for numb, l in enumerate(liens_videos[100:-3]):
            lien = l['href']
            print(lien)
            if lien == '#':
                nom_de_dossier = l.text.replace(' ', '').replace('\n', '').replace("'", '_').casefold()
                print(nom_de_dossier)
                newpath = rf'{CHEMIN_DLL}/{nom_de_dossier}'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                    # nb_dossier += 1

            else:
                r = session.get(lien, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                balise_iframes = soup.findAll('iframe')
                balise_titre = soup.find('div', {'class':'contenu-header'}).find('h1')
                titre = balise_titre.text.replace(' ', '_').replace("'", '_').replace('/', '_').casefold()
                # DLL des MP3
                bouton_mp3 = soup.findAll('a', {'class': 'btn-inverse'})
                try:
                    if bouton_mp3:
                        download_mp3(CHEMIN_DLL, nom_de_dossier, titre, bouton_mp3)
                except requests.exceptions.MissingSchema:
                    continue

                # DLL des videos (mêmes si plusieurs sur une page)
                for nb, iframe in enumerate(balise_iframes):
                    if nb >= 1:
                        titre = balise_titre.text.replace(' ', '_').replace("'", '_').replace('/', '_').casefold()
                        titre += "_part"+str(nb+1)
                    lien_iframe = 'https:' + iframe['src']
                    if HEBERGEUR not in lien_iframe:
                        continue
                    requete_iframe = session.get(lien_iframe, headers=headers)
                    regex = r"https:\/\/[a-zA-Z0-9-_=~%\.\/]+.mp4"
                    lien_final = re.findall(regex, requete_iframe.text)[1]  # change la qualité
                    r = session.get(lien_final)
                    print(r)
                    print(f"Downloading video {numb}/{len(liens_videos)} : {titre}")
                    with open(CHEMIN_DLL + nom_de_dossier + '/' + titre, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                f.write(chunk)
                    print(f"{numb}/{len(liens_videos)} downloaded!\n")

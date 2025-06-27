from flask import Flask, render_template
import random
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime

from fetch_results import get_latest_tirage_links, get_latest_draw_numbers
from numerologie import analyse_numerologique

app = Flask(__name__)

# ---------- CACHE AUTOMATIQUE DU DERNIER TIRAGE ----------
latest_data = {
    "tirage": [],
    "date": "",
    "analyse": [],
    "vibration_totale": 0,
    "vibration_reduite": 0
}

def reduire(n):
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n

def background_update():
    try:
        tirage, date = get_latest_draw_numbers()
        if tirage and date != latest_data["date"]:
            analyse_resultats = analyse_numerologique(tirage)
            vibration_totale = sum(item['chemin'] for item in analyse_resultats)
            vibration_reduite = reduire(vibration_totale)

            latest_data.update({
                "tirage": tirage,
                "date": date,
                "analyse": analyse_resultats,
                "vibration_totale": vibration_totale,
                "vibration_reduite": vibration_reduite
            })
            print(f"[INFO] Nouveau tirage détecté : {tirage} ({date})")
    except Exception as e:
        print(f"[ERREUR] Échec de mise à jour : {e}")

def update_thread():
    while True:
        background_update()
        time.sleep(3600)  # Répète toutes les heures

# ---------- TIRAGE AUTO BASÉ SUR LE CHIFFRE 9 ----------
def get_last_10_tirages():
    links = get_latest_tirage_links(limit=10)
    tirages = []
    for _, url in links:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            p = soup.find("p")
            nums = [int(x) for x in p.text.split() if x.isdigit()]
            if nums:
                tirages.append(nums)
        except Exception as e:
            print(f"[ERREUR] Tirage échoué pour {url} : {e}")
            continue
    return tirages

def chiffres_lies_au_9(tirages):
    flat = [n for sub in tirages for n in sub]
    unique = sorted(set(flat))
    return [n for n in unique if reduire(n) == 9]

# ---------- ROUTES FLASK ----------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tirage')
def tirage():
    numeros = sorted(random.sample(range(1, 100), 5))
    return render_template("tirage.html", numeros=numeros)

@app.route('/analyse')
def analyse():
    return render_template("analyse.html",
        tirage=latest_data["tirage"],
        analyse=latest_data["analyse"],
        date=latest_data["date"],
        vibration_totale=latest_data["vibration_totale"],
        vibration_reduite=latest_data["vibration_reduite"]
    )

@app.route('/historique')
def historique():
    liens = get_latest_tirage_links(limit=10)
    return render_template("historique.html", liens=liens)

@app.route('/tirage9auto')
def tirage9auto():
    tirages = get_last_10_tirages()
    selection = chiffres_lies_au_9(tirages)
    now = datetime.now().strftime("%d/%m/%Y à %Hh%M")
    return render_template("tirage9auto.html", tirage=selection, tirages_bruts=tirages, now=now)

# ---------- DÉMARRAGE ----------
if __name__ == '__main__':
    # 1. Mise à jour immédiate
    background_update()

    # 2. Mise à jour continue en arrière-plan
    threading.Thread(target=update_thread, daemon=True).start()

    # 3. Lancement de Flask
    app.run(debug=True)

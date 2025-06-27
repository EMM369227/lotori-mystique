import requests
from bs4 import BeautifulSoup

def get_latest_loto_results():
    url = "https://lonato-togo.com/resultats-du-loto-boom-tirage-104/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        h1_tags = soup.find_all("h1")
        for tag in h1_tags:
            if "BOOM Tir" in tag.text:
                # Cherche le <p> juste après ce <h1>
                result_text = tag.find_next("p").text
                numbers = [int(n) for n in result_text.split() if n.isdigit()]
                return numbers
        return []
    except Exception as e:
        print(f"Erreur lors du parsing HTML : {e}")
        return []

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lonato-togo.com/loto/resultats/"

def get_latest_tirage_links(limit=5):
    """
    Récupère les liens vers les derniers tirages publiés sur le site de la LONATO.
    Retourne une liste de tuples : (titre, url)
    """
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERREUR] Connexion à LONATO échouée : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a in soup.select("#breaking-news ul li a")[:limit]:
        title = a.get_text(strip=True)
        url = a.get("href")
        if url and url.startswith("http"):
            links.append((title, url))

    return links

def get_all_results():
    """
    Récupère les 10 derniers tirages.
    """
    return get_latest_tirage_links(limit=10)

def get_latest_draw_numbers():
    """
    Extrait les numéros et la date du dernier tirage.
    Retourne : (liste de numéros, date)
    """
    links = get_latest_tirage_links(limit=1)
    if not links:
        return [], "Aucun tirage disponible"

    _, url = links[0]

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERREUR] Chargement du tirage échoué : {e}")
        return [], "Erreur lors du chargement du tirage"

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔍 Extraire les numéros
    numbers = []
    strong_tags = soup.select(".entry-content strong")
    for tag in strong_tags:
        text = tag.get_text()
        nums = [int(n) for n in text.split() if n.isdigit()]
        if len(nums) >= 5:
            numbers = nums[:5]
            break

    # 📅 Extraire la date
    title_tag = soup.select_one(".entry-title")
    date = title_tag.get_text(strip=True) if title_tag else "Date inconnue"

    return numbers, date

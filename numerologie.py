# numerologie.py

def reduce_to_1_digit(n):
    """Réduit un nombre à un seul chiffre par somme des chiffres."""
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n

def analyse_numerologique(tirage):
    """
    Analyse numérologique d'une liste de numéros de tirage.
    Retourne une liste de dictionnaires contenant :
    - nombre : le numéro original
    - chemin : chiffre de chemin de vie (réduit)
    - message : signification mystique du chiffre
    """
    if not tirage or not isinstance(tirage, list):
        return []

    significations = {
        1: "Élan de départ, individualité, puissance de création",
        2: "Coopération, équilibre, sensibilité",
        3: "Expression, créativité, communication",
        4: "Stabilité, structure, fondation solide",
        5: "Changement, liberté, aventure",
        6: "Responsabilité, famille, harmonie",
        7: "Intuition, mystère, connaissance profonde",
        8: "Pouvoir, matérialité, maîtrise",
        9: "Sagesse, spiritualité, accomplissement"
    }

    analyse = []
    for num in tirage:
        if isinstance(num, int) and num > 0:
            chemin = reduce_to_1_digit(num)
            message = significations.get(chemin, "Message inconnu")
            analyse.append({
                'nombre': num,
                'chemin': chemin,
                'message': message
            })

    return analyse

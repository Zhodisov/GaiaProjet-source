import random
from flask import Flask, request, jsonify
import pymysql
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
import requests
import os
import logging

class Configuration:
    SCHEDULER_API_ENABLED = True

application = Flask(__name__)
application.config.from_object(Configuration())
planificateur = APScheduler()
planificateur.init_app(application)
planificateur.start()






config_bd = { #IDENTIFIANT VIA EMAIL
    'user': '', #IDENTIFIANT VIA EMAIL
    'password': '', #IDENTIFIANT VIA EMAIL
    'host': '', #IDENTIFIANT VIA EMAIL
    'port': 14463, #IDENTIFIANT VIA EMAIL
    'database': '', #IDENTIFIANT VIA EMAIL
    'charset': 'utf8mb4', #IDENTIFIANT VIA EMAIL
    'cursorclass': pymysql.cursors.DictCursor  #IDENTIFIANT VIA EMAIL
} #IDENTIFIANT VIA EMAIL






config_bd_locale = { #DATABASE XAMPP
    'user': 'root', #DATABASE XAMPP
    'password': 'WQi]n4Qga)8zKXBp', #DATABASE XAMPP
    'host': 'localhost', #DATABASE XAMPP
    'port': 3306, #DATABASE XAMPP
    'database': 'projetgaia', #DATABASE XAMPP
    'charset': 'utf8mb4', #DATABASE XAMPP
    'cursorclass': pymysql.cursors.DictCursor #DATABASE XAMPP
} #DATABASE XAMPP







cle_api = "" #IDENTIFIANT VIA EMAIL / OPENWEATHER (PLAN ETUDIANT SUR 6 MOIS) - OpenCall 3.0









logging.basicConfig(level=logging.DEBUG)
journal = logging.getLogger(__name__)


# Fonction pour obtenir la connexion à la base de données
def obtenir_connexion_bd():
    journal.debug("Obtention de la connexion à la base de données")
    return pymysql.connect(**config_bd_locale)


# Fonction pour enregistrer les données dans la base de données
def enregistrer_donnees(valeur_mise_a_jour):
    journal.debug("Enregistrement des données : %s", valeur_mise_a_jour)
    connexion = obtenir_connexion_bd()
    try:
        with connexion.cursor() as curseur:
            for cle, valeur in valeur_mise_a_jour.items():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                curseur.execute("""
                    INSERT INTO donnees (Timestamp, DCE, TCEAM, TCEAMB, TCEAV, ENS, EEC, FKIdPosition) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE 
                    DCE=VALUES(DCE), TCEAM=VALUES(TCEAM), TCEAMB=VALUES(TCEAMB), TCEAV=VALUES(TCEAV), ENS=VALUES(ENS), EEC=VALUES(EEC), Timestamp=VALUES(Timestamp)
                """, (timestamp, valeur['DCE'], valeur['TCEAM'], valeur['TCEAMB'], valeur['TCEAV'], valeur['ENS'], valeur['EEC'], valeur['FKIdPosition']))
        connexion.commit()
    finally:
        connexion.close()













# Fonction pour charger les données depuis la base de données
def charger_donnees(numero_client=None):
    journal.debug("Chargement des données pour le client : %s", numero_client)
    connexion = obtenir_connexion_bd()
    try:
        with connexion.cursor() as curseur:
            if numero_client:
                curseur.execute("""
                    SELECT u.Nom, u.Prenom, d.DCE, d.TCEAM, d.TCEAMB, d.TCEAV, d.ENS, d.EEC, d.Timestamp 
                    FROM donnees d
                    JOIN position p ON d.FKIdPosition = p.IdPosition
                    JOIN utilisateur u ON p.FKIdUtilisateur = u.IdUtilisateur
                    WHERE u.NumClient = %s
                """, (numero_client,))
            else:
                curseur.execute("""
                    SELECT u.Nom, u.Prenom, d.DCE, d.TCEAM, d.TCEAMB, d.TCEAV, d.ENS, d.EEC, d.Timestamp 
                    FROM donnees d
                    JOIN position p ON d.FKIdPosition = p.IdPosition
                    JOIN utilisateur u ON p.FKIdUtilisateur = u.IdUtilisateur
                """)
            donnees = curseur.fetchall()
            return donnees
    finally:
        connexion.close()













# Fonction pour trouver les données de l'utilisateur
def trouver_donnees_utilisateur(nom, numero_client):
    journal.debug("Recherche de l'utilisateur : %s, Numéro de client : %s", nom, numero_client)
    connexion = obtenir_connexion_bd()
    try:
        with connexion.cursor() as curseur:
            curseur.execute("SELECT * FROM utilisateur WHERE Nom=%s AND NumClient=%s", (nom, numero_client))
            utilisateur = curseur.fetchone()

            if utilisateur:
                id_utilisateur = utilisateur["IdUtilisateur"]

                curseur.execute("SELECT * FROM position WHERE FKIdUtilisateur=%s", (id_utilisateur,))
                positions_utilisateur = curseur.fetchall()

                curseur.execute("SELECT * FROM donnees WHERE FKIdPosition IN (%s)" % ','.join([str(pos['IdPosition']) for pos in positions_utilisateur]))
                donnees_utilisateur = curseur.fetchall()

                return {
                    "user": utilisateur,
                    "data": donnees_utilisateur,
                    "positions": positions_utilisateur
                }
    finally:
        connexion.close()
    return None












# Route pour la connexion
@application.route('/login', methods=['POST'])
def connexion():
    nom = request.json.get('Nom')
    numero_client = request.json.get('numClient')
    journal.debug("Tentative de connexion pour l'utilisateur : %s, Numéro de client : %s", nom, numero_client)
    donnees_utilisateur = trouver_donnees_utilisateur(nom, numero_client)

    if donnees_utilisateur:
        journal.debug("Utilisateur trouvé : %s", donnees_utilisateur)
        return jsonify({"message": "Utilisateur trouvé", "status": True, "data": donnees_utilisateur})

    journal.debug("Identifiants invalides")
    return jsonify({"message": "Identifiants invalides", "status": False})











# Route pour obtenir les données météorologiques
@application.route('/api/meteo', methods=['GET'])
def obtenir_meteo():

    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    if not latitude or not longitude:
        journal.debug("Coordonnées non fournies")
        return jsonify({"error": "Coordonnées non fournies"}), 400

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={cle_api}&units=metric"
    reponse = requests.get(url)
    if reponse.status_code == 200:
        donnees = reponse.json()
        if 'current' in donnees and 'weather' in donnees['current']:
            code_icone = donnees['current']['weather'][0]['icon']
            url_icone = f"http://openweathermap.org/img/wn/{code_icone}@2x.png"
            temperature = donnees['current']['temp']
            return jsonify({
                "icon_url": url_icone,
                "temperature": temperature,
                "data": donnees
            }), 200
        else:
            journal.debug("error URL API")
            return jsonify({"error URL API": "Données météorologiques pas complet reçues"}), 500
    else:
        journal.debug("error URL API")
        return jsonify({"error URL API": "Impossible de récupérer les données météorologiques"}), 500









# Route pour obtenir les prévision météorologiques
@application.route('/api/prevision', methods=['GET'])
def obtenir_prevision():

    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    date = request.args.get('date')
    journal.debug("Demande de prévision : lat=%s, lon=%s, date=%s", latitude, longitude, date)

    if not latitude or not longitude or not date:
        journal.debug("error : Coordonnées ou date non fournies")
        return jsonify({"error": "Coordonnées ou date non fournies"}), 400

    donnees_meteo = obtenir_donnees_meteo(latitude, longitude, date)
    
    if "error" in donnees_meteo:
        journal.debug("error dans obtenir_donnees_meteo : %s", donnees_meteo['error'])
        return jsonify({"error": donnees_meteo["error"]}), 400

    if donnees_meteo["historical"]:
        historique = donnees_meteo["historical"]
        if 'data' in historique[0] and historique[0]['data']:
            data = historique[0]['data'][0]
            response = {
                "temperature": data.get('temp', None),
                "temperature_min": data.get('temp_min', None),
                "temperature_max": data.get('temp_max', None),
                "precipitations": data.get('rain', {}).get('1h', 0),
                "description": data['weather'][0]['description'],
                "sunrise": data.get('sunrise', None),
                "sunset": data.get('sunset', None),
                "humidity": data.get('humidity', None),
                "uvi": data.get('uvi', None),
                "dew_point": data.get('dew_point', None),
                "wind_speed": data.get('wind_speed', None),
                "wind_deg": data.get('wind_deg', None),
                "wind_gust": data.get('wind_gust', None),
                "clouds": data.get('clouds', None),
                "pop": data.get('pop', None),
                "moonrise": data.get('moonrise', None),
                "moonset": data.get('moonset', None),
                "moon_phase": data.get('moon_phase', None)
            }
            return jsonify(response), 200
        else:
            journal.debug("error : Données historiques non disponibles")
            return jsonify({"error": "Données historiques non disponibles"}), 500
    elif donnees_meteo["forecast"]:
        prevision = donnees_meteo["forecast"]
        response = {
            "temperature": prevision['temp']['day'],
            "temperature_min": prevision['temp']['min'],
            "temperature_max": prevision['temp']['max'],
            "precipitations": prevision.get('rain', 0),
            "description": prevision['weather'][0]['description'],
            "sunrise": prevision['sunrise'],
            "sunset": prevision['sunset'],
            "moonrise": prevision['moonrise'],
            "moonset": prevision['moonset'],
            "moon_phase": prevision['moon_phase'],
            "humidity": prevision['humidity'],
            "dew_point": prevision['dew_point'],
            "wind_speed": prevision['wind_speed'],
            "wind_deg": prevision['wind_deg'],
            "wind_gust": prevision['wind_gust'],
            "clouds": prevision['clouds'],
            "pop": prevision['pop'],
            "uvi": prevision['uvi']
        }
        return jsonify(response), 200
    else:
        journal.debug("error : Données non disponibles")
        return jsonify({"error": "Données non disponibles"}), 500


def obtenir_donnees_meteo(lat, lon, date):

    donnees_meteo = {
        "historical": [],
        "forecast": []
    }

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            journal.debug("error : Format de date invalide")
            return {"error": "Format de date invalide"}

    aujourd_hui = datetime.today()
    journal.debug("Date demandée : %s, Date actuelle : %s", date_obj, aujourd_hui)

    if date_obj < aujourd_hui:
        timestamp = int(date_obj.timestamp())
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={cle_api}&units=metric"
        reponse = requests.get(url)
        if reponse.status_code == 200:
            donnees_meteo["historical"].append(reponse.json())
        else:
            journal.debug("error pour la date %s : %s - %s", date_obj, reponse.status_code, reponse.text)
            return {"error": f"error pour la date {date_obj} : {reponse.status_code} - {reponse.text}"}
    elif date_obj >= aujourd_hui:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={cle_api}&units=metric"
        reponse = requests.get(url)
        if reponse.status_code == 200:
            donnees_prevision = reponse.json()["daily"]
            for jour in donnees_prevision:
                date_prevision = datetime.fromtimestamp(jour["dt"]).date()
                if date_prevision == date_obj.date():
                    donnees_meteo["forecast"] = jour
                    break
        else:
            return {"error": f"error pour la prévision : {reponse.status_code} - {reponse.text}"}

    journal.debug("Données météorologiques obtenues : %s", donnees_meteo)
    return donnees_meteo







# Route pour gérer les données
@application.route('/api/donnees', methods=['GET', 'POST'])
def gerer_donnees():
    if request.method == 'POST':
        contenu = request.json
        journal.debug("Données reçues pour enregistrement : %s", contenu)
        enregistrer_donnees(contenu)
        return jsonify(contenu), 200
    else:
        numero_client = request.args.get('numClient')
        journal.debug("Chargement des données pour le client : %s", numero_client)
        donnees = charger_donnees(numero_client)
        return jsonify({"data": donnees}), 200








# Démarrer l'application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9200))
    application.run(host='0.0.0.0', port=port, debug=True)

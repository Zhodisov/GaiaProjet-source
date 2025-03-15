<br/><br/>
<div align="center"> 
  <img src="https://profile-counter.glitch.me/Zhodisov/count.svg" alt="Visitor's Count" />
</div>
<br/><br/>

<div align="center">
  
[![YOUTUBE](https://img.shields.io/badge/Youtube-fc0000?style=for-the-badge&logo=YOUTUBE&logoColor=white)](https://www.youtube.com/@Jodis974)
[![Discord](https://img.shields.io/badge/Discord-6a85b9?style=for-the-badge&logo=discord&logoColor=white)](https://safemarket.xyz/discord)
[![Safemarket Email](https://img.shields.io/badge/safemarket_email-333333?style=for-the-badge&logo=gmail&logoColor=red)](mailto:support-checkout@safemarket.xyz)
[![safemarket.xyz](https://img.shields.io/badge/safemarket.xyz-0077B5?style=for-the-badge&logo=internet&logoColor=white)](https://safemarket.xyz/)

</div>





## Lancement du Serveur Python et Client Android

### Requis
- Python 3.X.X
- Clé API chez [Openweathermap.org](https://openweathermap.org/)
- Base de données locale (projetgaia.sql importée dans XAMPP, le fichier SQL est fourni)
- Android Studio

### Lancement

1. **Serveur local**
  
- Ouvrir un cmd à l'endroit où se trouve le `server.py`
- Lancer `runServerLocal.bat` ce qui fera l'installation des librairies de `requirements.txt` et lancera le serveur Flask
- Utiliser le `PORT` (par défaut 9200, sauf modification) que Flask retourne pour l'implémenter dans Android Studio

Exemple : 
![alt text](image.png)

2. **Client Android**

- Ouvrir le projet Android Studio avec l'API 31 (modifiable) et changer les IP/port dans les fichiers `HomeActivity.kt` (page d'accueil), `MainActivity.kt` (page de connexion), `Statistique.kt` (page des statistiques)
- Par défaut, c'est `10.0.2.2:9200` (10.0.2.2 est un tunnel vers 127.0.0.1 car l'émulateur Android Studio utilise déjà 127.0.0.1) ![alt text](image-1.png)
- Lancer le projet


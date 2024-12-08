# DriveSearchAPi
# Recherche de fichiers Google Drive

Ce projet permet de rechercher des fichiers sur Google Drive à l'aide de l'API Google Drive. L'interface graphique (GUI) est construite avec Tkinter et permet à l'utilisateur de saisir un mot-clé pour rechercher des fichiers dont le nom contient ce mot-clé. Les résultats affichent le chemin complet du fichier et un lien vers celui-ci.

## Fonctionnement du Code

1. **Authentification Google** : Le code utilise OAuth 2.0 pour s'authentifier auprès de Google Drive. Un fichier de credentials (`file.json`) est nécessaire pour obtenir un token d'accès.
   
2. **Recherche de fichiers** : Lorsqu'un mot-clé est saisi, le code effectue une recherche dans Google Drive pour trouver les fichiers dont le nom contient le mot-clé. Les résultats incluent le chemin complet et l'URL de chaque fichier.

3. **Interface graphique (GUI)** : L'interface graphique est réalisée avec Tkinter, où l'utilisateur peut entrer un mot-clé, voir les résultats, et cliquer sur les liens pour ouvrir les fichiers dans le navigateur.

4. **Gestion des erreurs** : Si l'authentification échoue ou si l'API rencontre une erreur, le programme affiche un message d'erreur approprié.

## Fichiers nécessaires

- **file.json** : Fichier de credentials obtenu depuis la console Google Cloud pour activer l'API Google Drive.
- **token.json** : Ce fichier est généré automatiquement après la première authentification. Il contient les informations d'authentification nécessaires pour accéder à Google Drive.
- **Python script** : Le script principal contenant le code pour l'interface graphique et l'accès à Google Drive.

## Commandes pour exécuter le code

1. Installez les dépendances nécessaires :
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   pyhton main.py
   %Merci A vous Oualid Hamri

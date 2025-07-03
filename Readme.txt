🧾 Restaurant Ticket App – Kivy + ReportLab
Cette application est une interface de gestion de commandes pour restaurants, développée avec Kivy pour l'interface graphique et ReportLab pour la génération de tickets de caisse au format PDF.

🎯 Fonctionnalités principales
🎛️ Sélection du serveur et du numéro de table à partir de menus déroulants.

🍕 Ajout de produits à la commande via des boutons avec images (Pizza, Burger, Boissons, etc.).

🧾 Génération automatique d’un ticket PDF avec :

Le nom du serveur

Le numéro de table

La date

La liste des produits commandés avec leurs quantités, prix unitaires et le total à payer

🖨️ Ouverture automatique du ticket PDF une fois généré.

🎨 Interface intuitive avec un fond personnalisé et des visuels cliquables.

🛠️ Technologies utilisées
Python

Kivy pour le développement de l'interface utilisateur

ReportLab pour la génération de fichiers PDF

subprocess et os pour la gestion des fichiers et leur ouverture automatique

📷 Aperçu visuel
Interface moderne avec disposition en BoxLayout et GridLayout

Produits représentés par des images cliquables

Interaction utilisateur via popup de confirmation

📂 Utilisation
Lancer l'application :

bash
Copier
Modifier
python main.py
Sélectionner le serveur et le numéro de table.

Ajouter les produits à la commande.

Cliquer sur "Imprimer Ticket" pour générer et visualiser le ticket PDF.

📝 Remarques
Ce projet peut être utilisé dans le cadre de mini systèmes de gestion pour petits cafés, restaurants ou projets pédagogiques.

Les images des produits doivent être présentes dans le même dossier que le script (pizza.png, coca_cola.png, etc.).
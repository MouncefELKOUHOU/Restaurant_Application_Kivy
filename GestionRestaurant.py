import os
import subprocess
import datetime
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from kivy.graphics import Color as KivyColor, Rectangle

class RestaurantApp(App):
    def build(self):
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Couleur d'arrière-plan
        with layout.canvas.before:
            KivyColor(0.9, 0.9, 0.9, 1)  # Gris clair
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Liste des serveurs
        self.label_serveur = Label(text="Nom du Serveur:", font_size=32)
        layout.add_widget(self.label_serveur)

        self.spinner_serveur = Spinner(
            text='Choisir Le Nom de Serveur',
            values=('Serveur Mouncef', 'Serveur Amine', 'Serveur Mohamed', 'Serveur Rachid'),
            font_size=32,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.spinner_serveur)

        # Liste des numéros de table
        self.label_table = Label(text="Numéro de la Table:", font_size=32)
        layout.add_widget(self.label_table)

        self.spinner_table = Spinner(
            text='Choisir le Numéro de la table',
            values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            font_size=32,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.spinner_table)

        # Bouton pour créer une table
        self.button_creer_table = Button(text="Créer Table", font_size=32, size_hint_y=None, height=60)
        self.button_creer_table.bind(on_press=self.creer_table)
        layout.add_widget(self.button_creer_table)

        # GridLayout pour les produits
        self.grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # Ajouter des produits avec des images
        self.produits = [
            ("Pizza", 60, "pizza.png"),
            ("Coca-Cola", 15, "coca_cola.png"),
            ("Burger", 50, "burger.png"),
            ("Salade", 30, "salad.png"),
            ("Pâtes", 40, "pasta.png"),
            ("Steak", 80, "steak.png"),
            ("Frites", 25, "fries.png"),
            ("Tarte", 35, "hawai.png"),
            ("Glace", 20, "ice_cream.png"),
            ("Eau", 5, "water.png"),
            ("Jus d'Orange", 10, "orange_juice.png"),
            ("Thé", 12, "tea.png"),
            ("Café", 15, "coffee.png"),
            ("Soupe", 25, "soup.png"),
            ("Croissant", 10, "croissant.png"),
            ("Sandwich", 25, "sandwich.png"),
        ]
        
        for produit in self.produits:
            self.ajouter_produit_image(*produit)

        layout.add_widget(self.grid)

        # Bouton imprimer ticket
        self.button_imprimer = Button(text="Imprimer Ticket", font_size=32, size_hint_y=None, height=60)
        self.button_imprimer.bind(on_press=self.imprimer_ticket)
        layout.add_widget(self.button_imprimer)

        # Liste pour stocker les produits sélectionnés
        self.produits_selectionnes = {}

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def ajouter_produit_image(self, produit, prix, image_path):
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
        img = Image(source=image_path, allow_stretch=True, size_hint=(1, 0.8))

        # Rendre l'image cliquable
        img.bind(on_touch_down=lambda instance, touch: self.ajouter_produit(produit, prix) if instance.collide_point(*touch.pos) else None)

        btn = Button(text=f"{produit} - {prix} Dhs", size_hint=(1, 0.2))
        btn.bind(on_press=lambda x: self.ajouter_produit(produit, prix))

        layout.add_widget(img)
        layout.add_widget(btn)
        self.grid.add_widget(layout)

    def creer_table(self, instance):
        serveur = self.spinner_serveur.text
        table = self.spinner_table.text
        if serveur and table:
            popup = Popup(title='Succès',
                          content=Label(text=f"Table {table} créée pour le serveur {serveur}"),
                          size_hint=(0.7, 0.5))
            popup.open()
        else:
            popup = Popup(title='Erreur',
                          content=Label(text="Veuillez remplir les champs du serveur et de la table."),
                          size_hint=(0.7, 0.5))
            popup.open()

    def ajouter_produit(self, produit, prix):
        if produit in self.produits_selectionnes:
            self.produits_selectionnes[produit] += 1
        else:
            self.produits_selectionnes[produit] = 1
        
        popup = Popup(title='Ajout de produit',
                      content=Label(text=f"{produit} ajouté. Quantité: {self.produits_selectionnes[produit]}"),
                      size_hint=(0.7, 0.5))
        popup.open()

    def imprimer_ticket(self, instance):
        serveur = self.spinner_serveur.text
        table = self.spinner_table.text

        if not serveur or not table:
            popup = Popup(title='Erreur',
                          content=Label(text="Veuillez d'abord saisir les informations du serveur et de la table."),
                          size_hint=(0.7, 0.5))
            popup.open()
            return

        # Création du nom de fichier avec la date et l'heure actuelles
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"ticket_table_{table}_{now}.pdf"

        # Génération du PDF
        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4

        # Ajouter une couleur d'arrière-plan au PDF
        c.setFillColor(Color(0.9, 0.9, 0.9))  # Gris clair
        c.rect(0, 0, width, height, stroke=0, fill=1)  # Remplissage

        # Ajout d'un en-tête avec la date
        c.setFillColor(Color(0, 0, 0))  # Noir
        c.drawString(100, height - 50, f"---------- Ticket de la Table {table} ----------")
        c.drawString(100, height - 70, f"Serveur : {serveur}")
        
        # Affichage de la date
        date_aujourdhui = datetime.datetime.now().strftime("%d/%m/%Y")
        c.drawString(100, height - 90, f"Date : {date_aujourdhui}")

        # Affichage des produits sélectionnés
        total = 0
        for i, (produit, quantite) in enumerate(self.produits_selectionnes.items()):
            prix = next((p[1] for p in self.produits if p[0] == produit), 0)
            c.drawString(100, height - 100 - (i + 1) * 20, f"Produit : {produit}, Quantité : {quantite}, Prix Unitaire: {prix} Dhs, Total: {prix * quantite} Dhs")
            total += prix * quantite
        
        # Total
        c.drawString(100, height - 100 - (len(self.produits_selectionnes) + 2) * 20, f"Total à payer : {total} Dhs")

        # Ligne de fin
        c.drawString(100, height - 100 - (len(self.produits_selectionnes) + 3) * 20, "----------------------------------------------")

        # Sauvegarde du PDF
        c.showPage()
        c.save()

        # Afficher un message de succès
        popup = Popup(title='Impression',
                      content=Label(text=f"Ticket généré : {file_name}"),
                      size_hint=(0.7, 0.5))
        popup.open()

        # Ouvrir le fichier PDF automatiquement
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_name)
            elif os.name == 'posix':  # macOS ou Linux
                if 'darwin' in os.uname().sysname.lower():
                    subprocess.call(['open', file_name])
                else:
                    subprocess.call(['xdg-open', file_name])
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier PDF: {e}")  # Afficher l'erreur dans la console
            popup = Popup(title='Erreur',
                          content=Label(text=f"Erreur lors de l'ouverture du fichier PDF : {e}"),
                          size_hint=(0.7, 0.5))
            popup.open()

if __name__ == '__main__':
    RestaurantApp().run()

from flask import Flask, render_template, redirect, url_for
import os
import random
import re

app = Flask(__name__)

# Route für die Home-Seite mit dem Grid
@app.route('/')
def home():
    return render_template('home.html')

# Route für das Vokabel-Spiel
@app.route('/vokabeln')
def index():
    # Pfad zum Ordner mit den Bildern
    image_folder = 'static/img'
    
    # Alle Ordner im Bildordner auflisten
    all_folders = [f for f in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, f))]

    # Zufällig einen Ordner auswählen
    selected_folder = random.choice(all_folders)
    
    # Sicherstellen, dass das Label der ausgewählte Ordner ist
    label = selected_folder
    selected_images = []
    
    # Zufälliges Bild aus dem ausgewählten Ordner auswählen
    images_in_selected_folder = [
        f for f in os.listdir(os.path.join(image_folder, selected_folder))
        if re.match(r'.*\.(jpg|jpeg|png|gif)$', f)  # Nur Bilder auswählen
    ]

    if images_in_selected_folder:
        selected_image = random.choice(images_in_selected_folder)
        selected_images.append(os.path.join(image_folder, selected_folder, selected_image))

    # Aus den restlichen Ordnern Bilder auswählen
    remaining_folders = [f for f in all_folders if f != selected_folder]
    
    # Zufällige Auswahl von 3 weiteren Ordnern
    selected_additional_folders = random.sample(remaining_folders, min(3, len(remaining_folders)))
    
    # Bilder aus den zusätzlich ausgewählten Ordnern auswählen
    for folder in selected_additional_folders:
        images_in_folder = [
            f for f in os.listdir(os.path.join(image_folder, folder))
            if re.match(r'.*\.(jpg|jpeg|png|gif)$', f)
        ]

        if images_in_folder:
            selected_image = random.choice(images_in_folder)
            selected_images.append(os.path.join(image_folder, folder, selected_image))

    # Sicherstellen, dass genügend Bilder vorhanden sind (insgesamt 4)
    if len(selected_images) < 4:
        return "Nicht genügend Bilder im Verzeichnis", 404  # Fehlerbehandlung

    # Mischen der Bilder für zufällige Anordnung
    random.shuffle(selected_images)

    return render_template('index.html', images=selected_images, label=label)

if __name__ == '__main__':
    app.run(debug=True)

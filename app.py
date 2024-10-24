from flask import Flask, render_template
import os
import random
import re

app = Flask(__name__)

@app.route('/')
def index():
    image_folder = 'static/img'
    
    # Alle Level-Ordner auflisten
    level_folders = [f for f in os.listdir(image_folder) if os.path.isdir(os.path.join(image_folder, f))]

    # Zufällig einen Level-Ordner auswählen
    selected_level = random.choice(level_folders)
    
    # Debugging: Zeige ausgewählten Level-Ordner an
    print("Ausgewählter Level-Ordner:", selected_level)

    selected_level_path = os.path.join(image_folder, selected_level)

    # Alle Objekte im ausgewählten Level-Ordner auflisten
    objects_in_selected_level = [f for f in os.listdir(selected_level_path) if os.path.isdir(os.path.join(selected_level_path, f))]
    
    # Debugging: Zeige alle Objekte im ausgewählten Level-Ordner an
    print("Objekte im ausgewählten Level-Ordner:", objects_in_selected_level)

    selected_images = []
    audio_files = {}  # Dictionary für Audio-Pfade

    # Zufälliges Bild aus dem ausgewählten Objekt auswählen
    if objects_in_selected_level:
        selected_object = random.choice(objects_in_selected_level)
        selected_object_path = os.path.join(selected_level_path, selected_object)

        images_in_selected_object = [
            f for f in os.listdir(selected_object_path)
            if re.match(r'.*\.(jpg|jpeg|png|gif)$', f)  # Nur Bilder auswählen
        ]

        if images_in_selected_object:
            selected_image = random.choice(images_in_selected_object)
            selected_images.append(os.path.join(selected_object_path, selected_image))

            # Pfad zur Audiodatei hinzufügen
            audio_files[selected_image] = os.path.join(selected_object_path, selected_object + '.mp3')

    # Aus den restlichen Objekten Bilder auswählen
    remaining_objects = [obj for obj in objects_in_selected_level if obj != selected_object]
    
    # Zufällige Auswahl von 3 weiteren Objekten
    selected_additional_objects = random.sample(remaining_objects, min(3, len(remaining_objects)))
    
    for obj in selected_additional_objects:
        object_path = os.path.join(selected_level_path, obj)

        images_in_object = [
            f for f in os.listdir(object_path)
            if re.match(r'.*\.(jpg|jpeg|png|gif)$', f)
        ]

        if images_in_object:
            selected_image = random.choice(images_in_object)
            selected_images.append(os.path.join(object_path, selected_image))

            # Pfad zur Audiodatei hinzufügen
            audio_files[selected_image] = os.path.join(object_path, obj + '.mp3')

    # Sicherstellen, dass genügend Bilder vorhanden sind (insgesamt 4)
    if len(selected_images) < 4:
        print("Gefundene Bilder:", selected_images)  # Debugging: Zeige gefundene Bilder an
        return "Nicht genügend Bilder im Verzeichnis", 404  # Fehlerbehandlung

    # Mischen der Bilder für zufällige Anordnung
    random.shuffle(selected_images)

    return render_template('index.html', images=selected_images, label=selected_object, audio_files=audio_files)


if __name__ == '__main__':
    app.run(debug=True)

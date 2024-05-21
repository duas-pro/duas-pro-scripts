import requests
import os


# List defined using https://siratguide.com/wp-json/wp/v2/types
base_url = "https://siratguide.com/wp-json/wp/v2/"
endpoints = ["duaa", "a3mal", "zyarat", "noble", "marker", "video_guide", "how_to", "locate_move"]
params = ["ar", "en", "fr", "de", "es", "tr", "ur"]


# Funktion zum Erstellen des vollständigen URL-Pfads und zum Durchführen der Anfrage
def fetch_and_save(endpoint, param):
    # Erstelle die vollständige URL
    url = f"{base_url}{endpoint}"
    query_params = {"lang": param, "per_page": 100}

    try:
        # Sende eine GET-Anfrage an die URL
        response = requests.get(url, params=query_params)

        # Überprüfe, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # Erstelle den Dateinamen basierend auf dem Endpunkt und dem Parameter
            filename = f"response_{endpoint}_{param if param else 'default'}.json"
            # Erstelle den Ordner, falls er nicht existiert
            os.makedirs('01_responses', exist_ok=True)
            # Speichere den Inhalt der Antwort in eine Datei
            with open(os.path.join('01_responses', filename), 'wb') as file:
                file.write(response.content)
            print(f"Response successfully saved to {filename}")
        else:
            print(f"Failed to retrieve {url} with param {param}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {url} with param {param}: {e}")


if __name__ == '__main__':
    print("Hello, World!")
    # Iteriere über alle Kombinationen von Endpunkten und Parametern
    for endpoint in endpoints:
        for param in params:
            fetch_and_save(endpoint, param)
    print("All requests have been processed.")

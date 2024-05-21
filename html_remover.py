import json
import os

from bs4 import BeautifulSoup


def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_list = [p.get_text(strip=True) for p in soup.find_all(['p', 'div'])]
    return text_list


def get_language_from_filename(filename):
    # Extrahiere den Sprachcode aus dem Dateinamen
    parts = filename.split('_')
    if len(parts) > 1:
        return parts[-1].split('.')[0]
    return "unknown"


def convert_json_files(input_dir, output_dir):
    # Erstelle den Ausgabeordner, falls er nicht existiert
    os.makedirs(output_dir, exist_ok=True)

    # Iteriere über alle Dateien im Eingabeordner
    for filename in os.listdir(input_dir):
        if filename.startswith(("response_a3mal", "response_duaa", "response_zyarat")) and filename.endswith(".json"):
            # Vollständiger Pfad zur Eingabedatei
            input_file_path = os.path.join(input_dir, filename)

            # Extrahiere die Sprache aus dem Dateinamen
            language = get_language_from_filename(filename)

            # Lese die JSON-Daten aus der Datei
            with open(input_file_path, 'r', encoding='utf-8') as input_file:
                data = json.load(input_file)

            # Erstelle eine neue Liste von Objekten mit nur den gewünschten Feldern
            print("Length of " + filename + " is: " + str(len(data)))
            converted_data = []
            for item in data:
                title_html = item.get("content", {}).get("rendered", "")
                text_list = clean_html(title_html)
                cleaned_text_list = [s for s in text_list if s]

                converted_item = {
                    "id": item.get("id"),
                    "title": item.get("title", {}).get("rendered"),
                    "texts": cleaned_text_list
                }
                converted_data.append(converted_item)

            # Vollständiger Pfad zur Ausgabedatei
            output_file_path = os.path.join(output_dir, filename)

            # Schreibe die konvertierten Daten in die Ausgabedatei
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(converted_data, output_file, ensure_ascii=False, indent=4)

            print(f"Converted {filename} and saved to {output_file_path}")


if __name__ == '__main__':
    # Eingabe- und Ausgabeordner
    input_dir = '01_responses'
    output_dir = '02_converted_responses'

    # Rufe die Konvertierungsfunktion auf
    convert_json_files(input_dir, output_dir)

    print("All JSON files have been converted.")

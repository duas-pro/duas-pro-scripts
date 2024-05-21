import json
import os


def split_text(text_list):
    arabic_texts = []
    other_texts = []
    transliteration_texts = []

    # Überspringe den ersten Text
    text_list = text_list[1:]

    for i, text in enumerate(text_list):
        if i % 3 == 0:
            arabic_texts.append(text)
        elif i % 3 == 1:
            other_texts.append(text)
        elif i % 3 == 2:
            transliteration_texts.append(text)

    return arabic_texts, other_texts, transliteration_texts


def combine_texts(arabic_texts, other_texts, transliteration_texts, language):
    combined = []
    for ar, en, tr in zip(arabic_texts, other_texts, transliteration_texts):
        combined.append({
            "arabic": ar,
            language: en,
            "transliteration": tr
        })
    return combined


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
            converted_data = []
            for item in data:
                text_list = item.get("texts")

                arabic_texts, other_texts, transliteration_texts = split_text(text_list)
                combined_texts = combine_texts(arabic_texts, other_texts, transliteration_texts, language)

                converted_item = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "texts": combined_texts
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
    input_dir = '03_validated_converted_responses'
    output_dir = '04_converted_responses_split_text'

    # Rufe die Konvertierungsfunktion auf
    convert_json_files(input_dir, output_dir)

    print("All JSON files have been converted.")

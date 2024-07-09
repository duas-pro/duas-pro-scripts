import os

import requests
import json


def read_urls_from_file(file_path):
    """Liest URLs aus einer Datei und gibt sie als Liste zurück."""
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


def fetch_json_from_url(url, alternative_base_url=None):
    """Holt JSON-Daten von einer URL und verwendet eine alternative URL bei 404-Fehler."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404 and alternative_base_url:
            alt_url = f"{alternative_base_url}/{extract_last_part_of_url(url)}"
            response = requests.get(alt_url)
            response.raise_for_status()
            return response.json()
        else:
            raise


def extract_last_part_of_url(url):
    """Extrahiert das Wort nach dem letzten Slash in der URL."""
    return url.rstrip('/').split('/')[-1]


def extract_and_sort_slides(data):
    """Extrahiert und sortiert die 'slides'-Felder aus den JSON-Daten."""
    slides_dict = data.get("slides", {})
    slides = [slides_dict[str(i + 1)] for i in range(len(slides_dict))]
    return slides


def save_to_file(data, file_path):
    """Speichert die Daten in eine Datei."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main(input_file, output_dir, base_url, alternative_base_url):
    urls = read_urls_from_file(input_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        last_part = extract_last_part_of_url(url)
        modified_url = f"{base_url}/{last_part}" + "?langs=ar|en|tl&getSlides=true"
        try:
            json_data = fetch_json_from_url(modified_url, alternative_base_url)
            sorted_slides = extract_and_sort_slides(json_data)
            titles_dict = json_data.get("duaName", {})
            info_dict = json_data.get("info", {})
            audio_dict = json_data.get("audio", [])
            audio_ids = [audio["audioId"] for audio in audio_dict]

            json_dua = {
                "title": {
                    "ar": titles_dict['ar'] if 'ar' in titles_dict else None,
                    "tl": titles_dict['tl'] if 'tl' in titles_dict else None,
                    "en": titles_dict['en'] if 'en' in titles_dict else None
                },
                # "overall": {"de": [], "fr": [], "es": [], "tr": [], "ur": [], "fa": []},
                "source": modified_url,
                "route_name": json_data['routeName'],
                "is_popular": json_data['isPopular'],
                "narrated_by": info_dict['narratedBy'] if 'narratedBy' in info_dict else None,
                "image_url": "https://www.duaplayer.org/api/bg/dua/" + json_data['routeName'] + "/app_1080p/1",
                "audios": audio_ids,
                "lines": sorted_slides,
            }

            output_file_path = f"{output_dir}/{last_part}.json"
            save_to_file(json_dua, output_file_path)
            print(f"Saved sorted slides to {output_file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {modified_url}: {e}")


if __name__ == "__main__":
    input_file = 'scrapping-input/duaplayer_links_to_scrap.txt'  # Pfad zur Datei mit der Liste der URLs
    output_dir = 'scrapping-result'  # Verzeichnis, in das die Dateien gespeichert werden
    base_url = 'https://www.duaplayer.org/api/2'  # Basis-URL, die an den extrahierten Teil angehängt wird
    alternative_base_url = 'https://www.duaplayer.org/api/3'  # Alternative Basis-URL bei 404-Fehler
    main(input_file, output_dir, base_url, alternative_base_url)

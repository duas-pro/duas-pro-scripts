from config import supabase
import json


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def insert_into_supabase(data):
    for entry in data:
        # Insert into text table
        text_response = supabase.table("text").insert({"route_name": entry["id"]}).execute()
        text_id = text_response.data[0]['id']

        for i, text in enumerate(entry["texts"]):
            line_data = {
                "text_id": text_id,
                "line_number": i + 1,
                "type": "TEXT",
                "ar": text["arabic"],
                "tx": text.get("transliteration", ""),
                "en": text["translations"].get("en", ""),
                "de": text["translations"].get("de", ""),
                "es": text["translations"].get("es", ""),
                "fr": text["translations"].get("fr", ""),
                "it": None,
                "tr": text["translations"].get("tr", ""),
                "fa": None,
                "ur": None
            }

            supabase.table("text_line").insert(line_data).execute()


if __name__ == "__main__":
    print("Hello World!")
    response = supabase.table('text').select("*").execute()
    print(str(response))
    file_path = '05_merged_responses/response_a3mal_merged.json'
    data = load_json_file(file_path)
    insert_into_supabase(data)
    print("Finished")


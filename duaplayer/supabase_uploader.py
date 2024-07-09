import json
import os

from config import supabase


def read_json_file(file_path):
    """Liest JSON-Daten aus einer Datei."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == "__main__":
    """Fügt Übersetzungen zu einer Datei in Chargen hinzu."""
    for filename in os.listdir("upload-input"):
        print("Begin uploading " + filename + " ...")
        file_path = os.path.join("upload-input", filename)
        file_data = read_json_file(file_path)

        dua_response = supabase.table("duas").insert({
            "route_name": file_data["route_name"],
            "image_url": file_data["image_url"]
        }).execute()
        dua_id = dua_response.data[0]['id']

        source_response = supabase.table("references").insert(
            {"type": "Duaplayer Api",
             "url": file_data["source"],
             "dua_id": dua_id,
             "language_id": 1,
             }).execute()
        source_id = source_response.data[0]['id']

        ar_translation_response = supabase.table("dua_contents").insert({
            "dua_id": dua_id,
            "language_id": 2,
            "narrated_by": file_data["narrated_by"],
            "title": file_data["title"]['ar'].strip() if "ar" in file_data["title"] and file_data["title"]['ar'] is not None else None
        }).execute()
        ar_translation_id = ar_translation_response.data[0]['id']

        en_translation_response = supabase.table("dua_contents").insert({
            "dua_id": dua_id,
            "language_id": 1,
            "narrated_by": file_data["narrated_by"],
            "title": file_data["title"]['en'].strip() if "en" in file_data["title"] and file_data["title"]['en'] is not None else None
        }).execute()
        en_translation_id = en_translation_response.data[0]['id']

        tl_translation_response = supabase.table("dua_contents").insert({
            "dua_id": dua_id,
            "language_id": 3,
            "narrated_by": file_data["narrated_by"],
            "title": file_data["title"]['tl'].strip() if "tl" in file_data["title"] and file_data["title"]['tl'] is not None else None
        }).execute()
        tl_translation_id = tl_translation_response.data[0]['id']

        for i, line in enumerate(file_data["lines"]):
            count = line["count"] if "count" in line and isinstance(line["count"], int) else None

            supabase.table("dua_content_lines").insert({
                "dua_content_id": en_translation_id,
                "line_number": i + 1,
                "text": line['en'].strip() if 'en' in line else None,
                "repetitions_number": count
            }).execute()
            supabase.table("dua_content_lines").insert({
                "dua_content_id": ar_translation_id,
                "line_number": i + 1,
                "text": line['ar'].strip() if 'ar' in line else None,
                "repetitions_number": count
            }).execute()
            supabase.table("dua_content_lines").insert({
                "dua_content_id": tl_translation_id,
                "line_number": i + 1,
                "text": line['tl'].strip() if 'tl' in line else None,
                "repetitions_number": count
            }).execute()
        print(f"Uploaded file: {file_path}")
    print("Finished")

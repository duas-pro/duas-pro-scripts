import json
import os


def load_json_files(directory, prefix):
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith('.json')]
    file_contents = {}
    for file in files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            file_contents[file] = json.load(f)
    return file_contents


def merge_files(file_contents):
    merged_data = []
    file_keys = sorted(file_contents.keys())
    num_entries = len(file_contents[file_keys[0]])

    for i in range(num_entries):
        print("length of i " + str(num_entries) )
        merged_entry = {
            "id": file_contents[file_keys[0]][i]["id"],
            "title": file_contents[file_keys[0]][i]["title"],
            "texts": []
        }
        for j in range(len(file_contents[file_keys[0]][i]["texts"])):
            print("length of j " + str(len(file_contents[file_keys[0]][i]["texts"])))
            text_entry = {
                "arabic": file_contents[file_keys[0]][i]["texts"][j]["arabic"],
                "transliteration": file_contents[file_keys[0]][i]["texts"][j]["transliteration"],
                "translations": {}
            }
            print("text_entry: " + str(text_entry))
            # for key in file_keys:
            #     print("i: " + str(i) + " j : " + str(j) + " key: " + str(key))
            #     lang_code = key.split('_')[-1].split('.')[0]
            #     text_entry["translations"][lang_code] = file_contents[key][i]["texts"][j][lang_code]
            # merged_entry["texts"].append(text_entry)
            skip_entry = False
            for key in file_keys:
                lang_code = key.split('_')[-1].split('.')[0]
                if i < len(file_contents[key]) and j < len(file_contents[key][i]["texts"]):
                    text_entry["translations"][lang_code] = file_contents[key][i]["texts"][j].get(lang_code, "")
                else:
                    skip_entry = True
                    break
            if not skip_entry:
                merged_entry["texts"].append(text_entry)
        merged_data.append(merged_entry)

    return merged_data


def save_merged_file(directory, prefix, merged_data):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    output_file = os.path.join(directory, f'{prefix}_merged.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


def main():
    directory = '04_converted_responses_split_text'
    prefixes = set([f.split('_')[0] for f in os.listdir(directory) if f.startswith('response')])

    for prefix in ["response_duaa"]:
        file_contents = load_json_files(directory, prefix)
        merged_data = merge_files(file_contents)
        save_merged_file("05_merged_responses", prefix, merged_data)


if __name__ == "__main__":
    main()

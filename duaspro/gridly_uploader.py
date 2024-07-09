import json
import os
import requests


def read_json_file(file_path):
    """Liest JSON-Daten aus einer Datei."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == "__main__":
    """Fügt Übersetzungen zu einer Datei in Chargen hinzu."""
    for filename in os.listdir("gridly-upload-input"):
        file_path = os.path.join("data", filename)
        file_data = read_json_file(file_path)
        headers = {
            'Authorization': 'ApiKey 5p17thJtlJZ5eM',
            'Content-type': 'application/json'
        }
        print("Create new grid with name: " + file_data['title']['tl'])
        data_create_grid = {"name": file_data['title']['tl'], "templateGridId": "95vjt8mqlt34v"}
        response_create_grid = requests.post("https://api.gridly.com/v1/grids?dbId=2su97t4t36jnb", headers=headers,
                                             data=json.dumps(data_create_grid)).json()
        grid_id = response_create_grid['id']

        response_get_views = requests.get("https://api.gridly.com/v1/views?gridId=" + grid_id, headers=headers).json()
        view_id = response_get_views[0]['id']

        data_create_view = []
        for i in range(0, len(file_data['lines'])):
            line = file_data['lines'][i]
            count_line = line['count'] if 'count' in line else None
            data_create_view.append({"id": str(i), "cells": [
                {"columnId": "ar", "value": line['ar']},
                {"columnId": "tl", "value": line['tl']},
                {"columnId": "en", "value": line['en']},
                {"columnId": "de", "value": line['de']},
                {"columnId": "fr", "value": ""},
                {"columnId": "es", "value": line['es']},
                {"columnId": "tr", "value": ""},
                {"columnId": "ur", "value": ""},
                {"columnId": "fa", "value": ""},
                {"columnId": "type", "value": "Dua"},
                {"columnId": "count", "value": count_line},
            ]})

        requests.post("https://api.gridly.com/v1/views/" + view_id + "/records", headers=headers,
                      data=json.dumps(data_create_view)).json()
        print(f"Uploaded file: {file_path}")
    print("Finished")

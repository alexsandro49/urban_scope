import os
import requests
import gzip
import ijson
from dotenv import load_dotenv
from states.models import State
from municipalities.models import Municipality
from districts.models import District


def clear_data(data):
    clean_data = []

    for element in ijson.items(data, "item"):
        if (
            element["municipio"] != None
            and element["municipio"]["microrregiao"] != None
            and element["municipio"]["microrregiao"]["mesorregiao"] != None
            and element["municipio"]["microrregiao"]["mesorregiao"]["UF"] != None
        ):
            clean_data.append(element)

    return clean_data


def update_database_data(data):
    states = []
    municipalities = []
    districts = []

    states_id_saved = []
    municipalities_id_saved = []
    districts_id_saved = []

    for element in ijson.items(data, "item"):
        state_id = element["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]
        municipality_id = element["municipio"]["id"]
        district_id = element["id"]

        if state_id not in states_id_saved:
            states.append(
                State(
                    api_id=state_id,
                    name=element["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "nome"
                    ],
                    acronym=element["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "sigla"
                    ],
                )
            )
            states_id_saved.append(state_id)

        if municipality_id not in municipalities_id_saved:
            municipalities.append(
                Municipality(
                    api_id=municipality_id,
                    name=element["municipio"]["nome"],
                    state_id=state_id,
                )
            )
            municipalities_id_saved.append(municipality_id)

        if district_id not in districts_id_saved:
            districts.append(
                District(
                    api_id=district_id,
                    name=element["nome"],
                    state_id=state_id,
                    municipality_id=municipality_id,
                )
            )
            districts_id_saved.append(district_id)

    State.objects.bulk_create(
        states,
        update_conflicts=True,
        update_fields=["api_id", "name", "acronym"],
        unique_fields=["api_id"],
    )

    Municipality.objects.bulk_create(
        municipalities,
        update_conflicts=True,
        update_fields=["api_id", "name", "state_id"],
        unique_fields=["api_id"],
    )

    District.objects.bulk_create(
        districts,
        update_conflicts=True,
        update_fields=["api_id", "name", "state_id", "municipality_id"],
        unique_fields=["api_id"],
    )


def run():
    load_dotenv()

    API_URL = os.getenv("BASE_API_URL") + "distritos/"
    response = requests.get(API_URL, stream=True, headers={"Accept-Encoding": "gzip"})

    with gzip.GzipFile(fileobj=response.raw) as decompressed_data:
        clean_data = clear_data(decompressed_data)
        update_database_data(clean_data)

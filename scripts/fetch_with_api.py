import os
import requests
from dotenv import load_dotenv
from states.models import State
from municipalities.models import Municipality
from districts.models import District


def sanitize_data(data):
    clean_data = []

    for element in data:
        if (
            element["municipio"] != None
            and element["municipio"]["microrregiao"] != None
            and element["municipio"]["microrregiao"]["mesorregiao"] != None
            and element["municipio"]["microrregiao"]["mesorregiao"]["UF"] != None
        ):
            clean_data.append(element)

    return clean_data


def states_logic(data):
    states = []
    states_id = []

    for element in data:
        new_id = element["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]

        if new_id not in states_id:
            states.append(
                State(
                    api_id=new_id,
                    name=element["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "nome"
                    ],
                    acronym=element["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "sigla"
                    ],
                )
            )
            states_id.append(new_id)

    State.objects.bulk_create(
        states,
        update_conflicts=True,
        update_fields=["api_id", "name", "acronym"],
        unique_fields=["api_id"],
    )


def municipalities_logic(data):
    municipalities = []
    municipalities_id = []

    for element in data:
        state_id = element["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]
        state = State.objects.get(api_id=state_id)

        new_id = element["municipio"]["id"]

        if new_id not in municipalities_id:
            municipalities.append(
                Municipality(
                    api_id=new_id,
                    name=element["municipio"]["nome"],
                    state_id=state,
                )
            )
            municipalities_id.append(new_id)

    Municipality.objects.bulk_create(
        municipalities,
        update_conflicts=True,
        update_fields=["api_id", "name", "state_id"],
        unique_fields=["api_id"],
    )


def districts_logic(data):
    districts = []
    districts_id = []

    for element in data:
        state_id = element["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]
        state = State.objects.get(api_id=state_id)

        municipality_id = element["municipio"]["id"]
        municipality = Municipality.objects.get(api_id=municipality_id)

        new_id = element["id"]

        if new_id not in districts_id:
            districts.append(
                District(
                    api_id=new_id,
                    name=element["nome"],
                    state_id=state,
                    municipality_id=municipality,
                )
            )
            districts_id.append(new_id)

    District.objects.bulk_create(
        districts,
        update_conflicts=True,
        update_fields=["api_id", "name", "state_id", "municipality_id"],
        unique_fields=["api_id"],
    )


def run():
    load_dotenv()

    API_URL = os.getenv("BASE_API_URL") + "distritos/"
    result = requests.get(API_URL).json()
    clean_data = sanitize_data(result)

    states_logic(clean_data)
    municipalities_logic(clean_data)
    districts_logic(clean_data)

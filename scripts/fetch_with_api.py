import os
import requests
from dotenv import load_dotenv
from states.models import State
from municipalities.models import Municipality


def sanitize_data(result):
    clean_data = []
    for district in result:
        if (
            district["municipio"] != None
            and district["municipio"]["microrregiao"] != None
            and district["municipio"]["microrregiao"]["mesorregiao"] != None
            and district["municipio"]["microrregiao"]["mesorregiao"]["UF"] != None
        ):
            clean_data.append(district)

    return clean_data


def states_logic(districts):
    states = []
    states_id = []

    for district in districts:
        new_id = district["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]

        if new_id not in states_id:
            states.append(
                State(
                    api_id=new_id,
                    name=district["municipio"]["microrregiao"]["mesorregiao"]["UF"]["nome"],
                    acronym=district["municipio"]["microrregiao"]["mesorregiao"]["UF"][
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


def municipalities_logic(districts):
    municipalities = []
    municipalities_id = []

    for district in districts:
        state_id = district["municipio"]["microrregiao"]["mesorregiao"]["UF"]["id"]
        state = State.objects.get(api_id = state_id)

        new_id = district["municipio"]["id"]

        if new_id not in municipalities_id:
            municipalities.append(
                Municipality(
                    api_id = new_id,
                    name = district["municipio"]["nome"],
                    state_id = state,
                )
            )
            municipalities_id.append(new_id)

    Municipality.objects.bulk_create(
        municipalities,
        update_conflicts=True,
        update_fields=["api_id", "name", "state_id"],
        unique_fields=["api_id"],
    )


def run():
    load_dotenv()

    API_URL = os.getenv("BASE_API_URL") + "distritos/"
    result = requests.get(API_URL).json()

    clean_data = sanitize_data(result)

    states_logic(clean_data)
    municipalities_logic(clean_data)

    print('ok')
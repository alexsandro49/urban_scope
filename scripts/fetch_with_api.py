import os
import requests
from dotenv import load_dotenv
from states.models import State


def run():
    load_dotenv()

    API_URL = os.getenv("BASE_API_URL") + "distritos/"
    result = requests.get(API_URL).json()

    states = []
    for district in result:
        if (
            district["municipio"] != None
            and district["municipio"]["microrregiao"] != None
            and district["municipio"]["microrregiao"]["mesorregiao"] != None
            and district["municipio"]["microrregiao"]["mesorregiao"]["UF"] != None
        ):
            states.append(
                State(
                    api_id=district["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "id"
                    ],
                    name=district["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "nome"
                    ],
                    acronym=district["municipio"]["microrregiao"]["mesorregiao"]["UF"][
                        "sigla"
                    ],
                )
            )

    State.objects.bulk_create(
        states,
        update_conflicts=True,
        update_fields=["api_id", "name", "acronym"],
        unique_fields=["uuid"],
    )
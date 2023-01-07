from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from flask import Flask, request
from math import dist

import sys

# Please update to Python 3.11
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# Location models a location in our amazing system
@dataclass
class Location:
    x: int
    y: int

    def distance_to(self, other: Self) -> float:
        return dist((self.x, self.y), (other.x, other.y))


# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    lasso_length: int
    location: Location


# SpaceAnimalType is an enum of all possible space animals we may encounter
class SpaceAnimalType(str, Enum):
    PIG = "pig"
    COW = "cow"
    FLYING_BURGER = "flying_burger"


# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    type: SpaceAnimalType
    location: Location


# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_animals: list[SpaceAnimal] = []
space_cowboys: dict[str, SpaceCowboy] = {}

# the POST /entity endpoint adds an entity to your global space database
@app.route("/entity", methods=["POST"])
def create_entity():
    entities = request.get_json()["entities"]

    for e in entities:
        meta = e["metadata"]
        location = Location(**e["location"])

        match e["type"]:
            case "space_cowboy":
                # Not handling duplicate cowboy names as guaranteed to be unique
                space_cowboys[meta["name"]] = SpaceCowboy(meta["lassoLength"], location)

            case "space_animal":
                match (meta["type"]):
                    case "pig":
                        type = SpaceAnimalType.PIG
                    case "cow":
                        type = SpaceAnimalType.COW
                    case "flying_burger":
                        type = SpaceAnimalType.FLYING_BURGER
                    case _:
                        return "Invalid animal type", 400
                space_animals.append(SpaceAnimal(type, location))

            case _:
                return "Invalid entity type", 400

    return "OK", 200


# lassoable returns all the space animals a space cowboy can lasso given their name
@app.route("/lassoable", methods=["GET"])
def lassoable():
    name = request.get_json()["cowboy_name"]
    cowboy = space_cowboys[name]
    lassoable = [
        animal
        for animal in space_animals
        if cowboy.location.distance_to(animal.location) <= cowboy.lasso_length
    ]

    return {"space_animals": lassoable}, 200


# DO NOT TOUCH ME, thanks :D
if __name__ == "__main__":
    app.run(debug=True, port=8080)

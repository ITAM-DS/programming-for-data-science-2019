"""Simple simulador de turista."""

from .turista import (
    SimuladorTurista,
    Pais,
    Tablero,
    Turista,
    Jugador,
    Dados,
    Bloque,
    Pieza,
    Accion
)

__all__ = [
    "SimuladorTurista",
    "Pais",
    "Tablero",
    "Turista",
    "Jugador",
    "Dados",
    "Bloque",
    "Pieza",
    "Accion",
]

def setup_logging():
    import logging
    import logging.config
    import coloredlogs
    import yaml

    with open('config/logging.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        coloredlogs.install()

setup_logging()

def get_pyproject():
    import os
    import toml

    init_path = os.path.abspath(os.path.dirname(__file__))
    pyproject_path = os.path.join(init_path, "../pyproject.toml")

    with open(pyproject_path, "r") as fopen:
        pyproject = toml.load(fopen)

    return pyproject["tool"]["poetry"]


__version__ = get_pyproject()["version"]
__doc__ = get_pyproject()["description"]

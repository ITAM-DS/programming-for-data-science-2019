from __future__ import annotations # Alternativa para romper dependencia circular causada por los hints


# Una opción para no tener dependencias circulares
# https://www.stefaanlippens.net/circular-imports-type-hints-python.html
#from typing import TYPE_CHECKING
#if TYPE_CHECKING:
#    from .turista import Jugador, Accion, Bloque

import logging

logger = logging.getLogger('turista')

def log_accion(accion:Accion):
    def _log_accion(function):
        def log(self, *func_args, **func_kwargs):
            function_output = function(self, *func_args, **func_kwargs)
            jugador = self
            print(f"{jugador.pieza.name}|{jugador.turnos}|{jugador.posicion.nombre}|{accion.name}")
            return function_output # Regresamos lo que la función decorada regresa
        return log
    return _log_accion # Regresamos el decorador

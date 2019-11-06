

# #+CAPTION: Simulador de juegos de Turista: Tercera iteración
# #+ATTR_ORG: :width 800 :height 800
# #+ATTR_HTML: :width 800px :height 600px
# #+ATTR_LATEX: :height 10cm :width 8cm
# [[file:tercera_iteracion.png]]

# El objetivo final que estamos buscando es simular el juego para poder
# analizar su comportamiento, para lograrlo debemos de guardar los datos
# generados por la simulación.

# Una propuesta de qué datos queremos guardar es lo siguiente:

# #+begin_example org
# juego|ronda|jugador|pieza|turno|posicion|accion
# #+end_example

# Las columnas son:

# - juego :: Identificador de la simulación
# - ronda :: Identificador de la ronda del juego
# - jugador ::  Identificador del jugador
# - pieza :: Identificador de la pieza usada por el jugador
# - turno :: Turno del jugador
# - posicion :: País en el que termina el turno el jugador
# - accion :: Acción tomada por el jugador en el país

# Nota que puede haber más de un renglón por turno por jugador.

# Vamos a /decorar/ los métodos de la clase =Jugador=. En este caso el
# /decorador/ imprimirá a pantalla lo que necesitamos


import logging
import logging.config

logging.config.fileConfig("turista-logging.conf")
logger = logging.getLogger("turista")

def log_accion(accion:Accion):
    def _log_accion(function):
        def log(self, *func_args, **func_kwargs):
            function_output = function(self, *func_args, **func_kwargs)
            jugador = self
            log.info(f"{jugador.pieza}|{jugador.turnos}|{jugador.posicion}|{accion}")
            return function_output # Regresamos lo que la función decorada regresa
        return log
    return _log_accion # Regresamos el decorador



# Concentraremos la creación de las clases en un [[https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html][FactoryMethod]],
# básicamente esta clase aísla la creación de los roles de la clase =Pais=.


from abc import ABC, abstractmethod

def pais_role_factory(bloque:Bloque):
    class PaisRole(ABC):
        def __init__(self, pais):
            self.pais = pais

        @property
        def disponible(self) -> bool:
            return self.pais.dueño is None

        @property
        def hipotecable(self) -> bool:
            return False

        @property
        def construible(self) -> bool:
            return False

        @abstractmethod
        def colocar(self, jugador:Jugador) -> None:
            pass

    class DiplomaticoRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            print("Llegando a una estación diplomática...")

    class ImpuestosRole(PaisRole):
        def __init__(self, impuesto_fijo=10_000, tasa=0.10):
            self.impuesto_fijo = impuesto_fijo
            self.tasa = tasa

        @property
        def disponible(self) -> bool:
            return False

        def colocar(self, jugador:Jugador) -> None:
            jugador.pagar(min(ImpuestosRole.IMPUESTO, jugador.dinero*0.10))

    class RegularRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            if self.dueño is not jugador:
                jugador.pagar(self.renta)
                self.dueño.cobrar(self.renta)

    class ComunicacionesRole(PaisRole):
        @property
        def disponible(self) -> bool:
            return False

        def colocar(self, jugador:Jugador) -> None:
            print("Tomando una carta... Misteriosamente está en blanco... No hay consecuencias")

    class AeropuertoRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            print("Llegando a un Aeropuerto...")

    if bloque is Bloque.DIPLOMÁTICOS: return DiplomaticoRole()
    if bloque is Bloque.AEROPUERTOS: return AeropuertoRole()
    if bloque is Bloque.COMUNICACIONES: return ComunicacionesRole()
    if bloque is Bloque.IMPUESTOS:
        return ImpuestosRole()
    else:
        return RegularRole()

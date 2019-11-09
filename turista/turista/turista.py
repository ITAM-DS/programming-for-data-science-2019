from __future__ import annotations # Alternativa para romper dependencia circular causada por los hints

from typing import NewType, List
from enum import Enum, auto

from dataclasses import dataclass, field

from itertools import cycle

from collections import Counter

import numpy as np

from abc import ABC, abstractmethod

from .helpers import log_accion

import logging

logger = logging.getLogger('turista')

class Dados:

    def __init__(self, numero_caras=6, numero_dados=2):
        self.numero_dados = numero_dados
        self.total = None
        self.son_iguales = False
        self.caras = np.arange(1, numero_caras+1)
        self.tirada = None

    def tirar(self):
        self.tirada = np.random.choice(self.caras, self.numero_dados, replace=True)

        self.total = self.tirada.sum()
        self.son_iguales = len(set(self.tirada)) == 1

    def __repr__(self) -> str:
        return f"{self.tirada} (={self.total})"

Pieza = Enum('Pieza',
             'TOP_HAT BATTLESHIP RACECAR SCOTTIE_DOG CAT TREX PENGUIN RUBBER_DUCKY')

class SimuladorTurista:
    def __init__(self, numero_rondas=2, numero_simulaciones=2) -> None:
        self.numero_simulaciones = numero_simulaciones
        self.numero_rondas = numero_rondas


    def simular(self):
        for simulacion in range(self.numero_simulaciones):
            turista = Turista(maximo_rondas=self.numero_rondas)
            ganador = turista.jugar()
            logger.info(f"Ganador: {ganador}")

Bloque = Enum('Bloque',
              'ROJO MORADO VERDE NARANJA AZUL ROSA CAFÉ AMARILLO AEROPUERTOS DIPLOMÁTICOS COMUNICACIONES IMPUESTOS NINGUNO INICIAL DEPORTADO CÁRCEL')

class Tablero:

    NUMERO_PAISES = 40

    def __init__(self):
        self.paises:List[Pais] = []
        self.ronda = 0
        self._crear_tablero()

    def _crear_tablero(self) -> None:
        with open('data/paises.csv', 'r') as renglones:
            for renglon in renglones:
                if not renglon.startswith('indice'):
                    pais = Pais(*[columna.strip() for columna in renglon.split(',')])
                    pais.role = pais_role_factory(pais)
                    self.paises.append(pais)

    def siguiente_pais(self, pais_inicio, distancia) -> Pais:
        indice_final = (pais_inicio.indice + distancia) % Tablero.NUMERO_PAISES
        return self.paises[indice_final]

    @property
    def posicion_inicial(self) -> Pais:
        return self.paises[0]

    def __repr__(self) -> str:
        return f"{self.paises}"

class Turista:

    DINERO_INICIAL = 150_000
    SUELDO = 20_000

    def __init__(self, numero_jugadores=4, maximo_rondas=10):
        self.numero_jugadores:int = numero_jugadores
        self.maximo_rondas = maximo_rondas
        self.tablero:Tablero = Tablero()
        self.jugadores:List[Jugador] = self._crear_jugadores()
        self.rondas:int = 0
        self.jugador_actual = None
        self.dados = Dados()

    def _crear_jugadores(self) -> List[Jugador]:
        return [Jugador(pieza=pieza, tablero=self.tablero, dinero_inicial=Turista.DINERO_INICIAL)
                for pieza in Pieza][:self.numero_jugadores]

    def jugar(self) -> Jugador:

        while(self.continuar()):
            self.ronda()

        return self.ganador

    def ronda(self) -> None:
        for jugador in self.jugadores:
            self.jugador_actual = jugador
            if not self.jugador_actual.quebrado:
                self.jugador_actual.turno(self.dados)
        self.rondas += 1

    @property
    def hay_jugadores(self) -> bool:
        return any([not jugador.quebrado for jugador in self.jugadores])

    def continuar(self) -> bool:
        return self.rondas < self.maximo_rondas and self.hay_jugadores

    @property
    def ganador(self) -> Jugador:
        return self.jugadores[np.argmax([jugador.dinero_actual for jugador in self.jugadores])]

    def __repr__(self) -> str:
        return f"{self.jugadores}"

Accion = Enum('Accion', 'ATERRIZAR DESPEGAR COMPRAR PAGAR CONSTRUIR COBRAR SOBREVOLAR')

class Jugador:
    def __init__(self, pieza:Pieza, tablero:Tablero, dinero_inicial:int=0):
        self.pieza = pieza
        self.tablero:Tablero = tablero
        self.dinero_inicial:int = dinero_inicial
        self.dinero_actual:int = self.dinero_inicial
        self.vueltas:int = 0
        self.turnos:int = 0
        self.posicion = self.tablero.posicion_inicial
        self.propiedades:List[Pais] = []

    @property
    def quebrado(self) -> bool:
        return self.dinero_actual <= 0

    def turno(self, dados:Dados) -> None:
        self.turnos += 1
        self.mover(dados)
        if self.posicion.disponible:
            logger.debug(f"{self.posicion} está disponible")
            if self.dinero_actual >= self.posicion.precio:
                logger.debug(f"{self} comprando {self.posicion}")
                self.comprar(self.posicion)

    @log_accion(Accion.ATERRIZAR)
    def mover(self, dados:Dados) -> None:
        dados.tirar()
        logger.debug(f"{self} tiró {dados.tirada}")
        posicion_actual = self.posicion
        self.posicion = self.tablero.siguiente_pais(posicion_actual, dados.total)
        logger.info(f"{self} aterrizando en {self.posicion}")
        self.posicion.colocar(self)

    @log_accion(Accion.COMPRAR)
    def comprar(self, pais:Pais) -> None:
        logger.info(f"{self} compró {pais} por ${pais.precio}")
        self.dinero_actual -= pais.precio
        pais.dueño = self
        self.propiedades.append(pais)

    @log_accion(Accion.PAGAR)
    def pagar(self, cantidad:int) -> None:
        logger.info(f"{self} pagó ${cantidad}")
        self.dinero_actual -= cantidad

    @log_accion(Accion.COBRAR)
    def cobrar(self, cantidad:int) -> None:
        logger.info(f"{self} recibió {cantidad}")
        self.dinero_actual += cantidad

    @log_accion(Accion.CONSTRUIR)
    def construir(self) -> None:
        logger.info(f"{self} construye un restaurante por {self.posicion.costo_construccion}")


    def __repr__(self) -> str:
        return f"{self.pieza.name} @{self.posicion.nombre} ${self.dinero_actual} {self.propiedades if self.propiedades else ''}"

    def __str__(self) -> str:
        return f"{self.pieza.name}"

class Pais:
    def __init__(self, indice:int, nombre:str, precio:int,  bloque:str, renta_inicial:int, costo_construccion:int):
        self.nombre = str(nombre)
        self.indice = int(indice)
        try:
            self.precio = int(precio)
        except ValueError:
            self.precio = None
        try:
            self.renta_inicial = int(renta_inicial)
        except ValueError:
            self.renta_inicial = None
        try:
            self.costo_construccion = int(costo_construccion)
        except ValueError:
            self.costo_construccion = None
        self.bloque:Bloque = Bloque[bloque]
        self.dueño:Jugador = None
        self.construcciones: List[int] = None
        self.hipotecada:bool = False
        self.role = None

    @property
    def hipoteca(self) -> int:
        return round(self.precio/2)

    @property
    def renta(self) -> int:
        numero_construcciones = len(self.construcciones) if self.construcciones else 0
        return self.renta_inicial*self.incrementos(numero_construcciones)


    @property
    def disponible(self) -> bool:
        return self.role.disponible

    @property
    def construible(self) -> bool:
        return self.role.construible

    def colocar(self, jugador:Jugador) -> None:
        self.role.colocar(jugador)

    def incrementos(self, numero_construcciones: int) -> int:
        INCREMENTOS = [1,5,15,45,80,125]

        return INCREMENTOS[numero_construcciones]

    def __repr__(self) -> str:
        return f"{self.nombre} [{'D' if self.disponible else '' }{'H' if self.hipotecada else ''}{'C' if self.construible else ''} P: {self.precio}{', R: '+str(self.renta) if not self.disponible else ''}]"

    def __str__(self) -> str:
        return f"{self.nombre}"

def pais_role_factory(pais:Pais) -> PaisRole:
    class PaisRole(ABC):
        def __init__(self, pais:Pais):
            self.pais = pais

        @property
        def disponible(self) -> bool:
            return False

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
            logger.info(f"{jugador} llegando a una estación diplomática...")

    class ImpuestosRole(PaisRole):
        def __init__(self, pais:Pais, impuesto_fijo:int=10_000, tasa:float=0.10):
            self.impuesto_fijo = impuesto_fijo
            self.tasa = tasa
            PaisRole.__init__(self, pais)

        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"{jugador} debe de pagar impuestos")
            jugador.pagar(round(max(self.impuesto_fijo, jugador.dinero_actual*self.tasa)))

    class RegularRole(PaisRole):
        @property
        def disponible(self) -> bool:
            return self.pais.dueño is None

        @property
        def construible(self) -> bool:
            return True

        def colocar(self, jugador:Jugador) -> None:
            if self.pais.dueño and self.pais.dueño is not jugador:
                jugador.pagar(self.pais.renta)
                self.pais.dueño.cobrar(self.pais.renta)

    class ComunicacionesRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"{jugador} tomando una carta... Misteriosamente está en blanco... No hay consecuencias")

    class AeropuertoRole(PaisRole):
        @property
        def disponible(self) -> bool:
            return self.pais.dueño is None

        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"{jugador} llegando a un Aeropuerto...")

    class InicialRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"¡Bienvenido a México {jugador}! Toma $20,000")
            jugador.cobrar(20_000)

    class CarcelRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"¡{jugador} encarcelado!")
            jugador.encarcelado = True

    class DeportadoRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"¡{jugador} deportado!")
            jugador.deportado = True

    class NingunoRole(PaisRole):
        def colocar(self, jugador:Jugador) -> None:
            logger.info(f"{jugador} Disfruta del paisaje")

    if pais.bloque is Bloque.DIPLOMÁTICOS: return DiplomaticoRole(pais)
    if pais.bloque is Bloque.AEROPUERTOS: return AeropuertoRole(pais)
    if pais.bloque is Bloque.COMUNICACIONES: return ComunicacionesRole(pais)
    if pais.bloque is Bloque.INICIAL: return InicialRole(pais)
    if pais.bloque is Bloque.CÁRCEL: return CarcelRole(pais)
    if pais.bloque is Bloque.DEPORTADO: return DeportadoRole(pais)
    if pais.bloque is Bloque.IMPUESTOS: return ImpuestosRole(pais)
    if pais.bloque is Bloque.NINGUNO: return NingunoRole(pais)
    else:
        return RegularRole(pais)

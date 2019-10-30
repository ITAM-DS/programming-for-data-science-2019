# Primera iteración


from __future__ import annotations
from typing import NewType, List
from enum import Enum, auto
from abc import ABC, abstractmethod

from dataclasses import dataclass, field

from itertools import cycle

from collections import Counter

import numpy as np



# #+RESULTS:



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



# #+RESULTS:
# : [3 1] (=4)

# Las piezas en el Turista son aviones de colores, pero para darle una
# mayor variedad, copiaremos las que tiene el juego de [[https://coolmaterial.com/feature/the-story-behind-monopoly-pieces/][Monopoly]]:


Pieza = Enum('Pieza',
             'TOP_HAT BATTLESHIP RACECAR SCOTTIE_DOG CAT TREX PENGUIN RUBBER_DUCKY')



# #+RESULTS:
# : Pieza.TREX


class Pais:
    def __init__(self, nombre, posicion, tablero):
        self.nombre:str = nombre
        self.posicion:int = posicion
        self.turista:Turista =  tablero
        self.piezas:List[Pieza] = []

    def quitar(self, pieza:Pieza) -> None:
        pass

    def mover(self, movimientos:int) -> Pais:
        return self.turista.tablero[self.posicion + movimientos % self.turista.NUMERO_PAISES]


    def poner(self, jugador:Jugador) -> None:
        self.piezas.append(jugador.pieza)
        jugador.posicion = self

    def __repr__(self) -> str:
        return f"{self.nombre} [{self.posicion}]"



# #+RESULTS:



costa_rica = Pais(nombre="Costa Rica", posicion=2, tablero=None)
print(costa_rica)



# #+RESULTS:
# : Costa Rica [2]



@dataclass
class Jugador:
    pieza: Pieza
    posicion: Pais

    def turno(self, dados:Dados) -> int:
        dados.tirar()

        self.posicion.quitar(self)
        self.posicion = self.posicion.mover(dados.total)
        self.posicion.poner(self)

    @property
    def quebrado(self):
        return False


    def __repr__(self) -> str:
        return f"{self.pieza}@{self.posicion}"



# #+RESULTS:
# : Pieza.TREX@Costa Rica [2]



class Turista:

    NUMERO_PAISES = 40

    def __init__(self, numero_jugadores:int=4, maximo_rondas=50):
        self.numero_jugadores:int = numero_jugadores
        self.maximo_rondas:int = maximo_rondas
        self.jugadores:List[Jugador] = self._crear_jugadores()
        self.tablero:List[Pais] = self._crear_tablero()
        self.rondas:int = 0
        self.jugador_actual = None

    def _crear_tablero(self) -> List[Pais]:
        tablero = [Pais(f"P{posicion}", posicion, self) for posicion in range(Turista.NUMERO_PAISES)]
        return tablero

    def _crear_jugadores(self) -> List[Jugador]:
        return [Jugador(pieza=pieza,
                        posicion=None)
                for pieza in Pieza][:self.numero_jugadores]

    @property
    def posicion_inicial(self):
        return self.tablero[0]

    def colocar_tablero(self):
        for jugador in self.jugadores:
            self.posicion_inicial.poner(jugador)

        self.ganador = None

        self.rondas = 0

    def jugar(self):
        self.dados = Dados()

        self.colocar_tablero()

        print(self)

        while(self.continuar()):

            for jugador in self.jugadores:
                self.jugador_actual = jugador
                if not self.jugador_actual.quebrado:
                    self.jugador_actual.turno(dados)
            self.rondas += 1
            print(self)

        self.ganador = self.jugador_actual

    @property
    def hay_jugadores(self) -> bool:
        return all([not jugador.quebrado for jugador in self.jugadores])

    def continuar(self) -> bool:
        return self.rondas < self.maximo_rondas and self.hay_jugadores


    def __repr__(self) -> str:
        return f"{self.rondas}: {self.jugadores}"



# #+RESULTS:
# : 0: [Pieza.TOP_HAT@P0 [0], Pieza.BATTLESHIP@P0 [0], Pieza.RACECAR@P0 [0], Pieza.SCOTTIE_DOG@P0 [0]]
# : 1: [Pieza.TOP_HAT@P4 [4], Pieza.BATTLESHIP@P5 [5], Pieza.RACECAR@P7 [7], Pieza.SCOTTIE_DOG@P6 [6]]
# : 2: [Pieza.TOP_HAT@P13 [13], Pieza.BATTLESHIP@P11 [11], Pieza.RACECAR@P17 [17], Pieza.SCOTTIE_DOG@P13 [13]]



class SimuladorTurista:
    def __init__(self, numero_rondas=2, numero_simulaciones=2) -> None:
        self.numero_simulaciones = numero_simulaciones
        self.numero_rondas = numero_rondas
        self.turista:Turista = Turista(maximo_rondas=numero_rondas)

    def simular(self):
        for simulacion in range(self.numero_simulaciones):
            self.turista.jugar()

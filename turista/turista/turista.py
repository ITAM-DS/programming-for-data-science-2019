

# #+begin_notes

#     A "owns" B = Composition : B has no meaning or purpose in the system without A
#     A "uses" B = Aggregation : B exists independently (conceptually) from A

# #+end_notes


# #+CAPTION: Simulador de juegos de Turista: Primera iteración
# #+ATTR_ORG: :width 600 :height 600
# #+ATTR_HTML: :width 800px :height 600px
# #+ATTR_LATEX: :height 5cm :width 8cm
# [[file:primera_iteracion.png]]



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
# : [5 6] (=11)

# Las piezas en el Turista son aviones de colores, pero para darle una
# mayor variedad, copiaremos las que tiene el juego de [[https://coolmaterial.com/feature/the-story-behind-monopoly-pieces/][Monopoly]]:


Pieza = Enum('Pieza',
             'TOP_HAT BATTLESHIP RACECAR SCOTTIE_DOG CAT TREX PENGUIN RUBBER_DUCKY')



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




# #+CAPTION: Simulador de juegos de turista: Segunda iteración
# #+ATTR_ORG: :width 600 :height 600
# #+ATTR_HTML: :width 800px :height 600px
# #+ATTR_LATEX: :height 5cm :width 8cm
# [[file:segunda_iteracion.png]]



# Un punto /doloroso/ de nuestra primera iteración es causado por
# nuestra respuesta a la pregunta: ¿Cómo los jugadores mueven sus fichas
# en el tablero siguiendo las reglas de juego?



Bloque = Enum('Bloque',
              'ROJO MORADO VERDE NARANJA AZUL ROSA CAFÉ AMARILLO AEROPUERTOS DIPLOMÁTICOS COMUNICACIONES NINGUNO')



# #+RESULTS:
# : Costa Rica [ P: 8000, R: 1000]


# El código de la clase =Turista=, en la primera iteración era largo y
# complicado. La razón de esto[fn:1]  es la  /asignación
# de responsabilidades/, es decir, la clase hace muchas cosas.

# Vamos a dividirla en dos clases: =Tablero= y =Turista=. La responsabilidad de
# =Tablero= es contener los países y las piezas. =Turista= es el juego,
# se encarga de los turnos, contiene los jugadores y verifica si se han
# cumplido las condiciones para decretar un ganador.



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
                    self.paises.append(Pais(*[columna.strip() for columna in renglon.split(',')]))

    def siguiente_pais(self, pais_inicio, distancia) -> Pais:
        indice_final = pais_inicio.indice + distancia % Tablero.NUMERO_PAISES
        return self.paises[indice_final]

    @property
    def posicion_inicial(self) -> Pais:
        return self.paises[0]

    def __repr__(self) -> str:
        return f"{self.paises}"



# #+RESULTS:
# : [Venezuela [ P: 12000, R: 0]]

# La clase =Turista= contiene las reglas /globales/ (quién ganó, el
# sueldo a pagar por cada vuelta, las rondas, etc) y se encarga de
# manejar la colocación inicial de los jugadores en el tablero.



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
        self.ganador = None
        self.dados = Dados()

    def _crear_jugadores(self) -> List[Jugador]:
        return [Jugador(pieza=pieza, tablero=self.tablero, dinero_inicial=Turista.DINERO_INICIAL)
                for pieza in Pieza][:self.numero_jugadores]

    def jugar(self):
        self.dados = Dados()

        while(self.continuar()):
            self.ronda()

        self.ganador = self.jugador_actual

    def ronda(self) -> None:
        for jugador in self.jugadores:
            self.jugador_actual = jugador
            if not self.jugador_actual.quebrado:
                self.jugador_actual.turno(dados)
        self.rondas += 1

    @property
    def hay_jugadores(self) -> bool:
        return all([not jugador.quebrado for jugador in self.jugadores])

    def continuar(self) -> bool:
        return self.rondas < self.maximo_rondas and self.hay_jugadores

    def __repr__(self) -> str:
        return f"{self.jugadores}"



# #+RESULTS:

# Definamos un nuevo =Enum= que contenga las acciones posibles que puede
# tomar un jugador


Accion = Enum('Accion', 'ATERRIZAR DESPEGAR COMPRAR PAGAR CONSTRUIR COBRAR')



# #+RESULTS:

# #
# Con estos cambios, la clase =Jugador= ahora luce así


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
    def quebrado(self):
        return self.dinero_actual <= 0

    def turno(self, dados:Dados):
        self.turnos += 1
        self.mover(dados)

    @log_accion(Accion.ATERRIZAR)
    def mover(self, dados:Dados):
        dados.tirar()
        posicion_actual = self.posicion
        self.posicion = self.tablero.siguiente_pais(posicion_actual, dados.total)
        self.posicion.colocar(self)

    @log_accion(Accion.COMPRAR)
    def comprar(self, pais:Pais):
        if self.dinero_actual >= pais.precio:
            self.pagar(pais.precio)
            pais.dueño = self
            self.propiedades.append(pais)

    @log_accion(Accion.PAGAR)
    def pagar(self, cantidad):
        self.dinero_actual -= cantidad

    @log_accion(Accion.COBRAR)
    def cobrar(self, cantidad):
        self.dinero_actual += cantidad

    def __repr__(self) -> str:
        return f"{self.pieza.name} @{self.posicion.nombre} ${self.dinero_actual} {self.propiedades if self.propiedades else ''}"



# Diferentes países se comportan diferente, colocaremos este
# comportamiento en una clase aparte llamada =PaisRole=.



class Pais:
    def __init__(self, indice:int, nombre:str, precio:int,  bloque:Bloque, renta_inicial:int, costo_construccion:int):
        self.nombre = str(nombre)
        self.indice = int(indice)
        self.precio = int(precio)
        self.renta_inicial = int(renta_inicial)
        self.costo_construccion = int(costo_construccion)
        self.bloque = Bloque[bloque]
        self.dueño:Jugador = None
        self.construcciones: List[int] = None
        self.role = utils.pais_role_factory(self.bloque)

    @property
    def hipoteca(self) -> int:
        return self.precio/2

    @property
    def renta(self) -> int:
        numero_construcciones = len(self.construcciones) if self.construcciones else 0
        return self.renta_inicial*self.incrementos(numero_construcciones)

    @property
    def hipotecada(self) -> bool:
        self.role.hipotecada

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

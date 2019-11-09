""" Una interfaz de línea de comandos para el simulador de juegos de turista"""
import click

from dynaconf import settings

from .turista import (
    SimuladorTurista,
)

@click.command()
@click.option('--rondas', default=1, help='Número máximo de rondas por juego')
@click.option('--simulaciones', default=1, help='Número de simulaciones a ejecutar')
def simular(rondas, simulaciones):
    s = SimuladorTurista(numero_rondas=rondas, numero_simulaciones=simulaciones)
    s.simular()

if __name__ == "__main__":
    simular()

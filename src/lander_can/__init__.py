import asyncio

from .game import Game


def main():

    game = Game()
    asyncio.run(game.run())

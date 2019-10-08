# -*- coding: utf-8 -*-
import argparse, sys
import numpy as np
from random import randint

from dijkstra import Dijkstra

MATRICES = [
    np.array(
        [
            [None, 2, 3, None, None, None, None],
            [None, None, None, None, None, 10, None],
            [None, 3, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, 2, 5, None, None, 1],
            [None, None, 4, 7, 3, None, 5],
            [None, None, None, 1, None, None, None],
        ]
    ),
    np.array(
        [
            [None, 1, 3, None],
            [None, 2, None, None],
            [None, 1, None, 4],
            [None, None, 4, None],
        ]
    ),
    np.array(
        [
            [None, 2, 6, None, None, 10],
            [None, None, 4, None, 3, None],
            [None, None, None, 6, None, None],
            [None, None, None, None, 1, None],
            [None, None, 5, None, None, None],
            [None, 3, None, None, 1, None],
        ]
    ),
    np.array([[None, None, None], [1, None, 2], [3, None, None]]),
    np.array(
        [
            [None, 1, None, 3, 4, None, None, 9],
            [None, None, None, None, 1, None, 3, 4],
            [2, None, None, 5, None, None, 6, None],
            [None, None, None, None, 1, None, None, None],
            [None, None, None, None, None, None, 4, 2],
            [None, None, 7, None, None, None, None, None],
            [6, None, None, None, None, 6, None, 8],
            [None, None, None, 9, None, None, None, None],
        ]
    ),
]


class CustomError(Exception):
    pass


class Dijkstra_test:
    def __init__(self, mat, node, draw, random):
        if not random:
            if mat not in range(len(MATRICES)):
                raise CustomError(
                    f"Matrice inexistante ! (matrice disponibles: {list(range(len(MATRICES)))})"
                )

            M = MATRICES[mat]

            if node not in range(len(M)):
                raise CustomError(
                    f"Sommet {node} inexistant ! (noeuds disponibles: {list(range(len(M)))} pour la matrice {mat})"
                )
        else:
            M = self.generate_random()

        print(f"Matrice {mat if not random else 'aléatoire'} (None = pas de chemin): \n", M, "\n")

        obj = Dijkstra(M, node)
        obj.calc()

        print(obj)  # afficher le résulat dans la console

        if draw:
            obj.draw()  # afficher le graphe et le résulat sur une interface graphique

    def generate_random(self, max_int=10):
        s = randint(2, 8)
        attr = [None] + list(range(1,max_int))
        max_int -= 1
        perc = [0.6] + [0.4/max_int] * max_int
        return np.random.choice(attr, size=(s,s), p=perc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrice",
        type=int,
        default=0,
        help="Un entier identifiant de la matrice à utiliser",
    )
    parser.add_argument(
        "-n",
        "--node",
        type=int,
        default=0,
        help="Sommet de départ de la matrice choisie",
    )
    parser.add_argument(
        "-d",
        "--draw",
        dest="draw",
        action="store_true",
        help="Afficher l'interface graphique (graphe et résultat de l'algorithle de Dijkstra)",
    )
    parser.add_argument(
        "-r",
        "--random",
        dest="random",
        action="store_true",
        help="Générer une matrice aléatoire à utiliser",
    )
    args = parser.parse_args()

    try:
        Dijkstra_test(args.matrice, args.node, args.draw, args.random)  # lancer le test
    except CustomError as e:
        print("Error :\n", e, "\n")
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# DIJKSTRA

## Prérequis

* Avoir installé python (supérieur ou égale à la version : v3.6.8)
* Avoir installé pip (pour python3)

## Installation des dépendances

```
pip3 install -r requirements.txt
```

## Utilisation

```
$ python3 dijkstra_test.py --help

usage: dijkstra_test.py [-h] [-m MATRICE] [-n NODE] [-d] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -m MATRICE, --matrice MATRICE
                        Un entier identifiant de la matrice à utiliser
  -n NODE, --node NODE  Sommet de départ de la matrice choisie
  -d, --draw            Afficher l'interface graphique (graphe et résultat de
                        l'algorithle de Dijkstra)
  -r, --random          Générer une matrice aléatoire à utiliser
```
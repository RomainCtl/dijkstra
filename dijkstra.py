# -*- coding: utf-8 -*-
import warnings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

INF = 999999999


class Dijkstra:
    M: np.array
    node: int
    dist: list
    pred: list

    def __init__(self, M, node):
        M[np.isnan(M)] = INF
        self.M = M.astype(int)
        self.node = node
        self.dist = list()
        self.pred = list()

    def __construct_path(self) -> list:
        """
        create full path of predecessor for each node with 'self.pred' list
        """
        res = []
        for i in range(len(self.pred)):
            j = self.pred[i]
            res += [tuple()]
            if j == -1:
                continue  # go to next iteration
            while self.pred[j] != -1:
                res[i] += (j,)
                j = self.pred[j]

        # add parent node
        for i in range(len(self.pred)):
            if self.dist[i] != INF:
                res[i] += (self.node,)
                res[i] = res[i][::-1]  # reverse
                res[i] += (i,)
        return res

    def calc(self) -> None:
        """
        this function calc distance from selected node each others node
        and predecessor of the smallest path of each node
        with dijkstra algo
        """
        if self.node >= len(self.M):
            raise ValueError(f"Unknown node ! '{self.node}'")
        marked_node = [self.node]
        others_node = list(range(len(self.M)))
        others_node.remove(self.node)

        self.dist = list(INF for _ in range(len(self.M)))
        self.pred = list(INF for _ in range(len(self.M)))

        for i in range(len(self.M)):
            self.dist[i] = self.M[self.node, i]
            if self.M[self.node, i] != INF:
                self.pred[i] = self.node
            else:
                self.pred[i] = -1

        _dist = self.dist[:]  # copy of dist
        self.pred[self.node] = -1

        while len(others_node) != 0:
            # choose min path
            tmp = []
            for i in range(len(self.M)):
                if i in marked_node:
                    tmp += [INF]
                else:
                    tmp += [self.dist[i]]
            min_r_dist = _dist.index(sorted(tmp)[0])
            _dist[min_r_dist] = INF

            marked_node += [min_r_dist]
            if min_r_dist not in others_node:
                # no more path
                break
            others_node.remove(min_r_dist)

            for p in others_node:
                if self.dist[min_r_dist] + self.M[min_r_dist, p] < self.dist[p]:
                    _dist[p] = self.dist[p] = (
                        self.dist[min_r_dist] + self.M[min_r_dist, p]
                    )
                    self.pred[p] = min_r_dist

        self.pred = self.__construct_path()

    def draw(self) -> None:
        """
        draw table with result and network graph of M (matrice)
        """
        cells = []

        for i in range(len(self.dist)):
            if i != self.node:
                p = "->".join(map(str, self.pred[i])) or "<aucun>"
                d = (
                    "{:^17d}".format(self.dist[i])
                    if self.dist[i] != INF
                    else "<infini>"
                )
                cells.append(["{:^6d}".format(i), d, p])

        self.M[self.M == INF] = 0  # replace 'INF' by '0'
        G = nx.from_numpy_array(self.M, create_using=nx.DiGraph())
        pos = nx.circular_layout(G)
        edge_label = nx.get_edge_attributes(G, "weight")


        fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [1, 1.5]})

        # table
        a0.axis("off")
        a0.table(
            cellText=cells,
            colLabels=[
                "Sommet",
                f"Distance depuis {self.node}",
                "Chemin le plus court",
            ],
            loc="center",
        )
        a0.set_title(f"Sommet de départ : {self.node}")

        # directed graph
        warnings.simplefilter("ignore")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_label, ax=a1)
        nx.draw_networkx(G, pos, node_size=500, with_labels=True, arrows=True, connectionstyle='arc3,rad=0.06', ax=a1)
        a1.set_title("*lorsqu'une liaison entre deux sommets est à double sens,\n il n'y a que un coût de transfer affiché (sur 2), veuillez vérifier avec la matrice affiché dans la console.", fontdict=dict(fontsize=8))

        fig.tight_layout()
        plt.show()

    def __str__(self) -> str:
        """
        return object as string
        """
        res = f"Sommet de départ : {self.node}\n"
        res += f"Sommet | Distance depuis {self.node} | Chemin le plus court\n"
        for i in range(len(self.dist)):
            if i != self.node:
                p = "->".join(map(str, self.pred[i])) or "<aucun>"
                d = (
                    "{:^17d}".format(self.dist[i])
                    if self.dist[i] != INF
                    else "    <infini>     "
                )
                res += "{:^6d} | {} | {}\n".format(i, d, p)
        return res


if __name__ == "__main__":
    print("Try : python3 dijkstra_test.py --help ")

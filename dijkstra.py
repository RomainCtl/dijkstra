# -*- coding: utf-8 -*-
import warnings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

INF = 999999999


class Dijkstra:
    M: np.array
    peak: int
    dist: list
    pred: list

    def __init__(self, M, peak):
        self.M = M
        self.peak = peak
        self.dist = list()
        self.pred = list()

    def __construct_path(self) -> list:
        """
        create full path of predecessor for each peak with 'self.pred' list
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

        # add parent peak
        for i in range(len(self.pred)):
            if self.dist[i] != INF:
                res[i] += (peak,)
                res[i] = res[i][::-1]  # reverse
                res[i] += (i,)
        return res

    def calc(self) -> None:
        """
        this function calc distance from selected peak each others peak
        and predecessor of the smallest path of each peak
        with dijkstra algo
        """
        if self.peak >= len(self.M):
            raise ValueError(f"Unknown peak ! '{self.peak}'")
        marked_peak = [self.peak]
        others_peak = list(range(len(self.M)))
        others_peak.remove(self.peak)

        self.dist = list(INF for _ in range(len(self.M)))
        self.pred = list(INF for _ in range(len(self.M)))

        for i in range(len(self.M)):
            self.dist[i] = self.M[self.peak, i]
            if self.M[self.peak, i] != INF:
                self.pred[i] = self.peak
            else:
                self.pred[i] = -1

        self.dist[self.peak] = 0
        _dist = self.dist[:]  # copy of dist
        self.pred[self.peak] = -1

        while len(others_peak) != 0:
            # choose min path
            tmp = []
            for i in range(len(self.M)):
                if i in marked_peak:
                    tmp += [INF]
                else:
                    tmp += [self.dist[i]]
            min_r_dist = _dist.index(sorted(tmp)[0])
            _dist[min_r_dist] = INF

            marked_peak += [min_r_dist]
            if min_r_dist not in others_peak:
                # no more path
                break
            others_peak.remove(min_r_dist)

            for p in others_peak:
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
            if i != self.peak:
                p = "->".join(map(str, self.pred[i])) or "<aucun>"
                d = (
                    "{:^17d}".format(self.dist[i])
                    if self.dist[i] != INF
                    else "<infini>"
                )
                cells.append(["{:^6d}".format(i), d, p])

        N = self.M[:]
        N[N == INF] = 0  # replace 'INF' by '0'
        G = nx.from_numpy_array(N, create_using=nx.DiGraph())
        pos = nx.circular_layout(G)
        edge_label = nx.get_edge_attributes(G, "weight")

        fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw={"height_ratios": [1, 1.5]})

        # table
        a0.axis("off")
        a0.table(
            cellText=cells,
            colLabels=[
                "Sommet",
                f"Distance depuis {self.peak}",
                "Chemin le plus court",
            ],
            loc="center",
        )
        a0.set_title(f"Sommet de départ : {self.peak}")

        # directed graph
        warnings.simplefilter("ignore")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_label, ax=a1)
        nx.draw_networkx(G, pos, node_size=500, with_labels=True, arrows=True, ax=a1)

        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    M = np.array(
        [
            [INF, 2, 3, INF, INF, INF, INF],
            [INF, INF, INF, INF, INF, 10, INF],
            [INF, 3, INF, INF, INF, INF, INF],
            [INF, INF, INF, INF, INF, INF, INF],
            [INF, INF, 2, 5, INF, INF, 1],
            [INF, INF, 4, 7, 3, INF, 5],
            [INF, INF, INF, 1, INF, INF, INF],
        ]
    )
    peak = 0

    obj = Dijkstra(M, peak)
    obj.calc()
    obj.draw()

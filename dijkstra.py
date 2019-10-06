# -*- coding: utf-8 -*-
import numpy as np

INF = 999999999


def dijkstra(M, r):
    """
    param:
        M array numpy matrice
        r int sommet

    return:
        two list, distance to go to each peak and predecessor  of each peak
    """
    if r >= len(M):
        raise ValueError(f"Unknown peak ! '{r}'")
    marked_peak = [r]
    others_peak = list(range(len(M)))
    others_peak.remove(r)

    dist = list(INF for _ in range(len(M)))
    pred = list(INF for _ in range(len(M)))

    for i in range(len(M)):
        dist[i] = M[r, i]
        if M[r, i] != INF:
            pred[i] = r
        else:
            pred[i] = -1

    dist[r] = 0
    _dist = dist[:]  # copy of dist
    pred[r] = -1

    while len(others_peak) != 0:
        # choose min path
        tmp = []
        for i in range(len(M)):
            if i in marked_peak:
                tmp += [INF]
            else:
                tmp += [dist[i]]
        min_r_dist = _dist.index(sorted(tmp)[0])
        _dist[min_r_dist] = INF

        marked_peak += [min_r_dist]
        if min_r_dist not in others_peak:
            # no more path
            break
        others_peak.remove(min_r_dist)

        for p in others_peak:
            if dist[min_r_dist] + M[min_r_dist, p] < dist[p]:
                _dist[p] = dist[p] = dist[min_r_dist] + M[min_r_dist, p]
                pred[p] = min_r_dist

    return dist, pred


def construct_predecessor_path(dist, pred, peak):
    res = []
    for i in range(len(pred)):
        j = pred[i]
        res += [tuple()]
        if j == -1:
            continue  # go to next iteration
        while pred[j] != -1:
            res[i] += (j,)
            j = pred[j]

    # add parent peak
    for i in range(len(pred)):
        if dist[i] != INF:
            res[i] += (peak,)
            res[i] = res[i][::-1]  # reverse
    return res


if __name__ == "__main__":
    M = np.array(
        [
            [0, 2, 3, INF, INF, INF, INF],
            [INF, 0, INF, INF, INF, 10, INF],
            [INF, 3, 0, INF, INF, INF, INF],
            [INF, INF, INF, 0, INF, INF, INF],
            [INF, INF, 2, 5, 0, INF, 1],
            [INF, INF, 4, 7, 3, 0, 5],
            [INF, INF, INF, 1, INF, INF, 0],
        ]
    )
    peak = 0
    distance, predecessor = dijkstra(M, peak)
    predecessor = construct_predecessor_path(distance, predecessor, peak)

    print(f"Sommet de départ : {peak}")
    print(f"Sommet | Distance depuis {peak} | Chemin le plus court")
    for i in range(len(distance)):
        if i != peak:
            p = "->".join(map(str, predecessor[i])) or "<aucun>"
            d = "{:^17d}".format(distance[i]) if distance[i] != INF else "    <infini>     "
            print("{:^6d} | {} | {}".format(i, d, p))

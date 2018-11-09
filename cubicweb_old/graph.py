def dijkstra(arcs, orig, target):
    distances = {}
    arcs_dict = {}
    for arc in arcs:
        n_from = arc[0]
        n_to = arc[1]
        distances[n_from] = None
        distances[n_to] = None
        arcs_dict.setdefault(n_from, []).append((n_to, arc))
        arcs_dict.setdefault(n_to, []).append((n_from, arc))
    if orig not in distances:
        return []
    distances[orig] = 0 
    subgraph = set(distances.keys())
    previous = {}
    while subgraph:
        node, dist = _find_min(distances, subgraph)
        if dist is None: # no reachable node left
            break
        subgraph.remove(node)
        for neighbor, arc in arcs_dict[node]:
            if neighbor not in subgraph:
                continue
            alt = 1 + dist # all weights are the same
            if distances[neighbor] is None or distances[neighbor] > alt:
                distances[neighbor] = alt
                previous[neighbor] = node, arc
    path = []
    curr = target
    while curr in previous:
        prev, arc = previous[curr]
        path.append((prev, curr, arc))
        curr = prev
    return path[::-1]

def _find_min(distances, keys):
    mindist = None
    target = None
    for node in keys:
        dist = distances[node]
        if dist is None:
            continue
        if mindist is None or dist < mindist:
            mindist = dist
            target = node
    return target, mindist


if __name__ == '__main__':
    arcs = [(0, 1), (1, 2), (3, 1), (2, 3)]
    print dijkstra(arcs, 0, 3)
    arcs = [(0, 1), (4, 2), (1, 4), (5, 3), (0, 4)]
    print dijkstra(arcs, 0, 3)

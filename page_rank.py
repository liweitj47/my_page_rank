def page_rank(graph, damp=0.85, max_iter=100, min_delta=1e-5):
    node_num = len(graph)
    PR = {node: 1. / node_num for node in graph.nodes}  # initial values
    damping_value = (1 - damp) * (1 / node_num)
    for iter in range(max_iter):
        change = 0
        for node in graph.nodes():
            rank_sum = 0
            neighbors = graph.in_edges(node)  # find the nodes that point to the current one
            for n in neighbors:
                outlinks = graph.out_degree(n[0])  # the number of out edges of the incident page
                if outlinks > 0:
                    rank_sum += (1 / outlinks) * PR[n[0]]
                    # the PR of the incident page times the reciprocal of the number out edges
            rank = damping_value + damp * rank_sum
            change += abs(PR[node] - rank)
            PR[node] = rank
        
        if change < min_delta:
            print('finished in %d iterations' % (iter))
            break
    return PR


def link_rank(graph, damp=0.85, max_iter=100, min_delta=1e-5):
    node_num = len(graph)
    PR = {node: 1. / node_num for node in graph.nodes}  # initial values
    LR = {edge: [PR[edge[0]] * 1. / graph.out_degree(edge[0]), graph[edge[0]][edge[1]]['label']] for edge in
          graph.edges}
    damping_value = (1 - damp) * (1 / node_num)
    for iter in range(max_iter):
        print('%d iteration' % (iter), flush=True)
        change = 0
        for node in graph.nodes():
            rank_sum = 0
            incidents = graph.in_edges(node)  # find the nodes that point to the current one
            for e in incidents:
                rank_sum += LR[e][0]
            rank = damping_value + damp * rank_sum
            change += abs(PR[node] - rank)
            PR[node] = rank
        for node in graph.nodes:
            emergents = graph.out_edges(node)
            PR_emergents_sum = sum([math.exp(PR[i[1]]) for i in emergents])
            for e in emergents:
                LR[e][0] = PR[e[0]] * math.exp(PR[e[1]]) / PR_emergents_sum
        if change < min_delta:
            print('finished in %d iterations' % (iter))
            break
    return PR, LR

graph = {'A' : {'B':10, 'C':5, 'D':8}, 
          'B' : {'A':10,'E':9}, 
          'C' : {'A':5, 'D':2,'E':5},
          'D' : {'A':8, 'F':20, 'C':2},
          'E' : {'C':5, 'F':12, 'B':9},
          'F' : {'D':20, 'E': 12}}
queue = [['A', 0,['A']], ['B', 1000,[]], ['C', 1000,[]], ['D', 1000,[]], ['E', 1000,[]], ['F', 1000,[]]]
nodes_visited = []
def find_path(graph, queue, nodes_visited):
    temp_node = queue[0][0] 
    temp_dist = queue[0][1] 
    temp_route = queue[0][2].copy()
    for node in graph[temp_node].keys():
        for value in queue:
            if node == value[0]:
                if value[1] > graph[temp_node][node] + temp_dist:
                    value[1] = graph[temp_node][node] + temp_dist
                    value[2] = temp_route.copy()
                    value[2].append(value[0])
                    break
    nodes_visited.append(queue.pop(0))
    queue.sort(key = lambda x : x[1])
    if len(queue) == 0:
        return nodes_visited
    nodes_visited = find_path(graph, queue, nodes_visited)
    return nodes_visited

answer = find_path(graph, queue, nodes_visited)
print(answer)
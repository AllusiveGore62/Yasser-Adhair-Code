graph = {'A' : ['B', 'C'], 
          'B' : ['E','G'], 
          'C' : ['D'],
          'D' : ['C','G'],
          'E' : ['F','B'],
          'F' : ['E'],
          'G' : ['H', 'D', 'B'],
          'H' : ['G']} 

queue = ['A']
visited_set = set(queue)
visited = ['A']
def breadth(graph, queue, nodes_visited, nodes_visited_set):
    if len(queue) == 0:
        return nodes_visited, nodes_visited_set
    temp_node = queue.pop(0)
    for index,node in enumerate(graph[temp_node]):
        if node in nodes_visited_set:
            pass
        else:
            queue.insert(0+index,node) #Makes sure they are inserted in the correct order (left first)
    if temp_node in nodes_visited_set:
        pass
    else:
        nodes_visited.append(temp_node)
        nodes_visited_set.add(temp_node)
    nodes_visited, nodes_visited_set = breadth(graph, queue, nodes_visited, nodes_visited_set)
    return nodes_visited, nodes_visited_set
final, final_set = breadth(graph, queue, visited, visited_set)
print(final) 

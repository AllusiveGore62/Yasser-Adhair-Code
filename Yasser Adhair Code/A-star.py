class Node:
    def __init__(self,name,connecting_name, connecting_value, coordinates):
        self.name = name
        self.links = dict()
        for i in range(len(connecting_name)):
            self.links[connecting_name[i]] = connecting_value[i]
        self.cords = coordinates
        self.visited = False
        self.dist = 1000
    def find_heuristic(self, point_cords):
        self.hdist = abs(point_cords[0] - self.cords[0]) + abs(point_cords[1] - self.cords[1])    
    def new_path(self, path, dist):
        path.append(self.name)
        self.path = path
        self.dist = dist

A = Node('A', ['C','D'], [10,4],[2,2])
B = Node('B', ['C','F'], [6,4],[3,20])
C = Node('C', ['A','B','E'], [10,6,4],[3,13])
D = Node('D', ['A','E'], [4,1],[4,7])
E = Node('E', ['C','D','G','H','J'], [4,1,4,6,7],[6,8])
F = Node('F', ['B','I'], [4,5],[8,20])
G = Node('G', ['E','K'], [4,7],[8,3])
H = Node('H', ['E','I','M'], [6,9,6],[12,13])
I = Node('I', ['F','H','L'], [5,9,5],[14,23])
J = Node('J', ['E','K'], [7,5],[14,8])
K = Node('K', ['G','J', 'N'], [7,5,2],[16,2])
L = Node('L', ['I','M'], [5,4],[19,19])
M = Node('M', ['H','L'], [6,4],[19,14])
N = Node('N', ['K'], [2],[19,2])

node_list = [A,B,C,D,E,F,G,H,I,J,K,L,M,N]
name_set = set([node.name for node in node_list])
start_node_found = False
end_node_found = False
while start_node_found == False:
    start_node_name = str(input())
    if start_node_name in name_set:
        for node in node_list:
            if node.name == start_node_name:
                start_node = node
        start_node.dist = 0
        start_node.path = [start_node.name]
        start_node_found = True
        break
    else:
        print('Input valid node')
while end_node_found == False:
    end_node_name = str(input())
    if end_node_name in name_set and end_node_name != start_node_name:
        for node in node_list:
            if node.name == end_node_name:
                end_node = node
        end_node_found = True
        break
    else:
        print('Input valid node')

for node in node_list:
    node.find_heuristic(end_node.cords)

def find_path(nodes, start, end):
    if end.name in start.links.keys():
        dist = start.dist + start.links[end.name]
        end.new_path(start.path,dist)
        return start.path, dist
    else:
        min = 1000
        for node in start.links.keys():
            for temp_node in nodes:
                if temp_node.name == node:
                    if start.links[node] + temp_node.hdist + start.dist < min and temp_node.visited == False:
                        min = start.links[node] + temp_node.hdist + start.dist
                        min_node = temp_node
        start.visited = True
        min_node.new_path(start_node.path,start.links[min_node.name] + start.dist)
        route, distance = find_path(nodes, min_node,end)
        return route, distance
        
route, distance = find_path(node_list, start_node, end_node)
print(route)
print(distance)
        

                

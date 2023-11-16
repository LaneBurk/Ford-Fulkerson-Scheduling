from collections import deque

class Node:
    def __init__(self, name, edges):
        self.name = name
        #Edges are a list of form [tail node, head node, value]
        self.edgesTo = list(filter(lambda x: x[1] == name, edges))
        self.edgesFrom = list(filter(lambda x: x[0] == name, edges))

    def __str__(self):
        string = 'Name:\n' + self.name + '\nEdges:\n'
        for edge in self.edgesTo:
            string += str(edge[0]) + ' --> ' + str(edge[1]) + '\n'
        for edge in self.edgesFrom:
            string += str(edge[0]) + ' --> ' + str(edge[1]) + '\n'
        
        return string[:-1]
            

class Graph:
    def __init__(self, edges):
        self.nodes = {}
        self.edges = {}
        for edge in edges:
            if edge[0] not in self.nodes:
                #List comprehension pulls every edge that the tail node is part of
                newNode = Node(edge[0], [nodeEdge for nodeEdge in edges if edge[0] in nodeEdge])
                self.nodes[newNode.name] = newNode
            if edge[1] not in self.nodes:
                #List comprehension pulls every edge that the head node is part of
                newNode = Node(edge[1], [nodeEdge for nodeEdge in edges if edge[1] in nodeEdge])
                self.nodes[newNode.name] = newNode
            self.edges[(edge[0], edge[1])] = edge
        
    def node(self, name):
        if name in self.nodes:
            return self.nodes[name]
        print("No node by this name in graph")
        return None


    #Node must be node object
    def addNode(self, node):
        if node.name not in self.nodes:
            self.nodes[node.name] = node
            for edge in node.edgesTo + node.edgesFrom:
                self.edges[(edge[0], edge[1])] = edge
                if edge in node.edgesTo and self.node(edge[0]) is not None:
                    self.nodes[edge[0]].edgesFrom.append(edge)
        else:
            print("There is alrady a node with this name in the graph")

    #edge in [tail node, head node, value], node names as strings and value as an int
    def addEdge(self, edge):
        nodeH = None
        nodeT = None
        #Find Node objects for the tail and head, if they exist
        if edge[0] in self.nodes:
            nodeT = self.nodes[edge[0]]
        if edge[1] in self.nodes:
            nodeH = self.nodes[edge[1]]

        #Both exist just add the edge
        if nodeH and nodeT:
            nodeT.edgesFrom.append(edge)
            nodeH.edgesTo.append(edge)
        #Must add new node for tail, then add edge
        elif nodeH:
            newNode = Node(edge[0], [edge])
            self.addNode(newNode)
            nodeH.edgesTo.append(edge)
        #Must add new node for head, then add edge
        elif nodeT:
            newNode = Node(edge[1], [edge])
            self.addNode(newNode)
            nodeT.edgesFrom.append(edge)
        #Add new edges for both, then edge
        else:
            newHNode = Node(edge[1], [edge])
            newTNode = Node(edge[0], [edge])
            self.addNode(newHNode)
            self.addNode(newTNode)
        self.edges[(edge[0], edge[1])] = edge
        
    #Used to let print() work with Graph objects
    def __str__(self):
        string = ''
        for node in list(self.nodes.values()):
            for edge in node.edgesFrom:
                string += str(edge[0]) + ' --> ' + str(edge[1]) + '\n'
        return string[:-1]
    

    # Use DFS to check for a path between start s and destination d
    #Code adapted from https://www.techiedelight.com/find-path-between-vertices-directed-graph/
    def DFS(self, s, d, visited, path):
        # Mark the start node as visited and add it to the path
        visited[s] = True
        path.append(s)

        #If destination is reached return true
        if s == d:
            return True
        
        #Find node object for start node
        sNode = None
        sNode = self.nodes[s]

        #For every edge out of s, check to see if there is a path from
        #that node to d.
        for i in sNode.edgesFrom:
            if not visited[i[1]]:
                #Return true if destination is found
                if self.DFS(i[1], d, visited, path):
                    return True

        #Backtrack by removing current node from path
        path.pop()

        #Return false if d is not reachable from s
        return False

    #Takes the names of a source and destination node as strings
    def findPath(self, s, d):
        if s not in self.nodes or d not in self.nodes:
            print("One or more of s and d not in graph")
            return []
        #Mark every node as not visited
        visited = {node.name : False for node in list(self.nodes.values())}
        global path
        path = deque()
        self.DFS(s, d, visited, path)
        edgesPath = []
        path = list(path)

        for i in range(len(path) - 1):
            edgesPath += [self.edges[(path[i], path[i+1])]]
        path = edgesPath

        return (path)

#Example

'''
edges = [['A', 'B'], ['A', 'C'], ['B', 'C'], ['B', 'D'], ['C', 'D'],
         ['D', 'C'], ['E', 'F'], ['F', 'C']]
graph = Graph(edges)
print(graph)

node = Node("W", [["A", "W"], ["W", "E"]])
graph.addNode(node)
print("Added node W with edges to A and E")
print(graph)
graph.addEdge(["C", "A"])
print("Added edge from C to A")
print(graph)
print(graph.findPath("W", "B"))
'''

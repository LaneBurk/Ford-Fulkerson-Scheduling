from NodeGraph import *
from random import sample, randint
from timeit import timeit

def genTestCase(n):
    avail = {}
    days = ['d' + str(i) for i in range(1, n + 1)]
    for i in range(1, n+1):
        avail['p' + str(i)] = sample(days, randint(0,n))
    return avail

def makeEdges(avail):
    edges = []
    for person in avail:
        for i in range(1,len(avail) + 1):
            day = 'd' + str(i)
            if day not in avail[person]:
                edges.append([person, day, 1])
    for i in range(1,len(avail) + 1):
            edges.append(['d' + str(i), 'T', 1])
            edges.append(['S', 'p' + str(i), 1])
    return edges

def wrapper(func, *args): #wraps a function to allow the timeit function to use it
        def wrapped():
            return func(*args)
        return wrapped
    
def makeResidualGraph(graph, flow):
    #Make empty graph, then have it inherit all nodes, but no edges.
    resGraph = Graph([])

    for node in list(graph.nodes.values()):
        resGraph.addNode(Node(node.name, []))

    #Add a backward edge to the res graph anywhere the flow is 1
    #Add a foreward edge anywhere the flow is 0
    for edge in list(graph.edges.values()):
        if flow[tuple(edge[:2])] == 0:
            #add a forward edge to the residual graph
            resGraph.addEdge([edge[0], edge[1], 1])
        else:
            #add a backward edge to the residual graph
            #Then add it to the flow dict with flow 0
            resGraph.addEdge([edge[1], edge[0], -1])
            flow[tuple([edge[1], edge[0]])] = 0
    return resGraph, flow

def augment(flow, path):
    for edge in path:
        #This means its a forward edge, add one to the flow for that edge
        if edge[2] == 1:
            flow[tuple(edge[:2])] += 1
        #Backward edge, take one away from the flow
        else:
            flow[tuple(edge[:2])] -= 1
    return flow


def fordFulk(avail, edges):
    graph = Graph(edges)

    #Set flow on all edges to 0
    flow = {}
    for edge in list(graph.edges.values()):
        flow[tuple(edge[:2])] = 0

    #Find some path from source to sink, then set flow on that path to 1
    path = graph.findPath("S", "T")
    for edge in path:
        flow[tuple(edge[:2])] = 1

    #Make the residual graph for the new flow, then make a path on it.
    resGraph, flow = makeResidualGraph(graph, flow)
    path = resGraph.findPath("S", "T")

    #While there is a path from source to sink
    while path != []:
        flow = augment(flow, path)
        resGraph, flow = makeResidualGraph(resGraph, flow)
        path = resGraph.findPath("S", "T")
        
    #Theoretical maximum flow
    TFlow = sum([edge[2] for edge in graph.node("S").edgesFrom])
    #Max flow found by the algorithm
    maxFlow = sum([flow[tuple(edge[:2])] for edge in graph.node("S").edgesFrom])
    if TFlow == maxFlow:
        #print("Ergonomic")
        for key in flow:
            if key[0] != "S" and key[1] != "T": 
                if flow[key] == 1 and key[0] in avail:
                    True
                    #print(key)
    else:
        #Prints a certificate to show why no matching exists
        A = []
        AEdges = []
        for node in list(resGraph.nodes.values()):
            if resGraph.findPath("S", node.name) != []:
                A.append(node.name)
        A = [node for node in A if node in avail]
        for node in A:
            for edge in graph.node(node).edgesFrom:
                if edge[1] not in AEdges:
                    AEdges.append(edge[1])                   
        '''
        print("Not Ergonomic")
        print("A: ", A)
        print("Adjacent to A: ", AEdges)
        '''
        
        
    return flow

avail = {'p1' : ['d1', 'd4'], 'p2' : ['d2'], 'p3' : ['d1', 'd2', 'd4'], 'p4' : []}
edges = makeEdges(avail)

fordFulk(avail, edges)

print("")

avail = {'p1' : ['d2', 'd3', 'd4'], 'p2' : ['d2', 'd3', 'd4'], 'p3' : [], 'p4' : []}
edges = makeEdges(avail)

fordFulk(avail, edges)


for i in range(1,21):
    avail = genTestCase(i)
    edges = makeEdges(avail)
    x = wrapper(fordFulk, avail, edges)
    print(i, timeit(x, number = 5000)/5000) 




                      

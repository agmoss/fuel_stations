import math
import pickle

class Graph:
    '''
    class for a simple undirected graph. Nodes can contain descriptive data, and edges can contain weights.
    
    '''

    def __init__(self,graph_dict={},edges=[]):
        
        self.graph_dict={}
        self.edges = []
    
    @staticmethod
    def savePickle(G,file_name):
        outfile = open(file_name,'wb')
        pickle.dump(G.getGraph(),outfile)
        outfile.close()
    
    #@staticmethod
    def readPickle(self,file_name):
        infile = open(file_name,'rb')
        G = pickle.load(infile)
        infile.close()
        self.graph_dict=G
        #self.graph_dict = G
        #return(g)
        
    def addNode(self,node,neighbor=None,attributes={}):        
        if node not in self.graph_dict:
            self.graph_dict[node] = {'attributes':attributes,'connections':{}}
    
    def nodes(self):
        return(list(self.graph_dict.keys()))
    
    def node(self,n):
        return(self.graph_dict[n])

    # TODO: make sure that duplicate edges cant be added!
    def addEdge(self, node, neighbour, weight=None):
        if node not in self.graph_dict:
            self.addNode(node)
        if neighbour not in self.graph_dict:
            self.addNode(neighbour)
        
        self.graph_dict[node]["connections"][neighbour] = weight
        self.graph_dict[neighbour]["connections"][node] = weight
        self.edges.append([node, neighbour])

    def is_connection(self, node, neighbour):
        """
        uses hashing to quickly check if there is a connection. The worst case run time is a double hash lookup (n=number of nodes)
        """

        try:
            self.graph_dict[node]["connections"][neighbour]
            connection = True
        except KeyError:

            try:
                self.graph_dict[neighbour]["connections"][node]
                connection = True
            except KeyError:
                connection = False

        return connection

    # gets all direct connections
    def node_neighbors(self, node):
        neighbors = []
        for key in self.graph_dict[node]["connections"]:
            neighbors.append(key)

        return neighbors

    def edge_weight(self, node, neighbour):
        return self.graph_dict[node]["connections"][neighbour]

    def show_edges(self):
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                print("(", node, ", ", neighbour, ")")

    def remove_edges(self, edge_list):

        for edge in edge_list:
            del self.graph_dict[edge[0]]["connections"][edge[1]]
            del self.graph_dict[edge[1]]["connections"][edge[0]]

    def getGraph(self):
        return self.graph_dict

    def number_of_nodes(self):
        return len(self.graph_dict)

    def number_of_edges(self):
        return len(self.edges)

    def bfs(self, start_node, target=None):

        queue = []
        visited = {}
        queue.append(start_node)
        visited[start_node] = True
        level = {start_node: 0}
        parent = {start_node: None}
        i = 1

        while len(queue) != 0:
            node = queue.pop(0)
            node_neighbors = self.node_neighbors(node)
            for n in node_neighbors:
                if n not in visited:
                    queue.append(n)
                    visited[n] = True
                    level[n] = i
                    parent[n] = node
            i = i + 1

        shortest_path = []
        if target != None:
            x = target
            while x != start_node:
                x = parent[x]
                shortest_path.append(x)

            shortest_path.reverse()
            shortest_path.append(target)

        return (level, parent, shortest_path)

    def dijkstra(self, start,end=None):

        routes_from_city = {}
        visited_cities = []
        current_city = start

        for node in self.graph_dict:
            if node == start:
                routes_from_city[node] = [0, node]
            else:
                routes_from_city[node] = [math.inf, None]

        while current_city:
            visited_cities.append(current_city)

            neighbors = self.node_neighbors(current_city)

            for next_city in neighbors:
                price = self.edge_weight(current_city, next_city)

                if (routes_from_city[next_city][0] > price + routes_from_city[current_city][0]):
                    routes_from_city[next_city] = [price + routes_from_city[current_city][0],current_city]

            # find the cheapest unvisited neighbor

            current_city = None
            cheapest_route = math.inf
            for key, val in routes_from_city.items():
                price, previous_city = val[0], val[1]
                if price < cheapest_route and key not in visited_cities:
                    cheapest_route = price
                    current_city = key

        if end != None:
            next_city = end
            route = [end]
            
            while next_city != start:
                stop = routes_from_city[next_city][1]
                route.append(stop)
                next_city = stop
            route = route[::-1]  
            return(route)
        else:            
            return(routes_from_city)


if __name__ == "__main__":
    g= Graph()
    g.readPickle(r'C:\Users\mossgran\Documents\fuel_stations\ny_pickles\ELEC_CA_Max_500_Min_50.pickle')
#    g.addEdge('Calgary','Edmonton',weight=300)
#    g.addEdge('Calgary','Red Deer',weight=150)
#    g.addEdge('Red Deer','Edmonton',weight=150)
#    g.addEdge('Calgary','Banff',weight=126)
#    g.addEdge('Banff','Kelowna',weight=500)
#    g.addEdge('Kelowna','Vancouver',weight=100)
    
    #print(g.number_of_nodes())
    #G = g.getGraph()
    #'Calgary_T2E 8L6','London_N6L 1H5'
    path = g.dijkstra(start = 'Calgary_T2E 8L6')

#%%

 
















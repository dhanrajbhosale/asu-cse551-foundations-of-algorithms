import collections


def my_split(x):
    t = x.strip().split("\t")
    t[2] = int(t[2])
    t[3] = int(t[3])
    t[4] = int(t[4])
    return t


def get_flight_data():
    with open('data/flights.txt') as f:
        lines = f.readlines()
        return list(map(my_split, lines))


class Graph:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    # self.COL = len(gr[0])

    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''

    def BFS(self, s, t, parent):

        # Mark all the vertices as not visited
        visited = [False] * (self.ROW)

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

        # We didn't reach sink in BFS starting
        # from source, so return false
        return False

    # Returns the maximum flow from s to t in the given graph
    def FordFulkerson(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * (self.ROW)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.BFS(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        return max_flow


def t_convert(h):
    t_array = [18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    return t_array[h]


def main():
    graph = [[0]*242 for i in range(242)]
    airports_start = {'ORD': 0, 'ATL': 24, 'IAD': 48, 'SFO': 72, 'LAX': 96, 'BOS': 120, 'SEA': 144, 'DEN': 168, 'PHX': 192, 'JFK': 216}
    source, sink = 240, 241
    flight_data = get_flight_data()

    # draw edges for dummy nodes
    for i in range(24):
        graph[source][airports_start['LAX']+i]= float('inf')
        graph[airports_start['JFK'] + i][sink] = float('inf')

    # draw edges for actual flight
    for d_air, a_air, d_time, a_time, capacity in flight_data:
        row = airports_start[d_air] + t_convert(d_time)
        col = airports_start[a_air] + t_convert(a_time)
        graph[row][col] = capacity

    g = Graph(graph)
    print("The maximum possible flow is:", g.FordFulkerson(source, sink))


if __name__ == "__main__":
    main()
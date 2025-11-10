import heapq
from math import inf

def astar(graph,start,goal,h):
    openpq=[]
    heapq.heappush(openpq,(h[start],start))

    g={node: inf for node in graph}
    g[start]=0.0

    parent={start:None}

    while openpq:
        f_u,u=heapq.heappop(openpq)

        if u==goal:
            
            path=[]
            cur=u
            while cur is not None:
                path.append(cur)
                cur=parent[cur]
            path.reverse()
            return g[u],path
        
        for v,w in graph[u]:
            tentative=w+g[u]
            if tentative<g.get(v,inf):
                g[v]=tentative
                parent[v]=u
                f_v=tentative+h.get(v,0.0)
                heapq.heappush(openpq,(f_v,v))
    return inf,None

n=int(input("Enter the no.of nodes: "))

nodes=input("Enter the name of nodes: ").split()
graph={}
h={}

print(f"Enter the neigbour & weight of the nodes (type done to stop)")

for node in nodes:
    graph[node]=[]

   

    while True:
        entry=input(f"Neighbours of {node}: ")
        if entry=="done":
            break
        v,w=entry.split()
        w=float(w)
        graph[node].append((v,w))

print("Enter the heuristic values:")
for node in nodes:
    h[node]=float(input(f"h[{node}]: "))

start=input("Enter start node")
goal=input("Enter goal node")
cost,path=astar(graph,start,goal,h)

print("A* cost: ",cost)
print("A* path: ","->".join(path))
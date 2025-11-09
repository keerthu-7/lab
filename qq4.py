import math
def tsp(dist,n):
    memo=[[-1]*(1<<n) for _ in range(n)]
    parent=[[-1]*(1<<n) for _ in range(n)]
    start=int(input("Enter the start city"))-1

    def dp(pos,mask):
        if mask==(1<<n)-1:
            return dist[pos][start]
        if memo[pos][mask]!=-1:
            return memo[pos][mask]
        
        best,best_next=math.inf,-1
        
        
        for nxt in range(n):
            if not(mask&(1<<nxt)):
                cost=dist[pos][nxt]+dp(nxt,mask|(1<<nxt))
                if cost<best:
                    best,best_next=cost,nxt
        
        memo[pos][mask]=best
        parent[pos][mask]=best_next
    
        return best

    
    cost=dp(start,1<<start)
    cur,mask=start,1<<start
    path=[]
    path.append(start)

    while True:
        nxt=parent[cur][mask]
        if nxt==-1:
            break
        path.append(nxt)
        cur=nxt
        mask|=(1<<nxt)
    path.append(start)

    return cost,path
    
n=int(input("Enter no.of cities"))
dist=[]

for i in range(n):
    dist_row=list(map(int,input(f"Row {i+1}: ").split()))
    dist.append(dist_row)

cost,path=tsp(dist,n)

print(f"Optimal cost: {cost}")
print(f"Optimal path: ","->".join(str(p+1) for p in path))
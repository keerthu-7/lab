import random

class WumpusWord:
    def __init__(self,size=4,pits=3):
        self.size,self.agent,self.gold_got=size,[0,0],False
        self.alive,self.w_alive,self.arrow=True,True,True
        self.wumpus=self.cell([[0,0]])
        self.gold=self.cell([[0,0],self.wumpus])
        self.pits=[self.cell([[0,0],self.wumpus,self.gold]) for _ in range(pits)]
        self.percepts=[[[] for _ in range(size)] for _ in range(size)]
        self.gen_percepts()
    
    def cell(self,exc=[]):
        
        while True:
            r,c=random.randrange(self.size),random.randrange(self.size)
            if [r,c] not in exc:
                return (r,c)
    
    def nbrs(self,r,c):
        return [(r+dr,c+dc) for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)] 
                if 0<=r+dr<self.size and 0<=c+dc<self.size]
    
    def gen_percepts(self):
        for r,c in self.nbrs(*self.wumpus):
            self.percepts[r][c].append("Stench")
        
        for pr,pc in self.pits:
            for r,c in self.nbrs(pr,pc):
                self.percepts[r][c].append("Breeze")
        gr,gc=self.gold
        self.percepts[gr][gc].append("Glitter")
    
    def sense(self):
        r,c=self.agent
        p=list(self.percepts[r][c])
        if not self.w_alive:
            p.append("Scream")
        return p
    
    def move(self,d):
        if not self.alive:
           return print("DEAD")
        dr,dc={"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}.get(d,(0,0))
        nr,nc=dr+self.agent[0],dc+self.agent[1]
        if 0<=nr<self.size and 0<=nc<self.size:
            self.agent=[nr,nc]
            self.check()
        else:
            print("BUMP")
    
    def check(self):
        r,c=self.agent
        if (r,c) in self.pits:
            self.alive=False
            print("FELL INTO PIT")
        elif (r,c)==self.wumpus:
            self.alive=False
            print("WUMPUS ATE YOU")
        elif (r,c)==self.gold and not self.gold_got:
            print("GOLD HERE. PRESS G")
        else:
            print("Safe")
    
    def grab(self):
        if tuple(self.agent)==self.gold:
            self.gold_got=True
            print("Got gold, return to [0,0]")
        else:
            print("No gold")
    
    def shoot(self,d):
        if not self.arrow:
            return print("No arrows")
        self.arrow=False
        dr,dc={"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}.get(d,(0,0))

        r,c=self.agent
        while(0<=r<=self.size and 0<=c<=self.size):
            if(r,c)==self.wumpus :
                self.w_alive=False
                print("Scream, wumpus dead")
            r+=dr
            c+=dc
        print("MISSED")
    
    def show(self):
        print("\nGRID")
        for i in range(self.size):
            row=[]
            for j in range(self.size):
                if [i,j]==self.agent:
                    cell="A"
                elif (i,j)==self.wumpus:
                    cell="W"
                elif (i,j) in self.pits:
                    cell="P"
                elif (i,j)==self.gold and not self.gold_got:
                    cell="G"
                else:
                    cell="."
                
                row.append(cell)
            print(" ".join(row))
        print()
    
    def status(self):
        if self.alive and self.gold_got and self.agent==[0,0]:
            print("ESCAPED with gold")
            return False
        if not self.alive:
            print("GAME OVER")
            return False
        return True

if __name__=="__main__":
    g=WumpusWord()
    print("Commangs: U/D/L/R move|SU/SD/SL/SR shoot | G grab| Q quit")
    run=True
    while run:
        g.show()
        print(f"At {g.agent},Percepts: {g.sense()}")
        cmd=input(">>").upper()
        if cmd in "UDLR":
            g.move(cmd)
        elif cmd.startswith("S"):
            g.shoot(cmd[1:])
        elif cmd=="G":
            g.grab()
        elif cmd=="Q":
            break
        else:
            print("Invalid")
        run=g.status()

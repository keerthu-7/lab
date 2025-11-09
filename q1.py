def water_jug_problem(capacity1,capacity2,target):
    visited = set()
    steps=[]

    def is_goal(state):
        return target==state
    
    def get_next_states(x,y):
        return [
            (capacity1,y),
            (x,capacity2),
            (x,0),
            (0,y),
            (min(x+y,capacity1),y-(min(x+y,capacity1)-x)),
            (x-(min(x+y,capacity2)-y),min(x+y,capacity2))
            ]
    
    def dfs(x,y):
        if(x,y) in visited:
            return False
        visited.add((x,y))
        steps.append((x,y))

        if is_goal((x,y)):
             return True
        
        for state in get_next_states(x,y):
             if dfs(*state):
                  return True
        
        steps.pop()
        return False
    
    if dfs(0,0):
        print("Steps to reach the target: ")
        for s in steps:
            print(f"Jug1: {s[0]}L , Jug2: {s[1]}L")
    else:
        print("No possible solution")


print("WATER JUG PROBLEM")
capacity1=int(input("Enter capacity of jug1"))
capacity2=int(input("Enter capacity of jug1"))
target_input=input("Enter target in tuple(x,y)")

x,y=map(int,target_input.split(","))
target=(x,y)
water_jug_problem(capacity1,capacity2,target)
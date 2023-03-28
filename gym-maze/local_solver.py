import sys
import numpy as np
import math
import random
import json
import requests
from itertools import permutations
import time
import gym
import gym_maze
from gym_maze.envs.maze_manager import MazeManager
from riddle_solvers import *


cnt=0
detected_walls=0
saved_children=0

flood_fill_grid={
    "1":[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    "2":[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    "3":[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    "4":[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ],
    "exit":[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ]
}

def to_string123(x,y,dir):
    return str(x)+' '+str(y)+' '+dir



def avreage(cur_x=4,cur_y=4,vx=0,vy=-1,des=4):
    sum_x=0
    sum_y=0
    ans=[]
    cnt=0
    if vx==0:
        return cur_x,cur_y+des,1
    elif vy==0:
        return des+cur_x,cur_y,1
    else:
        c=1
        while c<des:
            x=cur_x+(c*vx)
            y=cur_y+((des-c)*vy)
            c+=1
            if(x>=0 and x<10 and y>=0 and y<10):
                ans.append((x,y))
    #Can chack if the len is one
    if len(ans)==1:
        return ans[0][0],ans[0][1],1
    
    m=len(ans)//2
    return ans[m][0],ans[m][1],0

walls=dict()

def flood_fill(x,y,index):
    # print("***********************************************")
    # print(x,y,index)
    global flood_fill_grid,walls
    visited=[
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ]
    flood_fill_grid[index][y][x]=0
    q=[]
    q.append((x,y))
    visited[y][x] =1
    while q:
        x=q[0][0]
        y=q[0][1]
        if (walls.get(to_string123(x,y,'N')) is None and y-1>=0 and visited[y-1][x]==0):
            flood_fill_grid[index][y-1][x] = flood_fill_grid[index][y][x] + 1
            q.append((x,y-1))
            visited[y-1][x] =1
        # else:
        #     #print("invalid or wall",x,y,'N')
        if (walls.get(to_string123(x,y,'S')) is None and y+1<10 and visited[y+1][x]==0):
            flood_fill_grid[index][y+1][x] = flood_fill_grid[index][y][x] + 1
            q.append((x,y+1))
            visited[y+1][x] =1
        # else:
        #     #print("invalid or wall",x,y,'S')
        if (walls.get(to_string123(x,y,'W')) is None and x-1>=0 and visited[y][x-1]==0):
            flood_fill_grid[index][y][x-1] = flood_fill_grid[index][y][x] + 1
            q.append((x-1,y))
            visited[y][x-1] =1
        # else:
        #     #print("invalid or wall",x,y,'W')
        if (walls.get(to_string123(x,y,'E')) is None and x+1<10 and visited[y][x+1]==0):
            flood_fill_grid[index][y][x+1] = flood_fill_grid[index][y][x] + 1
            q.append((x+1,y))
            visited[y][x+1] = 1
        # else:
        #     #print("invalid or wall",x,y,'E')
        q.pop(0)

children_state={
    "1":{
        "pos_sure":0,
        "arrived":0,
        "pos":[0,0],
    },
    "2":{
        "pos_sure":0,
        "arrived":0,
        "pos":[0,0],
    },
    "3":{
        "pos_sure":0,
        "arrived":0,
        "pos":[0,0],
    },
    "4":{
        "pos_sure":0,
        "arrived":0,
        "pos":[0,0],
    }
}

prev_pos=[-1,-1]
prev_action='A'
visited_cells=dict()
best_child=1
best_score=float('INF')


def select_action(state):
    time.sleep(0.05)
    print("Our state",state)
    #x=input()
    # Positions of not arrived childerns
    valid_set=[]
    global flood_fill_grid,visited_cells,detected_walls,best_child,best_score,saved_children
    global prev_action,prev_pos,children_state,walls,cnt
    cnt=cnt+1
    
    my_pos=state[0]
    #visited_cells[str(my_pos[0])+' '+str(my_pos[1])]=1
    distance=state[1]
    #print(distance)
    directions=state[2]
    
    # Check if i arrived to this children, and I didn't change it's state until yet
    if len(distance)>=1 and  children_state["1"]["arrived"]==0 and distance[0]<=0:
        saved_children=saved_children+1
        children_state["1"]["arrived"]=1
        children_state["1"]["pos_sure"]=1
        best_child=1
        best_score=float('INF')
    if len(distance)>=2 and  children_state["2"]["arrived"]==0 and distance[1]<=0:
        saved_children=saved_children+1
        children_state["2"]["arrived"]=1
        children_state["2"]["pos_sure"]=1
        best_child=1
        best_score=float('INF')
    if len(distance)>=3 and children_state["3"]["arrived"]==0 and distance[2]<=0:
        saved_children=saved_children+1
        children_state["3"]["arrived"]=1
        children_state["3"]["pos_sure"]=1
        best_child=1
        best_score=float('INF')
    if len(distance)>=4 and children_state["4"]["arrived"]==0 and distance[3]<=0:
        saved_children=saved_children+1
        children_state["4"]["arrived"]=1
        children_state["4"]["pos_sure"]=1
        best_child=1
        best_score=float('INF')

    
    # If i don't arrive to it in the past add it to the valid_set to go to it
    if len(distance)>=1 and distance[0]>0:
        valid_set.append("1")
    if len(distance)>=2 and distance[1]>0:
        valid_set.append("2")
    if len(distance)>=3 and distance[2]>0:
        valid_set.append("3")
    if len(distance)>=4 and distance[3]>0:
        valid_set.append("4")
    
    
    
    # if i not sure about its postion ->  edit its pos 
    if len(distance)>=1 and children_state["1"]["pos_sure"]==0:
        if distance[0]<=0:
            children_state["1"]["arrived"]=1
            children_state["1"]["pos_sure"]=1
            best_child=1
            best_score=float('INF')
        else:
            # Save the curr pos to past pos
            prev_child_pos=[]
            prev_child_pos.append(children_state["1"]["pos"][0])
            prev_child_pos.append(children_state["1"]["pos"][1])
            # Estimate a new one
            estimated_pos=avreage(my_pos[0],my_pos[1],directions[0][0],directions[0][1],distance[0])
            children_state["1"]["pos"][0]=estimated_pos[0]
            children_state["1"]["pos"][1]=estimated_pos[1]
            # if it sure save it to childern state
            if estimated_pos[2]==1:
                children_state["1"]["pos_sure"]=1
                best_child=1
                best_score=float('INF')
            # if it's don't like the past pos -> update its grid
            if prev_child_pos[0]!=estimated_pos[0] or prev_child_pos[1]!=estimated_pos[1]:
                flood_fill(children_state["1"]["pos"][0],children_state["1"]["pos"][1],"1")
                
                
    if len(distance)>=2 and  children_state["2"]["arrived"]==0 and children_state["2"]["pos_sure"]==0:
        if distance[1]<=0:
            children_state["2"]["arrived"]=1
            children_state["2"]["pos_sure"]=1
            best_child=1
            best_score=float('INF')
        else:
            prev_child_pos=[]
            prev_child_pos.append(children_state["2"]["pos"][0])
            prev_child_pos.append(children_state["2"]["pos"][1])
            estimated_pos=avreage(my_pos[0],my_pos[1],directions[1][0],directions[1][1],distance[1])
            children_state["2"]["pos"][0]=estimated_pos[0]
            children_state["2"]["pos"][1]=estimated_pos[1]
            if estimated_pos[2]==1:
                children_state["2"]["pos_sure"]=1
                best_child=1
                best_score=float('INF')
            if prev_child_pos[0]!=estimated_pos[0] or prev_child_pos[1]!=estimated_pos[1]:
                flood_fill(children_state["2"]["pos"][0],children_state["2"]["pos"][1],"2")
                
                
    if len(distance)>=3 and children_state["3"]["arrived"]==0 and children_state["3"]["pos_sure"]==0:
        if distance[2]<=0:
            children_state["3"]["arrived"]=1
            children_state["3"]["pos_sure"]=1
            best_child=1
            best_score=float('INF')
        else:
            prev_child_pos=[]
            prev_child_pos.append(children_state["3"]["pos"][0])
            prev_child_pos.append(children_state["3"]["pos"][1])
            estimated_pos=avreage(my_pos[0],my_pos[1],directions[2][0],directions[2][1],distance[2])
            children_state["3"]["pos"][0]=estimated_pos[0]
            children_state["3"]["pos"][1]=estimated_pos[1]
            if estimated_pos[2]==1:
                children_state["3"]["pos_sure"]=1
                best_child=1
                best_score=float('INF')
            if prev_child_pos[0]!=estimated_pos[0] or prev_child_pos[1]!=estimated_pos[1]:
                flood_fill(children_state["3"]["pos"][0],children_state["3"]["pos"][1],"3")
                
                
    if len(distance)>=4 and children_state["4"]["arrived"]==0 and children_state["4"]["pos_sure"]==0:
        if distance[3]<=0:
            children_state["4"]["arrived"]=1
            children_state["4"]["pos_sure"]=1
            best_child=1
            best_score=float('INF')
        else:
            prev_child_pos=[]
            prev_child_pos.append(children_state["4"]["pos"][0])
            prev_child_pos.append(children_state["4"]["pos"][1])
            estimated_pos=avreage(my_pos[0],my_pos[1],directions[3][0],directions[3][1],distance[3])
            children_state["4"]["pos"][0]=estimated_pos[0]
            children_state["4"]["pos"][1]=estimated_pos[1]
            if estimated_pos[2]==1:
                children_state["4"]["pos_sure"]=1
                best_child=1
                best_score=float('INF')
            if prev_child_pos[0]!=estimated_pos[0] or prev_child_pos[1]!=estimated_pos[1]:
                flood_fill(children_state["4"]["pos"][0],children_state["4"]["pos"][1],"4")
                
    # update all flood fill grids when we met a wall
    if my_pos[0]==prev_pos[0] and my_pos[1]==prev_pos[1]:
        #Recalculate global score please!!!!
        print("Detect wall")
        best_child=1
        best_score=float('INF')
        detected_walls=detected_walls+1
        #print("# of detected_walls",detected_walls)
        visited_cells.clear()
        walls[to_string123(my_pos[0],my_pos[1],prev_action)]=1
        #print("it's a wall",to_string123(my_pos[0],my_pos[1],prev_action))
        if prev_action=='N':
            walls[to_string123(my_pos[0],my_pos[1]-1,'S')]=1
            #print("it's also  a wall",to_string123(my_pos[0],my_pos[1]-1,'S'))
        if prev_action=='S':
            walls[to_string123(my_pos[0],my_pos[1]+1,'N')]=1
            #print("it's also  a wall",to_string123(my_pos[0],my_pos[1]+1,'N'))
        if prev_action=='E':
            walls[to_string123(my_pos[0]+1,my_pos[1],'W')]=1
            #print("it's also  a wall",to_string123(my_pos[0]+1,my_pos[1],'W'))
        if prev_action=='W':
            walls[to_string123(my_pos[0]-1,my_pos[1],'E')]=1
            #print("it's also  a wall",to_string123(my_pos[0]-1,my_pos[1],'E'))

        flood_fill(children_state["1"]["pos"][0],children_state["1"]["pos"][1],"1")
        flood_fill(children_state["2"]["pos"][0],children_state["2"]["pos"][1],"2")
        flood_fill(children_state["3"]["pos"][0],children_state["3"]["pos"][1],"3")
        flood_fill(children_state["4"]["pos"][0],children_state["4"]["pos"][1],"4")
        flood_fill(9,9,"exit")


    l = list(permutations(valid_set))
    # in the case of draw take the closest one
    local_child=1
    local_score=float('INF')
    
    if len(valid_set)==4:
        for i in l:
            path=flood_fill_grid[i[0]][my_pos[1]][my_pos[0]]+flood_fill_grid[i[1]] [children_state[i[0]]["pos"][1]][children_state[i[0]]["pos"][0]]+flood_fill_grid[i[2]] [children_state[i[1]]["pos"][1]][children_state[i[1]]["pos"][0]]+flood_fill_grid[i[3]] [children_state[i[2]]["pos"][1]][children_state[i[2]]["pos"][0]]+flood_fill_grid[i[3]] [9][9]
            # print("1",flood_fill_grid[i[3]] [9][9])
            # print("2",flood_fill_grid["exit"][children_state[i[3]]["pos"][1]][children_state[i[3]]["pos"][0]])
            
            if local_score>path:
                local_score=path
                local_child=i[0]
    elif len(valid_set)==3:
        for i in l:
            path=flood_fill_grid[i[0]][my_pos[1]][my_pos[0]]+flood_fill_grid[i[1]] [children_state[i[0]]["pos"][1]][children_state[i[0]]["pos"][0]]+flood_fill_grid[i[2]] [children_state[i[1]]["pos"][1]][children_state[i[1]]["pos"][0]]+flood_fill_grid[i[2]] [9][9]
            if local_score>path:
                local_score=path
                local_child=i[0]
    elif len(valid_set)==2:
        for i in l:
            path=flood_fill_grid[i[0]][my_pos[1]][my_pos[0]]+flood_fill_grid[i[1]] [children_state[i[0]]["pos"][1]][children_state[i[0]]["pos"][0]]+flood_fill_grid[i[1]] [9][9]
            if local_score>path:
                local_score=path
                local_child=i[0]
    elif len(valid_set)==1:
        for i in l:
            path=flood_fill_grid[i[0]][my_pos[1]][my_pos[0]]+flood_fill_grid[i[0]] [9][9]
            if local_score>path:
                local_score=path
                local_child=i[0]
    else:
        best_child="exit"
    
    
    if best_child!="exit" and local_score<best_score:
        best_score=local_score
        best_child=local_child
    
    

        
    next_move="A"
    min_cost=float('INF')
    print("best child ",best_child,best_score)
    print("my value",flood_fill_grid[best_child][my_pos[1]][my_pos[0]])
    if my_pos[0]-1>=0:
        print("W value",flood_fill_grid[best_child][my_pos[1]][my_pos[0]-1])
    if my_pos[0]+1<=9:
        print("E value",flood_fill_grid[best_child][my_pos[1]][my_pos[0]+1])
    if my_pos[1]-1>=0:
        print("N value",flood_fill_grid[best_child][my_pos[1]-1][my_pos[0]])
    if my_pos[1]+1<=9:
        print("S value",flood_fill_grid[best_child][my_pos[1]+1][my_pos[0]])
    
    maybe_move=[]
    
    if my_pos[0]-1>=0 and flood_fill_grid[best_child][my_pos[1]][my_pos[0]]==flood_fill_grid[best_child][my_pos[1]][my_pos[0]-1]+1 and walls.get(to_string123(my_pos[0],my_pos[1],'W')) is None:
        maybe_move.append([my_pos[0]-1,my_pos[1]])
        next_move='W'
    if my_pos[0]+1<=9 and flood_fill_grid[best_child][my_pos[1]][my_pos[0]]==flood_fill_grid[best_child][my_pos[1]][my_pos[0]+1]+1 and walls.get(to_string123(my_pos[0],my_pos[1],'E')) is None:
        maybe_move.append([my_pos[0]+1,my_pos[1]])
        next_move='E'
    if my_pos[1]-1>=0 and flood_fill_grid[best_child][my_pos[1]][my_pos[0]]==flood_fill_grid[best_child][my_pos[1]-1][my_pos[0]]+1 and walls.get(to_string123(my_pos[0],my_pos[1],'N')) is None:
        maybe_move.append([my_pos[0],my_pos[1]-1])
        next_move='N'
    if my_pos[1]+1<=9 and flood_fill_grid[best_child][my_pos[1]][my_pos[0]]==flood_fill_grid[best_child][my_pos[1]+1][my_pos[0]]+1 and walls.get(to_string123(my_pos[0],my_pos[1],'S')) is None:
        maybe_move.append([my_pos[0],my_pos[1]+1])
        next_move='S'
    
    if len(maybe_move)>1:
        #Explore
        manhatan_distance=-1
        #Exploite
        #manhatan_distance=float('INF')
        for i in maybe_move:
            if best_child == "exit" and (abs(i[0]-9)+abs(i[1]-9))>manhatan_distance:
                manhatan_distance=(abs(i[0]-9)+abs(i[1]-9))
                if i[0]<my_pos[0]:
                    next_move='W'
                elif i[0]>my_pos[0]:
                    next_move='E'
                elif i[1]<my_pos[1]:
                    next_move='N'
                elif i[1]>my_pos[1]:
                    next_move='S'
            elif best_child != "exit" and (abs(i[0]-children_state[best_child]["pos"][0])+abs(i[1]-children_state[best_child]["pos"][1]))>manhatan_distance:
                manhatan_distance=(abs(i[0]-children_state[best_child]["pos"][0])+abs(i[1]-children_state[best_child]["pos"][1]))
                if i[0]<my_pos[0]:
                    next_move='W'
                elif i[0]>my_pos[0]:
                    next_move='E'
                elif i[1]<my_pos[1]:
                    next_move='N'
                elif i[1]>my_pos[1]:
                    next_move='S'

    
    print("YAAAAAAAAAAAAAAAARBBB")
    print("next move",next_move)
    # actions = ['N', 'S', 'E', 'W']
    # random_action = random.choice(actions)
    # action_index = actions.index(next_move)
    prev_pos[0]=my_pos[0]
    prev_pos[1]=my_pos[1]
    prev_action=next_move
    return next_move


def local_inference(riddle_solvers):
    global saved_children
    obv = manager.reset(agent_id)

    for t in range(MAX_T):
        # Select an action
        state_0 = obv
        action = select_action(state_0) # Random action
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)

        if not info['riddle_type'] == None:
            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)

        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        print("OBV[0]",obv)
        print("Saved children here",saved_children)
        if saved_children==4 and np.array_equal(obv[0], (9,9)):
            manager.set_done(agent_id)
            break # Stop Agent

        if RENDER_MAZE:
            manager.render(agent_id)

        states[t] = [obv[0].tolist(), str(manager.get_rescue_items_status(agent_id))]       
        


if __name__ == "__main__":
    sample_maze = np.load("hackathon_sample.npy")
    agent_id = "9" # add your agent id here
    
    manager = MazeManager()
    manager.init_maze(agent_id, maze_cells=sample_maze)
    env = manager.maze_map[agent_id]

    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    maze = {}
    states = {}

    
    maze['maze'] = env.maze_view.maze.maze_cells.tolist()
    maze['rescue_items'] = list(manager.rescue_items_dict.keys())

    MAX_T = 5000
    RENDER_MAZE = True
    

    local_inference(riddle_solvers)
    print("steps",cnt)
    with open("./states.json", "w") as file:
        json.dump(states, file)

    
    with open("./maze.json", "w") as file:
        json.dump(maze, file)
    
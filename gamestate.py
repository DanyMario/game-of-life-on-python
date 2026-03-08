from life import *
import time

class GameState:
    def __init__(self,gridsize:tuple,grid_alive:set):
        self.grid=[]
        self.grid_alive=grid_alive
        self.gen=0
        self.grid_info = {}
        self.to_be={}
        for x in range(gridsize[0]):
            grid_inside=[]
            for y in range(gridsize[1]):
                if (x,y) in grid_alive:
                    grid_inside.append(Life((x,y),True))
                else:
                    grid_inside.append(Life((x,y),False))
            self.grid.append(grid_inside)


    def update_grid(self):
        self.grid_info.clear()
        self.to_be.clear()
        for i in self.grid_alive:
            for x in range(i[0]-1,i[0]+2):
                for y in range(i[1]-1,i[1]+2):
                    if (x,y) == i:
                        continue
                    if 0<=x<len(self.grid) and 0<=y<len(self.grid[0]):
                        if not (x,y) in self.grid_alive:
                            self.grid_info[(x,y)] = self.grid_info.get((x,y),0) + 1
                        else:
                            self.grid[i[0]][i[1]].neighbors+=1
            if self.grid[i[0]][i[1]].neighbors>=4 or self.grid[i[0]][i[1]].neighbors<=1:
                self.to_be[(i[0],i[1])] = False
            else:
                self.to_be[(i[0], i[1])] = True
        for coor,neigh in self.grid_info.items():
            if neigh >=3:
                self.to_be[coor] = True
            else:
                self.to_be[coor] = False

    def next_gen(self):
        for coor,alive in self.to_be.items():
            if alive:
                self.grid_alive.add(coor)
                self.grid[coor[0]][coor[1]].set_alive()
            if not alive:
                self.grid_alive.discard(coor)
                self.grid[coor[0]][coor[1]].death()

        self.gen+=1


    def __repr__(self):
        line = ""
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y].alive:
                    line+="X"
                else:
                    line+="O"
            line+="\n"
        return line+f"Generation: {self.gen}"







state = GameState((3,3), {(0,0),(1,0),(0,1),(2,2)})
print(state)
state.update_grid()
state.next_gen()
time.sleep(.5)
print(state)
state.update_grid()
state.next_gen()
time.sleep(.5)
print(state)


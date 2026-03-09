from life import *
import time

class GridState:
    def __init__(self,gridsize:tuple):
        self.grid=[]
        self.grid_alive=set()
        self.gen=0
        self.grid_info = {}
        self.to_be={}
        for x in range(gridsize[0]):
            grid_inside=[]
            for y in range(gridsize[1]):
                grid_inside.append(Life((x,y),False))
            self.grid.append(grid_inside)

    def set_alive(self,coord:tuple,was_alr=False):
        self.grid_alive.add(coord)
        self.grid[coord[0]][coord[1]].set_alive()
        if was_alr:
            print(f"Cell in {coord} has become alive!")

    def set_dead(self,coord:tuple,was_alr=False):
        self.grid_alive.discard(coord)
        self.grid[coord[0]][coord[1]].death()
        if was_alr:
            print(f"Cell in {coord} has died!")

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
            if neigh ==3:
                self.to_be[coor] = True
            else:
                self.to_be[coor] = False

    def next_gen(self):
        for coor,alive in self.to_be.items():
            if alive and coor in self.grid_alive:
                self.set_alive(coor,True)
            elif alive and not coor in self.grid_alive:
                self.set_alive(coor)
            if not alive and not coor in self.grid_alive:
                self.set_dead(coor)
            elif not alive and coor in self.grid_alive:
                self.set_dead(coor,True)
        self.gen+=1

    def reset(self):
        x=self.grid_alive.copy
        self.grid_alive.clear()
        self.grid_info.clear()
        self.to_be.clear()
        self.gen = 0
        return x


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







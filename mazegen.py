import random

def makeMaze(grid, sx, sy):
    width = len(grid)
    height = len(grid[0])

    dx = [ 1, 0, -1 , 0 ]
    dy = [ 0, -1, 0, 1 ]
    
    d = random.choice([0,1,2,3])
    for t in range(0,4):
        tx = sx + dx[(d+t)%4]*2
        ty = sy + dy[(d+t)%4]*2
        if(tx > 0 and ty > 0 and tx < width and ty < width):
            if(grid[tx][ty] == 1):
                td = (d+t)%4
                grid[sx+dx[td]][sy+dy[td]] = 0
                grid[tx][ty] = 0
                makeMaze(grid,tx,ty)
    return
    

    
    
    

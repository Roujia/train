#coding:UTF-8
from __future__ import print_function
from Sstack_recuesion import *
from SQueue import *
#迷宫问题，将迷宫平面映射为二维0/1矩阵，空位置用0表示，障碍和边界用1表示
dirs=[(0,1),(1,0),(0,-1),(-1,0)]#东南西北方向
def mark(maze,pos):#给迷宫maze的位置pos标2表示“到过了”
    maze[pos[0]][pos[1]]=2
def passable(maze,pos):#检查迷宫maze的位置pos是否可通过
    return maze[pos[0]][pos[1]]==0

#1、基于递归的迷宫求解法（利用pytho解释器中内部的运行站保存中间信息）
def find_path(maze,pos,end):#pos表示搜索的当前位置
    mark(maze,pos)
    if pos==end:#已到达出口
        print (pos,end=" ")#输出这个位置
        return True#成功结束
    for i in range(4):#否则按四个方向顺序探查
        nextp=(pos[0]+dirs[i][0],pos[1]+dirs[i][1])
        #考虑下一个可能方向
        if passable(maze,nextp):#不可行的相邻位置不管
            if find_path(maze,nextp,end):#从nextp可达出口
                print(pos,end=" ")#输出这个点
                return True#成功结束
    return False

# if __name__=="__main__":
#     a=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,1,0,0,0,1,0,0,0,1],[1,0,1,0,0,0,0,1,0,1,0,1,0,1],
#        [1,0,1,0,1,1,1,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,0,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,0,0,0,1],
#        [1,0,1,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,1,1,1,0,1,0,1,1,0,1],[1,0,1,0,1,0,1,0,1,0,1,0,0,1],
#        [1,0,1,0,1,0,1,0,1,1,1,1,0,1],[1,0,1,0,0,0,1,0,0,1,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#     find_path(a,(1,1),(10,12))


#2、栈和回溯法
def maze_solver(maze,start,end):
    if start==end:
        print(start)
        return
    st=SStack()
    mark(maze,start)
    st.push((start,0))#入口和方向0的序对入栈,即初始的pos和nxt
    while not st.is_empty():#走不通时回退
        pos,nxt=st.pop()#取栈顶及其探查方向
        for i in range(nxt,4):#依次检查未探查的方向
            nextp=(pos[0]+dirs[i][0],pos[1]+dirs[i][1])#算出下一位置
            if nextp==end:#到达出口，打印路径
                st.push((end,0))
                st.push((pos,0))
                while not st.is_empty():
                    print(st.pop()[0],end=' ')
                return
            if passable(maze,nextp):#遇到未探查的新位置
                st.push((pos,i+1))#原位置和下一方向入栈
                mark(maze,nextp)
                st.push((nextp,0))#新位置入栈
                break#退出内层循环，下次迭代将以新栈顶为当前位置继续

    print("No path found.")#找不到路径

# if __name__=="__main__":
#     a=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,1,0,0,0,1,0,0,0,1],[1,0,1,0,0,0,0,1,0,1,0,1,0,1],
#        [1,0,1,0,1,1,1,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,0,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,0,0,0,1],
#        [1,0,1,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,1,1,1,0,1,0,1,1,0,1],[1,0,1,0,1,0,1,0,1,0,1,0,0,1],
#        [1,0,1,0,1,0,1,0,1,1,1,1,0,1],[1,0,1,0,0,0,1,0,0,1,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#     maze_solver(a,(1,1),(10,12))

#3、基于队列的逐步扩张
def maze_solver_queue(maze,start,end):
    if start==end:
        print("Path finds.")
        return
    qu=SQueue()
    precedent=dict()
    mark(maze,start)
    qu.enqueue(start)#start位置入队
    while not qu.is_empty():#还有候选位置
        pos=qu.dequeue()#取出下一个位置
        for i in range(4):#检查每个方向
            nextp=(pos[0]+dirs[i][0],pos[1]+dirs[i][1])#列举各位置
            if passable(maze,nextp):#找到新的探索方向
                if nextp==end:#是出口
                    print("Path find.")
                    global path
                    path=[]
                    path.append(end)
                    while pos != start:
                        path.append(pos)#将字典中存放的历史位置加入到列表中
                        pos = precedent[pos]#取出字典中的值
                    path.append(start)
                    path.reverse()
                    for x in path:
                        print(x, end=' ')
                    return
                mark(maze,nextp)
                precedent[nextp] = pos  # 利用字典反向回溯找到路径
                qu.enqueue(nextp)#新位置入队

    print("No path.")#没有路径，失败！

if __name__=="__main__":
    a=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,1,1,0,0,0,1,0,0,0,1],[1,0,1,0,0,0,0,1,0,1,0,1,0,1],
       [1,0,1,0,1,1,1,1,0,1,0,1,0,1],[1,0,1,0,0,0,0,0,0,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,0,0,0,1],
       [1,0,1,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,1,1,1,0,1,0,1,1,0,1],[1,0,1,0,1,0,1,0,1,0,1,0,0,1],
       [1,0,1,0,1,0,1,0,1,1,1,1,0,1],[1,0,1,0,0,0,1,0,0,1,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    maze_solver_queue(a,(1,1),(10,12))

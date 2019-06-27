#coding:UTF-8
from __future__ import print_function
#1、二叉树的list实现
#非空二叉树用[d,l,r]表示：d表示存在根节点的元素，l表示左子树，r表示右子树
def BinTree(data,left=None,right=None):
    return [data,left,right]

def is_empty_BinTree(btree):
    return btree is None

def root(btree):
    return btree[0]

def left(btree):
    return btree[1]

def right(btree):
    return btree[2]

def set_root(btree,data):
    btree[0]=data

def set_left(btree,left):
    btree[1]=left

def set_right(btree,right):
    btree[2]=right

# if __name__=="__main__":
#     t1=BinTree(2,BinTree(4),BinTree(8))
#     set_left(left(t1),BinTree(5))
#     print t1
#

#2、二叉树的类实现
#定义二叉树节点类(链接实现)
class BinTNodeError(ValueError):
    pass
class BinTNode:
    def __init__(self,dat,left=None,right=None):
        self.data=dat
        self.left=left
        self.right=right

    #统计树中结点个数
def count_BinTNodes(btree):
    if btree is None:
        return 0
    else:
        return 1+count_BinTNodes(btree.left)+count_BinTNodes(btree.right)

#假设结点中保存数值，求这种二叉树里所有数值和
def sum_BinTNodes(btree):
    if btree is None:
        return 0
    else:
        return btree.data+sum_BinTNodes(btree.left)+sum_BinTNodes(btree.right)

#深度优先遍历：
#以先根序遍历为例(递归)
def preorder(btree,proc):#proc是具体的结点数据操作
    if btree is None:
        return
    proc(btree.data)
    preorder(btree.left,proc)
    preorder(btree.right,proc)
#非递归实现形式
from Sstack import *
def preorder_nonrec(btree,proc):
    s=SStack()
    while btree is not None or not s.is_empty():
        while btree is not None:#_沿左分支下行
            proc(btree.data)#先根序先处理根数据
            s.push(btree.right)#右分支入栈
            btree=btree.left
        btree=s.pop()#遇到空树回溯
# 非递归的后根序遍历算法实现
def postorder_nonrec(btree,proc):
    s=SStack()
    while btree is not None or not s.is_empty():
        while btree is not None:#下行循环直至栈顶的两子树空
            s.push(btree)
            btree=btree.left if btree.left is not None else btree.right
            #能左就左，否则向右一步
        btree=s.pop()#栈顶是应访问结点
        proc(btree.data)
        if not s.is_empty() and s.top().left==btree:
            #栈不空且当前结点是栈顶的左子结点
            btree=s.top().right
        else:
            btree=None#没有右子树或者右子树遍历完毕，强迫退栈


#宽度优先遍历
#以先根序遍历为例
from SQueue import *
def levelorder(btree,proc):
    qu=SQueue()
    qu.enqueue(btree)
    while not qu.is_empty():
        btree=qu.dequeue()
        if btree is None:#弹出的树为空则直接跳过
            continue
        qu.enqueue(btree.left)
        qu.enqueue(btree.right)
        proc(btree.data)

t=BinTNode(1,BinTNode(2,BinTNode(4),BinTNode(5)),BinTNode(3))
preorder_nonrec(t,lambda x:print(x,end=""))
preorder(t,lambda x:print(x,end="   "))
levelorder(t,lambda x:print(x,end=""))
postorder_nonrec(t,lambda x:print(x,end=""))
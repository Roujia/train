#coding:UTF-8
#Josephus问题
from __future__ import print_function
from Llist import LCList
#1、基于list和“数组”概念
#把list看作元素个数固定的对象，只修改元素的值，不改变表的结构
def josephus_A(n,k,m):
    people=list(range(1,n+1))#建立一个包含n人的列表，表元素为0表示没有人

    i=k-1
    for num in range(n):
        count=0
        while count<m:
            if people[i]>0:
                count+=1
            if count==m:
                print (people[i],end="")
                people[i]=0#数到第m个人，将元素置
            i=(i+1)%n#取模n保持i的取值范围正确
        if num<n-1:
            print(",",end="")
        else:
            print("")
    return


#2、基于顺序表
#将人员编号按list列表处理，谁退出就删除谁的编号
def josephus_L(n,k,m):
    people=list(range(1,n+1))

    num,i=n,k-1#num表示表的长度，每退出一人，减1
    for num in range(n,0,-1):
        i=(i+m-1)%num
        print(people.pop(i),
              end="," if num>1 else "\n")
    return
# if __name__=='__main__':
#     josephus_L(10,2,7)

#3、基于循环单链表
class Josephus(LCList):
    def turn(self,m):#将循环表对象的rear指针沿next方向移m步，即结点环旋转
        for i in range(m):
            self._rear=self._rear.next

    def __init__(self,n,k,m):
        LCList.__init__(self)#先调用基类LCList的初始化函数建立一个空表
        for i in range(n):#通过循环建立包含n个结点和相应数据的初始循环表
            self.append(i+1)
        self.turn(k-1)#指针找到第K个人
        while not self.is_empty():
            self.turn(m-1)
            print(self.pop(),end="\n" if self.is_empty() else ",")

if __name__=='__main__':
    Josephus(10,2,7)
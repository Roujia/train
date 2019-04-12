#coding:UTF-8
#双链表类的实现
from random import randint
from Llist import LNode
from Llist import LList1
from Llist import LinkedListUnderflow
from Llist import LCList

#1、定义双链表的结点，采用派生方法
class DLNode(LNode):#双链表结点类
    def __init__(self,elem,prev=None,next_=None):
        LNode.__init__(self,elem,next_)
        self.prev=prev

#2、定义双链表类
class DLList(LList1):
    def __init__(self):
        LList1.__init__(self)

    def prepend(self,elem):
        p=DLNode(elem,None,self._head)
        if self._head is None:#空表
            self._rear=p
        else:#非空表，设置prev引用
            p.next.prev=p
        self._head=p

    def append(self,elem):
        p=DLNode(elem,self._rear,None)
        if self._head is None:#空表插入
            self._head=p
        else:#非空表，设置next引用
            p.prev.next = p
        self._rear=p

    def pop(self):
        if self._head is None:
            raise LinkedListUnderflow("in pop of DLList")
        e=self._head.elem
        self._head= self._head.next
        if self._head is not None:#因为是双链表，要删除prev指针，作为首元素
            self._head.prev=None
        return e

    def pop_last(self):
        if self._head is None:
            raise LinkedListUnderflow("in pop_last of DLList")
        e=self._rear.elem
        self._rear=self._rear.prev
        if self._rear is None:#设置_head保证is_empty正确工作
            self._head=None
        else:
            self._rear.next=None
        return e



#循环双链表的实现
class DCList(LCList):#循环双链表
    def __init__(self):
        LCList.__init__(self)

    def prepend(self,elem):
        p=DLNode(elem)
        if self._rear is None:
            p.next=p
            self._rear=p
        else:
            p.next=self._rear.next
            p.next.prev=p
            self._rear.next=p

    def pop(self):#前端弹出
        if self._rear is None:
            raise LinkedListUnderflow("in pop of DCList")
        p=self._rear.next
        if self._rear is p:#只有一个表元素
            self._rear=None
        else:
            self._rear.next=p.next
        return p.elem

    def pop_last(self):
        if self._rear is None:
            raise LinkedListUnderflow("in pop_last of DCList")
        p=self._rear
        if self._rear.next is p:
            self._rear=None
        else:
            self._rear=p.prev
        return p.elem


if __name__=='__main__':
    mlist1 = DCList()
    mlist1.prepend(99)
    # for i in range(11, 20):
    #     mlist1.append(randint(1, 20))
    mlist1.printall()
    print(mlist1.pop_last())


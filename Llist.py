#coding:UTF-8
#单链表类的实现
from __future__ import print_function
from random import randint
#1、定义结点类
class LNode:
    def __init__(self,elem,next_=None):#next_避免与python标准函数next重名
        self.elem=elem
        self.next=next_

#2、自定义异常
class LinkedListUnderflow(ValueError):
     pass

#3、LList类的定义、初始化函数和简单操作
class LList():
    def __init__(self):#表对象里只有一个引用链接结点的_head域
        self._head=None

    def is_empty(self):
        return self._head is None

    def prepend(self,elem):#在表头插入数据
        self._head=LNode(elem,self._head)

    def pop(self):#弹出
        if self._head is None:#无结点，引发异常
            raise LinkedListUnderflow("in pop")
        e=self._head.elem
        self._head=self._head.next
        return e

    def append(self,elem):#先遍历，再插入
        if self._head is None:#空表直接插入
            self._head=LNode(elem)
            return
        p=self._head
        while p.next is not None:
            p=p.next
        p.next=LNode(elem)

    def pop_lasd(self):#删除表中最后元素
        if self._head is None:#空表
            raise LinkedListUnderflow("in pop_last")
        p=self._head
        if p.next is None:#表中只有一个元素
            e=p.elem
            self._head=None
            return e
        while p.next.next is not None:#直到p.next是在最后结点
            p=p.next
        e=p.next.elem
        p.next=None
        return e
    #其他操作举例，找到满足给定条件的第一个表元素
    def find(self,pred):
        p=self._head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p=p.next

    def printall(self):
        p=self._head
        while p is not None:
            print(p.elem,end='')#end语法是python3版本，因此开头import future
            if p.next is not None:
                print(',',end='')
            p=p.next
        print('')

    def for_each(self,proc):#表的遍历,proc的实参是可以作用于表元素的操作函数，将被作用于每个表元素，比如print
        p=self._head
        while p is not None:
            proc(p.elem)
            p=p.next

    def elements(self):#定义生成器函数->迭代器
        p=self._head
        while p is not None:
            yield p.elem#yield就是return返回的一个值，并且记住这个返回的位置。下一次迭代就从这个位置开始。
            p=p.next

    def filter(self,pred):#筛选生成器（基于给定谓词返回所有满足条件的表元素）
        p=self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p=p.next

# mlist1=LList()
# for i in range(1,10):
#     mlist1.prepend(i)
# for i in range(11,20):
#     mlist1.append(i)
# mlist1.printall()
# mlist1.for_each(print)
# for x in mlist1.elements():
#     print(x,end=' ')
# for i in mlist1.filter(lambda i:i>10):#谓词参数，返回单链表中元素大于10的元素,在python中可以使用lambda表达式定制这个“判断谓词参数”
#     print(i,end=' ')

#单链表的简单变形：增加表为结点引用域
class LList1(LList):
    def __init__(self):
        LList.__init__(self)
        self._rear=None

    #重新定义前端插入操作
    def prepend(self,elem):
        if self._head is None:#是空表
            self._head = LNode(elem, self._head)
            self._rear=self._head
        else:
            self._head = LNode(elem, self._head)

    def append(self,elem):
        if self._head is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next=LNode(elem)
            self._rear=self._rear.next

    def pop_lasd(self):
        if self._head is None:#是空表
            raise LinkedListUnderflow("in pop_last")
        p=self._head
        if p.next is None:#表中只有一个元素
            e=p.elem
            self._head=None
            return e
        while p.next.next is not None:#直到p.next是最后结点
            p=p.next
        e=p.next.elem
        p.next=None
        self._rear=p
        return e

# mlist1=LList1()
# mlist1.prepend(99)
# for i in range (11,20):
#     mlist1.append(randint(1,20))
# for i in mlist1.elements():
#     print(i, end=' ')
#
# for x in mlist1.filter(lambda i:i%2==0):
#     print(x)

#循环单链表类
class LCList:
    def __init__(self):
        self._rear=None

    def is_empty(self):
        return self._rear is None

    def prepend(self,elem):#前端插入
        p=LNode(elem)
        if self._rear is None:
            p.next=p#建立一个结点的环
            self._rear=p
        else:
            p.next=self._rear.next
            self._rear.next=p#尾结点引用不变，即self._rear未变

    def append(self,elem):#尾端插入
        self.prepend(elem)
        self._rear=self._rear.next#更新尾结点引用

    def pop(self):#前端弹出
        if self._rear is None:
            raise LinkedListUnderflow("in pop of CLList")
        p=self._rear.next
        if self._rear is p:#表中只有一个元素
            self._rear=None
        else:
            self._rear.next=p.next
        return p.elem

    def printall(self):#输出表元素
        if self.is_empty():
            return
        p=self._rear.next
        while True:
            print(p.elem)
            if p is self._rear:
                break
            p=p.next


mlist1 = LCList()
mlist1.prepend(99)
for i in range(11, 20):
    mlist1.append(randint(1, 20))
mlist1.printall()
print(mlist1.pop())
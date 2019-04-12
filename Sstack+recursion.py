#coding:UTF-8
#栈：概念和实现
class StackUnderflow(ValueError):#栈下溢（空栈访问）
    pass
#1、基于顺序表定义栈类
class SStack():
    def __init__(self):#用list_elems存储栈中元素
        self._elems=[]#所有栈操作都映射到list操作

    def is_empty(self):
        return self._elems==[]

    def top(self):#取得栈里最后压入的元素，不删除
        if self._elems==[]:
            raise StackUnderflow("in SStack.top()")
        return self._elems[-1]

    def push(self,elem):#将元素elem压入栈
        self._elems.append(elem)

    def pop(self):
        if self._elems==[]:
            raise StackUnderflow("in SStack.pop()")
        return self._elems.pop()

# if __name__=="__main__":
#     st1=SStack()
#     st1.push(3)
#     st1.push(5)
#     print (st1.top())
#     while not st1.is_empty():
#         print(st1.pop())

#2、基于链接表定义栈类
class LNode():
    def __init__(self,elem,next_=None):
        self.elem=elem
        self.next=next_

class LStack():#用LNode作为结点
    def __init__(self):
        self._top=None

    def is_empty(self):
        return self._top is None

    def top(self):
        if self._top is None:
            raise StackUnderflow("in LStack.top()")
        return self._top.elem

    def push(self,elem):
        self._top=LNode(elem,self._top)

    def pop(self):
        if self._top is None:
            raise StackUnderflow("in LStack.pop()")
        p=self._top
        self._top=p.next
        return p.elem

# if __name__=="__main__":
#     st1=LStack()
#     st1.push(3)
#     st1.push(5)
#     print (st1.top())
#     while not st1.is_empty():
#         print(st1.pop())


#栈的应用
#1、颠倒一组元素的顺序
# st1=SStack()
# list1=[3,4,5,6]
# print list1
# for x in list1:
#     st1.push(x)
# list2=[]
# while not st1.is_empty():
#     list2.append(st1.pop())
# print list2

#2、括号匹配问题
#括号配对检查函数，text是被检查的正文串
def check_parens(text):
    # 首先，定义几个变量记录检查中有用的数据
    parens = "() [] {}"  # 所有括号字符
    open_parens = "( [ {"  # 开括号字符
    opposite = {")": "(", "]": "[", "}": "{"}  # 表示配对关系的字典

    #括号生成器，每次调用返回text里的下一括号及其位置->使用yield
    def parentheses(text):
        i,text_len=0,len(text)
        while True:#迭代生成器
            while i<text_len and text[i] not in parens:
                i+=1
            if i>=text_len:
                return
            yield text[i],i
            i+=1

    st=SStack()#保存括号的栈
    for pr,i in parentheses(text):#对text里各括号和位置迭代
        if pr in open_parens:#开括号，压进栈并继续
            st.push(pr)
        elif st.pop()!=opposite[pr]:#不匹配就是失败，退出
            print ("Unmatching is found at %s for '%s'"%(i,pr))
            return False#终止符,阻止向下执行
            #break
            #continue
        #else:这是一次括号配对成功，什么也不做，继续
        #也可以写作
        #else:
            #pass

    print("All parentheses are correctly matched.")
    return True

# if __name__=="__main__":
#     check_parens("abc(){}[}(]")

#3、栈与递归
#将递归定义的函数改造成一个非递归的函数，利用栈保存计算中的临时信息。
def norec_fact(n):#自己管理栈，模拟函数的调用过程
    res=1
    st=SStack()
    while n>0:
        st.push(n)
        n-=1
    while not st.is_empty():
        res*=st.pop()
    return res
#背包问题：能否从n件物品中选出若干件使得重量之和等于背包的承重—>用递归方法更简单
def knap_rec(weight,wlist,n):#weight表示背包可承受的总重量,wlist记录各物品重量的表，n为物品数目
#对于n件物品的背包问题，归结为两个n-1件物品的背包问题
    #前面两个if处理三种简单情况
    if weight==0:
        return True
    if weight<0 or (weight>0 and n<1):
        return False
    #后面两个if通过递归调用得到结果
    if knap_rec(weight-wlist[n-1],wlist,n-1):#加上最后一件物品重量，剩余重量为0
        print ("Item"+str(n)+":",wlist[n-1])
        return True
    if knap_rec(weight,wlist,n-1):#不需要最后一件物品剩余重量已经为0
        return True
    else:
        return False

if __name__=="__main__":
    knap_rec(7,[1,2,4,5],4)
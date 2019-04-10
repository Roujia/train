#coding:UTF-8
#字符串匹配：子串查找
#1、朴素算法（暴力破解法）：复杂度O(m*n)
def naive_matching(t,p):
    m,n=len(p),len(t)
    i,j=0,0
    while i<m and j<n:#i==m说明找到匹配
        if p[i]==t[j]:#字符相同！考虑下一对字符
            i,j=i+1,j+1
            if i == m:  # 找到匹配，返回t中开始下标
                print(j - i)
                j, i = j - i + 1, 0#写在循环中，找出所有子串的位置
        else:#字符不同！考虑t中下一位置
            j,i=j-i+1,0
        # if i==m:#找到匹配，返回t中开始下标
        #     print(j-i)
    return -1#无匹配，返回特殊值
    print(naive_matching())

#naive_matching("123451236123","123")

#2、KMP算法：复杂度O(m+n)
def matching_KMP(t,p,pnext):
    j,i=0,0
    n,m=len(t),len(p)
    while j<n and i<m:#i==m说明找到了匹配
        if i==-1 or t[j]==p[i]:#考虑p中下一字符
            j,i=j+1,i+1
            if i == m:  # 找到匹配，返回t中开始下标
                print(j - i)
                j, i = j - i + 1, 0#写在循环中，找出所有子串的位置
        else:#失败！考虑pnext决定的下一字符串
            i=pnext[i]
    # if i==m:#找到匹配，返回t中开始下标
    #     print (j-i)
    return -1

#生成针对p中各位置i的下一处检查位置表，用于KMP算法：递推计算最长相等前后缀的长度
def gen_pnext1(p):
    i,k,m=0,-1,len(p)#k为p中前缀集合与后缀集合的交集中最长元素的长度，即PMT(Partial Match Table)的元素值
    pnext=[-1]*m#初始数组元素全为-1
    while i<m-1:#生成下一个pnext元素值
        if k==-1 or p[i]==p[k]:
            i,k=i+1,k+1
            pnext[i]=k#设置pnext元素
        else:
            k=pnext[k]#退到更短相同前缀，模式串的自我匹配，不断地递归k = next[k]
    return pnext

#稍许修改的优化版本
def gen_pnext2(p):
    i,k,m=0,-1,len(p)
    pnext=[-1]*m
    while i<m-1:
        if k==-1 or p[i]==p[k]:
            i,k=i+1,k+1
            if p[i]==p[k]:#如果pi和tj失配，当pi=pk时，pk必然也与tj失配，所以模式串还可以进一步递归，提高配对效率
                pnext[i]=pnext[k]
            else:
                pnext[i]=k
        else:
            k=pnext[k]
    return pnext
print(gen_pnext2("abababca"))
matching_KMP("123451236123","123",gen_pnext2("123"))
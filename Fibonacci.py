#coding:UTF-8
#斐波那契数列：前面两项之和构成后一项
#递归
def fibonacci(i):
    # if i==0:
    #     return 0
    # elif i==1:
    #     return 1
    # else:
    #     return fibonacci(i-2)+fibonacci(i-1)
    return i if i<2 else fibonacci(i-2)+fibonacci(i-1)
if __name__=="__main__":
    print (fibonacci(7))

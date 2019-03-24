#coding=UTF-8
#人事记录的实现
import datetime
#针对准备实现的类定义，派生两个专用的异常类
class PersonTypeError (TypeError):
    pass
class PersonValueError (ValueError):
    pass

#1、公共人员类的实现
class Person(object):#super只能应用于新类 ，所有类都必须要有继承的类，如果什么都不想继承，就继承到object类
    _num=0
    def __init__(self,name,sex,birthday,ident):
        if not(isinstance(name,str) and
               sex in ("女","男")):
            raise PersonValueError(name,sex)
        try:
            birth= datetime.date(*birthday)#生成一个日期对象
            #在变量前加*，则多余的函数参数会作为一个元组存在args中
        except:
            raise PersonValueError("wrong data:",birthday)
        self._name=name
        self._sex=sex
        self._birthday=birth
        self._id=ident
        Person._num+=1#实例计数
    def id(self):
        return self._id
    def name(self):
        return self._name
    def sex(self):
        return self._sex
    def birthday(self):
        return datetime.date.today().year-self._birthday.year
    def set_name(self,name):#修改名字
        if not isinstance(name,str):
            raise PersonValueError("set_name",name)
        self._name=name
    def __lt__(self,another):#判断self对象是否小于other对象,gt为>
        if not isinstance(another,Person):
            raise PersonTypeError(another)
        return  self._id<another._id
    @classmethod#定义一个类方法，以便取得类中的人员计数值
    def num(cls):
        return Person._num
    def __str__(self):#返回一个字符串，在使用print语句时被调用
        return " ".join((self._id,self._name,
                        self._sex,str(self._birthday)))#join方法要求参数是可迭代对象，这里是一个tuple
    def details(self):
        return ",".join(("编号："+self._id,
                         "姓名："+self._name,
                         "性别："+self._sex,
                         "出生日期："+str(self._birthday)))

# p1=Person("谢玉洁","女",(1995,7,30),"1201510111")
# p2=Person("李国栋","男",(1990,2,17),"1201380324")
# plist=[p1,p2]
# for p in plist:
#     print(p)
#
# print ("\nAfter sorting:")
# plist.sort()
# for p in plist:
#     print (p.details())
#
# print ("People created:",Person.num(),"\n")


#2、学生类的实现
class Student(Person):
    _id_num=0

    @classmethod
    def _id_gen(cls):#生成学号的规则
        cls._id_num+=1
        year=datetime.date.today().year
        return "1{:04}{:05}".format(year,cls._id_num)#首位为1，与职工号区分，4位10进制数表示入学年份，5位表示序号

    def __init__(self,name,sex,birthday,department):
        Person.__init__(self,name,sex,birthday,Student._id_gen())
        self._department=department
        self._enroll_date=datetime.date.today()
        self._courses={}#一个空字典，记录课程学习成绩

    def set_course(self,course_name):
        self._courses[course_name]=None

    def set_score(self,course_name,score):
        if course_name not in self._courses:
            raise PersonValueError("No this course selected:",course_name)
        self._courses[course_name]=score

    def scores(self):
        return [(cname,self._courses[cname])
                for cname in self._courses]
    #用表描述式给出所有成绩的列表

    #定义新的details方法，覆盖基类中已有定义的details方法。应维持原方法的参数形式，并提供类似的行为，以保证派生类的对象
    #能用在要求基类对象的环境中（“替换原理”）
    def __str__(self):#替换同上
        return " ".join((Person.__str__(self),
                        self._department))
    def details(self):
        return ",".join((Person.details(self),
                        "入学日期："+str(self._enroll_date),
                        "院系："+self._department,
                        "课程记录："+str(self.scores())))

# s1=Student("谢玉洁","女",(1995,7,30),"计算机与信息学院")
# s1.set_course("a")#字典指定key，并且为其赋值一个value，如果key存在，就是修改value，反之就添加一个Entry
# s1.set_course("b")
# s1.set_score("a",80)
# s1.set_score("b",90)
# print s1._courses
# s2=Student("李国栋","男",(1990,2,17),"土木院")
# slist=[s1,s2]
# for s in slist:
#     print(s)
#
# print ("\nAfter sorting:")
# slist.sort()
# for s in slist:
#     print (s.details())
#
# print ("Students created:",Person.num(),"\n")


#3、教职工类的实现
class Staff(Person):
    _id_num=0

    @classmethod
    def _id_gen(cls,birthday):#实现职工号生成规则
        cls._id_num+=1
        birth_year=datetime.date(*birthday).year
        return "0{:04}{:05}".format(birth_year,cls._id_num)

    def __init__(self,name,sex,birthday,entry_date=None):
        super(Staff, self).__init__(name,sex,birthday,Staff._id_gen(birthday))
        if entry_date:
            try:
                self._entry_date=datetime.date(*entry_date)
            except:
                raise PersonValueError("Wrong date:",entry_date)
        else:
            self._entry_date=datetime.date.today()
        self._salary=1720#默认设为最低工资，可修改
        self._department="未定"#需另行设定
        self._position="未定"#需另行设定

    def set_salary(self,amount):
        if not type(amount) is int:
            raise TypeError
        self._salary=amount

    def set_department(self,department):
        self._department=department

    def set_position(self,position):
        self._position=position

    def __str__(self):  # 替换同上
        return " ".join((super(Staff, self).__str__(),
                         self._department,
                         self._position,
                         str(self._salary)))

    def details(self):
        return ",".join((super(Staff, self).details(),
                         "入职日期：" + str(self._entry_date),
                         "院系：" + self._department,
                         "职位：" + self._position,
                         "工资："+str(self._salary)))

s1 = Staff("谢玉洁", "女", (1995, 7, 30))
s2 = Staff("李国栋", "男", (1990, 2, 17))
s1.set_department("math")
s1.set_position("associate professor")
s1.set_salary(9000)
slist = [s1, s2]
for s in slist:
    print(s)

print ("\nAfter sorting:")
slist.sort()
for s in slist:
    print (s.details())

print ("Staffs created:", Person.num(), "\n")
from student import Student


class StudentManager(object):

    def __init__(self):
        # 存储数据所用列表
        self.student_list = []

    # 一. 程序入口函数，启动程序后执行的函数
    def run(self):
        # 1. 加载学员信息
        self.load_student()

        while True:
            # 2. 显示功能菜单
            self.show_menu()
            # 3. 输入功能序号
            menu_num = int(input('please input the menu num: '))
            if menu_num == 1:
                self.add_student()
            elif menu_num == 2:
                self.del_student()
            elif menu_num == 3:
                self.modify_student()
            elif menu_num == 4:
                self.search_student()
            elif menu_num == 5:
                self.show_student()
            elif menu_num == 6:
                # save info
                self.save_student()
            elif menu_num == 7:
                # exit
                break

    @staticmethod
    def show_menu():
        print('请选择如下功能-----------------')
        print('1:添加学员')
        print('2:删除学员')
        print('3:修改学员信息')
        print('4:查询学员信息')
        print('5:显示所有学员信息')
        print('6:保存学员信息')
        print('7:退出系统')

    # 2.2 添加学员
    def add_student(self):
        # 1. 用户输入姓名、性别、手机号
        name = input('请输入您的姓名：')
        gender = input('请输入您的性别：')
        tel = input('请输入您的手机号：')

        # 2. 创建学员对象：先导入学员模块，再创建对象
        student = Student(name, gender, tel)

        # 3. 将该学员对象添加到列表
        self.student_list.append(student)

        # 打印信息
        print(self.student_list)
        print(student)

    # 2.3 删除学员
    def del_student(self):
        # 1. 用户输入目标学员姓名
        del_name = input('请输入要删除的学员姓名：')
        # 2. 如果用户输入的目标学员存在则删除，否则提示学员不存在
        for i in self.student_list:
            if i.name == del_name:
                self.student_list.remove(i)
                break
        else:
            print('查无此人')

        print(self.student_list)

    # 2.4 修改学员信息
    def modify_student(self):
        # 1. 用户输入目标学员姓名
        modify_name = input('请输入要修改的学员的姓名：')
        # 2. 如果用户输入的目标学员存在则修改姓名、性别、手机号等数据，否则提示学员不存在
        for i in self.student_list:
            if i.name == modify_name:
                i.name = input('请输入学员姓名：')
                i.gender = input('请输入学员性别：')
                i.tel = input('请输入学员手机号：')
                print(f'修改该学员信息成功，姓名{i.name},性别{i.gender}, 手机号{i.tel}')
                break
        else:
            print('查无此人')

    # 2.5 查询学员信息
    def search_student(self):
        # 1. 用户输入目标学员姓名
        search_name = input('请输入要查询的学员的姓名：')

        # 2. 如果用户输入的目标学员存在，则打印学员信息，否则提示学员不存在
        for i in self.student_list:
            if i.name == search_name:
                print(f'{i.name}-{i.gender}-{i.tel}')
                break
        else:
            print('查无此人')

    # 2.6 显示所有学员信息
    def show_student(self):
        print('姓名\t性别\t手机号')
        for i in self.student_list:
            print(f'{i.name}\t{i.gender}\t{i.tel}')

    # 2.7 保存学员信息
    def save_student(self):
        f = open('student.data', 'w')
        new_list = [i.__dict__ for i in self.student_list]
        print(new_list)
        f.write(str(new_list))
        f.close()

    '''
        class A(object):
            a = 0

            def __init__(self):
                self.b = 1


            aa = A()
        # 返回类内部所有属性和方法对应的字典
        print(A.__dict__)
        # 返回实例属性和值组成的字典
        print(aa.__dict__)
    '''

    # 2.8 加载学员信息
    def load_student(self):
        try:
            f = open('student.data', 'r')
        except:
            f = open('student.data', 'w')
        else:
            data = f.read()
            # 文件中读取的数据都是字符串且字符串内部为字典数据，故需要转换数据类型再转换字典为对象后存储到学员列表
            list = eval(data)
            self.student_list = [Student(i['name'], i['gender'], i['tel']) for i in list]
        finally:
            f.close()
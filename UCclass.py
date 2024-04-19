from sympy import symbols, diff, sympify, simplify, pi, E, exp, sin, cos, tan, log
import pandas as pd
import numpy as np
from tabulate import tabulate
import wcwidth
from tkinter import *
from tkinter import filedialog

pd.set_option('display.unicode.ambiguous_as_wide', True)  # 将模糊字符宽度设置为2
pd.set_option('display.unicode.east_asian_width', True)  # 检查东亚字符宽度属性


class UncertaintyCalculate:
    def __init__(self, analysis_data=pd.DataFrame()):

        self.analysis_data = analysis_data  # 初始化一个空数据框,储存分析要分析的数据

        self.x_size = 0  # 分量个数
        self.xi_size = 0  # 单个分量数据个数

        self.x_mean = np.array([])  # 初始化一个空列表来存储每一列的平均值
        self.func_value = np.array([])  # 函数值
        self.func_output = pd.DataFrame()  # 初始化一个空数据框,储存函数值

        self.x = []  # 初始化一个空列表来存储变量
        self.func_string = simplify('x')  # 函数表达式
        self.diff_exp = []  # 初始化一个空列表来存储偏导数的表达式
        self.diff_value = np.array([])  # 初始化一个空列表来存储偏导数的值

        self.std_values = np.array([])  # 标准差
        self.a_uncertainty = np.array([])  # A类不确定度
        self.b_uncertainty = np.array([])  # B类不确定度
        self.uc_uncertainty = np.array([])  # 合成不确定度
        self.u_uncertainty = np.array([])  # 扩展不确定度
        self.ar_uncertainty = np.array([])  # A类相对不确定度
        self.br_uncertainty = np.array([])  # B类相对不确定度
        self.ucr_uncertainty = np.array([])  # 合成相对不确定度
        self.ur_uncertainty = np.array([])  # 扩展相对不确定度

        self.AR_values = []  # 字符A类相对不确定度
        self.BR_values = []  # 字符B类相对不确定度
        self.ucR_values = []  # 字符合成相对不确定度
        self.UR_values = []  # 字符扩展相对不确定度

        self.min_division = np.array([])  # 最小分度值
        self.k = 0  # 初始化包含因子k

        self.index = ['A类不确定度', 'B类不确定度', '偏导表达式', '偏导数值', '合成不确定度', '扩展不确定度', '平均值']
        self.output = pd.DataFrame()  # 初始化一个空数据框,储存输出结果

        #  数据预处理
        self.i = 1  # 初始化一个计数器

    def initialization(self):
        self.x_size = self.analysis_data.shape[1]  # 分量个数
        self.xi_size = self.analysis_data.shape[0]  # 单个分量数据个数

        #  函数表达式
        self.func_string = sympify(input("请输入函数表达式："))

        # 生成符号变量
        for i in range(1, self.x_size + 1):
            var_name = 'x' + str(i)  # 生成变量名称，例如 'x1', 'x2', ...
            var = symbols(var_name, real=True)  # 创建符号变量
            self.x.append(var)  # 将变量添加到列表中

        #  替换变量
        for i in range(self.x_size):
            self.func_string = self.func_string.subs('x' + str(i + 1), self.x[i])

        #  计算偏导数
        for i in range(self.x_size):
            self.diff_exp.append(diff(self.func_string, self.x[i]))
        self.diff_exp.append('None')  # 补空值

        #  分度值
        self.min_division = np.zeros(self.x_size)
        for i in range(self.x_size):
            self.min_division[i] = float(input("请输入第{}个分量的仪器最小分度(注意单位)：".format(i + 1)))

        #  包含因子k
        self.k = float(input("请输入包含因子k："))

    # 数据处理
    def data_process(self):

        input_array = self.analysis_data.values  # 将数据框转换为数组

        self.output = pd.DataFrame(columns=self.x, index=self.index)  # 初始化数据框,储存输出结果
        self.output.insert(self.output.shape[1], 'f(X)', 'None')

        # 计算均值
        self.x_mean = np.mean(input_array, axis=0)

        # 各分量的不确定度
        #  计算A类不确定度
        self.std_values = np.std(input_array, axis=0, ddof=1)  # 计算每一列的标准偏差
        self.a_uncertainty = self.std_values / np.sqrt(self.xi_size)  # 计算A类不确定度
        self.std_values = np.append(self.std_values, 'None')

        #  计算B类不确定度
        for i in range(self.x_size):
            self.b_uncertainty = np.append(self.b_uncertainty, self.min_division[i] / np.sqrt(3))

        #  计算函数的A,B类不确定度
        #  计算函数值
        for i in range(self.xi_size):
            self.func_value = np.append(self.func_value,
                                        self.func_string.subs(list(zip(self.x, input_array[i, :]))).evalf())

        #  计算偏导数的值
        for i in range(self.x_size):
            self.diff_value = np.append(self.diff_value, self.diff_exp[i].subs(list(zip(self.x, self.x_mean))).evalf())

        # A
        self.a_uncertainty = np.append(self.a_uncertainty,
                                       (np.sum(self.diff_value ** 2 * self.a_uncertainty ** 2)) ** 0.5)

        # B
        self.b_uncertainty = np.append(self.b_uncertainty,
                                       (np.sum(self.diff_value ** 2 * self.b_uncertainty ** 2)) ** 0.5)

        self.x_mean = np.append(self.x_mean, np.mean(self.func_value))
        #  A类相对不确定度
        self.ar_uncertainty = self.a_uncertainty / self.x_mean
        #  B类相对不确定度
        self.br_uncertainty = self.b_uncertainty / self.x_mean

        #  合成不确定度
        self.uc_uncertainty = (self.a_uncertainty ** 2 + self.b_uncertainty ** 2) ** 0.5
        # 合成相对不确定度
        self.ucr_uncertainty = self.uc_uncertainty / self.x_mean

        #  扩展不确定度
        self.u_uncertainty = self.k * self.uc_uncertainty
        # 扩展相对不确定度
        self.ur_uncertainty = self.u_uncertainty / self.x_mean

        #  相对不确定度字符化
        for i in range(self.x_size + 1):
            self.AR_values.append(str(self.ar_uncertainty[i] * 100) + '%')
            self.BR_values.append(str(self.br_uncertainty[i] * 100) + '%')
            self.ucR_values.append(str(self.ucr_uncertainty[i] * 100) + '%')
            self.UR_values.append(str(self.ur_uncertainty[i] * 100) + '%')

        #  补充空值
        self.diff_value = np.append(self.diff_value, 'None')

        #  输出结果
        self.output.loc['A类不确定度'] = self.a_uncertainty
        self.output.loc['B类不确定度'] = self.b_uncertainty
        self.output.loc['偏导表达式'] = self.diff_exp
        self.output.loc['偏导数值'] = self.diff_value
        self.output.loc['合成不确定度'] = self.uc_uncertainty
        self.output.loc['扩展不确定度'] = self.u_uncertainty
        self.output.loc['平均值'] = self.x_mean
        self.output.loc['A类相对不确定度'] = self.AR_values
        self.output.loc['B类相对不确定度'] = self.BR_values
        self.output.loc['合成相对不确定度'] = self.ucR_values
        self.output.loc['扩展相对不确定度'] = self.UR_values

        self.func_output = pd.DataFrame(self.func_value)

    #  打印函数部分

    def print_default(self):
        print('函数值为：')
        print(tabulate(self.func_output, headers='keys', tablefmt='grid'))

        output_default = pd.DataFrame(columns=self.x)  # 初始化数据框,储存输出结果
        output_default.insert(output_default.shape[1], 'f(X)', 'None')

        output_default.loc['平均值'] = self.x_mean
        output_default.loc['扩展不确定度'] = self.u_uncertainty
        output_default.loc['扩展相对不确定度'] = self.UR_values

        print('\n不确定度：')
        print(tabulate(output_default, headers='keys', tablefmt='grid'))

    def print_all(self):
        print('\n不确定度：')
        print(tabulate(self.output, headers='keys', tablefmt='grid'))

    def print_uncertainty(self):
        output_uncertainty = pd.DataFrame(columns=self.x)  # 初始化数据框,储存输出结果
        output_uncertainty.insert(output_uncertainty.shape[1], 'f(X)', 'None')

        output_uncertainty.loc['A类不确定度'] = self.a_uncertainty
        output_uncertainty.loc['B类不确定度'] = self.b_uncertainty
        output_uncertainty.loc['合成不确定度'] = self.uc_uncertainty

        print(tabulate(output_uncertainty, headers='keys', tablefmt='grid'))

    def print_diff(self):
        output_diff = pd.DataFrame(columns=self.x)  # 初始化数据框,储存输出结果
        output_diff.insert(output_diff.shape[1], 'f(X)', 'None')

        output_diff.loc['偏导表达式'] = self.diff_exp
        output_diff.loc['偏导数值'] = self.diff_value

        # 在 output_diff 中替换 pi, E
        output_diff_T = output_diff.T
        output_diff_T['偏导表达式'] = output_diff_T['偏导表达式'].apply(
            lambda x: str(x).replace(str(pi), 'pi').replace(str(E), 'e'))

        print(tabulate(output_diff_T.T, headers='keys', tablefmt='grid'))

    def print_ru(self):
        output_ru = pd.DataFrame(columns=self.x)  # 初始化数据框,储存输出结果
        output_ru.insert(output_ru.shape[1], 'f(X)', 'None')

        output_ru.loc['A类相对不确定度'] = self.AR_values
        output_ru.loc['B类相对不确定度'] = self.BR_values
        output_ru.loc['合成相对不确定度'] = self.ucR_values

        print(tabulate(output_ru, headers='keys', tablefmt='grid'))

    def save_output(self, root2):
        root2.destroy()
        # 选择保存名1
        filename = input("请输入保存文件名(不需要后缀)(如果留空，默认文件名为'不确定度计算结果'，直接按回车就行)：")
        if filename == "":
            filename = '不确定度计算结果.xlsx'
        else:
            filename += '.xlsx'
        # 实例化
        root = Tk()
        root.geometry("500x500")
        root.withdraw()
        # 获取文件夹路径
        f_path = filedialog.askdirectory()
        if f_path == "":
            print("未选择文件")
            root.destroy()
            return self.windows()
        root.destroy()
        print('文件的保存路径为：' + f_path + '/' + filename)
        self.output.to_excel(f_path + '/' + filename, index=True)
        self.windows()

    def windows(self):
        root2 = Tk()
        root2.title('不确定度分析')
        root2.geometry('300x300+888+444')

        button1 = Button(root2, text="全部打印", command=self.print_all)
        button1.pack(pady=5)
        button2 = Button(root2, text="其他不确定度", command=self.print_uncertainty)
        button2.pack(pady=5)
        button3 = Button(root2, text="偏导数", command=self.print_diff)
        button3.pack(pady=5)
        button4 = Button(root2, text="其他相对不确定度", command=self.print_ru)
        button4.pack(pady=5)
        button5 = Button(root2, text="保存结果", command=lambda: self.save_output(root2))
        button5.pack(pady=5)

        root2.mainloop()

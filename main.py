import time
from pynput.keyboard import Controller
import tkinter as tk
from tkinter import scrolledtext
import base64,os
from exchange_logo.logo import img
def all_in_one(filename):
    if os.path.splitext(filename)[1] != '.txt':
        text_area.config(state='normal', font=('Arial', 12))
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, "文件格式错误，请选择txt文件\n")
        text_area.config(state='disabled')
        raise
    else:
        text_area.config(state='normal', font=('Arial', 12))
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, "开始转换\n")
        text_area.config(state='disabled')
        root.update()
        time.sleep(2)
        # 打开原始文件并读取内容
        try:
            print(f"正在打开文件 {filename}")
            text_area.config(state='normal', font=('Arial', 12))
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.INSERT, f"正在打开文件{filename}")
            text_area.config(state='disabled')
            root.update()
            time.sleep(2)
            with open(filename, encoding='utf-8', mode='r') as file:
                lines = file.readlines()
            # 读取文本删除特定的字符串后转换为一行，并且在头部加上特定的字符串
            update_line = [line.replace("@&@&@~:", "") for line in lines]
            single_line = ''.join(line.strip() for line in update_line)
            text_area.config(state='normal', font=('Arial', 12))
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.INSERT, "读取完成\n")
            text_area.config(state='disabled')
            root.update()
            time.sleep(1)
            # 输出转换后的单行文本到新文件
            with open('data.txt', encoding='utf-8', mode='w') as output_file:
                output_file.write("START@&@&@~:" + single_line)
            text_area.config(state='normal', font=('Arial', 12))
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.INSERT, "转换成功\n")
            text_area.config(state='disabled')
            root.update()
            time.sleep(3)
        except FileNotFoundError:
            text_area.config(state='normal', font=('Arial', 10))
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.INSERT, "转换失败,请检查以下原因后重试\n1.文件路径是否正确\n2.文件是否存在\n3.文件是否为txt（utf-8）格式")
            text_area.config(state='disabled')
            raise

def send():
    keyboard = Controller()
    countdown_time = 5
    for i in range(countdown_time, 0, -1):
        text_area.config(state='normal', font=('Arial', 12))
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, f"{i}秒内用鼠标点击文本框\n")
        text_area.config(state='disabled')
        root.update()
        time.sleep(1)
    text_area.config(state='normal', font=('Arial', 12))
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.INSERT, "开始输入\nPs:1.出现轻微卡顿请在输入框内轻微移动鼠标\n2.输入过程中请勿点击鼠标")
    text_area.config(state='disabled')
    root.update()
    data_dict = {}
    for line in open("data.txt", encoding='utf-8', mode='r'):
        parts = line.split('@&@&@~:')
        key, value = parts
        data_dict[key] = value
    for key, value in data_dict.items():
        line = f"{value}"
        keyboard.type(line)
    os.remove("data.txt")
    time.sleep(3)
    text_area.config(state='normal', font=('Arial', 12))
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.INSERT, "输入完成\n")
    text_area.config(state='disabled')


def gui():
    filename= entry.get()
    try:
        with open(filename, 'r') as file:
            content = file.read()
            text_area.config(state='normal', font=('Arial', 12))
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.INSERT, content)
            text_area.config(state='disabled')
    except FileNotFoundError:
        text_area.config(state='normal', font=('Arial', 12))
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.INSERT, "文件未找到，请检查文件地址")
        text_area.config(state='disabled')
        raise

# 创建主窗口
root = tk.Tk()
root.title("Cxtext GUI")
root.configure(bg='gray')
root.geometry("350x170")

icon = open("gui.ico", "wb+")
icon.write(base64.b64decode(img))
icon.close()
root.iconbitmap("gui.ico")
os.remove("gui.ico")

# 创建文本
label = tk.Label(root, text="请输入文件地址:",font=('Arial', 12), bg='gray', fg='black')
label.pack(side=tk.TOP,pady=1)

# 创建用户输入框
entry = tk.Entry(root, width=50, bg='gray', fg='black')
entry.insert(0, "记得删除文件地址的引号")
entry.pack(pady=0)

# 创建发送按钮，点击后调用send函数
button_send = tk.Button(root, width=10,height=2,text="开始", command=lambda: [all_in_one(entry.get()), send()],font=('Arial', 12), bg='gray', fg='black')
button_send.pack(pady=1)

# 创建内容打印框
text_area = scrolledtext.ScrolledText(root, width=50, height=5, bg='gray',font=('Arial', 12), fg='white', state='disabled')
text_area.pack(pady=0)

# 运行主循环
root.mainloop()
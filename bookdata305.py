import re
import tkinter as tk
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def get_webpage_content():
    # 从输入框获取网址
    
    url = url_entry.get()
    #print(url)

    try:
        # 发送 HTTP 请求获取网页内容
        response = urlopen(url)

        # 获取网页的 HTML 内容
        html_content = response.read().decode('utf-8')

        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')

        # 使用 select 方法查找匹配的元素
        span_element = soup.select('span.text')[7]

        # 提取元素的文本内容
        span_text = span_element.text

        # 使用正则表达式提取数字
        numbers = re.findall(r'\d+', span_text)

        # 创建新的 DataFrame
        df = pd.DataFrame(numbers, columns=['Number'])

        # 读取之前保存的 Excel 文件
        previous_df = pd.read_excel('numbers5.xlsx')

      
        # 获取之前保存的最后一行的索引
        last_index = previous_df.index[-1] + 1 if len(previous_df) > 0 else 0
        # 获取之前保存的数字
        previous_number = previous_df.iloc[-1, 0] if len(previous_df) > 0 else None
        
        # 比较当前数字与上次保存的数字
        if previous_number is not None and int(numbers[0]) == previous_number:
           difference = 0
        else:
           difference = int(numbers[0]) - previous_number if previous_number is not None else 0
           # 如果当前数字与上次保存的数字不相等，保存新的数字和差值
        if previous_number is None or int(numbers[0]) != previous_number:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            df['Time'] = current_time
            df['Difference'] = difference
            
            # 将新的数字追加到之前的 DataFrame 中
            updated_df = pd.concat([previous_df, df], ignore_index=True)
            
            # 将更新后的 DataFrame 保存到 Excel 文件中
            with pd.ExcelWriter('numbers5.xlsx') as writer:
              updated_df.to_excel(writer, index=False)
        else:
           difference = 0

        # 打印差值
        result_label.config(text="差值: {}".format(difference))

    except:
        result_label.config(text="获取网页内容失败！")

# 创建主窗口
window = tk.Tk()
window.title("获取点击")

# 创建网址输入框
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# 创建获取按钮
button = tk.Button(window, text="获取", command=get_webpage_content)
button.pack()

# 创建结果标签
result_label = tk.Label(window, text="点击新增: ")
result_label.pack()

# 运行窗口
window.mainloop()

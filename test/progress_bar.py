import time
from alive_progress import alive_bar

def fancy_progress_bar():
    total = 100
    
    with alive_bar(total) as bar:
        for i in range(total):
            time.sleep(0.1)  # 模拟耗时操作
            bar()
    
    print("进度条完成！")

fancy_progress_bar()
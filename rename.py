import os
import re

# 定义文件夹路径
folder_path = './datatest'  # 替换为你的文件夹路径

num=input("输入要增加的数量：")

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 使用正则表达式匹配文件名中的数字
    match = re.match(r'(\d+)(\.txt|\.jpg|\.png)', filename)
    if match:
        # 提取数字部分和扩展名
        number = int(match.group(1))
        extension = match.group(2)
        
        # 数字增加100
        new_number = number + int (num)
        
        # 构建新的文件名
        new_filename = f"{new_number}{extension}"
        
        # 获取文件的完整路径
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # 重命名文件
        os.rename(old_file, new_file)
        print(f"Renamed {filename} to {new_filename}")

print("批量重命名完成！")

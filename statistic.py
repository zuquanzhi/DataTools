import os
import sys
from collections import defaultdict
from tqdm import tqdm

def read_txt_file(file_path):
    """读取文件内容"""
    if not os.path.exists(file_path):
        print("文件未找到: ", file_path)
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_txt_files(path):
    """获取指定路径下的所有txt文件"""
    if os.path.isfile(path) and path.endswith('.txt'):
        return [path]
    
    txt_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def statistic(path):
    """统计文件或文件夹中的标签ID"""
    txt_files = get_txt_files(path)
    if not txt_files:
        print(f"未找到任何txt文件在: {path}")
        return
    
    # 使用defaultdict初始化总计数器
    total_counts = defaultdict(int)
    file_counts = {}  # 记录每个文件的单独统计
    total_lines = 0
    
    # 使用tqdm创建进度条
    with tqdm(total=len(txt_files), 
             desc="处理文件", 
             bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
             colour="green") as pbar:
        
        # 处理每个文件
        for txt_file in txt_files:
            content = read_txt_file(txt_file)
            if content is None:
                pbar.update(1)
                continue
            
            # 当前文件的计数器
            current_file_counts = defaultdict(int)
            
            # 按行处理文件内容
            lines = content.splitlines()
            for line in lines:
                if line.strip():  # 跳过空行
                    try:
                        # 提取每行的首个ID值
                        id_value = line.strip().split()[0]  # 假设ID是每行的第一个值
                        current_file_counts[id_value] += 1
                        total_counts[id_value] += 1
                        total_lines += 1
                    except Exception as e:
                        print(f"\n错误处理文件 {txt_file} 中的行: {line}, 错误信息: {e}")
            
            # 保存当前文件的统计结果
            if current_file_counts:
                file_counts[txt_file] = dict(current_file_counts)
            
            # 更新进度条
            pbar.update(1)
            pbar.set_postfix({"总行数": total_lines})
    
    # 打印详细统计结果
    print("\n=== 详细统计结果 ===")
    for txt_file, counts in file_counts.items():
        print(f"\n文件: {txt_file}")
        for label, count in sorted(counts.items()):
            print(f"ID {label}: {count} 次")
    
    # 打印总体统计结果
    print("\n=== 总体统计结果 ===")
    print(f"处理文件总数: {len(txt_files)} 个")
    print(f"总行数: {total_lines} 行")
    print(f"不同ID总数: {len(total_counts)} 个")
    print("\n按数量排序的ID统计:")
    for label, count in sorted(total_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"ID {label}: {count} 次")
    
    return total_counts

def main():
    if len(sys.argv) != 2:
        print("使用方法: python statistic.py <文件路径或文件夹路径>")
        sys.exit(1)
    
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"路径不存在: {path}")
        sys.exit(1)
    
    statistic(path)

if __name__ == "__main__":
    main()

import os
import re
import argparse
from tqdm import tqdm

def rename_files(folder_path, number_change, file_types=None, dry_run=False):
    """
    批量重命名文件，修改文件名中的数字
    
    Args:
        folder_path: 文件夹路径
        number_change: 数字变化量（可以是正数或负数）
        file_types: 要处理的文件类型列表，默认为 ['.txt', '.jpg', '.png']
        dry_run: 如果为True，只显示会进行的更改但不实际执行
    """
    if file_types is None:
        file_types = ['.txt', '.jpg', '.png']

    # 确保文件夹存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在")
        return False

    # 获取所有文件并排序
    try:
        files = [f for f in os.listdir(folder_path) 
                if os.path.splitext(f)[1].lower() in file_types]
        files.sort()
    except Exception as e:
        print(f"读取文件夹时出错: {str(e)}")
        return False

    if not files:
        print("未找到符合条件的文件")
        return True

    # 保存重命名操作的映射，用于检查冲突
    rename_map = {}
    processed = 0
    skipped = 0
    
    print(f"{'预览更改' if dry_run else '开始重命名'}...")
    
    # 使用tqdm创建进度条
    for filename in tqdm(files, desc="处理文件"):
        try:
            # 使用正则表达式匹配文件名中的数字
            match = re.match(r'(\d+)(\..*)', filename)
            if not match:
                if not dry_run:
                    print(f"跳过 {filename} - 未找到数字")
                skipped += 1
                continue

            # 提取数字和扩展名
            number = int(match.group(1))
            extension = match.group(2)
            
            # 计算新数字
            new_number = number + number_change
            if new_number < 0:
                print(f"警告：{filename} 重命名后数字为负，已跳过")
                skipped += 1
                continue
                
            # 构建新文件名
            new_filename = f"{new_number:d}{extension}"
            
            # 检查是否会覆盖现有文件
            if new_filename in rename_map.values() or \
               (os.path.exists(os.path.join(folder_path, new_filename)) and \
                new_filename != filename):
                print(f"警告：{filename} -> {new_filename} 会造成冲突，已跳过")
                skipped += 1
                continue
            
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)
            
            if dry_run:
                print(f"将重命名: {filename} -> {new_filename}")
            else:
                os.rename(old_path, new_path)
            
            rename_map[filename] = new_filename
            processed += 1
            
        except Exception as e:
            print(f"\n处理 {filename} 时出错: {str(e)}")
            skipped += 1
            continue

    # 打印统计信息
    print(f"\n{'预览' if dry_run else '重命名'}完成!")
    print(f"处理成功: {processed} 个文件")
    print(f"跳过/失败: {skipped} 个文件")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='批量重命名文件中的数字')
    parser.add_argument('--folder', '-f', type=str, required=True,
                      help='要处理的文件夹路径')
    parser.add_argument('--change', '-c', type=int, required=True,
                      help='数字增加的数量（可以为负数）')
    parser.add_argument('--types', '-t', type=str, default='.txt,.jpg,.png',
                      help='要处理的文件类型，用逗号分隔 (默认: .txt,.jpg,.png)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                      help='预览模式：只显示将进行的更改，不实际重命名')

    args = parser.parse_args()
    
    file_types = [t.strip() if t.startswith('.') else f'.{t.strip()}' 
                 for t in args.types.split(',')]
    
    success = rename_files(args.folder, args.change, file_types, args.dry_run)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
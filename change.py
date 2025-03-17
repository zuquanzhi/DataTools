import os
import argparse
from tqdm import tqdm

def create_number_mapping(mapping_str):
    """
    解析数字映射关系字符串
    
    Args:
        mapping_str: 格式如 "23:32,24:33" 的映射字符串
    Returns:
        dict: 数字映射字典
    """
    mapping = {}
    try:
        pairs = mapping_str.split(',')
        for pair in pairs:
            old, new = pair.strip().split(':')
            mapping[float(old)] = str(new)
        return mapping
    except ValueError as e:
        raise ValueError("映射格式错误，应为'旧值:新值,旧值:新值'，例如'23:32,24:33'") from e

def modify_numbers_in_txt_files(directory, number_mapping, recursive=True, backup=True):
    """
    修改指定文件夹下txt文件中每行第一个数字
    
    Args:
        directory: 要修改的文件夹路径
        number_mapping: 数字映射字典
        recursive: 是否递归处理子文件夹
        backup: 是否创建备份文件
    """
    try:
        # 获取所有需要处理的txt文件
        txt_files = []
        if recursive:
            for root, _, files in os.walk(directory):
                txt_files.extend(
                    os.path.join(root, f) for f in files if f.endswith('.txt')
                )
        else:
            txt_files = [
                os.path.join(directory, f) 
                for f in os.listdir(directory) 
                if f.endswith('.txt')
            ]

        modified_files = 0
        modified_lines = 0
        skipped_files = 0

        # 使用tqdm创建进度条
        for file_path in tqdm(txt_files, desc="处理文件"):
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 创建备份
                if backup:
                    backup_path = file_path + '.bak'
                    if not os.path.exists(backup_path):
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)

                # 修改内容
                new_lines = []
                file_modified = False
                
                for line in lines:
                    parts = line.strip().split()
                    if not parts:  # 跳过空行
                        new_lines.append(line)
                        continue
                        
                    try:
                        first_number = float(parts[0])
                        if first_number in number_mapping:
                            parts[0] = number_mapping[first_number]
                            file_modified = True
                            modified_lines += 1
                    except ValueError:
                        pass  # 不是数字，保持原样
                    
                    new_lines.append(' '.join(parts) + '\n')

                # 只有在文件确实被修改时才写入
                if file_modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    modified_files += 1
                
            except Exception as e:
                print(f"\n处理文件 {file_path} 时出错: {str(e)}")
                skipped_files += 1
                continue

        # 打印统计信息
        print(f"\n处理完成!")
        print(f"已修改: {modified_files} 个文件")
        print(f"修改了: {modified_lines} 行内容")
        print(f"跳过/失败: {skipped_files} 个文件")

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description='批量修改txt文件中的标签数字')
    parser.add_argument('--dir', '-d', type=str, required=True,
                      help='要处理的文件夹路径')
    parser.add_argument('--mapping', '-m', type=str, required=True,
                      help='数字映射关系，格式如 "23:32,24:33"')
    parser.add_argument('--no-recursive', '-nr', action='store_true',
                      help='不递归处理子文件夹')
    parser.add_argument('--no-backup', '-nb', action='store_true',default=False,
                      help='不创建备份文件')

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print("错误：指定的文件夹不存在！")
        return 1

    try:
        number_mapping = create_number_mapping(args.mapping)
    except ValueError as e:
        print(f"错误：{str(e)}")
        return 1

    success = modify_numbers_in_txt_files(
        args.dir,
        number_mapping,
        not args.no_recursive,
        not args.no_backup
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
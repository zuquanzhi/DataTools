import os
import argparse
from tqdm import tqdm

def restore_from_backup(directory, recursive=True, remove_backup=False):
    """
    从备份文件恢复原始文件
    
    Args:
        directory: 要处理的文件夹路径
        recursive: 是否递归处理子文件夹
        remove_backup: 恢复后是否删除备份文件
    """
    try:
        # 获取所有备份文件
        backup_files = []
        if recursive:
            for root, _, files in os.walk(directory):
                backup_files.extend(
                    os.path.join(root, f) for f in files if f.endswith('.txt.bak')
                )
        else:
            backup_files = [
                os.path.join(directory, f) 
                for f in os.listdir(directory) 
                if f.endswith('.txt.bak')
            ]

        if not backup_files:
            print("未找到任何备份文件！")
            return True

        restored_count = 0
        failed_count = 0

        print(f"找到 {len(backup_files)} 个备份文件")
        for backup_file in tqdm(backup_files, desc="恢复文件"):
            try:
                # 获取原始文件路径
                original_file = backup_file[:-4]  # 移除 .bak 后缀
                
                # 恢复文件
                with open(backup_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(original_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 如果需要，删除备份文件
                if remove_backup:
                    os.remove(backup_file)
                
                restored_count += 1
                
            except Exception as e:
                print(f"\n恢复文件 {backup_file} 时出错: {str(e)}")
                failed_count += 1
                continue

        print("\n恢复完成!")
        print(f"成功恢复: {restored_count} 个文件")
        print(f"恢复失败: {failed_count} 个文件")
        if remove_backup:
            print("备份文件已删除")
        else:
            print("备份文件已保留")

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description='从备份文件恢复原始文件')
    parser.add_argument('--dir', '-d', type=str, required=True,
                      help='要处理的文件夹路径')
    parser.add_argument('--no-recursive', '-nr', action='store_true',
                      help='不递归处理子文件夹')
    parser.add_argument('--remove-backup', '-rm', action='store_true',
                      help='恢复后删除备份文件')

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print("错误：指定的文件夹不存在！")
        return 1

    success = restore_from_backup(
        args.dir,
        not args.no_recursive,
        args.remove_backup
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
import os
import argparse
from collections import defaultdict
from tqdm import tqdm

def read_txt_file(file_path):
    """读取文件内容"""
    if not os.path.exists(file_path):
        print("文件未找到: ", file_path)
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_txt_files(path, recurse=False):
    """获取指定路径下的所有txt文件，如果recurse为True，则会递归子文件夹"""
    if os.path.isfile(path) and path.endswith('.txt'):
        return [path]
    
    txt_files = []
    if recurse:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))
    else:
        # 仅获取当前文件夹的txt文件
        for file in os.listdir(path):
            if file.endswith('.txt'):
                txt_files.append(os.path.join(path, file))
    return txt_files

def statistic(path, recurse=False):
    """统计文件或文件夹中的标签ID并返回统计结果"""
    txt_files = get_txt_files(path, recurse)
    if not txt_files:
        print(f"未找到任何txt文件在: {path}")
        return None
    
    total_counts = defaultdict(int)
    file_counts = {}
    total_lines = 0
    
    with tqdm(total=len(txt_files), 
             desc="处理文件", 
             bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
             colour="green") as pbar:
        
        for txt_file in txt_files:
            content = read_txt_file(txt_file)
            if content is None:
                pbar.update(1)
                continue
            
            current_file_counts = defaultdict(int)
            lines = content.splitlines()
            for line in lines:
                if line.strip():
                    try:
                        id_value = line.strip().split()[0]
                        current_file_counts[id_value] += 1
                        total_counts[id_value] += 1
                        total_lines += 1
                    except Exception as e:
                        print(f"\n错误处理文件 {txt_file} 中的行: {line}, 错误信息: {e}")
            
            if current_file_counts:
                file_counts[txt_file] = dict(current_file_counts)
            pbar.update(1)
            pbar.set_postfix({"总行数": total_lines})
    
    stats = {
        'total_files': len(txt_files),
        'total_lines': total_lines,
        'total_ids': len(total_counts),
        'total_counts': dict(total_counts),
        'file_counts': file_counts
    }
    return stats

def save_statistics(stats, output_path, sort_by='id'):
    """将统计结果保存到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== 总体统计 ===\n")
        f.write(f"处理文件总数: {stats['total_files']} 个\n")
        f.write(f"总行数: {stats['total_lines']} 行\n")
        f.write(f"不同ID总数: {stats['total_ids']} 个\n\n")
        f.write("按{}排序的ID统计:\n".format("ID从小到大" if sort_by == 'id' else "数量从大到小"))
        
        # 根据排序方式排序
        if sort_by == 'id':
            sorted_items = sorted(stats['total_counts'].items(), key=lambda x: int(x[0]))
        else:
            sorted_items = sorted(stats['total_counts'].items(), key=lambda x: -x[1])
        
        for label, count in sorted_items:
            f.write(f"ID {label}: {count} 次\n")
        
        f.write("\n\n=== 按文件统计 ===\n")
        for file, counts in stats['file_counts'].items():
            f.write(f"\n文件: {file}\n")
            if sort_by == 'id':
                sorted_counts = sorted(counts.items(), key=lambda x: int(x[0]))
            else:
                sorted_counts = sorted(counts.items(), key=lambda x: -x[1])
            for label, count in sorted_counts:
                f.write(f"ID {label}: {count} 次\n")

def get_default_output_path(input_path):
    """生成默认的输出文件路径"""
    input_path = os.path.normpath(input_path)
    if os.path.isfile(input_path):
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        name, _ = os.path.splitext(base_name)
    else:
        dir_name = input_path
        name = os.path.basename(input_path)
    default_name = f"{name}_stat.txt"
    return os.path.join(dir_name, default_name)

def main():
    parser = argparse.ArgumentParser(description='统计TXT文件中的标签ID出现次数')
    parser.add_argument('input_path', help='输入文件或文件夹的路径')
    parser.add_argument('--output', help='输出文件路径（默认自动生成）')
    parser.add_argument('--sort-by', choices=['id', 'count'], default='id',
                        help='排序方式：id（按ID从小到大，默认）或 count（按数量从大到小）')
    parser.add_argument('--silent', action='store_true', help='不打印统计结果到控制台')
    parser.add_argument('--recurse', action='store_true', help='递归遍历子文件夹')
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print(f"路径不存在: {args.input_path}")
        return

    output_path = args.output if args.output else get_default_output_path(args.input_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    stats = statistic(args.input_path, recurse=args.recurse)
    if stats is None:
        return

    save_statistics(stats, output_path, args.sort_by)

    if not args.silent:
        print("\n=== 总体统计结果 ===")
        print(f"处理文件总数: {stats['total_files']} 个")
        print(f"总行数: {stats['total_lines']} 行")
        print(f"不同ID总数: {stats['total_ids']} 个")
        print(f"\n按{'ID从小到大' if args.sort_by == 'id' else '数量从大到小'}排序的ID统计:")
        
        # 根据排序方式排序
        if args.sort_by == 'id':
            sorted_items = sorted(stats['total_counts'].items(), key=lambda x: int(x[0]))
        else:
            sorted_items = sorted(stats['total_counts'].items(), key=lambda x: -x[1])
        
        for label, count in sorted_items:
            print(f"ID {label}: {count} 次")
        print(f"\n统计结果已保存至: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()

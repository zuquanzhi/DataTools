import os
import shutil
from tqdm import tqdm
import argparse

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='提取包含指定标签的图像和标注文件')
    parser.add_argument('--source', '-s', type=str, required=True,
                      help='源文件夹路径')
    parser.add_argument('--target', '-t', type=str, required=True,
                      help='目标文件夹路径')
    parser.add_argument('--labels', '-l', type=str, required=True,
                      help='要提取的标签，用逗号分隔(例如: 2,5,8)')
    parser.add_argument('--quiet', '-q', action='store_true',default=False,
                      help='安静模式，减少输出信息')
    return parser.parse_args()

def extract_and_copy_files(source_folder, target_folder, labels, quiet=False):
    """
    从源文件夹中提取包含指定标签的txt文件及其对应的图片文件到目标文件夹
    
    Args:
        source_folder: 源文件夹路径
        target_folder: 目标文件夹路径
        labels: 要提取的标签列表
        quiet: 是否启用安静模式
    """
    try:
        os.makedirs(target_folder, exist_ok=True)
        txt_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
        
        processed_count = 0
        skipped_count = 0
        
        if not quiet:
            print(f"开始处理文件...")
        
        for filename in tqdm(txt_files, desc="处理进度", disable=quiet):
            txt_path = os.path.join(source_folder, filename)
            
            try:
                with open(txt_path, 'r') as file:
                    lines = file.readlines()
                    has_target_label = any(line.strip().split()[0] in labels for line in lines)
                    
                    if has_target_label:
                        base_name = os.path.splitext(filename)[0]
                        image_found = False
                        
                        for ext in ['.jpg', '.png']:
                            image_filename = base_name + ext
                            image_path = os.path.join(source_folder, image_filename)
                            
                            if os.path.exists(image_path):
                                shutil.copy2(txt_path, os.path.join(target_folder, filename))
                                shutil.copy2(image_path, os.path.join(target_folder, image_filename))
                                processed_count += 1
                                image_found = True
                                break
                        
                        if not image_found and not quiet:
                            print(f"警告: 未找到对应的图片文件 {base_name}（.jpg 或 .png）")
                            skipped_count += 1
                            
            except Exception as e:
                if not quiet:
                    print(f"处理文件 {filename} 时出错: {str(e)}")
                skipped_count += 1
                continue
        
        if not quiet:
            print(f"\n处理完成!")
            print(f"成功处理: {processed_count} 对文件")
            print(f"跳过/失败: {skipped_count} 个文件")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False
    
    return True

def main():
    args = parse_args()
    labels = [label.strip() for label in args.labels.split(',')]
    
    if not os.path.exists(args.source):
        print("错误：源文件夹不存在！")
        return 1
        
    success = extract_and_copy_files(args.source, args.target, labels, args.quiet)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
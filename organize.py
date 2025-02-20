import os
import shutil
from pathlib import Path
import argparse

DATASET_STRUCTURES = {
    'split': {
        'description': '包含训练和验证集分割的结构 (images/train, images/val, labels/train, labels/val)',
        'dirs': ['images/train', 'images/val', 'labels/train', 'labels/val']
    },
    'simple': {
        'description': '简单的图像和标签结构 (images, labels)',
        'dirs': ['images', 'labels']
    },
    'flat': {
        'description': '扁平结构，所有文件在同一目录下',
        'dirs': ['.']
    }
}

def create_target_structure(target_dir, structure_type):
    """创建目标目录结构"""
    target_path = Path(target_dir)
    for dir_path in DATASET_STRUCTURES[structure_type]['dirs']:
        (target_path / dir_path).mkdir(parents=True, exist_ok=True)

def organize_dataset(source_dir, target_dir, mode='copy', structure_type='simple'):
    """
    整理数据集文件
    
    Args:
        source_dir (str): 源数据集目录
        target_dir (str): 目标目录
        mode (str): 'copy' 或 'move'，决定是复制还是移动文件
        structure_type (str): 目标数据集结构类型
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # 创建目标结构
    create_target_structure(target_dir, structure_type)
    
    # 分析源目录结构
    print("\n分析源目录结构...")
    has_split = any(d in ['train', 'val'] for d in os.listdir(source_dir) if Path(source_dir, d).is_dir())
    has_img_label = any(d in ['images', 'labels'] for d in os.listdir(source_dir) if Path(source_dir, d).is_dir())
    
    print(f"检测到的结构特征：")
    print(f"- 训练/验证集分割: {'是' if has_split else '否'}")
    print(f"- 图像/标签分离: {'是' if has_img_label else '否'}")
    
    def get_target_subdir(file_path):
        """确定文件的目标子目录"""
        rel_path = os.path.relpath(file_path, source_dir)
        parts = Path(rel_path).parts
        
        if structure_type == 'flat':
            return ''
        
        # 根据文件扩展名判断是图像还是标签
        is_image = Path(file_path).suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']
        base_dir = 'images' if is_image else 'labels'
        
        if structure_type == 'split':
            # 判断是否属于训练或验证集
            if 'train' in parts or 'val' in parts:
                split_type = 'train' if 'train' in parts else 'val'
                return f"{base_dir}/{split_type}"
            return f"{base_dir}/train"  # 默认放入训练集
        
        return base_dir

    # 处理文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            source_file = Path(root) / file
            target_subdir = get_target_subdir(source_file)
            target_file = target_path / target_subdir / file
            
            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                if mode == 'copy':
                    shutil.copy2(source_file, target_file)
                else:
                    shutil.move(str(source_file), str(target_file))
                print(f"{'复制' if mode == 'copy' else '移动'} {source_file} -> {target_file}")
            except Exception as e:
                print(f"处理文件 {source_file} 时出错: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='数据集整理工具')
    parser.add_argument('source_dir', help='源数据集目录')
    parser.add_argument('target_dir', help='目标目录')
    parser.add_argument('--mode', choices=['copy', 'move'], default='copy',help='操作模式: copy(复制) 或 move(移动)')
    parser.add_argument('--structure', choices=list(DATASET_STRUCTURES.keys()),default='simple', help='目标数据集结构类型')
    
    args = parser.parse_args()
    
    print("\n可用的数据集结构:")
    for key, value in DATASET_STRUCTURES.items():
        print(f"- {key}: {value['description']}")
    
    print(f"\n选择的结构: {args.structure}")
    print(f"开始{'复制' if args.mode == 'copy' else '移动'}数据集...")
    organize_dataset(args.source_dir, args.target_dir, args.mode, args.structure)
    print("\n完成！")

if __name__ == "__main__":
    main()
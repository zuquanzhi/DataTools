import cv2 as cv
import os
import numpy as np
from collections import deque
import argparse

def draw_annotations(img, annotations):
    """在图像上绘制标注"""
    img_copy = img.copy()
    
    for line in annotations:
        parts = line.strip().split()
        class_id = parts[0]
        coords = [float(x) for x in parts[1:]]
        
        points = [(int(coords[i] * img.shape[1]), int(coords[i+1] * img.shape[0])) 
                 for i in range(0, len(coords), 2)]
        
        for i in range(0, len(points), 4):
            quadrilateral = points[i:i+4]
            
            for j in range(len(quadrilateral) - 1):
                cv.line(img_copy, quadrilateral[j], quadrilateral[j+1], 
                       color=(0, 255, 0), thickness=1)
            
            if len(quadrilateral) == 4:
                cv.line(img_copy, quadrilateral[-1], quadrilateral[0], 
                       color=(0, 255, 0), thickness=1)
        
        for point in points:
            cv.circle(img_copy, point, 3, (255, 0, 0), -1)
        
        if len(points) >= 4:
            center = np.mean(points[:4], axis=0).astype(int)
            label_position = (center[0] + 10, center[1] - 10)
            cv.putText(img_copy, class_id, label_position, 
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
    
    return img_copy
import cv2 as cv
import os
import numpy as np
from collections import deque
import argparse

def load_image_and_annotations(image_path, label_path):
    """加载图像和标注"""
    img = cv.imread(image_path)
    if img is None:
        return None, None
    
    annotations = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            annotations = f.readlines()
    
    return img, annotations

def draw_annotations(img, annotations):
    """在图像上绘制标注"""
    # ...existing code...

def visualize_annotations(folder1, folder2):
    """
    同时显示两个文件夹中的同名图像及其标注，方便对比。
    支持方向键切换图片，按 q 退出。
    """
    # 获取两个文件夹中的图片文件
    image_files1 = [f for f in os.listdir(folder1) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    image_files2 = [f for f in os.listdir(folder2) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    # 获取两个文件夹共有的文件
    common_files = sorted(list(set(image_files1) & set(image_files2)))
    
    if not common_files:
        print("未找到两个文件夹中的共同图片文件。")
        return
    
    # 创建固定窗口
    window_title = "Image Comparison Viewer"
    cv.namedWindow(window_title, cv.WINDOW_NORMAL)
    
    # 设置窗口大小（双倍宽度）
    window_width, window_height = 2560, 720  # 双倍宽度
    cv.resizeWindow(window_title, window_width, window_height)
    
    # 初始化图像缓存
    cache_size = 3
    image_cache1 = {}
    image_cache2 = {}
    current_index = 0
    total_images = len(common_files)
    
    def preload_images(center_idx):
        """预加载两个文件夹中的图像"""
        indices = [(center_idx + i) % total_images for i in range(-1, 2)]
        for idx in indices:
            if idx not in image_cache1:
                image_file = common_files[idx]
                # 加载第一个文件夹的图像
                image_path1 = os.path.join(folder1, image_file)
                label_path1 = os.path.join(folder1, os.path.splitext(image_file)[0] + ".txt")
                img1, annot1 = load_image_and_annotations(image_path1, label_path1)
                if img1 is not None:
                    scale_factor = min(window_width/2 / img1.shape[1], window_height / img1.shape[0])
                    resized_img1 = cv.resize(img1, (int(img1.shape[1] * scale_factor), int(img1.shape[0] * scale_factor)))
                    image_cache1[idx] = (resized_img1, annot1, image_file)
                
            if idx not in image_cache2:
                image_file = common_files[idx]
                # 加载第二个文件夹的图像
                image_path2 = os.path.join(folder2, image_file)
                label_path2 = os.path.join(folder2, os.path.splitext(image_file)[0] + ".txt")
                img2, annot2 = load_image_and_annotations(image_path2, label_path2)
                if img2 is not None:
                    scale_factor = min(window_width/2 / img2.shape[1], window_height / img2.shape[0])
                    resized_img2 = cv.resize(img2, (int(img2.shape[1] * scale_factor), int(img2.shape[0] * scale_factor)))
                    image_cache2[idx] = (resized_img2, annot2, image_file)
        
        # 清理缓存
        for cache in [image_cache1, image_cache2]:
            keys = list(cache.keys())
            for k in keys:
                if k not in indices:
                    del cache[k]
    
    # 首次预加载
    preload_images(current_index)
    
    while True:
        if current_index in image_cache1 and current_index in image_cache2:
            img1, annotations1, image_file = image_cache1[current_index]
            img2, annotations2, image_file = image_cache2[current_index]
            
            # 绘制两幅图像的标注
            img_copy1 = draw_annotations(img1, annotations1) if annotations1 else img1.copy()
            img_copy2 = draw_annotations(img2, annotations2) if annotations2 else img2.copy()
            
            # 添加文件信息
            info_text = f"File: {image_file} ({current_index + 1}/{total_images})"
            for img in [img_copy1, img_copy2]:
                cv.putText(img, info_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 
                          0.7, (0, 255, 255), 2, cv.LINE_AA)
            
            # 添加文件夹路径信息
            cv.putText(img_copy1, f"Path: {folder1}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 
                      0.7, (0, 255, 255), 2, cv.LINE_AA)
            cv.putText(img_copy2, f"Path: {folder2}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 
                      0.7, (0, 255, 255), 2, cv.LINE_AA)
            
            # 合并图像
            combined_img = np.hstack((img_copy1, img_copy2))
            
            # 更新窗口标题
            cv.setWindowTitle(window_title, f"Compare: {image_file}")
            
            # 显示合并后的图像
            cv.imshow(window_title, combined_img)
        
        # 等待用户输入
        key = cv.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == 81 or key == ord('a'):  # 左方向键或'a'
            current_index = (current_index - 1) % total_images
            preload_images(current_index)
        elif key == 83 or key == ord('d'):  # 右方向键或'd'
            current_index = (current_index + 1) % total_images
            preload_images(current_index)
        elif key == 255:  # 没有按键
            continue
    
    cv.destroyWindow(window_title)

def parse_arguments():
    parser = argparse.ArgumentParser(description="数据集标注对比可视化工具")
    parser.add_argument("--folder1", type=str, required=True, help="第一个图像文件夹路径")
    parser.add_argument("--folder2", type=str, required=True, help="第二个图像文件夹路径")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    visualize_annotations(args.folder1, args.folder2)
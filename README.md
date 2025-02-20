# DataTools 数据处理工具集

一个用于处理和管理数据集的Python工具集合，提供多个实用功能。

## 🚀 主要功能

### 1. 数据集整理工具 (organize.py)
- **多种数据集结构支持**
  - `split`: 训练/验证集分割结构
    - 📁 images/train
    - 📁 images/val
    - 📁 labels/train
    - 📁 labels/val
  - `simple`: 简单的图像/标签结构
    - 📁 images
    - 📁 labels
  - `flat`: 扁平结构（单目录）

使用示例：
```bash
# 复制并组织为简单结构
python organize.py /源数据集路径 /目标路径

# 移动并组织为训练验证集结构
python organize.py /源数据集路径 /目标路径 --mode move --structure split
```

### 2. 标签统计工具 (statistic.py)
- ✨ 实时进度显示
- 📊 详细的文件级统计
- 📈 总体统计结果
- 🔄 支持按数量排序

使用示例：
```bash
python statistic.py /数据集路径
```

### 3. 批量重命名工具 (rename.py)
- 支持批量修改文件名中的数字
- 兼容多种文件格式：.txt、.jpg、.png
- 保持原有文件扩展名

使用示例：
```bash
python rename.py
# 根据提示输入要增加的数值
```

## 📦 安装

### 依赖安装
```bash
pip install tqdm
```

### 下载项目
```bash
git clone https://github.com/yourusername/DataTools.git
cd DataTools
```

## 📁 目录结构

```
DataTools/
├── README.md
├── organize.py    # 数据集整理工具
├── statistic.py   # 标签统计工具
└── rename.py      # 批量重命名工具
```

## ⚠️ 注意事项

1. 使用 rename.py 前请备份重要文件
2. organize.py 将自动创建目标目录结构
3. statistic.py 支持 UTF-8 编码的文本文件
4. 确保具有足够的磁盘空间和文件操作权限

## 🔧 常见问题解决

1. 文件权限问题
```bash
chmod +x *.py
```

2. 编码错误
```python
# 修改文件编码
with open(file_path, 'r', encoding='utf-8') as f:
    ...
```

## 🤝 贡献

欢迎提交问题和改进建议！

1. Fork 项目
2. 创建新分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解更多详情
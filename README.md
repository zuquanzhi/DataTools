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
- 🔄 支持多种排序方式

使用示例：
```bash
# 基本用法
python statistic.py /数据集路径

# 按数量从大到小排序
python statistic.py /数据集路径 --sort-by count

# 递归统计子文件夹
python statistic.py /数据集路径 --recurse

# 指定输出文件
python statistic.py /数据集路径 --output /输出路径/统计结果.txt

# 静默模式（不在控制台显示结果）
python statistic.py /数据集路径 --silent
```

输出示例：
```
=== 总体统计 ===
处理文件总数: 10 个
总行数: 1000 行
不同ID总数: 20 个

按ID从小到大排序的统计:
ID 0: 150 次
ID 1: 200 次
...
```

### 3. 批量重命名工具 (rename.py)
- 支持批量修改文件名中的数字
- 兼容多种文件格式：.txt、.jpg、.png
- 保持原有文件扩展名
- 交互式操作，安全可靠

使用示例：
```bash
python rename.py
输入要增加的数量：100
# 将把所有文件名中的数字增加100
# 例如：001.jpg → 101.jpg
```

## 📦 安装与配置

### 环境要求
- Python 3.6+
- Linux/Windows/MacOS

### 依赖安装
```bash
# 安装所需依赖
pip install tqdm

# 克隆项目
git clone https://github.com/yourusername/DataTools.git
cd DataTools

# 添加执行权限（Linux/MacOS）
chmod +x *.py
```

## 📁 目录结构

```
DataTools/
├── README.md          # 项目说明文档
├── organize.py        # 数据集整理工具
├── statistic.py       # 标签统计工具
├── rename.py          # 批量重命名工具
└── LICENSE           # 开源许可证
```

## ⚠️ 注意事项

1. 数据安全
   - 使用 rename.py 前请备份重要文件
   - organize.py 的 move 模式会移动原始文件

2. 文件编码
   - 所有工具默认使用 UTF-8 编码
   - 如遇编码问题，请确保文件为 UTF-8 格式

3. 系统要求
   - 确保具有足够的磁盘空间
   - 检查文件夹的读写权限

## 🔧 常见问题解决

1. 权限不足
```bash
# Linux/MacOS
chmod +x *.py
sudo chown -R $USER:$USER /目标目录
```

2. 编码错误
```python
# 使用其他编码打开文件
with open(file_path, 'r', encoding='gbk') as f:
    ...
```

3. 内存不足
   - 增大可用内存
   - 减少同时处理的文件数量

## 🤝 贡献

欢迎提交问题和改进建议！

1. Fork 项目
2. 创建新分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解更多详情
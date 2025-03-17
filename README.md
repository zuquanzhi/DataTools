# 🛠 DataTools 数据处理工具集

一个功能强大的数据集处理工具集合，专注于图像数据集的标注处理、视频对比和文件管理。

## 📚 功能模块

### 1. 📊 数据集整理工具 (organize.py)
组织和重构数据集文件结构，支持多种常用布局。

**支持的数据集结构：**
- 📁 `split`: 训练/验证集分割结构
  ```
  dataset/
  ├── images/
  │   ├── train/
  │   └── val/
  └── labels/
      ├── train/
      └── val/
  ```
- 📁 `simple`: 简单的图像/标签结构
  ```
  dataset/
  ├── images/
  └── labels/
  ```
- 📁 `flat`: 扁平结构（单目录）

**功能特点：**
- ✨ 自动识别源数据集结构
- 🔄 支持复制或移动模式
- 📋 保持原始文件关系
- 🚀 批量处理大规模数据集

**使用示例：**
```bash
# 基本用法 - 复制并组织为简单结构
python organize.py /源数据集路径 /目标路径

# 移动文件并组织为训练验证集结构
python organize.py /源数据集路径 /目标路径 --mode move --structure split

# 查看支持的结构类型
python organize.py --help
```

### 2. 📝 标注修改工具 (change.py)
批量修改标注文件中的标签数字。

**核心功能：**
- 🔄 支持复杂的数字映射关系
- 📑 自动创建备份文件
- 🌳 递归处理子文件夹
- 📊 详细的处理统计

**使用示例：**
```bash
# 修改标签 (23→32, 24→33)
python change.py --dir /数据集路径 --mapping "23:32,24:33"

# 不创建备份文件
python change.py --dir /数据集路径 --mapping "1:2" --no-backup

# 不处理子文件夹
python change.py --dir /数据集路径 --mapping "1:2" --no-recursive
```

### 3. 🔄 备份恢复工具 (backup.py)
管理和恢复文件备份。

**主要特性：**
- 🔍 自动查找备份文件
- 📂 支持递归恢复
- 🗑 可选是否删除备份
- 📊 详细的恢复报告

**使用示例：**
```bash
# 恢复备份文件
python backup.py --dir /数据集路径

# 恢复并删除备份
python backup.py --dir /数据集路径 --remove-backup

# 仅处理当前目录
python backup.py --dir /数据集路径 --no-recursive
```

### 4. 🎥 视频对比工具 (videocomparer.py)
实时对比两个视频的播放内容。

**功能亮点：**
- 🖥 并排显示两个视频
- ⏯ 丰富的播放控制
- 🎚 进度条跳转
- 🔍 帧信息显示

**键盘控制：**
- `空格`: 暂停/继续
- `←/→`: 前一帧/后一帧
- `A/D`: 反向/正向播放
- `1-9`: 跳转进度(10%-90%)
- `Q`: 退出程序

**使用示例：**
```bash
python videocomparer.py --video1 视频1.mp4 --video2 视频2.mp4
```

### 5. 📊 标签统计工具 (statistic.py)
分析标注文件中的标签分布情况。

**统计功能：**
- 📈 标签频率统计
- 📊 文件级别统计
- 🔄 多种排序方式
- 📑 导出统计报告

**使用示例：**
```bash
# 基本统计
python statistic.py /数据集路径

# 按数量排序并递归统计
python statistic.py /数据集路径 --sort-by count --recurse

# 导出统计结果
python statistic.py /数据集路径 --output 统计报告.txt --silent
```

### 6. 🔍 数据提取工具 (extract.py)
根据标签提取指定的图像和标注文件。

**核心功能：**
- 🎯 多标签筛选
- 🔄 自动匹配相关文件
- 📁 保持目录结构
- 📊 详细的处理报告

**使用示例：**
```bash
# 提取指定标签的数据
python extract.py --source /源目录 --target /目标目录 --labels "2,5,8"

# 安静模式
python extract.py -s /源目录 -t /目标目录 -l "1,2,3" --quiet
```

## 🔧 安装配置

### 系统要求
- 💻 Python 3.6+
- 🖥 OpenCV 4.0+
- 📦 NumPy
- 📊 tqdm

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/zuquanzhi/DataTools.git
cd DataTools
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 添加执行权限（Linux/MacOS）：
```bash
chmod +x *.py
```

## ⚠️ 注意事项

### 1. 数据安全
- 💾 重要操作前先备份数据
- ⚡ 大量文件处理时注意磁盘空间
- 🔒 检查文件权限设置

### 2. 性能优化
- 📊 分批处理大量文件
- 💻 监控内存使用情况
- 🚀 使用SSD可提升处理速度

### 3. 常见问题
- 🔓 权限不足：使用 `sudo` 或修改权限
- 📝 编码错误：确保使用UTF-8
- 💾 内存不足：减少批处理数量

## 🤝 参与贡献

欢迎提交问题和改进建议！

1. 🔀 Fork 项目
2. 📝 创建特性分支：`git checkout -b feature/新功能`
3. 💾 提交更改：`git commit -m '添加新功能'`
4. 📤 推送分支：`git push origin feature/新功能`
5. 📫 提交 Pull Request

## 📄 开源协议

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情
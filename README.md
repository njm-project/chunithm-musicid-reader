# CHUNITHM 数据导出工具集
## 📦 安装依赖
```bash 
pip install -r requirements.txt
```
## 🎵 musicid_exporter.py
### 功能
从XML文件提取：

- `dataName`
- `name/str`
- `乐曲版本信息`
### 使用示例
```bash
python musicid_exporter.py --data ".example/data" --option ".example/option"
```
## 🖼️ dds-reader.py
### 功能
转换 `DDS游戏文件`

### 使用示例
```bash
python dds-reader.py --data "./example/data" --option "./example/option"
```

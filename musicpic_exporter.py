import argparse
import os
import re
import subprocess
from pathlib import Path

def convert_dds_to_png(dds_path, output_dir, music_id):
    try:
        # 添加文件存在性检查
        if not os.path.exists(dds_path):
            print(f"文件不存在: {dds_path}")
            return False
            
        output_path = os.path.join(output_dir, f"music{music_id}.png")
        

        # 使用完整路径调用magick
        subprocess.run([
            'magick', 'convert',
            os.path.abspath(dds_path),
            '-flatten',
            '-alpha', 'off',
            os.path.abspath(output_path)
        ], check=True, stderr=subprocess.PIPE)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e.stderr.decode().strip()}")
    except Exception as e:
        print(f"未知错误: {str(e)}")
    return False

def process_jacket_files(base_dirs):
    jacket_dir = os.path.join(os.getcwd(), 'jacket')
    os.makedirs(jacket_dir, exist_ok=True)
    
    # 匹配CHU_UI_Jacket文件名的正则模式
    pattern = re.compile(r'CHU_UI_Jacket_(\d+)\.dds', re.IGNORECASE)
    
    processed = 0
    for base_dir in base_dirs:
        # 修改遍历路径为音乐数据根目录
        for root, _, files in os.walk(base_dir):
            for file in files:
                match = pattern.match(file)
                if match:
                    music_id = match.group(1)
                    dds_path = os.path.join(root, file)
                    print(f"发现曲绘文件：{dds_path}")  # 添加调试信息
                    
                    if convert_dds_to_png(dds_path, jacket_dir, music_id):
                        processed += 1
    return processed

def main():
    parser = argparse.ArgumentParser(description='CHUNITHM 曲绘导出工具')
    parser.add_argument('--data', required=True, help='主数据目录路径')
    parser.add_argument('--option', required=True, help='扩展数据目录路径')
    args = parser.parse_args()
    
    total = process_jacket_files([args.data, args.option])
    print(f"转换完成！共处理 {total} 张曲绘，保存在 {os.path.abspath('jacket')}")

if __name__ == '__main__':
    main()
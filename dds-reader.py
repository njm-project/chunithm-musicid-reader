import argparse
import os
import time
import imageio.v3 as iio
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description='DDS文件转换工具')
    parser.add_argument('--data', required=True, help='主数据目录路径')
    parser.add_argument('--option', required=True, help='扩展数据目录路径')
    return parser.parse_args()

def convert_dds_to_png(src_dirs, output_base):
    success = 0
    fail = 0
    start_time = time.time()
    
    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.lower().endswith('.dds'):
                    src_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, src_dir)
                    dest_dir = os.path.join(output_base, os.path.basename(src_dir), relative_path)
                    dest_path = os.path.join(dest_dir, f"{os.path.splitext(file)[0]}.png")

                    os.makedirs(dest_dir, exist_ok=True)
                    
                    try:
                        img = iio.imread(src_path)
                        iio.imwrite(dest_path, img)
                        success += 1
                    except Exception as e:
                        print(f"转换失败 {src_path}: {str(e)}")
                        fail += 1

    return success, fail, time.time() - start_time

def main():
    args = parse_arguments()
    output_dir = os.path.join(os.getcwd(), "convert")
    
    print("开始转换DDS文件...")
    success, fail, duration = convert_dds_to_png(
        [args.data, args.option],
        output_dir
    )
    
    print(f"\n转换完成！耗时 {duration:.2f} 秒")
    print(f"成功: {success} 个文件")
    print(f"失败: {fail} 个文件")
    print(f"输出目录: {output_dir}")

if __name__ == '__main__':
    main()
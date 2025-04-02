import argparse
import os
import xml.etree.ElementTree as ET
from openpyxl import Workbook

def parse_music_xml(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # 提取dataName并处理前缀
        data_name = root.find('./dataName').text
        music_id = data_name.replace('music', '') if data_name else ''
        
        # 定位name元素下的str（对应第18行内容）
        music_name = root.find('./name/str').text
        
        return music_id, music_name
    except Exception as e:
        print(f"解析失败 {filepath}: {str(e)}")
        return None, None

def main():
    parser = argparse.ArgumentParser(description='CHUNITHM Music ID 导出工具')
    parser.add_argument('--data', required=True, help='主数据目录路径')
    parser.add_argument('--option', required=True, help='扩展数据目录路径')
    args = parser.parse_args()

    wb = Workbook()
    ws = wb.active
    ws.append(['Music ID', 'Music Name'])

    # 遍历两个目录的所有music.xml
    for base_dir in [args.data, args.option]:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.lower() == 'music.xml':
                    xml_path = os.path.join(root, file)
                    music_id, music_name = parse_music_xml(xml_path)
                    
                    if music_id and music_name:
                        ws.append([music_id, music_name])

    output_file = os.path.join(os.getcwd(), 'music_list.xlsx')
    wb.save(output_file)
    print(f"导出完成！文件已保存至：{output_file}")

if __name__ == '__main__':
    main()
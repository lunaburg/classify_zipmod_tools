import os
import argparse
import struct
from io import BytesIO, IOBase
import zipfile
import xml.etree.ElementTree as ET
import shutil
from argparse import ArgumentParser
import csv
from BinaryReader import BinaryReader



class ZipmodSearcher:
    def __init__(self):
        self.mod_names = set() #依赖mod列表
        self.missing_mods =set() #缺失mod列表
        self.missing_abdata =set() #缺失abdata列表
        self.card_path = set()
        self.game_dir = "" #游戏目录
        self.input_dir = "" #png文件夹
        self.output_dir = "" #mods输出文件夹
    def set_game_dir(self,game_dir):
        self.game_dir = game_dir
    def set_input_dir(self,input_dir):
        self.input_dir = input_dir
    def set_output_dir(self,output_dir):
        self.output_dir = output_dir
    def set_dir(self,game_dir,input_dir,output_dir):
        self.set_game_dir(game_dir)
        self.set_input_dir(input_dir)
        self.set_output_dir(output_dir)
    
    def search_mods_with_files(self):#多文件搜索   
        if not os.path.isdir(self.game_dir):
            print(f"错误：{self.game_dir} 不是有效文件夹")    
        if not os.path.isdir(self.input_dir):
            print(f"错误：{self.input_dir} 不是有效文件夹")
        if not os.path.isdir(self.output_dir):
            self.output_dir = os.path.join(self.input_dir, "output")
            os.makedirs(self.output_dir, exist_ok=True)#输出人物卡文件路径
        self.mod_names ,self.missing_mods ,self.missing_abdata = self.search_for_mods(self.game_dir,self.input_dir,self.output_dir)



    def search_for_mods(self,game_dir,input_dir,output_dir):#game_dir:游戏目录，input_dir:png文件夹，output_dir:mods输出文件夹
        
        if not os.path.isdir(input_dir):
            print(f"错误：{input_dir} 不是有效文件夹")
        if not os.path.isdir(output_dir):
            print(f"错误：{output_dir} 不是有效文件夹")
        
        # 初始化路径
        out_mods_dir = os.path.join(output_dir, 'mods')#输出mod目录
        game_mods_dir = os.path.join(game_dir, 'mods')#游戏mod目录
        os.makedirs(out_mods_dir, exist_ok=True)

        mod_names = set()#依赖mod列表
        mod_names_backup = mod_names#备份mod列表
        png_dest_path = os.path.join(output_dir, "UserData\\chara\\female")
        os.makedirs(png_dest_path, exist_ok=True)#输出人物卡文件路径

        # 遍历所有PNG文件
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    if self.process_png(file_path, mod_names):#判断是否是AIS
                        dest_path = os.path.join(png_dest_path, file)
                        shutil.copy2(file_path, dest_path)#复制人物卡到输出文件夹

        # 查找所有zipmod文件
        zipmod_files = self.find_zipmod_files(game_mods_dir)

        # 处理每个zipmod文件
        for idx, zipmod_path in enumerate(zipmod_files, 1):
            print(f"正在处理文件 {idx}/{len(zipmod_files)}...", end='\r')
            self.process_zipmod(zipmod_path, mod_names, game_mods_dir, out_mods_dir)
        
        #缺失mod列表(guid)
        missing_mods=mod_names
        for idx, mod_name in enumerate(missing_mods, 1):
            print(f"{idx}/{len(missing_mods)}: {mod_name}")

        missing_abdata = self.search_for_missing_abdata(game_dir,output_dir)
        for idx, ab_path in enumerate(missing_abdata, 1):
            print(f"{idx}/{len(missing_abdata)}: {ab_path}")

        return mod_names_backup,missing_mods,missing_abdata


    def find_zipmod_files(self,game_mods_dir):
        """在mods目录及其子目录中查找所有zipmod文件"""
        zipmod_files = []
        for root, _, files in os.walk(game_mods_dir):
            for file in files:
                if file.lower().endswith('.zipmod'):
                    zipmod_files.append(os.path.join(root, file))
        return zipmod_files

    def process_zipmod(self,zipmod_path, mod_names, game_mods_dir, out_mods_dir):
        """处理单个zipmod文件"""
        try:
            with zipfile.ZipFile(zipmod_path, 'r') as zf:
                # 检查是否存在manifest.xml
                if 'manifest.xml' not in zf.namelist():
                    return
                
                # 读取并解析manifest.xml
                with zf.open('manifest.xml') as xml_file:
                    try:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        guid_element = root.find('guid')
                        
                        if guid_element is not None and guid_element.text:
                            guid = guid_element.text.strip()
                            
                            if guid in mod_names:
                                # 从集合中移除已找到的mod
                                mod_names.remove(guid)
                                
                                # 构建目标路径并复制文件
                                relative_path = os.path.relpath(zipmod_path, game_mods_dir)
                                target_path = os.path.join(out_mods_dir, relative_path)
                                
                                # 创建目标目录
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                
                                # 复制文件（保留元数据）
                                shutil.copy2(zipmod_path, target_path)
                                print(f"已复制: {relative_path}")
                    except ET.ParseError:
                        print(f"无法解析文件: {zipmod_path}")
        except zipfile.BadZipFile:
            print(f"损坏的zipmod文件: {zipmod_path}")
        except Exception as e:
            print(f"处理文件时发生错误 {zipmod_path}: {str(e)}")


    def parse_mod_data(self,card_bytes):
        """解析HS2的mod列表数据并自动去重"""
        mod_names = []
        seen_mods = set()
        mod_id_pattern = bytes([0x4D, 0x6F, 0x64, 0x49, 0x44])  # b'ModID'
        data = bytearray(card_bytes)
        position = 0
        data_length = len(data)
        pattern_length = len(mod_id_pattern)

        while position <= data_length - pattern_length:
            found = data.find(mod_id_pattern, position)
            if found == -1:
                break

            p = found + pattern_length
            if p >= data_length:
                break

            try:
                b = data[p]
                p += 1
            except IndexError:
                break

            if b < 0xC0:
                length = b - 0xA0
            else:
                if p >= data_length:
                    break
                length = data[p]
                p += 1

            if length <= 0 or p + length > data_length:
                break

            try:
                mod_str = bytes(data[p:p+length]).decode('utf-8')
                if mod_str not in seen_mods:
                    mod_names.append(mod_str)
                    seen_mods.add(mod_str)
            except UnicodeDecodeError:
                pass

            position = p + length

        return mod_names


    def search_AIS_card(self,input_dir):#更新png集合
        self.card_path.clear()
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    if self.judge_AIS_card(file_path):#判断是否是AIS
                        self.card_path.add(file_path)
        if len(self.card_path)==0:
            return False
        else:
            return True
    
    def judge_game_dir(self,game_dir):#判断是否是游戏目录
        """判断是否是游戏目录"""
        if not os.path.isdir(game_dir):
            print(f"错误：{game_dir} 不是有效文件夹")
            return False
        file_path = os.path.join(game_dir, "HoneySelect2.exe")
        if os.path.exists(file_path):
            return True
        else:
            return False

    def judge_AIS_card(self,file_path):#判断是否是人物卡
        """处理单个PNG文件"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            return
        iend_pos = data.find(b'IEND') - 4  # PNG块结构：长度(4字节)+类型(4字节)
        
        if iend_pos == -5:
            return
        
        # 计算图像数据结束位置（IEND块结尾）
        image_end = iend_pos + 8  # IEND块固定长度：4(type)+4(crc)
        
        card_data = data[image_end :]
        if len(card_data) < 100:
            return

        reader = BinaryReader(BytesIO(card_data))
        reader.read_bytes(8)
        #判断是否是AIS卡
        if (reader.read_string()!="【AIS_Chara】" and reader.read_string()!="【AIS_Clothes】"):
            return False
        else:
            return True


    def process_png(self,file_path, mod_set):#判断是否是人物卡，并添加mod依赖
        """处理单个PNG文件"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            return

        iend_pos = data.find(b'IEND') - 4  # PNG块结构：长度(4字节)+类型(4字节)
        
        if iend_pos == -5:
            return
        
        # 计算图像数据结束位置（IEND块结尾）
        image_end = iend_pos + 8  # IEND块固定长度：4(type)+4(crc)
        
        card_data = data[image_end :]
        if len(card_data) < 100:
            return

        reader = BinaryReader(BytesIO(card_data))
        reader.read_bytes(8)
        #判断是否是AIS卡
        if (reader.read_string()!="【AIS_Chara】" and reader.read_string()!="【AIS_Clothes】"):
            return False


        mod_list = self.parse_mod_data(card_data)
        mod_set.update(mod_list)

        return True



    def process_zipmod_abdata(self,zipmod_path,missing_abdata):
        """处理单个zipmod文件的AB数据并验证存在性"""
        abdata_list = set()
        
        try:
            with zipfile.ZipFile(zipmod_path, 'r') as zf:
                # 获取zipmod内所有文件的标准化路径集合
                zip_files = {
                    os.path.normpath(name).lower().replace('\\', '/') 
                    for name in zf.namelist()
                }
                
                # 筛选所有csv文件
                csv_files = [f for f in zf.namelist() if f.lower().endswith('.csv')]
                
                for csv_file in csv_files:
                    with zf.open(csv_file) as f:
                        reader = csv.reader(line.decode('utf-8-sig') for line in f)
                        
                        try:
                            # 读取前四行
                            rows = [next(reader) for _ in range(4)]
                        except StopIteration:
                            continue
                        
                        # 获取MainAB/ThumbAB列索引
                        header_row = rows[3] if len(rows) >=4 else []
                        target_columns = [
                            idx for idx, col in enumerate(header_row)
                            if col.strip() in {"MainAB", "ThumbAB"}
                        ]
                        
                        if not target_columns:
                            continue
                        
                        # 处理剩余行
                        for row in reader:
                            for col_idx in target_columns:
                                if col_idx < len(row):
                                    ab_value = row[col_idx].strip()
                                    if ab_value:
                                        abdata_list.add(ab_value)
                                        
                                        
        except Exception as e:
            print(f"处理文件 {zipmod_path} 时出错: {str(e)}")

        for ab_path in abdata_list:
            # 标准化AB路径
            normalized_ab = os.path.normpath(ab_path)
            normalized_ab = normalized_ab.replace('\\', '/').lower()
            # 检查路径存在性
            if not any(
                name.endswith(normalized_ab) 
                for name in zip_files
            ):
                missing_abdata.add(ab_path)



    def search_for_missing_abdata(self,game_dir,output_dir):#game_dir:游戏目录，output_dir:mods输出文件夹
        
        out_mods_dir = os.path.join(output_dir, 'mods')#输出mod目录
        #构建目录路径
        game_abdata_dir = os.path.join(game_dir, 'abdata')#游戏abdata目录
        out_abdata_dir = os.path.join(output_dir, 'abdata')#输出abbdata目录
        os.makedirs(out_abdata_dir, exist_ok=True)#创建abdata输出目录

        missing_abdata = set()#缺少的abdata路径

        # 遍历所有已复制的zipmod文件
        zipmod_files = self.find_zipmod_files(out_mods_dir)
        # 处理每个zipmod文件
        for idx, zipmod_path in enumerate(zipmod_files, 1):
            print(f"正在处理文件 {idx}/{len(zipmod_files)}...", end='\r')
            self.process_zipmod_abdata(zipmod_path,missing_abdata)


        not_found_abdata = set()#未找到的unity3d文件路径
        total = len(missing_abdata)
        current = 0
        for rel_path in missing_abdata.copy():  # 遍历副本避免修改问题
            current += 1
            print(f"处理进度: {current}/{total} | 当前文件: {rel_path}", end='\r')
            
            src_path = os.path.join(game_abdata_dir, rel_path)
            dest_path = os.path.join(out_abdata_dir, rel_path)

            if os.path.exists(src_path):
                try:
                    # 创建目标目录
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    # 复制文件并保留元数据
                    shutil.copy2(src_path, dest_path)
                except Exception as e:
                    print(f"\n复制失败 {rel_path}: {str(e)}")
            else:
                not_found_abdata.add(rel_path)
        
        return not_found_abdata




#search_for_mods("D:/Games/uw","test/input","test/output")




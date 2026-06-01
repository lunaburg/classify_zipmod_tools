import sys
import time
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextBrowser, QVBoxLayout, QWidget
from PySide6.QtCore import QRunnable, QThreadPool, QObject, Signal, Slot
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

# ==================== 任务信号发射器 ====================
class TaskSignals(QObject):
    progress = Signal(float)    # 进度信号
    progress_msg = Signal(str)
    result = Signal(object)   # 结果信号
    progress_title = Signal(str)
    error = Signal(Exception) # 错误信号

# ==================== 基础任务类 ====================
class BaseTask(QRunnable):
    def __init__(self, task_id, task_type, MainWindow):
        super().__init__()
        self.task_id = task_id
        self.task_type = task_type
        self.MainWindow = MainWindow
        self.signals = TaskSignals()
        self._is_canceled = False

    def run(self):
        try:
            if self._is_canceled:
                return
                
            # 模拟不同类型任务的处理逻辑
            if self.task_type == "search_cards":
                self.search_cards_task()
            elif self.task_type == "extract_mods":
                self.extract_mods_task()
            elif self.task_type == "sort_mods":
                self.sort_mods_task()
            else:
                raise ValueError("未知任务类型")

        except Exception as e:
            self.signals.error.emit(e)

    def cancel(self):
        self._is_canceled = True

    # ---------- 具体任务实现 ----------
    def search_cards_task(self):
        if self.MainWindow.ConfigDataList.input_dir == self.MainWindow.ui.lineEdit.text():
            return
        self.MainWindow.ConfigDataList.set_input_dir(self.MainWindow.ui.lineEdit.text())
        self.search_AIS_card(self.MainWindow.ConfigDataList.input_dir,self.MainWindow.ConfigDataList.card_path)
        self.signals.result.emit(f"在当前输入目录下共找到{len(self.MainWindow.ConfigDataList.card_path)}张人物卡")

    def extract_mods_task(self):
        if not os.path.isdir(self.MainWindow.ui.lineEdit_3.text()):
            self.signals.result.emit("未指定游戏路径")
            return
        else:
            if not self.judge_game_dir(self.MainWindow.ui.lineEdit_3.text()):
                self.signals.result.emit("该路径不是游戏路径")
                return 
        if not os.path.isdir(self.MainWindow.ui.lineEdit.text()):
            self.signals.result.emit("未指定输入目录")
            return
        else:
            if len(self.MainWindow.ConfigDataList.card_path) == 0:
                self.signals.result.emit("在输入目录下未找到人物卡")
                return
        if not os.path.isdir(self.MainWindow.ui.lineEdit_2.text()):
            self.signals.result.emit("未指定输出目录,将在输入目录下创建默认输出目录")
            output_dir = os.path.join(self.MainWindow.ui.lineEdit.text(), "output")
            os.makedirs(output_dir, exist_ok=True)#创建默认输出目录
            self.signals.result.emit(f"在输入目录下创建默认输出目录{output_dir}")
            self.MainWindow.ui.lineEdit_2.setText(output_dir)
            self.MainWindow.ConfigDataList.set_output_dir(output_dir)


        self.extract_mods(self.MainWindow.ConfigDataList.game_dir,self.MainWindow.ConfigDataList.card_path,self.MainWindow.ConfigDataList.output_dir)
            
        
       
    def sort_mods_task(self):
        pass    
    
   


    
    def extract_mods(self,game_dir,card_paths,output_dir):
        # 初始化路径
        output_mods_dir = os.path.join(output_dir, 'mods')#输出mod目录
        png_dest_path = os.path.join(output_dir, "UserData\\chara\\female")#r输出人物卡文件路径
        game_mods_dir = os.path.join(game_dir, 'mods')#游戏mod目录 

        os.makedirs(output_mods_dir, exist_ok=True)#创建mods目录
        os.makedirs(png_dest_path, exist_ok=True)#输出人物卡文件目录

        self.signals.progress_msg.emit("正在获取人物卡依赖mods-guid...")
        depend_mods_guids = self.get_depend_mods_guids(card_paths)#获取人物卡依赖mods-guid
        depend_mods_guids_backup = depend_mods_guids.copy()#拷贝人物卡依赖mods-guid副本
        
        self.signals.progress_msg.emit("正在拷贝人物卡到输出目录...")
        self.copy_cards_to_female(card_paths, png_dest_path)#拷贝人物卡至输出目录

        self.signals.progress_msg.emit("正在提取依赖mods路径...")
        zipmod_files = self.find_zipmod_files(game_mods_dir)#获取mods目录下的zipmod文件
        depend_mods_paths = self.get_depend_mods_paths(depend_mods_guids, zipmod_files)#获取人物卡依赖mods-guid对应的mods路径

        self.signals.progress_msg.emit("正在拷贝依赖mods到输出目录...")
        self.copy_depend_mods_to_output(depend_mods_paths, game_mods_dir,output_mods_dir)#拷贝mods到输出目录

        missing_mods_guids = depend_mods_guids #缺失的依赖mod-guid

        self.signals.progress_msg.emit("正在搜索缺失的unity3d文件...")
        missing_abdata = self.search_for_missing_abdata(game_dir,output_dir)#缺失的unity3d文件

        self.signals.result.emit(f"mods提取完成")

        
    def get_depend_mods_guids(self, card_paths):#获取人物卡依赖mods-guid
        self.signals.progress_title.emit("获取依赖mods-guid")
        tolal_cards = len(card_paths)
        card_count = 0
        depend_mod_guids = set()
        for card_path in card_paths:
            card_count += 1
            self.signals.progress.emit(card_count / tolal_cards * 100)
            self.process_png(card_path, depend_mod_guids)
        self.signals.result.emit(f"人物卡所需mod数量:{len(depend_mod_guids)}")
        return depend_mod_guids
    def get_depend_mods_paths(self,depend_mod_guids,zipmod_files):#获取依赖的mods路径
        self.signals.progress_title.emit("获取依赖mods路径")
        total_files = len(zipmod_files)
        file_count = 0
        depend_mod_paths = set()
        for zipmod_path in zipmod_files:
            file_count += 1
            self.signals.progress.emit(file_count / total_files * 100)
            self.add_depend_mod_path(zipmod_path, depend_mod_guids, depend_mod_paths)
        self.signals.result.emit(f"一共找到{len(depend_mod_paths)}个mod")
        return depend_mod_paths
            

    def copy_cards_to_female(self, card_paths,dest_dir):
        self.signals.progress_title.emit("拷贝人物卡")
        total_cards = len(card_paths)
        card_count = 0
        for card_path in card_paths:
            card_count += 1
            self.signals.progress.emit(card_count / total_cards * 100)
            shutil.copy2(card_path, dest_dir)
        self.signals.result.emit(f"拷贝{len(card_paths)}张人物卡至输出目录")

    def copy_depend_mods_to_output(self,depend_mod_paths,game_mods_dir,output_mods_dir):
        self.signals.progress_title.emit("拷贝依赖mods")
        total_files = len(depend_mod_paths)
        file_count = 0
        for depend_mod_path in depend_mod_paths:
            file_count += 1
            self.signals.progress.emit(file_count / total_files * 100)
            relative_path = os.path.relpath(depend_mod_path, game_mods_dir)
            target_path = os.path.join(output_mods_dir, relative_path)
            target_dir = os.path.dirname(target_path)
            # 创建目标目录
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制文件（保留元数据）
            shutil.move(depend_mod_path, target_dir)
        self.signals.result.emit(f"拷贝{len(depend_mod_paths)}个mods至输出目录")

    def add_depend_mod_path(self,zipmod_path,depend_mod_guids, depend_mod_paths):#添加依赖mod路径
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
                            
                            if guid in depend_mod_guids:
                                # 从集合中移除已找到的mod
                                depend_mod_guids.remove(guid)
                                depend_mod_paths.add(zipmod_path)
                    except ET.ParseError:
                        print(f"无法解析文件: {zipmod_path}")
        except zipfile.BadZipFile:
            print(f"损坏的zipmod文件: {zipmod_path}")
        except Exception as e:
            print(f"处理文件时发生错误 {zipmod_path}: {str(e)}")
        

    #工具函数
    def find_zipmod_files(self,game_mods_dir):
        """在mods目录及其子目录中查找所有zipmod文件"""
        zipmod_files = []
        for root, _, files in os.walk(game_mods_dir):
            for file in files:
                if file.lower().endswith('.zipmod'):
                    zipmod_files.append(os.path.join(root, file))
        return zipmod_files
             
  

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


    def serach_all_file_paths(self,path):#收集路径下所有文件的路径
        file_paths = set()
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.add(file_path)
        return file_paths

    def search_AIS_card(self,input_dir,card_paths):#更新png集合 
        self.signals.progress_title.emit("搜索人物卡")

        card_paths.clear()
        file_paths = self.serach_all_file_paths(input_dir)
        file_count = 0
        total_files = len(file_paths) 


        for file_path in file_paths:
            file_count += 1
            self.signals.progress.emit((file_count/total_files)*100)
            if file_path.lower().endswith('.png'):
                if self.judge_AIS_card(file_path):#判断是否是AIS
                    card_paths.add(file_path)
        if len(card_paths)==0:
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

    def get_manifest_value(self,zipmod_path,param_name):
        """获取zipmod的manifest.xml中指定参数的值"""
        try:
            with zipfile.ZipFile(zipmod_path, 'r') as zf:
                # 检查是否存在manifest.xml
                if 'manifest.xml' not in zf.namelist():
                    return "[E]no_manifest"
                # 读取并解析manifest.xml
                with zf.open('manifest.xml') as xml_file:
                    try:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        param_element = root.find(param_name)
                        
                        if param_element is not None and param_element.text:
                            param = param_element.text.strip()
                            return param
                        return "[E]no_value"
                            
                    except ET.ParseError:
                        print(f"无法解析文件: {zipmod_path}")
        except zipfile.BadZipFile:
            print(f"损坏的zipmod文件: {zipmod_path}")
            return "[E]corrupted"
        except Exception as e:
            print(f"处理文件时发生错误 {zipmod_path}: {str(e)}")
            return "[E]other_error"
       

    def find_missing_unity3d_paths(self,out_mods_dir):
        missing_unity3d_paths = set()
        # 遍历所有已复制的zipmod文件
        zipmod_files = self.find_zipmod_files(out_mods_dir)
        # 处理每个zipmod文件
        for zipmod_path in zipmod_files:
            self.process_zipmod_abdata(zipmod_path,missing_unity3d_paths)
        return missing_unity3d_paths


    def search_for_missing_abdata(self,game_dir,output_dir):#game_dir:游戏目录，output_dir:mods输出文件夹
        
        self.signals.progress_title.emit("搜索缺失unity3d")
        out_mods_dir = os.path.join(output_dir, 'mods')#输出mod目录
        #构建目录路径
        game_abdata_dir = os.path.join(game_dir, 'abdata')#游戏abdata目录
        out_abdata_dir = os.path.join(output_dir, 'abdata')#输出abbdata目录
        os.makedirs(out_abdata_dir, exist_ok=True)#创建abdata输出目录

        missing_abdata = self.find_missing_unity3d_paths(out_mods_dir)

        not_found_abdata = set()#未找到的unity3d文件路径
        total = len(missing_abdata)
        count = 0
        for rel_path in missing_abdata.copy():  # 遍历副本避免修改问题
            count += 1
            self.signals.progress.emit(count/total*100)
            
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

    def sort_mods(self,input_dir,output_dir,delete_empty):
        zipmod_files = self.find_zipmod_files(input_dir)

        sort_dir = os.path.join(output_dir, 'sort')
        error_dir = os.path.join(output_dir, 'error')
        error_subdirs = {
            'corrupted': os.path.join(error_dir, 'corrupted'),
            'no_manifest': os.path.join(error_dir, 'no_manifest'),
            'other_error': os.path.join(error_dir, 'other_error'),
            'no_author': os.path.join(error_dir, 'no_author'),
        }

        os.makedirs(sort_dir, exist_ok=True)
        os.makedirs(error_dir, exist_ok=True)
        for subdir in error_subdirs.values():
            os.makedirs(subdir, exist_ok=True)

        total_files = len(zipmod_files)
        file_count = 0


        # 使用进度条处理文件

        for zipmod_file in zipmod_files:
            file_count += 1
            self.signals.progress.emit(file_count/total_files*100)
            self.sort_signal_zipmod(zipmod_file, sort_dir, error_subdirs)

        if delete_empty:
            exclude = [sort_dir, error_dir]
            remove_empty_dirs(input_dir, exclude)
    
    def sort_signal_zipmod(self,zipmod_path, sort_dir, error_dirs):
        author = self.get_manifest_value(zipmod_path,'author')
        if author == "[E]no_manifest":
            safe_move(zipmod_path, error_dirs['no_manifest'])
            return
        elif author == "[E]no_value":
            safe_move(zipmod_path, error_dirs['no_author'])
            return
        elif author == "[E]corrupted":
            safe_move(zipmod_path, error_dirs['corrupted'])
            return
        elif author == "[E]other_error":
            safe_move(zipmod_path, error_dirs['other_error'])
            return
        else:
            target_dir = os.path.join(sort_dir, author)
            os.makedirs(target_dir, exist_ok=True)
            name = self.get_manifest_value(zipmod_path,'name')
            if name == "[E]no_value":
                name = None
            dest_path = self.generate_new_filename(target_dir, author, name)
            shutil.move(zipmod_path, dest_path)
        
    def generate_new_filename(self,target_dir, author, name):
        """生成符合规则的文件名并处理冲突"""
        if name:
            base_name = f"[{author}]_{name}"
            new_filename = f"{base_name}.zipmod"
            dest_path = os.path.join(target_dir, new_filename)
            counter = 1
            
            while os.path.exists(dest_path):
                new_filename = f"{base_name}_{counter}.zipmod"
                dest_path = os.path.join(target_dir, new_filename)
                counter += 1
        else:
            base = f"[{author}]_Noname"
            pattern = re.compile(re.escape(base) + r'(\d+)\.zipmod$')
            max_num = 0
            
            for filename in os.listdir(target_dir):
                match = pattern.match(filename)
                if match:
                    try:
                        num = int(match.group(1))
                        max_num = max(max_num, num)
                    except ValueError:
                        pass
            
            new_num = max_num + 1
            new_filename = f"{base}{new_num}.zipmod"
            dest_path = os.path.join(target_dir, new_filename)
            
            while os.path.exists(dest_path):
                new_num += 1
                new_filename = f"{base}{new_num}.zipmod"
                dest_path = os.path.join(target_dir, new_filename)
        
        return dest_path

    def remove_empty_dirs(root_dir, exclude_dirs):
        """删除所有空文件夹（排除指定目录）"""
        exclude_abs = [os.path.abspath(d) for d in exclude_dirs]
        
        for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
            current_abs = os.path.abspath(dirpath)
            
            if any(current_abs == ex or current_abs.startswith(ex + os.sep) for ex in exclude_abs):
                continue
            
            if not os.listdir(dirpath):
                try:
                    os.rmdir(dirpath)
                    print(f"删除空目录: {dirpath}")
                except OSError as e:
                    print(f"删除失败 {dirpath}: {e.strerror}")
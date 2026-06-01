

def safe_move(src, dst_dir):
    """安全移动文件，避免覆盖目标目录中的同名文件"""
    filename = os.path.basename(src)
    base, ext = os.path.splitext(filename)
    counter = 1
    dest_path = os.path.join(dst_dir, filename)
    while os.path.exists(dest_path):
        dest_path = os.path.join(dst_dir, f"{base}_{counter}{ext}")
        counter += 1
    shutil.move(src, dest_path)
    return dest_path

def generate_new_filename(target_dir, author, name):
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

 def process_zipmod(file_path, sort_dir, error_dirs):
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'manifest.xml' not in zf.namelist():
                safe_move(file_path, error_dirs['no_manifest'])
                return
            try:
                manifest_data = zf.read('manifest.xml')
            except Exception:
                safe_move(file_path, error_dirs['corrupted'])
                return
    except (zipfile.BadZipFile, Exception):
        safe_move(file_path, error_dirs['corrupted'])
        return

    try:
        xml_str = manifest_data.decode('utf-8')
    except UnicodeDecodeError:
        try:
            xml_str = manifest_data.decode('gbk')
        except UnicodeDecodeError:
            safe_move(file_path, error_dirs['invalid_xml'])
            return

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError:
        safe_move(file_path, error_dirs['invalid_xml'])
        return

    author_elements = root.findall('.//author')
    if not author_elements or not author_elements[0].text:
        safe_move(file_path, error_dirs['no_author'])
        return
    author = author_elements[0].text.strip()

    name = None
    name_elements = root.findall('.//name')
    if name_elements and name_elements[0].text:
        name = name_elements[0].text.strip()

    target_dir = os.path.join(sort_dir, author)
    os.makedirs(target_dir, exist_ok=True)

    try:
        dest_path = generate_new_filename(target_dir, author, name)
        shutil.move(file_path, dest_path)
    except Exception as e:
        safe_move(file_path, error_dirs['corrupted'])

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='根据manifest.xml分类并重命名.zipmod文件')
    parser.add_argument('directory', help='输入目录路径')
    parser.add_argument('-d', '--delete-empty', action='store_true',
                      help='处理完成后删除所有空文件夹')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误：目录不存在 '{args.directory}'")
        exit(1)

    main(args.directory, args.delete_empty)
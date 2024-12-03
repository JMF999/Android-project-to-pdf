import os
import time
from fpdf import FPDF, XPos, YPos


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # 添加中文字体
        self.add_font("NotoSansSC", style="", fname="NotoSansSC-Regular.ttf")
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # 设置页眉
        self.set_font("NotoSansSC", size=12)
        self.cell(0, 10, "Android Project Report", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

    def chapter_title(self, title):
        # 设置章节标题
        self.set_font("NotoSansSC", size=12)
        self.cell(0, 10, title, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        self.ln(5)

    def chapter_body(self, text, line_height=4):
        # 添加章节内容
        self.set_font("NotoSansSC", size=10)
        self.multi_cell(0, line_height, text)
        self.ln()

    def add_header_info(self, project_path):
        """在首页添加时间和项目信息"""
        self.set_font("NotoSansSC", size=10)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 10, f"Generated on: {current_time}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.cell(0, 10, f"Project Path: {project_path}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(10)


def is_valid_file(file_path):
    """
    判断文件是否为安卓项目的重要文件
    """
    include_extensions = [
        ".java", ".kt",                  # 源代码文件
        ".gradle", ".gradle.kts",        # 构建脚本
        ".properties", ".pro",           # 配置文件
        ".xml",                          # 资源文件
        "AndroidManifest.xml"            # 应用程序清单
    ]
    exclude_patterns = [
        "build/", "bin/", ".idea/", ".gradle/", "__pycache__/", "node_modules/"
    ]

    # 排除无用目录和文件
    if any(pattern in file_path.replace("\\", "/") for pattern in exclude_patterns):
        return False

    # 包含特定扩展名的文件
    return any(file_path.endswith(ext) for ext in include_extensions)


def scan_directory(target_dir, extensions=None):
    """
    扫描目标目录，返回符合条件的文件列表
    :param target_dir: 要扫描的目录路径
    :param extensions: 要筛选的文件扩展名（如 `.xml`）
    :return: 文件路径列表
    """
    if not os.path.exists(target_dir):
        return []

    matched_files = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
            matched_files.append(os.path.join(root, file))
    return matched_files


def read_file(file_path):
    """
    读取文件内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


def android_project_to_pdf(project_path):
    """
    主程序：将安卓项目转化为 PDF
    """
    output_pdf = os.path.join(project_path, "ProjectReport.pdf")

    # 如果文件存在，删除以便替换
    if os.path.exists(output_pdf):
        os.remove(output_pdf)

    pdf = PDF()
    pdf.add_page()

    # 添加项目信息
    pdf.add_header_info(project_path)

    # 写入项目结构目录
    pdf.chapter_title("Project Directory Structure")
    project_structure = []
    file_count = 0

    # 专门检查 layout 目录下的文件
    layout_dir = os.path.join(project_path, "app", "src", "main", "res", "layout")
    layout_files = scan_directory(layout_dir, extensions=[".xml"])
    if layout_files:
        print(f"Found {len(layout_files)} layout files in {layout_dir}")

    # 遍历整个项目目录
    for root, dirs, files in os.walk(project_path):
        # 跳过无关目录
        dirs[:] = [d for d in dirs if not any(skip in d for skip in ["build", ".idea", "__pycache__", "node_modules"])]
        for file in files:
            file_path = os.path.join(root, file)
            if is_valid_file(file_path):
                relative_path = os.path.relpath(file_path, project_path)
                # 避免重复记录 layout 文件
                if file_path not in layout_files:
                    project_structure.append(relative_path)
                    file_count += 1

    # 将 layout 文件加入结构目录
    project_structure.extend([os.path.relpath(f, project_path) for f in layout_files])

    # 写入目录结构
    for item in project_structure:
        pdf.chapter_body(f"{item}", line_height=4)

    # 写入所有文件内容
    pdf.add_page()
    pdf.chapter_title("Main Files Content")
    for file_path in project_structure:
        full_path = os.path.join(project_path, file_path)
        content = read_file(full_path)
        pdf.chapter_title(f"File: {file_path}")
        pdf.chapter_body(content, line_height=4)

    # 输出 PDF
    pdf.output(output_pdf)
    print(f"PDF saved at {output_pdf}. Processed {file_count + len(layout_files)} files.")


if __name__ == "__main__":
    project_directory = input("Enter the Android project directory path: ")
    android_project_to_pdf(project_directory)

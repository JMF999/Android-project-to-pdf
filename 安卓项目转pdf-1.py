import os
import time
from fpdf import FPDF, XPos, YPos

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # 使用静态字体文件
        self.add_font("NotoSansSC", style="", fname="NotoSansSC-Regular.ttf")
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("NotoSansSC", size=12)
        self.cell(0, 10, "Android Project Report", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

    def chapter_title(self, title):
        self.set_font("NotoSansSC", size=12)
        self.cell(0, 10, title, new_x=XPos.LEFT, new_y=YPos.NEXT, align="L")
        self.ln(5)

    def chapter_body(self, text, line_height=4):
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

def is_main_file(file_name):
    """选择安卓项目中的必要文件类型"""
    main_file_types = [
        ".java", ".kt",                  # 源代码文件
        ".xml", ".xml.kts",              # 布局文件（XML 和 Kotlin DSL XML）
        ".gradle", ".gradle.kts",        # 构建脚本（Gradle 和 Kotlin DSL）
        ".properties",                   # 配置文件
        ".pro",                          # ProGuard 配置文件
        "AndroidManifest.xml"            # 应用程序清单
    ]
    return any(file_name.endswith(ext) for ext in main_file_types)

def should_skip_directory(directory_name):
    """跳过编译输出和无关文件夹"""
    skip_dirs = [
        "build", "bin", ".gradle", ".idea", "out",  # 编译输出
        "__pycache__", "node_modules"             # 临时目录
    ]
    return any(directory_name.endswith(skip) for skip in skip_dirs)

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def android_project_to_pdf(project_path):
    # 设置输出文件路径
    output_pdf = os.path.join(project_path, "ProjectReport.pdf")
    
    # 如果文件存在，删除以便替换
    if os.path.exists(output_pdf):
        os.remove(output_pdf)

    pdf = PDF()
    pdf.add_page()

    # 添加项目的头部信息
    pdf.add_header_info(project_path)

    # 写入项目结构目录
    pdf.chapter_title("Project Directory Structure")
    project_structure = []
    file_count = 0

    for root, dirs, files in os.walk(project_path):
        # 跳过无关目录
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]
        for file in files:
            if is_main_file(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                project_structure.append(relative_path)
                file_count += 1

    # 写入目录结构
    for item in project_structure:
        pdf.chapter_body(f"{item}", line_height=4)

    # 写入各文件内容
    pdf.add_page()
    pdf.chapter_title("Main Files Content")
    for file_path in project_structure:
        full_path = os.path.join(project_path, file_path)
        content = read_file(full_path)
        pdf.chapter_title(f"File: {file_path}")
        pdf.chapter_body(content, line_height=4)

    # 输出 PDF
    pdf.output(output_pdf)
    print(f"PDF saved at {output_pdf}. Processed {file_count} files.")

if __name__ == "__main__":
    project_directory = input("Enter the Android project directory path: ")
    android_project_to_pdf(project_directory)

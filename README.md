# 安卓项目转PDF工具

## 项目简介

本项目是一个将安卓项目文件结构和内容转化为 PDF 的工具，旨在便于项目的归档和共享，特别适用于与人工智能（如 ChatGPT）协作分析项目时提供全面的上下文支持。

通过此工具，您可以快速生成一个 PDF 文件，其中包含安卓项目的目录结构和关键文件的内容，为代码审查、问题诊断和文档化提供便利。

---

## 功能特点

- **支持安卓项目的重点文件筛选**：
  - 包括 `.java`、`.kt` 源代码文件，`AndroidManifest.xml` 应用清单文件，`layout` 等目录中的 `.xml` 文件，以及 Gradle 构建脚本。
  
- **自动处理项目的目录结构**：
  - 扫描整个项目，过滤无关目录（如 `build/`、`.idea/`）和临时文件。

- **灵活的目录检查**：
  - 自动检测并处理 `res/layout` 目录中的所有 `.xml` 文件，确保布局文件不会遗漏。

- **一键生成 PDF**：
  - 生成的 PDF 文件包括项目结构和每个关键文件的完整内容，便于归档和分析。

---

## 使用方法

1. **安装依赖**：
   - 确保已安装 Python 3，并通过 `pip` 安装以下依赖库：
     ```bash
     pip install fpdf
     ```
2. **确保您同时下载了项目中包含的字体文件**
   - 项目中包含了多个版本py文件，其实没有区别，建议使用第三版。
   - 第一版测试过程不知道为什么总是缺少activity_main.xml文件。
   
4. **运行脚本**：
   - 在命令行中运行脚本，输入安卓项目的根目录路径：
     ```bash
     python android_project_to_pdf.py
     ```
   - 生成的 PDF 文件将保存在项目根目录下，命名为 `ProjectReport.pdf`。

5. **查看 PDF**：
   - 打开生成的 PDF 文件，查看项目的目录结构和文件内容。

---

## 注意事项

1. **文件过滤规则**：
   - 工具会自动忽略如 `build/` 和 `.idea/` 等生成目录，确保 PDF 只包含有意义的项目文件。
   
2. **文件大小限制**：
   - 对于过大的项目，PDF 文件可能较大，请确保存储空间充足。

3. **布局文件自动处理**：
   - 默认扫描 `res/layout` 目录下的所有 `.xml` 文件，如果布局文件名不是 `activity_main.xml`，也能被正确处理。
     
4. **字体文件**：
   - 项目中包含了程序运行所需的字体文件，需要放置在程序同一目录下。

5. **项目中包含了多个版本py文件**
   - 其实没有区别，建议使用第三版，第一版不知道为什么总是缺少layout目录下activity_main.xml文件，水平有限没检查出来问题。

6. **本程序全部由ChatGPT-4o完成** 
---

## 示例输出

注意：PDF会输出到在程序刚开始运行时，您输入的指定项目目录下，名为ProjectReport.pdf

生成的 PDF 文件示例包含以下内容：
1. 创建时间(Generated on: 2024-12-04 01:24:47)
2. 项目地址(Project Path: D:\... )
3. 主要文件目录(Project Directory Structure)
4. 具体文件内容(Main Files Content)

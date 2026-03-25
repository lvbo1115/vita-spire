#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 转 Hugo Markdown 产品文件生成器
- Cat. → 文件名
- Class ID → 二级分类（子目录）
- Sheet 名称 → 一级分类（主目录）
用法：python excel_to_hugo.py products.xlsx
"""

import pandas as pd
import os
import re
import argparse
from pathlib import Path

# ============ 配置区域 ============
EXCEL_FILE = "products.xlsx"
OUTPUT_ROOT = "content/products"

# Sheet 名称 → 一级分类目录映射（根据 hugo.toml 菜单配置）
SHEET_TO_CATEGORY = {
    "Biomedical & Health Materials": "biomedical-health-materials",
    "Human Nutrition Solutions": "human-nutrition-solutions",
    "Advanced Industrial Materials": "advanced-industrial-materials",
    # 如果 sheet 名称不同，请在这里修改
}

# Excel 列名 → Hugo Front Matter 字段名映射
FIELD_MAPPING = {
    "Product Name": "title",
    "Background": "background",
    "Product Description": "product_description",
    "Morphology & Appearance": "morphology_appearance",
    "Purity": "purity",
    "Thickness": "thickness",
    "Diameter": "diameter",
    "Length": "length",
    "Layer": "layer",
    "Surface Area": "surface_area",
    "Particle Size": "particle_size",
    "Product Size": "product_size",
    "Manufacture Method": "manufacture_method",
    "Viscosity": "viscosity",
    "Molecular weight": "molecular_weight",
    "Tap Density": "tap_density",
    "CAS Number": "cas_number",
    "Key Components": "key_components",
    "Impurities": "impurities",
    "Source": "source",
    "Solubility": "solubility",
    "Storage": "storage",
    "Concentration": "concentration",
    "Shipping & Packaging": "shipping_packaging",
    "Application": "application",
    "Usage": "usage",
    "Warning": "warning",
    "References": "references",
    "Images": "images",
    "Images2": "images2",
    "Keywords": "keywords",
    "Cat.": "cat",  # 产品编号也写入 Front Matter
}

# 需要保留换行的字段（使用 YAML 的 | 符号）
MULTILINE_FIELDS = ["background", "product_description", "application", "usage", "warning", "references"]

# ============ 工具函数 ============

def slugify(text):
    """将文本转换为安全的目录/文件名"""
    if not text:
        return "untitled"
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def clean_value(value):
    """清理值，返回 None 如果是空的"""
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value == "" or value.lower() in ["nan", "none", "null"]:
        return None
    return value

def format_yaml_value(key, value):
    """格式化 YAML 值，处理多行文本和特殊字符"""
    if not value:
        return None
    
    # 多行文本使用 | 符号
    if key in MULTILINE_FIELDS and '\n' in value:
        lines = value.split('\n')
        formatted = "|\n" + "\n".join([f"  {line}" for line in lines])
        return formatted
    # 包含特殊字符的使用引号
    elif any(c in value for c in [':', '#', '[', ']', '{', '}', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '\\']):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    else:
        return f'"{value}"'

def generate_front_matter(row):
    """生成 Front Matter，只包含非空字段"""
    lines = ["---"]
    
    for excel_col, hugo_field in FIELD_MAPPING.items():
        if excel_col in row:
            value = clean_value(row[excel_col])
            if value:  # 只添加非空值
                formatted = format_yaml_value(hugo_field, value)
                if formatted:
                    lines.append(f"{hugo_field}: {formatted}")
    
    lines.append("---")
    return "\n".join(lines)

def generate_filename(row):
    """使用 Cat. 列的值生成文件名"""
    cat_value = clean_value(row.get("Cat.", ""))
    if cat_value:
        # 直接使用 Cat. 值，如 "PC-ADV-002.md"
        return f"{cat_value}.md"
    
    # 如果没有 Cat.，使用 Product Name
    product_name = clean_value(row.get("Product Name", ""))
    if product_name:
        return f"{slugify(product_name)}.md"
    
    return "untitled.md"

def get_output_path(row, sheet_name):
    """
    构建输出路径：
    content/products/{一级分类}/{Class ID}/
    """
    # 一级分类：从 Sheet 名称映射
    main_category = SHEET_TO_CATEGORY.get(sheet_name, slugify(sheet_name))
    
    # 二级分类：从 Class ID 列获取
    class_id = clean_value(row.get("Class ID", ""))
    
    # 构建路径
    if class_id:
        # 将 Class ID 转换为 slug 格式（如 "Electronic Materials" → "electronic-materials"）
        sub_category = slugify(class_id)
        return Path(OUTPUT_ROOT) / main_category / sub_category
    else:
        # 如果没有 Class ID，直接放在主分类下
        return Path(OUTPUT_ROOT) / main_category

def process_sheet(df, sheet_name):
    """处理单个 sheet"""
    print(f"\n📊 处理 Sheet: {sheet_name} ({len(df)} 条数据)")
    
    created = 0
    skipped = 0
    
    for idx, row in df.iterrows():
        try:
            # 检查是否有 Cat. 或 Product Name
            cat_value = clean_value(row.get("Cat.", ""))
            product_name = clean_value(row.get("Product Name", ""))
            
            if not cat_value and not product_name:
                print(f"  ⚠️  跳过第 {idx+1} 行：缺少 Cat. 和 Product Name")
                skipped += 1
                continue
            
            # 1. 构建输出目录
            output_dir = get_output_path(row, sheet_name)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 2. 生成文件名（使用 Cat.）
            filename = generate_filename(row)
            filepath = output_dir / filename
            
            # 避免覆盖
            if filepath.exists():
                print(f"  ⚠️  跳过已存在：{filepath}")
                skipped += 1
                continue
            
            # 3. 生成 Front Matter
            front_matter = generate_front_matter(row)
            
            # 4. 添加正文内容（可选，目前为空）
            content = f"{front_matter}\n"
            
            # 5. 写入文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            display_name = product_name or cat_value
            print(f"  ✅ 生成：{filepath.relative_to(OUTPUT_ROOT)} - {display_name[:50]}...")
            created += 1
            
            # 6. 自动创建 _index.md（如果子分类下没有）
            index_file = output_dir / "_index.md"
            if not index_file.exists() and output_dir.name != OUTPUT_ROOT.split('/')[-1]:
                class_id = clean_value(row.get("Class ID", ""))
                if class_id:
                    with open(index_file, "w", encoding="utf-8") as f:
                        f.write(f"""---
title: "{class_id}"
---
""")
                    print(f"  📄 创建分类页：{index_file.relative_to(OUTPUT_ROOT)}")
            
        except Exception as e:
            print(f"  ❌ 第 {idx+1} 行失败：{e}")
            import traceback
            traceback.print_exc()
    
    return created, skipped

def main():
    parser = argparse.ArgumentParser(description="Excel 转 Hugo Markdown (Cat.→文件名，Class ID→子目录)")
    parser.add_argument("excel", nargs="?", default=EXCEL_FILE, help="Excel 文件路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不写入文件")
    args = parser.parse_args()
    
    print(f"📖 读取文件：{args.excel}")
    
    # 读取所有 sheet
    try:
        xl_file = pd.ExcelFile(args.excel)
        sheet_names = xl_file.sheet_names
        print(f"📑 发现 {len(sheet_names)} 个 Sheet: {', '.join(sheet_names)}")
    except Exception as e:
        print(f"❌ 读取 Excel 失败：{e}")
        return
    
    total_created = 0
    total_skipped = 0
    
    for sheet_name in sheet_names:
        try:
            df = pd.read_excel(args.excel, sheet_name=sheet_name)
            created, skipped = process_sheet(df, sheet_name)
            total_created += created
            total_skipped += skipped
        except Exception as e:
            print(f"❌ 处理 Sheet '{sheet_name}' 失败：{e}")
    
    print(f"\n{'='*60}")
    print(f"🎉 完成！")
    print(f"   ✅ 生成：{total_created} 个产品文件")
    print(f"   ⚠️  跳过：{total_skipped} 个（已存在或缺少必要字段）")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
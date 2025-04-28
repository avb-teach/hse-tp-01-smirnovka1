#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from pathlib import Path

def copy_files(input_dir, output_dir, max_depth=None):
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    # Создаем выходную директорию, если её нет
    output_path.mkdir(parents=True, exist_ok=True)
    
    if max_depth is None:
        copy_without_structure(input_path, output_path)
    else:
        copy_with_max_depth(input_path, output_path, max_depth)

def copy_without_structure(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            source_file = Path(root) / filename
            copy_file_with_rename(source_file, output_dir)

def copy_with_max_depth(input_dir, output_dir, max_depth):
    input_dir = Path(input_dir)
    
    for root, dirs, files in os.walk(input_dir):
        root_path = Path(root)
        
        rel_path = root_path.relative_to(input_dir)
        depth = len(rel_path.parts)
        
        if depth <= max_depth:
            if str(rel_path) == '.':
                target_dir = output_dir
            else:
                target_dir = output_dir / rel_path
                target_dir.mkdir(parents=True, exist_ok=True)
            
            for filename in files:
                source_file = root_path / filename
                copy_file_with_rename(source_file, target_dir)
        else:
            parts = rel_path.parts
            preserved_path = Path(*parts[:max_depth])
            
            target_dir = output_dir / preserved_path
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for filename in files:
                source_file = root_path / filename
                copy_file_with_rename(source_file, target_dir)

def copy_file_with_rename(src_file, dest_dir):
    filename = src_file.name
    dest_path = dest_dir / filename
    
    if dest_path.exists():
        stem = src_file.stem
        suffix = src_file.suffix
        counter = 1
        
        while (dest_dir / f"{stem}{counter}{suffix}").exists():
            counter += 1
        
        dest_path = dest_dir / f"{stem}{counter}{suffix}"
    
    shutil.copy2(src_file, dest_path)

def main():
    parser = argparse.ArgumentParser(description="Копирует файлы из входной директории в выходную.")
    parser.add_argument("input_dir", help="Входная директория")
    parser.add_argument("output_dir", help="Выходная директория")
    parser.add_argument("--max_depth", type=int, help="Максимальная глубина вложенности для сохранения структуры")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"Ошибка: Входная директория не существует: {args.input_dir}")
        sys.exit(1)
    
    copy_files(args.input_dir, args.output_dir, args.max_depth)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from pathlib import Path

def copy_files(input_dir, output_dir, max_depth=None):
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    if max_depth == 0:
        for item in input_path.iterdir():
            if item.is_file():
                copy_file_with_rename(item, output_path)
            elif item.is_dir():
                dest_dir = output_path / item.name
                dest_dir.mkdir(exist_ok=True)
                shutil.copytree(item, dest_dir, dirs_exist_ok=True)
    else:
        process_directory(input_path, output_path, 1, input_path, max_depth)

def process_directory(current_dir, output_dir, current_depth, base_path, max_depth=None):
    if max_depth is not None and current_depth > max_depth:
        rel_path = current_dir.relative_to(base_path)
        target_dir = output_dir / rel_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(current_dir, target_dir / current_dir.name, dirs_exist_ok=True)
        return
    
    for item in current_dir.iterdir():
        if item.is_file():
            if max_depth is None:
                copy_file_with_rename(item, output_dir)
            else:
                rel_path = item.parent.relative_to(base_path)
                target_dir = output_dir / rel_path
                target_dir.mkdir(parents=True, exist_ok=True)
                copy_file_with_rename(item, target_dir)
                
        elif item.is_dir():
            if max_depth is not None and current_depth < max_depth:
                new_output = output_dir / item.name
                new_output.mkdir(exist_ok=True)
                process_directory(item, new_output, current_depth + 1, base_path, max_depth)
            else:
                process_directory(item, output_dir, current_depth + 1, base_path, max_depth)

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


parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("output_dir")
parser.add_argument("--max_depth", type=int)
    
args = parser.parse_args()
    
if not os.path.isdir(args.input_dir):
    print(f"Ошибка: Входная директория не существует: {args.input_dir}")
    sys.exit(1)
    
copy_files(args.input_dir, args.output_dir, args.max_depth)

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

    input_path = Path(input_dir)
    
    for root, dirs, files in os.walk(input_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(input_path)
        depth = len(rel_path.parts)
        for filename in files:
            source_file = root_path / filename
            
            if depth <= max_depth:

                target_dir = output_dir
                if rel_path.parts:  
                    target_dir = output_dir / rel_path
                target_dir.mkdir(parents=True, exist_ok=True)
                copy_file_with_rename(source_file, target_dir)
            else:

                start_index = depth - max_depth
                
                # Создаем целевой путь
                new_path_parts = rel_path.parts[start_index:]
                target_dir = output_dir
                for part in new_path_parts[:-1]: 
                    target_dir = target_dir / part
                    target_dir.mkdir(parents=True, exist_ok=True)
                
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
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--max_depth", type=int)
    
    args = parser.parse_args()

if __name__ == "__main__":
    main()

    
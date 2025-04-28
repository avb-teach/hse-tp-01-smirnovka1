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

    all_paths = []
    for root, dirs, files in os.walk(input_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(input_path)

        for file in files:
            source_file = root_path / file
            all_paths.append((source_file, rel_path, 'file'))
        
        for dir_name in dirs:
            source_dir = root_path / dir_name
            all_paths.append((source_dir, rel_path, 'dir'))


    for source_path, rel_path, type_path in all_paths:
        if type_path == 'file':

            depth = len(rel_path.parts)
            
            if depth <= max_depth:

                if rel_path.parts:
                    target_dir = output_dir / rel_path
                else:
                    target_dir = output_dir
                
                target_dir.mkdir(parents=True, exist_ok=True)
                copy_file_with_rename(source_path, target_dir)
            else:
                above_max_depth_path = Path(*rel_path.parts[:max_depth])
                
                remainder_path = Path(*rel_path.parts[max_depth:])
                if remainder_path.parent != Path('.'):
                    target_dir = output_dir / above_max_depth_path / remainder_path.parent
                else:
                    target_dir = output_dir / above_max_depth_path
                
                target_dir.mkdir(parents=True, exist_ok=True)
                copy_file_with_rename(source_path, target_dir)

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
    
    copy_files(args.input_dir, args.output_dir, args.max_depth)

if __name__ == "__main__":
    main()
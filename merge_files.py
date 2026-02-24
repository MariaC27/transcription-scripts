#!/usr/bin/env python3
"""
Script to merge CSV files from reviewed_files folder in a specific order.
Files are identified by names containing: Louis, Maria, David, Michael
and merged in that exact order.
"""

import csv
import os
import glob
import argparse
from pathlib import Path


def find_file_by_name(folder, name_pattern):
    """
    Find a CSV file in folder whose name contains the pattern.
    
    Args:
        folder (str): Folder to search in
        name_pattern (str): String to search for in filename
    
    Returns:
        str: Path to matching file, or None if not found
    """
    all_files = glob.glob(os.path.join(folder, "*.csv"))
    
    for file_path in all_files:
        filename = os.path.basename(file_path)
        if name_pattern.lower() in filename.lower():
            return file_path
    
    return None


def merge_files_in_order(input_folder, output_file, name_order):
    """
    Merge CSV files in a specific order based on name patterns.
    
    Args:
        input_folder (str): Folder containing CSV files
        output_file (str): Path to output merged CSV file
        name_order (list): List of name patterns to match in order
    """
    print(f"Looking for CSV files in: {input_folder}\n")
    
    # Validate input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist")
        return
    
    # Find files for each name in order
    files_to_merge = []
    for name in name_order:
        file_path = find_file_by_name(input_folder, name)
        if file_path:
            print(f"✓ Found file for '{name}': {os.path.basename(file_path)}")
            files_to_merge.append(file_path)
        else:
            print(f"✗ Warning: No file found containing '{name}'")
    
    if not files_to_merge:
        print("\nError: No files found to merge")
        return
    
    print(f"\nMerging {len(files_to_merge)} files in order...")
    
    # Merge files
    header_written = False
    total_rows = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = None
        
        for i, file_path in enumerate(files_to_merge, 1):
            filename = os.path.basename(file_path)
            print(f"\n{i}. Processing: {filename}")
            
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    
                    # Read header
                    try:
                        header = next(reader)
                    except StopIteration:
                        print(f"   Warning: File is empty, skipping...")
                        continue
                    
                    # Write header only once (from first file)
                    if not header_written:
                        writer = csv.writer(outfile)
                        writer.writerow(header)
                        header_written = True
                        print(f"   Header: {', '.join(header)}")
                    
                    # Write all data rows
                    file_rows = 0
                    for row in reader:
                        writer.writerow(row)
                        file_rows += 1
                        total_rows += 1
                    
                    print(f"   Rows added: {file_rows}")
                    
            except Exception as e:
                print(f"   Error processing {filename}: {e}")
                continue
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully merged {len(files_to_merge)} files into {output_file}")
    print(f"Total rows written: {total_rows}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge CSV files in specific order based on name patterns"
    )
    parser.add_argument(
        "-i", "--input-folder",
        default="reviewed_files",
        help="Folder containing CSV files to merge (default: reviewed_files)"
    )
    parser.add_argument(
        "-o", "--output",
        default="merged_output.csv",
        help="Output CSV file (default: merged_output.csv)"
    )
    parser.add_argument(
        "-n", "--names",
        nargs='+',
        default=["Louis", "Maria", "David", "Michael"],
        help="Name patterns in order (default: Louis Maria David Michael)"
    )
    
    args = parser.parse_args()
    
    merge_files_in_order(args.input_folder, args.output, args.names)


if __name__ == "__main__":
    main()

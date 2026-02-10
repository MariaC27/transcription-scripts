#!/usr/bin/env python3
"""
Script to stitch multiple CSV files containing script names and transcriptions
into one combined CSV file.

By default, reads all CSV files from the 'files' folder in the current directory.
"""

import csv
import glob
import os
import argparse
from pathlib import Path


def stitch_csv_files(input_folder, output_file, sort_files=True):
    """
    Combine multiple CSV files into a single CSV file.
    
    Args:
        input_folder (str): Path to folder containing CSV files
        output_file (str): Path to the output CSV file
        sort_files (bool): Whether to sort input files alphabetically before combining
    """
    # Find all CSV files in the specified folder
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in folder: {input_folder}")
        return
    
    if sort_files:
        csv_files.sort()
    
    print(f"Found {len(csv_files)} CSV files to stitch together")
    
    # Track if we've written the header yet
    header_written = False
    rows_written = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = None
        
        for csv_file in csv_files:
            print(f"Processing: {csv_file}")
            
            try:
                with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    
                    # Read the header
                    try:
                        header = next(reader)
                    except StopIteration:
                        print(f"  Warning: {csv_file} is empty, skipping...")
                        continue
                    
                    # Write header only once (from the first file)
                    if not header_written:
                        writer = csv.writer(outfile)
                        writer.writerow(header)
                        header_written = True
                    
                    # Write all data rows
                    for row in reader:
                        writer.writerow(row)
                        rows_written += 1
                        
            except Exception as e:
                print(f"  Error processing {csv_file}: {e}")
                continue
    
    print(f"\nSuccessfully stitched {len(csv_files)} files into {output_file}")
    print(f"Total rows written: {rows_written}")


def main():
    parser = argparse.ArgumentParser(
        description="Stitch multiple CSV files together into one combined CSV file"
    )
    parser.add_argument(
        "-i", "--input-folder",
        default="files",
        help="Folder containing CSV files (default: files)"
    )
    parser.add_argument(
        "-o", "--output",
        default="combined_transcriptions.csv",
        help="Output CSV file name (default: combined_transcriptions.csv)"
    )
    parser.add_argument(
        "--no-sort",
        action="store_true",
        help="Don't sort input files before combining"
    )
    
    args = parser.parse_args()
    
    # Check if input folder exists
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist")
        return
    
    if not os.path.isdir(args.input_folder):
        print(f"Error: '{args.input_folder}' is not a directory")
        return
    
    stitch_csv_files(
        args.input_folder,
        args.output,
        sort_files=not args.no_sort
    )


if __name__ == "__main__":
    main()

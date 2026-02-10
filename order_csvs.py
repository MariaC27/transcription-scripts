#!/usr/bin/env python3
"""
Script to order two CSV files to match each other based on a common column.
Outputs sorted versions of both files with the same row order.
"""

import csv
import argparse
from pathlib import Path


def order_csv_files(file1, file2, sort_column, output_suffix="_ordered"):
    """
    Order two CSV files to have matching row order based on a sort column.
    
    Args:
        file1 (str): Path to first CSV file
        file2 (str): Path to second CSV file
        sort_column (str): Column name to sort by (must exist in both files)
        output_suffix (str): Suffix to add to output filenames
    """
    print(f"Reading {file1}...")
    rows1 = []
    headers1 = None
    
    with open(file1, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers1 = reader.fieldnames
        rows1 = list(reader)
    
    print(f"Reading {file2}...")
    rows2 = []
    headers2 = None
    
    with open(file2, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers2 = reader.fieldnames
        rows2 = list(reader)
    
    # Check if sort column exists in both files
    if sort_column not in headers1:
        print(f"Error: Column '{sort_column}' not found in {file1}")
        print(f"Available columns: {', '.join(headers1)}")
        return
    
    if sort_column not in headers2:
        print(f"Error: Column '{sort_column}' not found in {file2}")
        print(f"Available columns: {', '.join(headers2)}")
        return
    
    print(f"\nSorting both files by '{sort_column}'...")
    
    # Sort both files by the sort column
    rows1_sorted = sorted(rows1, key=lambda x: x[sort_column])
    rows2_sorted = sorted(rows2, key=lambda x: x[sort_column])
    
    # Generate output filenames
    path1 = Path(file1)
    path2 = Path(file2)
    
    output1 = path1.stem + output_suffix + path1.suffix
    output2 = path2.stem + output_suffix + path2.suffix
    
    # Write sorted file 1
    print(f"\nWriting ordered {output1}...")
    with open(output1, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers1)
        writer.writeheader()
        writer.writerows(rows1_sorted)
    
    # Write sorted file 2
    print(f"Writing ordered {output2}...")
    with open(output2, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers2)
        writer.writeheader()
        writer.writerows(rows2_sorted)
    
    print(f"\nSuccess!")
    print(f"File 1: {len(rows1_sorted)} rows written to {output1}")
    print(f"File 2: {len(rows2_sorted)} rows written to {output2}")
    
    # Check if all sort values match
    values1 = [row[sort_column] for row in rows1_sorted]
    values2 = [row[sort_column] for row in rows2_sorted]
    
    if values1 == values2:
        print(f"\n✓ Both files have matching {sort_column} values in the same order")
    else:
        print(f"\n⚠ Warning: Files have different {sort_column} values")
        in_1_not_2 = set(values1) - set(values2)
        in_2_not_1 = set(values2) - set(values1)
        
        if in_1_not_2:
            print(f"  In {file1} but not {file2}: {len(in_1_not_2)} items")
        if in_2_not_1:
            print(f"  In {file2} but not {file1}: {len(in_2_not_1)} items")


def main():
    parser = argparse.ArgumentParser(
        description="Order two CSV files to match each other based on a common column"
    )
    parser.add_argument(
        "file1",
        help="First CSV file to order"
    )
    parser.add_argument(
        "file2",
        help="Second CSV file to order"
    )
    parser.add_argument(
        "-c", "--column",
        default="Filename",
        help="Column name to sort by (default: Filename)"
    )
    parser.add_argument(
        "-s", "--suffix",
        default="_ordered",
        help="Suffix to add to output filenames (default: _ordered)"
    )
    
    args = parser.parse_args()
    
    order_csv_files(args.file1, args.file2, args.column, args.suffix)


if __name__ == "__main__":
    main()

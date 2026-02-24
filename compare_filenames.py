#!/usr/bin/env python3
"""
Script to compare filenames between two CSV files to find missing/extra rows.
"""

import csv
import argparse


def compare_filenames(file1, file2):
    """
    Compare filenames in two CSV files and report differences.
    
    Args:
        file1 (str): Path to first CSV file
        file2 (str): Path to second CSV file
    """
    print(f"\nComparing filenames between:")
    print(f"  File 1: {file1}")
    print(f"  File 2: {file2}")
    print("=" * 60)
    
    # Read filenames from file1
    filenames1 = []
    with open(file1, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                filenames1.append(row[0])  # First column is filename
    
    # Read filenames from file2
    filenames2 = []
    with open(file2, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                filenames2.append(row[0])  # First column is filename
    
    # Convert to sets for comparison
    set1 = set(filenames1)
    set2 = set(filenames2)
    
    # Find differences
    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1
    
    print(f"\nFile 1 total filenames: {len(filenames1)}")
    print(f"File 2 total filenames: {len(filenames2)}")
    print(f"File 1 unique filenames: {len(set1)}")
    print(f"File 2 unique filenames: {len(set2)}")
    print(f"Common filenames: {len(set1 & set2)}")
    
    if only_in_file1:
        print(f"\n\n{'='*60}")
        print(f"Filenames ONLY in {file1}: {len(only_in_file1)}")
        print(f"{'='*60}")
        for filename in sorted(only_in_file1):
            print(f"  - {filename}")
    
    if only_in_file2:
        print(f"\n\n{'='*60}")
        print(f"Filenames ONLY in {file2}: {len(only_in_file2)}")
        print(f"{'='*60}")
        for filename in sorted(only_in_file2):
            print(f"  - {filename}")
    
    if not only_in_file1 and not only_in_file2:
        print("\n✓ Both files have the exact same filenames!")
        
        # Check for duplicates within each file
        dups1 = [f for f in set1 if filenames1.count(f) > 1]
        dups2 = [f for f in set2 if filenames2.count(f) > 1]
        
        if dups1:
            print(f"\nDuplicates in {file1}:")
            for dup in sorted(dups1):
                count = filenames1.count(dup)
                print(f"  - {dup} appears {count} times")
        
        if dups2:
            print(f"\nDuplicates in {file2}:")
            for dup in sorted(dups2):
                count = filenames2.count(dup)
                print(f"  - {dup} appears {count} times")


def main():
    parser = argparse.ArgumentParser(
        description="Compare filenames between two CSV files"
    )
    parser.add_argument("file1", help="First CSV file")
    parser.add_argument("file2", help="Second CSV file")
    
    args = parser.parse_args()
    
    compare_filenames(args.file1, args.file2)


if __name__ == "__main__":
    main()

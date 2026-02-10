#!/usr/bin/env python3
"""
Script to reorder one CSV file to match the exact row order of another CSV file
based on a matching column (typically Filename).
"""

import csv
import argparse


def reorder_to_match(reference_file, file_to_reorder, output_file, match_column="Filename"):
    """
    Reorder file_to_reorder to match the exact row order of reference_file.
    
    Args:
        reference_file (str): CSV file whose order we want to match
        file_to_reorder (str): CSV file to be reordered
        output_file (str): Path for the reordered output file
        match_column (str): Column name to match rows on
    """
    print(f"Reading reference order from {reference_file}...")
    
    # Read reference file to get the desired order
    reference_order = []
    with open(reference_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reference_order.append(row[match_column])
    
    print(f"Found {len(reference_order)} rows in reference file")
    
    # Read the file to reorder into a dictionary
    print(f"\nReading {file_to_reorder}...")
    rows_dict = {}
    headers = None
    
    with open(file_to_reorder, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        if match_column not in headers:
            print(f"Error: Column '{match_column}' not found in {file_to_reorder}")
            print(f"Available columns: {', '.join(headers)}")
            return
        
        for row in reader:
            key = row[match_column]
            rows_dict[key] = row
    
    print(f"Found {len(rows_dict)} rows in file to reorder")
    
    # Reorder rows to match reference
    print(f"\nReordering to match reference file...")
    reordered_rows = []
    missing_count = 0
    
    for ref_key in reference_order:
        if ref_key in rows_dict:
            reordered_rows.append(rows_dict[ref_key])
        else:
            print(f"  Warning: '{ref_key}' in reference but not in file to reorder")
            missing_count += 1
    
    # Check for extra rows not in reference
    extra_keys = set(rows_dict.keys()) - set(reference_order)
    if extra_keys:
        print(f"\n  Warning: {len(extra_keys)} rows in {file_to_reorder} not in reference file")
        print(f"  These will be appended at the end:")
        for key in sorted(extra_keys)[:5]:  # Show first 5
            print(f"    - {key}")
        if len(extra_keys) > 5:
            print(f"    ... and {len(extra_keys) - 5} more")
        
        # Append extra rows at the end
        for key in extra_keys:
            reordered_rows.append(rows_dict[key])
    
    # Write reordered file
    print(f"\nWriting reordered file to {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(reordered_rows)
    
    print(f"\nSuccess! Wrote {len(reordered_rows)} rows to {output_file}")
    print(f"Rows matched: {len(reordered_rows) - len(extra_keys) - missing_count}")
    if missing_count > 0:
        print(f"Rows missing: {missing_count}")
    if extra_keys:
        print(f"Extra rows appended: {len(extra_keys)}")


def main():
    parser = argparse.ArgumentParser(
        description="Reorder a CSV file to match the row order of a reference CSV file"
    )
    parser.add_argument(
        "-r", "--reference",
        default="metadata_ copy.csv",
        help="Reference CSV file (whose order to match) (default: metadata_ copy.csv)"
    )
    parser.add_argument(
        "-i", "--input",
        default="combined_transcriptions_duration.csv",
        help="CSV file to reorder (default: combined_transcriptions_duration.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        default="combined_transcriptions_duration_reordered.csv",
        help="Output file path (default: combined_transcriptions_duration_reordered.csv)"
    )
    parser.add_argument(
        "-c", "--column",
        default="Filename",
        help="Column name to match rows on (default: Filename)"
    )
    
    args = parser.parse_args()
    
    # Confirm overwrite if output equals input
    if args.output == args.input:
        print(f"⚠ Warning: This will overwrite {args.input}")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    reorder_to_match(args.reference, args.input, args.output, args.column)


if __name__ == "__main__":
    main()

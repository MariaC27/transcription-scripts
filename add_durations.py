#!/usr/bin/env python3
"""
Script to add duration_sec column from metadata file to combined transcriptions.
Matches on Filename column and outputs a new CSV with duration included.
"""

import csv
import argparse


def add_durations(metadata_file, transcriptions_file, output_file):
    """
    Add duration_sec from metadata file to transcriptions file based on Filename.
    
    Args:
        metadata_file (str): Path to metadata CSV with Filename and duration_sec columns
        transcriptions_file (str): Path to transcriptions CSV with Filename and Transcription columns
        output_file (str): Path to output CSV file
    """
    # First, read the metadata file and create a dictionary mapping Filename -> duration_sec
    duration_map = {}
    
    print(f"Reading metadata from {metadata_file}...")
    with open(metadata_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['Filename']
            duration = row['duration_sec']
            duration_map[filename] = duration
    
    print(f"Loaded {len(duration_map)} duration entries")
    
    # Now read the transcriptions file and add the duration column
    print(f"\nProcessing transcriptions from {transcriptions_file}...")
    rows_processed = 0
    rows_matched = 0
    rows_unmatched = 0
    
    with open(transcriptions_file, 'r', newline='', encoding='utf-8') as infile:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            
            # Write header with duration_sec column added (using 'transcript' to match metadata format)
            fieldnames = ['Filename', 'duration_sec', 'transcript']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Process each row
            for row in reader:
                filename = row['Filename']
                # Handle both 'Transcription' and 'transcript' column names in input
                transcription = row.get('Transcription') or row.get('transcript', '')
                
                # Look up duration from metadata
                duration = duration_map.get(filename, '')
                
                if duration:
                    rows_matched += 1
                else:
                    rows_unmatched += 1
                    print(f"  Warning: No duration found for {filename}")
                
                # Write row with duration (using 'transcript' header)
                writer.writerow({
                    'Filename': filename,
                    'duration_sec': duration,
                    'transcript': transcription
                })
                
                rows_processed += 1
    
    print(f"\nProcessing complete!")
    print(f"Total rows processed: {rows_processed}")
    print(f"Rows matched: {rows_matched}")
    print(f"Rows unmatched: {rows_unmatched}")
    print(f"\nOutput written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Add duration_sec column to transcriptions CSV by matching Filename"
    )
    parser.add_argument(
        "-m", "--metadata",
        default="metadata_ copy.csv",
        help="Metadata CSV file with duration_sec (default: metadata_ copy.csv)"
    )
    parser.add_argument(
        "-t", "--transcriptions",
        default="combined_transcriptions.csv",
        help="Transcriptions CSV file (default: combined_transcriptions.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        default="combined_transcriptions_duration.csv",
        help="Output CSV file (default: combined_transcriptions_duration.csv)"
    )
    
    args = parser.parse_args()
    
    add_durations(args.metadata, args.transcriptions, args.output)


if __name__ == "__main__":
    main()

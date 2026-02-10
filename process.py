#!/usr/bin/env python3
"""
Main orchestration script to process transcription files for a specific person.

This script runs the following pipeline:
1. Stitch CSV files together from {name}_files folder
2. Add duration_sec column from metadata_copy.csv
3. Reorder to match metadata_copy.csv row order
4. Save final output to {name}_generated_files folder

Usage:
    python3 process.py <person_name>
    python3 process.py Sarah
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """
    Run a shell command and handle errors.
    
    Args:
        command (list): Command and arguments as a list
        description (str): Human-readable description of what's being done
    """
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(command)}\n")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print stdout
    if result.stdout:
        print(result.stdout)
    
    # Print stderr if there are any errors
    if result.stderr:
        print("Errors/Warnings:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    if result.returncode != 0:
        print(f"\nError: Command failed with exit code {result.returncode}")
        sys.exit(1)
    
    print(f"✓ {description} completed successfully")


def process_transcriptions(name):
    """
    Run the full transcription processing pipeline for a person.
    
    Args:
        name (str): Person's name (used for folder naming)
    """
    # Define folder and file paths
    input_folder = f"{name}_files"
    output_folder = f"{name}_generated_files"
    metadata_file = "metadata_copy.csv"
    
    # Intermediate and final file paths in the generated folder
    combined_file = os.path.join(output_folder, "combined_transcriptions.csv")
    with_duration_file = os.path.join(output_folder, "combined_transcriptions_duration.csv")
    final_file = os.path.join(output_folder, f"{name}_final.csv")
    
    print(f"\n{'='*60}")
    print(f"Processing transcriptions for: {name}")
    print(f"{'='*60}")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Metadata file: {metadata_file}")
    
    # Validate input folder exists
    if not os.path.exists(input_folder):
        print(f"\nError: Input folder '{input_folder}' does not exist")
        print(f"Please create a folder named '{input_folder}' with CSV files to process")
        sys.exit(1)
    
    if not os.path.isdir(input_folder):
        print(f"\nError: '{input_folder}' exists but is not a directory")
        sys.exit(1)
    
    # Check for CSV files in input folder
    csv_files = list(Path(input_folder).glob("*.csv"))
    if not csv_files:
        print(f"\nError: No CSV files found in '{input_folder}'")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Validate metadata file exists
    if not os.path.exists(metadata_file):
        print(f"\nError: Metadata file '{metadata_file}' not found")
        print(f"Please ensure '{metadata_file}' exists in the current directory")
        sys.exit(1)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder ready: {output_folder}")
    
    # Step 1: Stitch files together
    run_command(
        ["python3", "stitch_chunks.py", "-i", input_folder, "-o", combined_file],
        f"Stitching CSV files from {input_folder}"
    )
    
    # Step 2: Add duration column
    run_command(
        ["python3", "add_durations.py", "-m", metadata_file, "-t", combined_file, "-o", with_duration_file],
        "Adding duration_sec column from metadata"
    )
    
    # Step 3: Reorder to match metadata
    run_command(
        ["python3", "reorder_to_match.py", "-r", metadata_file, "-i", with_duration_file, "-o", final_file],
        "Reordering to match metadata row order"
    )
    
    print(f"\n{'='*60}")
    print(f"Processing complete for {name}!")
    print(f"{'='*60}")
    print(f"\nGenerated files:")
    print(f"  1. {combined_file}")
    print(f"  2. {with_duration_file}")
    print(f"  3. {final_file} (final output)")
    print(f"\nAll files saved in: {output_folder}")


def main():
    parser = argparse.ArgumentParser(
        description="Process transcription files for a specific person",
        epilog="Example: python3 process.py Sarah"
    )
    parser.add_argument(
        "name",
        help="Person's name (will look for {name}_files folder)"
    )
    parser.add_argument(
        "-m", "--metadata",
        default="metadata_copy.csv",
        help="Path to metadata CSV file (default: metadata_copy.csv)"
    )
    
    args = parser.parse_args()
    
    # Update global metadata file if specified
    if args.metadata != "metadata_copy.csv":
        global metadata_file
        metadata_file = args.metadata
    
    process_transcriptions(args.name)


if __name__ == "__main__":
    main()

# Transcription Processing Scripts

A collection of Python scripts to process, combine, and organize transcription CSV files

### Steps

- Combine multiple CSV files into one
- Add duration metadata to transcriptions
- Reorder CSV files to match a reference order

<br>
<br>

### Requirements

- **Python 3.10+**

- **Input folder**: `{name}_files/` containing CSV files to process
- **Metadata file**: `metadata_copy.csv` in the project root

<br>
<br>


### Usage

Run main processing script with someone's name or another unique key:

```bash
python3 process.py <person_name>
```

<br>


For example, running "python3 process.py maria" will:
1. Look for CSV files in `maria_files/` folder
2. Stitch them together
3. Add duration data from `metadata_copy.csv`
4. Reorder to match metadata row order
5. Save all outputs to `maria_generated_files/`


**Example folder structure:**
```
transcription-scripts/
├── metadata_copy.csv          # Required: contains duration_sec data
├── maria_files/               # Your input CSVs
│   ├── chunk_001.csv
│   ├── chunk_002.csv
│   └── chunk_003.csv
└── maria_generated_files/     # Auto-created output folder
    ├── combined_transcriptions.csv
    ├── combined_transcriptions_duration.csv
    └── maria_final.csv        # Final output!
```
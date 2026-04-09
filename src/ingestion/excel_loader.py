import pandas as pd
from pathlib import Path
from typing import List
from src.utils.logger import log

def load_spreadsheet(file_path: str | Path) -> List[dict]:
    file_path = Path(file_path)
    log.info(f"Loading spreadsheet: {file_path.name}")
    chunks = []
   
    try:
        # Check if it's CSV or Excel
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Fill empty cells with "N/A" so the code doesn't crash
        df = df.fillna("N/A")

        for index, row in df.iterrows():
            # Convert the row into a string: "Column1: Value1 | Column2: Value2..."
            row_data = [f"{col}: {val}" for col, val in row.items()]
            row_string = " | ".join(row_data)
           
            chunks.append({
                "text": row_string,
                "source": file_path.name,
                "row_index": index + 1,
                "file_type": "spreadsheet"
            })
           
        log.info(f"Spreadsheet loaded: {len(chunks)} rows processed.")
        return chunks
    except Exception as e:
        log.error(f"Failed to load spreadsheet {file_path.name}: {e}")
        raise
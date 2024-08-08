import openpyxl
from typing import List, Dict, Any
import csv



def create_excel(documents: List[Dict[str, Any]], file_path: str):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    # Assuming documents are list of dicts
    if documents:
        # Add headers (keys of the first document)
        worksheet.append(list(documents[0].keys()))
        for document in documents:
            # Add row values
            worksheet.append(list(document.values()))
    workbook.save(file_path)


def create_csv(documents: List[Dict[str, Any]], file_path: str):
    # Assuming documents are list of dicts
    if documents:
        # Get the headers from the first document
        headers = list(documents[0].keys())
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for document in documents:
                writer.writerow(document)

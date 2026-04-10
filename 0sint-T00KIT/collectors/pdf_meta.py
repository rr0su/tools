"""
pdf_meta.py
-----------
Bulk metadata extractor for PDFs/documents. Safe, read-only.
Uses exiftool (must be installed) for full coverage.
Outputs JSON summary for ingestion.
"""

import os, json, subprocess, argparse
from tqdm import tqdm

def run_exiftool(path):
    # exiftool outputs many keys; we capture only the interesting ones
    try:
        out = subprocess.check_output(['exiftool', '-j', path], text=True)
        data = json.loads(out)
        return data[0] if isinstance(data, list) and data else {}
    except Exception as e:
        return {"error": str(e)}

def collect_folder(folder, outpath="pdf_metadata.json"):
    results = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(('.pdf', '.docx', '.doc', '.xlsx', '.pptx', '.jpg', '.png')):
                full = os.path.join(root, f)
                meta = run_exiftool(full)
                results.append({"file": full, "meta": meta})
    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("[+] Saved", outpath)
    return outpath

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--folder", required=True, help="Folder of files to parse")
    p.add_argument("--out", default="pdf_metadata.json")
    args = p.parse_args()
    collect_folder(args.folder, args.out)

"""
08_duplicate_file_finder.py
Category: Intermediate / Systems & File I/O

Description:
A multi-tier duplicate file finder:
- Stage 1: Group files by byte size (unique sizes are skipped immediately)
- Stage 2: Quick hash check of the first 4KB chunk
- Stage 3: Full streaming SHA-256 hash for identical chunk collisions
- Prevents loading large files into memory using chunked streaming
- Reports duplicate sets and recoverable disk space
"""

import hashlib
import os
import tempfile
from collections import defaultdict
from typing import Dict, List, Tuple

CHUNK_SIZE = 64 * 1024  # 64 KB read buffer
PARTIAL_CHUNK = 4096    # 4 KB quick fingerprint


def get_partial_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        chunk = f.read(PARTIAL_CHUNK)
        hasher.update(chunk)
    return hasher.hexdigest()


def get_full_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(directory: str) -> Dict[str, List[str]]:
    """
    Finds duplicate files in `directory` recursively.
    Returns mapping of full_hash -> list of duplicate filepaths.
    """
    size_map = defaultdict(list)

    # Stage 1: Filter by size
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                if os.path.isfile(filepath) and not os.path.islink(filepath):
                    size = os.path.getsize(filepath)
                    if size > 0:  # Ignore empty files
                        size_map[size].append(filepath)
            except (OSError, PermissionError):
                continue

    # Filter to sizes with at least 2 files
    candidate_size_groups = [paths for paths in size_map.values() if len(paths) > 1]

    # Stage 2: Partial hash comparison (first 4KB)
    partial_hash_map = defaultdict(list)
    for group in candidate_size_groups:
        for path in group:
            try:
                p_hash = get_partial_hash(path)
                partial_hash_map[(os.path.getsize(path), p_hash)].append(path)
            except (OSError, PermissionError):
                continue

    candidate_partial_groups = [
        paths for paths in partial_hash_map.values() if len(paths) > 1
    ]

    # Stage 3: Full SHA-256 hash confirmation
    duplicates = defaultdict(list)
    for group in candidate_partial_groups:
        for path in group:
            try:
                f_hash = get_full_hash(path)
                duplicates[f_hash].append(path)
            except (OSError, PermissionError):
                continue

    # Only return hashes with multiple identical files
    return {h: paths for h, paths in duplicates.items() if len(paths) > 1}


def main():
    print("=== 08: Duplicate File Finder Demo ===")

    # Create temporary directory with simulated duplicates
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Creating test files in sandbox: {temp_dir}")
        file_a = os.path.join(temp_dir, "document.txt")
        file_b = os.path.join(temp_dir, "document_copy.txt")
        file_c = os.path.join(temp_dir, "document_backup.txt")
        file_d = os.path.join(temp_dir, "distinct_report.txt")

        content_1 = b"Hello world! This is a repeated text content for duplicate testing." * 50
        content_2 = b"Different unique content that should not match any duplicate." * 50

        with open(file_a, "wb") as f: f.write(content_1)
        with open(file_b, "wb") as f: f.write(content_1)
        with open(file_c, "wb") as f: f.write(content_1)
        with open(file_d, "wb") as f: f.write(content_2)

        print("\nScanning directory for duplicates...")
        dupes = find_duplicates(temp_dir)

        print(f"Found {len(dupes)} set(s) of duplicates:")
        total_wasted_bytes = 0
        for h, paths in dupes.items():
            file_size = os.path.getsize(paths[0])
            wasted = file_size * (len(paths) - 1)
            total_wasted_bytes += wasted
            print(f"\n[Hash: {h[:12]}...] (Size: {file_size} bytes)")
            for p in paths:
                print(f"  -> {os.path.basename(p)}")
            print(f"  Wasted redundant space: {wasted} bytes")

        print(f"\nTotal reclaimable space: {total_wasted_bytes} bytes.")


if __name__ == "__main__":
    main()

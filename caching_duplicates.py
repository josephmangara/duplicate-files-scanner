import os
import hashlib
import json

CACHE_FILE = "file_cache.json"

def calculate_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading cache: {e}")
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, 'w') as file:
            json.dump(cache, file, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")

def find_duplicates(directory, cached_hashes):
    hash_map = cached_hashes.copy()
    duplicates = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in hash_map.values():  # Skip files already in cache
                continue
            
            file_hash = calculate_hash(file_path)
            if file_hash:
                if file_hash in hash_map:
                    duplicates.setdefault(file_hash, []).append(file_path)
                else:
                    hash_map[file_hash] = file_path
    return hash_map, duplicates

def main():
    directory = input("Enter the directory path to scan for duplicates: ")
    if not os.path.exists(directory):
        print("The specified directory does not exist.")
        return

    print("Loading cached data...")
    cached_hashes = load_cache()

    print("Scanning for duplicate files...")
    updated_cache, duplicates = find_duplicates(directory, cached_hashes)

    if duplicates:
        print("\nDuplicate files found:")
        for file_hash, file_list in duplicates.items():
            print(f"\nHash: {file_hash}")
            for file in file_list:
                print(f" - {file}")
    else:
        print("No duplicate files found.")

    print("Saving updated cache...")
    save_cache(updated_cache)
    print("Scan complete. Cache updated.")

if __name__ == "__main__":
    main()

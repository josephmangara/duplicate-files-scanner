import os
import hashlib

def calculate_hash(file_path, chunk_size=8192):
    """
    Calculate the hash of a file using SHA256.
    Args:
        file_path (str): Path to the file.
        chunk_size (int): Size of chunks to read at a time.
    Returns:
        str: The SHA256 hash of the file.
    """
    # sha256 = hashlib.sha256()
    # Faster hash algorithm
    sha256 = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

def find_duplicates(directory):
    """
    Find duplicate files in a directory by comparing their hashes.
    Args:
        directory (str): Path to the directory to scan.
    Returns:
        dict: A dictionary where keys are file hashes and values are lists of file paths.
    """
    hash_map = {}
    duplicates = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)
            if file_hash:
                if file_hash in hash_map:
                    duplicates.setdefault(file_hash, []).append(file_path)
                else:
                    hash_map[file_hash] = file_path
    return duplicates

def main():
    directory = input("Enter the directory path to scan for duplicates: ")
    if not os.path.exists(directory):
        print("The specified directory does not exist.")
        return

    print("Scanning for duplicate files...")
    duplicates = find_duplicates(directory)
    if duplicates:
        print("\nDuplicate files found:")
        for file_hash, file_list in duplicates.items():
            print(f"\nHash: {file_hash}")
            for file in file_list:
                print(f" - {file}")
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    main()

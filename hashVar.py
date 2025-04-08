# v0.0.2
# Verify SHA256


import hashlib

def calculate_sha256(file_path):
    """
    Calculate the SHA256 hash of a file.
    
    Args:
        file_path (str): Path to the file to hash
        
    Returns:
        str: Hexadecimal SHA256 hash or error message if file not found
    """
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()  # Read entire file as bytes
            readable_hash = hashlib.sha256(file_bytes).hexdigest()
            return readable_hash
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: An unexpected issue occurred - {str(e)}"

def main():
    # Get user inputs
    original_hash = input("Enter the original SHA256 hash: ").strip()
    file_path = input("Enter the file path: ").strip()

    # Calculate the hash of the provided file
    calculated_hash = calculate_sha256(file_path)

    # Display results in a copy-friendly format
    print("\n=== SHA256 Verification Results ===")
    print(f"Original Hash : {original_hash}")
    print(f"Calculated Hash: {calculated_hash}")
    
    # Compare and provide feedback
    if calculated_hash.startswith("Error"):
        print("Status: Unable to verify due to an error")
    elif original_hash.lower() == calculated_hash.lower():  # Case-insensitive comparison
        print("Status: MATCH - The hashes are identical!")
    else:
        print("Status: MISMATCH - The hashes do not match.")

if __name__ == "__main__":
    main()
#v0.0.1
#Verify SHA256






import hashlib

original = input("Enter the original 256 hash: ")
file = input("Enter the file and its path: ")
def calculate_sha256(file_path):
    try:

        with open(file,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest();
            return readable_hash
    except FileNotFoundError:
        return "File not found"

# Replace 'yourfile.txt' with the name of your file
print(calculate_sha256('yourfile.txt'))
print(original)

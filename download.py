import urllib.request
import zipfile
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://ti.arc.nasa.gov/m/project/prognostic-repository/CMAPSSData.zip"
zip_path = "CMAPSSData.zip"
out_dir = "data/raw"

print(f"Downloading CMAPSS dataset from {url}...")
urllib.request.urlretrieve(url, zip_path)

print("Extracting...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(out_dir)

print("Done extracting. Cleaning up zip file.")
os.remove(zip_path)

# Show files in directory
print("Files in data/raw:")
for f in os.listdir(out_dir):
    print(f)

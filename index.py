import os
import torch
import clip
import faiss
import pickle
from PIL import Image
import numpy as np
from tqdm import tqdm
from tkinter import Tk, filedialog

# -------------------------------
# Select folder manually (GUI)
# -------------------------------
Tk().withdraw()
image_folder = filedialog.askdirectory(title="Select Image Folder")

if not image_folder:
    print("❌ No folder selected. Exiting...")
    exit()

print(f"📁 Selected folder: {image_folder}")

# -------------------------------
# Supported image formats
# -------------------------------
SUPPORTED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tif", ".gif"
)

# -------------------------------
# Load model
# -------------------------------
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# -------------------------------
# Collect valid image paths
# -------------------------------
image_paths = [
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if f.lower().endswith(SUPPORTED_EXTENSIONS)
]

if not image_paths:
    print("❌ No valid images found in selected folder.")
    exit()

embeddings = []

print("🔄 Indexing images...")

# -------------------------------
# Process images
# -------------------------------
for path in tqdm(image_paths):
    try:
        image = preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            emb = model.encode_image(image)
            emb = emb / emb.norm(dim=-1, keepdim=True)
        embeddings.append(emb.cpu().numpy())
    except Exception as e:
        print(f"❌ Skipped: {path} | Error: {e}")

# -------------------------------
# Convert embeddings
# -------------------------------
embeddings = np.vstack(embeddings).astype("float32")

# -------------------------------
# Create FAISS index
# -------------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # cosine similarity
index.add(embeddings)

# -------------------------------
# Save index and paths (custom + safe)
# -------------------------------
Tk().withdraw()

# Ask user where to save index
index_file = filedialog.asksaveasfilename(
    title="Save FAISS Index",
    defaultextension=".faiss",
    initialdir=os.getcwd(),
    filetypes=[("FAISS Index", "*.faiss")],
)

if not index_file:
    print("❌ Index save cancelled.")
    exit()

# Try saving index safely
try:
    faiss.write_index(index, index_file)
    print(f"✅ Index saved to: {index_file}")
except Exception as e:
    print(f"⚠️ Failed to save at chosen location: {e}")
    fallback_index = os.path.join(os.getcwd(), "index.faiss")
    faiss.write_index(index, fallback_index)
    print(f"✅ Saved instead at: {fallback_index}")
    index_file = fallback_index

# Ask user where to save paths
paths_file = filedialog.asksaveasfilename(
    title="Save Image Paths",
    defaultextension=".pkl",
    initialdir=os.getcwd(),
    filetypes=[("Pickle File", "*.pkl")],
)

if not paths_file:
    print("❌ Paths save cancelled.")
    exit()

# Try saving paths safely
try:
    with open(paths_file, "wb") as f:
        pickle.dump(image_paths, f)
    print(f"✅ Paths saved to: {paths_file}")
except Exception as e:
    print(f"⚠️ Failed to save at chosen location: {e}")
    fallback_paths = os.path.join(os.getcwd(), "image_paths.pkl")
    with open(fallback_paths, "wb") as f:
        pickle.dump(image_paths, f)
    print(f"✅ Saved instead at: {fallback_paths}")

print("🎉 Indexing completed successfully!")

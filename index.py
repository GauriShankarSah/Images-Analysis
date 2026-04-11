import os
import torch
import clip
import faiss
import pickle
from PIL import Image
import numpy as np
from tqdm import tqdm

# Load model
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

image_folder = "images"
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]

embeddings = []

print("🔄 Indexing images...")

for path in tqdm(image_paths):
    try:
        image = preprocess(Image.open(path)).unsqueeze(0).to(device)
        with torch.no_grad():
            emb = model.encode_image(image)
            emb = emb / emb.norm(dim=-1, keepdim=True)
        embeddings.append(emb.cpu().numpy())
    except:
        print(f"❌ Skipped: {path}")

embeddings = np.vstack(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # cosine similarity
index.add(embeddings)

# Save
faiss.write_index(index, "index.faiss")

with open("image_paths.pkl", "wb") as f:
    pickle.dump(image_paths, f)

print("✅ Index created successfully!")

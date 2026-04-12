import torch
import clip
import faiss
import pickle
from PIL import Image
import tempfile

device = "cpu"

model = None
preprocess = None
index = None
image_paths = None


def load_assets(faiss_file, pkl_file):
    global model, preprocess, index, image_paths

    if model is None:
        print("🔄 Loading CLIP model + FAISS index...")

        model, preprocess = clip.load("ViT-B/32", device=device)

        # Save FAISS file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as f:
            faiss_file.save(f.name)
            index = faiss.read_index(f.name)

        # Save PKL file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as f:
            pkl_file.save(f.name)
            with open(f.name, "rb") as pf:
                image_paths = pickle.load(pf)

        print("✅ Loaded successfully!")


def search_image(query_path, top_k=5):
    global model

    if model is None:
        raise Exception("❌ Model not loaded! Please load FAISS + PKL first.")

    image = preprocess(Image.open(query_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model.encode_image(image)
        emb = emb / emb.norm(dim=-1, keepdim=True)

    emb = emb.cpu().numpy().astype("float32")

    scores, indices = index.search(emb, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append((image_paths[idx], float(score)))

    return results

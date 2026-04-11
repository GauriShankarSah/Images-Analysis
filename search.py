import torch
import clip
import faiss
import pickle
from PIL import Image

device = "cpu"

model = None
preprocess = None
index = None
image_paths = None


def load_assets():
    global model, preprocess, index, image_paths

    if model is None:
        print("🔄 Loading CLIP model + FAISS index...")

        model, preprocess = clip.load("ViT-B/32", device=device)

        index = faiss.read_index("index.faiss")

        with open("image_paths.pkl", "rb") as f:
            image_paths = pickle.load(f)

        print("✅ Loaded successfully!")


def search_image(query_path, top_k=5):
    load_assets()

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

import os
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import math
from keybert import KeyBERT
from .constants import CATEGORIES
os.environ["TOKENIZERS_PARALLELISM"] = "false"

device = "cpu"
semantic_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def is_valid_embedding(embedding, expected_dim=768):
    if not isinstance(embedding, list) or len(embedding) != expected_dim:
        return False
    arr = np.array(embedding)
    return np.all(np.isfinite(arr)) and not np.all(arr == 0)

import numpy as np

def safe_encode(text, model, expected_dim=768):
    try:
        emb = model.encode(text, device='cpu')  # Force CPU
        if isinstance(emb, np.ndarray):
            emb_list = emb.flatten().tolist()
        elif hasattr(emb, 'cpu'):  # torch.Tensor
            emb_list = emb.cpu().numpy().flatten().tolist()
        else:
            print("❌ Unexpected embedding type:", type(emb))
            return None

        if len(emb_list) != expected_dim:
            print(f"❌ Invalid dimension: {len(emb_list)} ≠ {expected_dim}")
            return None
        if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in emb_list):
            print(f"❌ Non-finite values in: {emb_list[:5]}")
            return None

        return emb_list
    except Exception as e:
        print(f"❌ safe_encode failed: {e}")
        return None



def classify_article_semantically(title: str, summary: str, category_embeddings, model, device="cpu") -> str:
    text = f"{title}. {summary or ''}"
    emb = model.encode(text, convert_to_tensor=True)
    
    if device == "cpu":
        emb = emb.cpu()
    else:
        emb = emb.to(device)

    best_cat = "Uncategorized"
    best_score = -1

    for cat, reps in category_embeddings.items():
        reps = reps.to(emb.device)  # ensure same device
        sim = util.cos_sim(emb, reps).max().item()
        if sim > best_score:
            best_cat = cat
            best_score = sim

    return best_cat

kw_model = KeyBERT()

category_embeddings = {
    cat: semantic_model.encode(examples, convert_to_tensor=True)
    for cat, examples in CATEGORIES.items()
}

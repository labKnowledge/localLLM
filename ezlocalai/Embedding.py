from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer
from ezlocalai.Helpers import get_tokens, chunk_content
from huggingface_hub import snapshot_download

import torch
import os


class Embedding:
    def __init__(self):
        snapshot_download(
            repo_id="hooman650/bge-m3-onnx-o4",
            cache_dir=os.path.join(os.getcwd(), "models"),
            local_dir_use_symlinks=False,
        )

        self.model = ORTModelForFeatureExtraction.from_pretrained(
            "hooman650/bge-m3-onnx-o4",
            cache_dir=os.path.join(os.getcwd(), "models"),
            local_dir_use_symlinks=False,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "hooman650/bge-m3-onnx-o4",
            cache_dir=os.path.join(os.getcwd(), "models"),
            local_dir_use_symlinks=False,
        )

    def get_embeddings(self, input):
        tokens = get_tokens(input)
        sentences = chunk_content(input)
        encoded_input = self.tokenizer(
            sentences, padding=True, truncation=True, return_tensors="pt"
        ).to("cuda" if torch.cuda.is_available() else "cpu")
        out = self.model(**encoded_input, return_dict=True).last_hidden_state
        dense_vecs = torch.nn.functional.normalize(out[:, 0], dim=-1)
        return {
            "object": "list",
            "data": [{"object": "embedding", "index": 0, "embedding": dense_vecs}],
            "model": "bge-m3",
            "usage": {"prompt_tokens": tokens, "total_tokens": tokens},
        }

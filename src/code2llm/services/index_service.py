from pathlib import Path
from typing import List, Dict
import tiktoken


class MarkdownChunker:
    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size
        self.encoder = tiktoken.encoding_for_model("gpt-4")

    def chunk_markdown(self, file_path: Path, repo_name: str) -> List[Dict]:
        """对 Markdown 进行分块"""
        chunks = []

        with open(file_path, "r", encoding="utf-8") as f:
            current_chunk = []
            current_tokens = 0

            for line in f:
                tokens = len(self.encoder.encode(line))
                if current_tokens + tokens > self.chunk_size:
                    chunks.append({
                        "content": "\n".join(current_chunk),
                        "metadata": {
                            "repo": repo_name,
                            "chunk_id": f"chunk-{len(chunks)}"
                        }
                    })
                    current_chunk = []
                    current_tokens = 0

                current_chunk.append(line)
                current_tokens += tokens

            if current_chunk:
                chunks.append({
                    "content": "\n".join(current_chunk),
                    "metadata": {"repo": repo_name}
                })

        return chunks

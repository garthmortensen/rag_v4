# Model Landscape — Ollama & Hugging Face

**Hugging Face** = the giant warehouse.

**Ollama** = the curated app store.

A one-pager to cut through the noise: what kinds of models exist, what to pick
for what job, and how the names and tags actually work.

See also: [embedder_providers.md](embedder_providers.md) for *how* HF and
Ollama distribute models. This file is about *which* models to pick.

---

## The two jobs in a RAG pipeline

| Job          | What it does                                       | Used by                    |
|--------------|----------------------------------------------------|----------------------------|
| **Embedder** | Text → fixed-size vector (for similarity search)   | `ingest.py`, `query.py`    |
| **Chat LLM** | Prompt → generated text (the answer)               | `query.py`, `ragas` judge  |

Different model families, different sizes, different leaderboards. Don't mix
them up — an "embedding model" is not a chat model and vice versa.

---

## Picking an embedder

Embedders are small (50 MB – 1 GB), fast, and cheap to swap. The headline
numbers to look at:

- **Dimension** — vector size (384, 768, 1024, 1536, 3072…). Bigger ≈ more
  expressive, but more storage and slower search.
- **Max sequence length** — tokens per input (256, 512, 8192…). If your
  `chunk_size` exceeds this, the tail gets silently truncated.
- **MTEB score** — the standard embedding leaderboard
  ([huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard)).
  Filter by "Retrieval" for RAG-relevant scores.

### Reasonable defaults

| Provider   | Model                        | Dim   | Max tokens | Notes                                 |
|------------|------------------------------|-------|------------|---------------------------------------|
| HuggingFace| `all-MiniLM-L6-v2`           | 384   | 256        | Tiny, fast, this repo's default       |
| HuggingFace| `BAAI/bge-small-en-v1.5`     | 384   | 512        | Better quality, same size class       |
| HuggingFace| `BAAI/bge-large-en-v1.5`     | 1024  | 512        | Top open retrieval scores             |
| HuggingFace| `intfloat/e5-large-v2`       | 1024  | 512        | Strong general-purpose retrieval      |
| Ollama     | `nomic-embed-text`           | 768   | 8192       | Long-context, runs in Ollama          |
| Ollama     | `mxbai-embed-large`          | 1024  | 512        | Higher-quality Ollama option          |
| OpenAI     | `text-embedding-3-small`     | 1536  | 8191       | Cheap API, used by RAGAS in this repo |
| OpenAI     | `text-embedding-3-large`     | 3072  | 8191       | Best OpenAI quality                   |

Switching embedders requires **re-ingesting** — vectors from different models
live in incompatible spaces.

---

## Picking a chat LLM

Chat LLMs vary by orders of magnitude in size, cost, and quality. The model
*name* usually encodes four things:

```
   llama3.2  :  3b      -instruct-  q4_K_M
   ────┬───     ──┬─    ─────┬────  ───┬───
    family    size      tuning      quant
```

- **Family** — `llama`, `mistral`, `qwen`, `gemma`, `phi`, `deepseek`,
  `claude`, `gpt`, …
- **Size** — parameter count (`3b`, `7b`, `8b`, `70b`, `405b`). Roughly 2 GB
  of RAM per billion params at 4-bit.
- **Tuning** — `-base` (raw), `-instruct` / `-chat` (follows instructions),
  `-code` (programming), `-r1` (reasoning). **For RAG, always use an
  instruct/chat variant.**
- **Quantization** *(Ollama/GGUF only)* — `q4_K_M`, `q5_K_M`, `q8_0`, `fp16`.
  Lower bits = smaller and faster, with some quality loss. `q4_K_M` is the
  common sweet spot.

### Reasonable defaults

| Tier              | Local (Ollama)                | API (OpenAI / Anthropic)             |
|-------------------|-------------------------------|--------------------------------------|
| **Tiny / fast**   | `llama3.2:3b`, `phi3:mini`    | `gpt-4o-mini`, `claude-haiku`        |
| **Mid-quality**   | `llama3.1:8b`, `qwen2.5:7b`   | `gpt-4o`, `claude-sonnet`            |
| **Best**          | `llama3.1:70b` (needs ~40 GB) | `gpt-5`, `claude-opus`               |
| **Reasoning**     | `deepseek-r1:7b`              | `o1`, `o3`                           |
| **Code**          | `qwen2.5-coder:7b`            | `gpt-4o`, `claude-sonnet`            |

### Picking for this repo

- **`[rag.llm]`** — answers user questions. Quality matters; small local
  models often hallucinate. `gpt-4o-mini` is the cheap-but-good default.
- **`[rag.evaluation]`** — judges the answers (RAGAS). **Must** support
  structured output reliably; tiny models fail silently here. Use at minimum
  `gpt-4o-mini` / `claude-haiku` / `llama3.1:8b`.

---

## File formats: what you actually download

The same model can be packaged very differently depending on where you get it.
Below: what `llama3.1:8b-instruct` actually looks like on disk in each ecosystem.

### Hugging Face — `meta-llama/Meta-Llama-3.1-8B-Instruct`

A git repo. You get the full-precision weights, the tokenizer, and metadata.
Everything is human-inspectable text *except* the weight files themselves.

```
~/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3.1-8B-Instruct/
├── config.json                      # 1 KB   — architecture (layers, heads, dims)
├── tokenizer.json                   # 9 MB   — merges + vocab
├── tokenizer_config.json            # 50 KB  — chat template, special tokens
├── special_tokens_map.json          # 500 B
├── generation_config.json           # 200 B  — default temperature, top_p, …
├── model.safetensors.index.json     # 25 KB  — which tensor lives in which shard
├── model-00001-of-00004.safetensors # 4.8 GB ┐
├── model-00002-of-00004.safetensors # 4.8 GB │  fp16 / bf16 weights, sharded
├── model-00003-of-00004.safetensors # 4.8 GB │  total ≈ 16 GB
├── model-00004-of-00004.safetensors # 1.2 GB ┘
└── README.md                        # model card
```

Example `config.json`:

```json
{
  "architectures": ["LlamaForCausalLM"],
  "hidden_size": 4096,
  "num_attention_heads": 32,
  "num_hidden_layers": 32,
  "vocab_size": 128256,
  "max_position_embeddings": 131072,
  "torch_dtype": "bfloat16"
}
```

You load it with `transformers.AutoModelForCausalLM.from_pretrained(...)`,
which reads `config.json` to build the architecture, then mmaps the
`.safetensors` files into the model's tensors by name.

### Ollama — `llama3.1:8b`

A single quantized blob plus a tiny config. No separate tokenizer file — it's
embedded inside the GGUF. The on-disk layout is content-addressed (SHA256):

```
~/.ollama/models/
├── manifests/registry.ollama.ai/library/llama3.1/8b   # JSON pointer
└── blobs/
    ├── sha256-8eeb52df...   # 4.7 GB  — the GGUF (weights + tokenizer + metadata)
    ├── sha256-948af2a0...   # 1.4 KB  — chat template (Go template string)
    ├── sha256-0ba8f0e3...   # 12 B    — license blurb
    └── sha256-56bb8bd4...   # 96 B    — Modelfile parameters (stop tokens, etc.)
```

The manifest ties them together:

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
  "config": { "digest": "sha256:..." , "size": 485 },
  "layers": [
    { "mediaType": "application/vnd.ollama.image.model",    "digest": "sha256:8eeb52df...", "size": 4661211424 },
    { "mediaType": "application/vnd.ollama.image.template", "digest": "sha256:948af2a0...", "size": 1481 },
    { "mediaType": "application/vnd.ollama.image.license",  "digest": "sha256:0ba8f0e3...", "size": 12403 },
    { "mediaType": "application/vnd.ollama.image.params",   "digest": "sha256:56bb8bd4...", "size": 96 }
  ]
}
```

### What is GGUF?

**GGUF** (GPT-Generated Unified Format) is `llama.cpp`'s single-file model
format. It bundles **everything needed for inference** into one binary:

```
┌─ Header ─────────────────────────────┐
│ magic = "GGUF"                       │
│ version = 3                          │
│ tensor_count = 291                   │
│ metadata_kv_count = 27               │
├─ Metadata (key → typed value) ───────┤
│ general.architecture          = llama│
│ general.name                  = Llama 3.1 8B Instruct
│ llama.context_length          = 131072
│ llama.embedding_length        = 4096
│ llama.block_count             = 32
│ llama.attention.head_count    = 32
│ tokenizer.ggml.model          = gpt2
│ tokenizer.ggml.tokens         = ["<|begin_of_text|>", ...]
│ tokenizer.ggml.merges         = [...]
│ tokenizer.chat_template       = "{% for message in messages %}..."
│ general.quantization_version  = 2
│ general.file_type             = MOSTLY_Q4_K_M
├─ Tensor info table ──────────────────┤
│ token_embd.weight   dims=[4096,128256]  type=Q4_K   offset=0
│ blk.0.attn_q.weight dims=[4096,4096]    type=Q4_K   offset=…
│ … (291 tensors total)                                       │
├─ Tensor data (aligned blob) ─────────┤
│ <binary weights, quantized>          │
└──────────────────────────────────────┘
```

Key properties:
- **Single file** — no separate tokenizer, config, or shards to manage.
- **Self-describing** — the metadata block tells the runtime the
  architecture, so the same GGUF works in `llama.cpp`, `ollama`, `LM Studio`,
  and `koboldcpp` without code changes.
- **mmap-friendly** — the runtime memory-maps the file and reads tensors
  lazily; startup is near-instant.
- **Quantized in-place** — common types: `Q4_K_M` (4-bit, ~⅓ size of fp16,
  the default sweet spot), `Q5_K_M` (5-bit, slightly better quality),
  `Q8_0` (8-bit, very close to fp16), `F16` (no quantization).

### Side-by-side

|                       | Hugging Face (safetensors)          | Ollama (GGUF)                |
|-----------------------|-------------------------------------|------------------------------|
| Files per model       | 6–20 (config, tokenizer, shards)    | 1 weights blob + tiny meta   |
| Precision             | fp16 / bf16 (full)                  | Quantized (typically 4-bit)  |
| Size (8B model)       | ~16 GB                              | ~5 GB                        |
| Tokenizer location    | Separate JSON files                 | Embedded in GGUF metadata    |
| Chat template         | `tokenizer_config.json`             | Embedded in GGUF metadata    |
| Runtime               | `transformers`, `vLLM`, `TGI`       | `llama.cpp`, `ollama`        |
| Best for              | Training, fine-tuning, GPU serving  | Local CPU/GPU inference      |

You can always convert HF → GGUF with `llama.cpp/convert_hf_to_gguf.py`. The
other direction (GGUF → HF) is rarely done — quantization is lossy.

---

## Where to browse

- **Hugging Face Hub** — [huggingface.co/models](https://huggingface.co/models).
  Filter by task: *Sentence Similarity* (embedders), *Text Generation* (chat).
- **Ollama Registry** — [ollama.com/library](https://ollama.com/library). Each
  model page lists every available tag (`:3b`, `:7b`, `:70b-instruct-q4_K_M`).
- **MTEB leaderboard** — [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard).
  Compare embedders on retrieval tasks.
- **Chatbot Arena** — [lmarena.ai](https://lmarena.ai). Compare chat LLMs via
  blind head-to-head voting (the most-cited "vibes" benchmark).

---

## Rules of thumb

- For RAG, embedder quality usually moves results more than LLM quality.
- Start small, measure faithfulness scores, scale up only if metrics demand it.
- If you change embedder *or* chunking, re-ingest.
- If switching LLM provider, also swap `[rag.evaluation]` — keeping the eval
  model on a stronger provider gives more trustworthy scores.

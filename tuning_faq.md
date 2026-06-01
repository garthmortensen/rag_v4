# Tuning FAQ

## Unused RAGAS metrics

RAGAS ships many more metrics than the three this project uses. The table below covers the
RAG-relevant ones and explains why each is absent.

| Metric | What it measures | Why not used here |
|---|---|---|
| **Context Recall** | What fraction of the ground-truth answer's claims are supported by the retrieved context — the complement of CP. High recall means the retriever found everything it needed. | Requires a `reference` (human-written ground-truth answer) for each question. This project has no labelled answer set, so reference-free metrics were chosen instead. |
| **Factual Correctness** | Whether the claims in the generated answer match those in a reference answer (precision / recall / F1 over atomic claims). This is the "is the answer actually right?" metric — unlike Faithfulness, it checks against ground truth rather than retrieved context. | Also requires a `reference`. Would be the gold-standard metric for this domain but needs manual annotation first. |
| **Noise Sensitivity** | How often the LLM produces incorrect claims when its retrieved context contains irrelevant (noisy) chunks. Lower is better. Computed by comparing answer claims against both the retrieved context and the reference. | Requires a `reference`. It is a useful complement to Faithfulness: Faithfulness catches hallucination relative to retrieved context; Noise Sensitivity catches hallucination relative to ground truth. |
| **Context Entities Recall** | Whether named entities present in the reference answer are also present in the retrieved context. A lightweight, non-LLM alternative to Context Recall. | Requires `reference_contexts`. Useful for entity-heavy domains (e.g. financial filings with many institution names and figures) but needs labelled retrieval sets. |
| **Semantic Similarity** | Cosine similarity between the generated answer embedding and a reference answer embedding. Quick sanity-check for answer drift but conflates style with content. | Requires a `reference`. Also less informative than Factual Correctness for this domain. |
| **Traditional NLP (BLEU, ROUGE, CHRF)** | N-gram overlap between generated and reference text. Fast and deterministic but poorly correlated with semantic quality for open-ended RAG answers. | Requires a `reference` and penalises valid paraphrases heavily — not appropriate for free-form answer evaluation. |
| **Agent metrics (Topic Adherence, Tool Call Accuracy, etc.)** | Correctness of multi-step tool-calling and goal completion in agentic pipelines. | Not applicable — this is a single-turn RAG system with no tool use. |

**In short:** every unused metric either requires a labelled `reference` answer per question,
or is designed for agent/tool-use pipelines that don't apply here. Adding Context Recall and
Factual Correctness would give the most additional signal; doing so requires writing one
authoritative answer per benchmark question and storing it alongside the query set.

---

## What drives each RAGAS metric?

The tuning space in this project is `embedder_model × chunk_size × chunk_overlap × top_k`.
Here is how each metric relates to those knobs (and to factors outside the tuning grid).

---

### Faithfulness (F)

Faithfulness measures whether every claim in the generated answer is supported by the
retrieved context. The judge LLM extracts atomic statements from the answer and verifies
each one against the retrieved chunks.

**Primary driver: the generator LLM** (`llm_model`, `llm_temperature`). A model that stays
grounded in what it was handed scores high; one that draws on parametric (training-time)
knowledge instead of the retrieved chunks scores low. Temperature also matters — lower
temperature produces more conservative, context-hugging answers.

**Secondary drivers from the tuning grid:**

- **`top_k`** — providing more chunks gives the LLM more material to cite faithfully. Too
  few chunks and the LLM may fill gaps from memory.
- **`chunk_size`** — larger chunks contain more context per unit, reducing the chance that a
  relevant fact falls outside the retrieved window. However, oversized chunks dilute
  embeddings and may hurt retrieval quality (see CP).
- **`embedder_model`** — indirectly. Faithfulness is scored against *whatever was retrieved*,
  not against ground truth. If the embedder pulls irrelevant chunks, the LLM has less
  trustworthy material to be faithful to, but a capable LLM will still tend to hallucinate
  regardless of chunk quality.

**What faithfulness does *not* measure:** whether the answer is factually correct — only
whether it is consistent with the retrieved context.

---

### Answer Relevancy (AR)

Answer Relevancy measures how directly and completely the answer addresses the question.
The judge LLM generates several synthetic questions that the answer could plausibly answer,
then computes the average cosine similarity of those synthetic questions back to the
original. Vague, hedging, or off-topic answers score low.

**Primary driver: the generator LLM** (`llm_model`, `llm_temperature`). A model that
produces focused, direct answers scores high. One that hedges excessively ("this is a
complex topic…") or drifts into adjacent content scores low. Lower temperature generally
helps by reducing verbosity and tangents.

**Secondary drivers from the tuning grid:**

- **`top_k`** — retrieving too many chunks floods the context with loosely related material,
  which the LLM may incorporate into the answer even when it does not directly address the
  question. A smaller `top_k` often improves AR by keeping the context tight.
- **`chunk_size`** — large chunks are more likely to contain off-topic sentences that bleed
  into the generated answer, pulling AR down.
- **`embedder_model`** — indirectly. A better embedder returns more on-topic chunks, giving
  the LLM less reason to wander. The effect is usually smaller than the LLM's own tendency
  to stay on task.
- **`chunk_overlap`** — minimal effect on AR in most cases.

---

### Context Precision (CP)

Context Precision measures whether the most relevant chunks appear near the *top* of the
retrieved set. The judge LLM decides for each chunk whether it contributed to answering the
question, then computes a precision-at-k style score that rewards relevant chunks ranked
early and penalises relevant chunks buried at the bottom.

**Primary driver: the embedder** (`embedder_model`). Better embeddings produce higher cosine
similarity for truly relevant chunks, pushing them toward rank 1. Swapping the embedder
model is the single biggest lever for CP.

**Secondary drivers from the tuning grid:**

- **`chunk_size` / `chunk_overlap`** — a chunk that mixes relevant and irrelevant content
  gets a diluted embedding and tends to rank lower than a tightly focused chunk. Smaller
  chunks often improve CP, though very small chunks can fragment context (hurting F and AR).
- **`top_k`** — CP rewards relevant chunks ranked *early*. A larger `top_k` introduces more
  noise candidates, making it harder for the metric to reward good ordering even if the
  relevant chunks are still present.
- **The generator LLM** — indirectly. RAGAS judges whether each chunk *contributed to the
  answer*. If the generator produces a vague answer that does not clearly draw on specific
  chunks, the judge has a harder time attributing relevance, which can depress CP scores
  even when retrieval is good.

# RAG Tuning Results

Generated from 16 log files in `logs/`.

## Summary Table

> - **Faithfulness (F)**: Measures whether every claim in the generated answer is supported by the retrieved context. The judge LLM extracts atomic statements from the answer and verifies each one against the chunks. A score of 1.0 means nothing was hallucinated; 0.0 means the answer is entirely unsupported. Low faithfulness usually signals the LLM is drawing on parametric knowledge instead of the retrieved documents. *Example: if the answer states "the stress test threshold is 4.5%" but no retrieved chunk mentions that figure, that claim is unfaithful and lowers the score.*
> - **Answer Relevancy (AR)**: Measures how directly the answer addresses the question — penalising vague, incomplete, or off-topic responses. It works by prompting the LLM to generate several questions that the answer could plausibly answer, then computing the average cosine similarity of those synthetic questions back to the original. High AR means the answer is focused and on-point; low AR means it drifted or hedged excessively. *Example: if the question asks "what is the purpose of stress testing?" and the answer spends most of its content describing who conducts stress tests rather than why, the synthetic questions generated from it will not closely match the original, pulling AR down.*
> - **Context Precision (CP)**: Measures whether the most relevant chunks appear near the top of the retrieved set. The judge LLM decides for each chunk whether it actually contributed to answering the question, then computes a precision-at-k style score that rewards relevant chunks ranked early and penalises relevant chunks buried at the bottom. Low CP suggests the retriever is returning a lot of noise before the useful material. *Example: if the single chunk that contains the answer is ranked 9th out of 10, CP will be low even though the answer was technically reachable — a better embedding or smaller chunk size would surface it earlier.*
> - **Context Recall (CR)**: What fraction of the reference answer's claims are supported by the retrieved context. High recall means the retriever found all the content needed to answer correctly. Only computed for queries with a ground-truth reference (`n/a` for no-reference queries).
> - **Answer Correctness (AC)**: How closely the generated answer matches the reference, combining factual claim overlap (NLI) with semantic similarity. Only computed for ref queries.
> - **Noise Sensitivity (NS)**: How often the LLM produces incorrect claims even when relevant context was retrieved. Lower is better. Only computed for ref queries.
> 
> Collections sorted by F mean (descending). `n/a` = eval disabled, scoring failed, or no reference available.

| Collection | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | Q12 | Q13 | Q14 | Q15 | Q16 | Q17 | Q18 | Q19 | Q20 | Q21 | Q22 | Q23 | Q24 | Q25 | Q26 | Q27 | Q28 | Q29 | Q30 | Q31 | Q32 | Q33 | Q34 | Q35 | Q36 | Q37 | Q38 | Q39 | Q40 | Q41 | Q42 | Q43 | Q44 | Q45 | Q46 | Q47 | Q48 | Q49 | **F Mean** | **AR Mean** | **CP Mean** | **CR Mean** | **AC Mean** | **NS Mean** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chunk_size_1000_chunk_overlap_100` | 1.0000 | 1.0000 | 0.6667 | 0.8750 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.5714 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.8000 | 0.0000 | 0.5000 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7778 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 0.7500 | 0.6667 | 1.0000 | **0.7886** | **0.7594** | **0.5139** | **0.7826** | **0.4850** | **0.3304** |
| `chunk_size_500_chunk_overlap_300` | 1.0000 | 1.0000 | 1.0000 | 0.8571 | 0.5556 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.7500 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8571 | 0.0000 | 0.8000 | 1.0000 | 0.6000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1667 | 0.6667 | 1.0000 | **0.7844** | **0.7925** | **0.5810** | **0.8370** | **0.4940** | **0.2429** |
| `chunk_size_1000_chunk_overlap_50` | n/a | 1.0000 | 0.5000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8750 | 0.0000 | 0.8750 | 0.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 0.6667 | 1.0000 | 1.0000 | **0.7579** | **0.6861** | **0.4880** | **0.7391** | **0.4701** | **0.3446** |
| `chunk_size_2000_chunk_overlap_50` | n/a | 1.0000 | 1.0000 | 0.7273 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.8750 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.8750 | 1.0000 | 0.7143 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 0.9000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | **0.7531** | **0.6598** | **0.4778** | **0.8342** | **0.4792** | **0.3164** |
| `chunk_size_1000_chunk_overlap_300` | 1.0000 | 1.0000 | 0.5000 | 1.0000 | n/a | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.6667 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 0.0000 | 0.5000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7520** | **0.7329** | **0.5427** | **0.8025** | **0.5069** | **0.3538** |
| `chunk_size_3000_chunk_overlap_200` | n/a | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 0.6000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.8000 | 0.8750 | 1.0000 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.6667 | 1.0000 | **0.7507** | **0.6858** | **0.5785** | **0.8560** | **0.4788** | **0.3565** |
| `chunk_size_500_chunk_overlap_100` | 0.6667 | 1.0000 | 0.6667 | 0.8571 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.8000 | 0.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.5000 | 0.0000 | 1.0000 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 0.3333 | 0.6667 | 0.0000 | **0.7422** | **0.7516** | **0.5567** | **0.7790** | **0.4386** | **0.2746** |
| `chunk_size_2000_chunk_overlap_200` | 0.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.6000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7399** | **0.6668** | **0.4897** | **0.8777** | **0.4814** | **0.3567** |
| `chunk_size_1000_chunk_overlap_200` | 1.0000 | 1.0000 | 0.4000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.5714 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.3333 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.5000 | 0.3333 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | **0.7352** | **0.7118** | **0.4668** | **0.8025** | **0.4800** | **0.3239** |
| `chunk_size_3000_chunk_overlap_100` | n/a | 1.0000 | 1.0000 | 0.8000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 0.8000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.8750 | 1.0000 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7143 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | n/a | 0.0000 | 0.0000 | 1.0000 | 0.6667 | 1.0000 | **0.7329** | **0.6803** | **0.5776** | **0.8053** | **0.4693** | **0.3537** |
| `chunk_size_2000_chunk_overlap_100` | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.8333 | 0.8750 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9000 | 1.0000 | 1.0000 | 1.0000 | n/a | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | **0.7306** | **0.6535** | **0.4849** | **0.8342** | **0.4698** | **0.3086** |
| `chunk_size_3000_chunk_overlap_50` | n/a | 1.0000 | 1.0000 | 0.9231 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.8000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.8000 | 0.8750 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | n/a | 0.0000 | 1.0000 | 0.0000 | 0.6667 | 1.0000 | **0.7222** | **0.6750** | **0.5542** | **0.8487** | **0.4827** | **0.3439** |
| `chunk_size_2000_chunk_overlap_300` | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.9167 | 0.8750 | 1.0000 | 0.7143 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 0.9091 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7209** | **0.6885** | **0.5016** | **0.8234** | **0.5340** | **0.3508** |
| `chunk_size_3000_chunk_overlap_300` | 0.0000 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0.8000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.8333 | 1.0000 | 0.6250 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6667 | 1.0000 | **0.6922** | **0.6860** | **0.5862** | **0.7908** | **0.4544** | **0.3235** |
| `chunk_size_500_chunk_overlap_50` | 0.5000 | 1.0000 | n/a | 0.8000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.7000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | 0.8750 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5714 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.7500 | 0.6667 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.6667 | 0.0000 | **0.6638** | **0.6888** | **0.5330** | **0.7138** | **0.4102** | **0.2781** |
| `chunk_size_500_chunk_overlap_200` | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.8182 | 1.0000 | 0.7778 | 0.0000 | 0.0000 | 0.1429 | 0.0000 | 0.6667 | 1.0000 | 0.8571 | 0.8571 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.4286 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | **0.3893** | **0.4016** | **0.2861** | **0.4601** | **0.2472** | **0.0815** |

---

## Question 1: How did stress testing start, and how has it evolved?

### 1. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.6771 | CP: 1.0000 | CR: 0.6667 | AC: 0.7203 | NS: 0.0000

Stress testing started with individual banks measuring and managing risk using their own internal stress tests. However, supervisory stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This initiative evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.6771 | CP: 0.8333 | CR: 0.5000 | AC: 0.7843 | NS: 0.4286

Stress testing started with individual banks using their own internal stress tests to measure and manage risk. However, supervisory stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This program evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011, which is conducted to determine whether banks are adequately capitalized to withstand adverse economic conditions. Stress testing has become an important risk management tool for both banks and supervisors, helping to identify potential vulnerabilities and ensuring sufficient capital to withstand severe economic shocks.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.6468 | CP: 0.1111 | CR: 1.0000 | AC: 0.5172 | NS: 0.8333

Stress testing started as a response to the reforms following the Global Financial Crisis, becoming an important element of the Board's regulatory framework and supervisory program since 2009. It has evolved to improve transparency and reduce the volatility of capital buffer requirements, ensuring that large supervised institutions maintain sufficient capital to absorb losses and continue lending during economic downturns.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.6510 | CP: 0.1667 | CR: 0.6667 | AC: 0.8180 | NS: 0.7143

Stress testing started as a response to the Global Financial Crisis, becoming an important element of the Federal Reserve Board's regulatory framework and supervisory program since 2009. It was designed to ensure that large supervised institutions have sufficient capital to absorb losses and continue lending during economic downturns. Over time, there has been a commitment to improve the transparency of stress tests and reduce the volatility of capital buffer requirements, indicating an evolution towards more refined and transparent practices in stress testing.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8175 | CP: 0.2000 | CR: 0.6667 | AC: 0.7630 | NS: 0.7143

Stress testing started as a response to the Global Financial Crisis and has been an important part of the regulatory framework and supervisory program since 2009. It was born out of reforms aimed at ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during economic downturns. Over time, there has been a commitment to improve the transparency of stress tests and reduce the volatility of capital buffer requirements, indicating an evolution in the approach to stress testing.

### 6. `chunk_size_500_chunk_overlap_100` — F: 0.6667 | AR: 0.8194 | CP: 0.5000 | CR: 0.3333 | AC: 0.5690 | NS: 0.3333

Stress testing in the U.S. began with the Federal Reserve’s implementation of supervisory stress testing in 2009. Historically, individual banks measured and managed risk using their own internal stress tests, but the formal supervisory approach marked a significant evolution in the practice.

### 7. `chunk_size_500_chunk_overlap_50` — F: 0.5000 | AR: 0.8194 | CP: 0.5000 | CR: 0.3333 | AC: 0.7735 | NS: 0.1667

Stress testing in the U.S. began with the Federal Reserve’s implementation of supervisory stress testing in 2009. Historically, individual banks measured and managed risk using their own internal stress tests. Over time, the process has evolved to include more standardized supervisory stress tests to identify potential vulnerabilities and ensure that banks have sufficient capital to withstand severe economic shocks.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0257 | NS: 0.0000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0257 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7757 | NS: 0.0000

I don't know.

### 11. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7757 | NS: 0.0000

I don't know.

### 12. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7757 | NS: 0.0000

I don't know.

### 13. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7757 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0257 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7757 | NS: 0.0000

I don't know.

---

## Question 2: How does the Projections Calculator handle missing values in regulatory reports?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.5781 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. For loans with missing model inputs, each missing input is generally set to the 90th percentile value calculated across all loans of the equivalent type. When an input value for a categorical variable is missing, the value that best matches the 90th percentile is used.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.4967 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. For loans with missing model inputs, each missing input is generally set to the 90th percentile value calculated across all loans of the equivalent type. When an input value for a categorical variable is missing, the value that best matches the 90th percentile is used. If more than 50 percent of records within a portfolio or segment are missing a significant share of direct model inputs, the portfolio is assigned the 90th percentile of the projected balance-adjusted loss rate.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.8271 | NS: 0.3333

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.4967 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. For loans with missing model inputs, each missing input is generally set to the 90th percentile value calculated across all loans of the equivalent type. When an input value for a categorical variable is missing, the value that best matches the 90th percentile is used. If more than 50 percent of records within a portfolio or segment are missing a significant share of direct model inputs, the portfolio is assigned the 90th percentile of the projected balance-adjusted loss rate.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.4967 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. For loans with missing model inputs, each missing input is generally set to the 90th percentile value calculated across all loans of the equivalent type. When an input value for a categorical variable is missing, the value that best matches the 90th percentile is used. If more than 50 percent of records within a portfolio or segment are missing a significant share of direct model inputs, the portfolio is assigned the 90th percentile of the projected balance-adjusted loss rate.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 0.2000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 0.3333 | CR: 1.0000 | AC: 0.8271 | NS: 0.3333

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 0.2250 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 0.7500 | CR: 1.0000 | AC: 0.8271 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.8271 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.7271 | NS: 0.3333

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 1.0000 | CR: 1.0000 | AC: 0.6021 | NS: 0.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

---

## Question 3: In the first lien model, how are 2008 and after vintages combined?

### 1. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8952 | CP: 0.8583 | CR: 1.0000 | AC: 0.9196 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 2. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8952 | CP: 0.7688 | CR: 1.0000 | AC: 0.9196 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 3. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8952 | CP: 0.8084 | CR: 1.0000 | AC: 0.8863 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 4. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.5411 | CP: 0.7620 | CR: 1.0000 | AC: 0.9154 | NS: 0.0000

For loans originated in 2008 and after, they are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 5. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.7326 | CP: 0.7947 | CR: 1.0000 | AC: 0.9276 | NS: 0.0000

For vintages from 2008 and after, they are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 6. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8952 | CP: 0.9060 | CR: 1.0000 | AC: 0.9196 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 7. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8952 | CP: 1.0000 | CR: 1.0000 | AC: 0.9196 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 8. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8952 | CP: 0.9060 | CR: 1.0000 | AC: 0.8863 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 9. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8881 | CP: 0.9060 | CR: 1.0000 | AC: 0.9799 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure. 

If none of these criteria are met, the origination year is applied directly.

### 10. `chunk_size_500_chunk_overlap_100` — F: 0.6667 | AR: 0.8559 | CP: 1.0000 | CR: 0.0000 | AC: 0.6898 | NS: 0.0000

In the first lien model, the 2008 vintages are treated similarly to the 2003-2004 vintages, as they have similar delinquency rates. Additionally, the vintages from 2009-2011 and 2012+ are considered post-crisis vintages under tighter underwriting standards, making them less likely to become delinquent compared to the earlier vintages. Thus, the model combines the 2008 vintages with the 2003-2004 vintages for risk assessment purposes.

### 11. `chunk_size_1000_chunk_overlap_100` — F: 0.6667 | AR: 0.8952 | CP: 0.8583 | CR: 1.0000 | AC: 0.3735 | NS: 0.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are Option ARMs, or the loans meet certain characteristics that would lead to a sparse categorization if not combined.

### 12. `chunk_size_1000_chunk_overlap_50` — F: 0.5000 | AR: 0.6343 | CP: 0.8857 | CR: 1.0000 | AC: 0.3649 | NS: 0.0000

In the first lien model, loans originated in 2008 and after are combined if any of the following criteria are met: the loans are Option ARMs, or they meet certain characteristics that would avoid categories becoming too sparse.

### 13. `chunk_size_1000_chunk_overlap_300` — F: 0.5000 | AR: 0.8952 | CP: 0.9444 | CR: 1.0000 | AC: 0.8304 | NS: 0.2500

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are Option ARMs, or there are specific characteristics that warrant their combination to avoid categories becoming too sparse.

### 14. `chunk_size_1000_chunk_overlap_200` — F: 0.4000 | AR: 0.5638 | CP: 0.6595 | CR: 1.0000 | AC: 0.5542 | NS: 0.4000

In the first lien model, loans originated in 2008 and after are combined if any of the following criteria are met: the loans are Option ARMs, or they are grouped to avoid categories becoming too sparse. Specifically, for Option ARMs, loans from 2007 and after are combined, and for other loans, those from 2008 and after are combined based on the same criteria.

### 15. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7723 | NS: 0.0000

I don't know.

### 16. `chunk_size_500_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.7917 | CR: 0.0000 | AC: 0.7723 | NS: 0.0000

I don't know.

---

## Question 4: Tell me about how quickly the first lien model can transition current loans to default.

### 1. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8475 | CP: 0.8389 | CR: 1.0000 | AC: 0.7774 | NS: 0.2500

The first lien model assumes that current loans cannot directly transition to default. Instead, a loan must first transition to delinquent status before it can default. Specifically, the model defines current loans as those that are less than 90 days past due, while defaulted loans are those that are greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, loans may transition directly from current to default, but this is not modeled due to its infrequency and the principle of simplicity in the model design.

### 2. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8475 | CP: 1.0000 | CR: 1.0000 | AC: 0.7496 | NS: 0.1429

The first lien model assumes that current loans cannot directly transition to default. Instead, a loan must first fall into delinquency before it can transition to default. Specifically, the model defines current loans as those that are less than 90 days past due, while defaulted loans are those that are greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In rare circumstances, loans may transition directly from current to default, but such cases are removed from the estimation sample and ignored in the model.

### 3. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8525 | CP: 0.9861 | CR: 1.0000 | AC: 0.8897 | NS: 0.1667

The first lien model assumes that current loans cannot directly transition to default. Instead, it defines current loans as those that are less than 90 days past due, while defaulted loans are those that are greater than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default.

### 4. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.7049 | CP: 0.9861 | CR: 1.0000 | AC: 0.6779 | NS: 0.3333

The model assumes that two quarters are needed for a loan to transition from current to delinquent to default. In extremely rare circumstances, loans may transition directly from current to default, but this is not modeled due to its rarity, covering approximately 0.01 percent of observations in the data used to calibrate the model coefficients. The Board tested allowing loans to transition directly from current to default and found that projected loss rates were unchanged.

### 5. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7981 | CP: 0.8957 | CR: 1.0000 | AC: 0.6039 | NS: 0.2000

The First Lien PD Model assumes that two quarters are needed for a loan to transition from current to delinquent to default. This means that a loan must first become delinquent (90-179 days past due) before it can reach default status (180 days or more past due). In extremely rare circumstances, loans may transition directly from current to default, but the model does not account for this rare transition to maintain simplicity.

### 6. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.7095 | CP: 1.0000 | CR: 1.0000 | AC: 0.7875 | NS: 0.1250

Current loans cannot directly transition to default. According to the model's definitions, current loans are classified as less than 90 days past due, while defaulted loans are classified as greater than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In extremely rare cases, loans may transition directly from current to default, but this is not modeled due to its infrequency and the principle of simplicity in the Stress Testing Policy Statement.

### 7. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7610 | CP: 0.9765 | CR: 1.0000 | AC: 0.4462 | NS: 0.5000

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another. A current loan can transition to default if it becomes delinquent first. Specifically, a borrower must fall into delinquency before they can default. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan is in default, it is treated as a terminal status, meaning it cannot transition back to a current status. The exact timing for a current loan to transition to default is not specified in the context, but it is clear that the transition requires the loan to first become delinquent.

### 8. `chunk_size_3000_chunk_overlap_50` — F: 0.9231 | AR: 0.7391 | CP: 0.9765 | CR: 0.6667 | AC: 0.5242 | NS: 0.5385

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another. A current loan can transition to default if it becomes delinquent. Specifically, a borrower must first fall into delinquency, which is defined as being 90 or more days past due or in foreclosure proceedings. Once in delinquent status, the loan may remain delinquent, receive a loan modification, self-cure the delinquency, or default. The model does not specify an exact timeframe for how quickly a current loan can transition to default, as it depends on the borrower's actions and circumstances leading to delinquency. However, the transition from current to delinquent status can occur relatively quickly, and once a loan is delinquent, it can then transition to default based on the probabilities defined in the model.

### 9. `chunk_size_1000_chunk_overlap_100` — F: 0.8750 | AR: 0.8781 | CP: 0.9889 | CR: 1.0000 | AC: 0.7824 | NS: 0.1111

The first lien model cannot directly transition current loans to default. Current loans, defined as those less than 90 days past due, must first fall into delinquency before they can transition to default. The model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, about 0.01 percent of observations, loans may transition directly from current to default, but this is not modeled due to its rarity and the principle of simplicity.

### 10. `chunk_size_500_chunk_overlap_100` — F: 0.8571 | AR: 0.8468 | CP: 0.8401 | CR: 1.0000 | AC: 0.9795 | NS: 0.5714

Current loans cannot directly transition to default in the first lien model. The model defines current loans as those less than 90 days past due and defaulted loans as those greater than 180 days past due. Therefore, it assumes that two quarters are needed for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, about 0.01 percent of observations, loans may transition directly from current to default, but this is not the standard process.

### 11. `chunk_size_500_chunk_overlap_300` — F: 0.8571 | AR: 0.8781 | CP: 0.8690 | CR: 0.5000 | AC: 0.6601 | NS: 0.0000

The first lien model cannot transition current loans directly to default. Current loans are defined as being less than 90 days past due, while defaulted loans are defined as being greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, a small percentage of loans may transition directly from current to default, but this is not the norm.

### 12. `chunk_size_3000_chunk_overlap_300` — F: 0.8333 | AR: 0.7391 | CP: 0.9765 | CR: 1.0000 | AC: 0.4413 | NS: 0.2500

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another. A current loan can transition to default if it becomes delinquent, which is defined as being 90 or more days past due or in foreclosure proceedings. Once a loan is in delinquent status, it may remain delinquent, receive a loan modification, self-cure the delinquency, or default. The model does not specify an exact timeframe for how quickly a current loan can transition to default, but it indicates that the transition occurs through the delinquency status. Therefore, the speed of transition from current to default depends on the borrower's ability to maintain payments and avoid delinquency.

### 13. `chunk_size_500_chunk_overlap_50` — F: 0.8000 | AR: 0.8508 | CP: 0.7393 | CR: 1.0000 | AC: 0.6946 | NS: 0.4000

The first lien model assumes that current loans cannot directly transition to default. Instead, it requires two quarters for a loan to transition from current to delinquent and then to default. This means that current loans are relatively unlikely to default in the first six months, and they are considerably more likely to default afterwards.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.8000 | AR: 0.0000 | CP: 0.9765 | CR: 0.6667 | AC: 0.5549 | NS: 0.4286

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another. A current loan can transition to default if it becomes delinquent first. Specifically, a borrower must fall into delinquency before they can default. The model defines a loan as delinquent if it is 90-179 days past due or in foreclosure proceedings. Once a loan is marked as default, it is treated as a terminal status and cannot transition back to any other status. The exact timing for a current loan to transition to default depends on the borrower's payment behavior and the time it takes for the loan to become delinquent. However, the model does not provide a specific timeframe for how quickly this transition can occur.

### 15. `chunk_size_2000_chunk_overlap_50` — F: 0.7273 | AR: 0.7285 | CP: 0.9750 | CR: 1.0000 | AC: 0.3960 | NS: 0.4545

The First Lien PD Model uses a loan-level, state transition model approach to determine the probability of a loan transitioning from one payment status to another. To reach default, a borrower must first fall into delinquency. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan is marked as default, it is considered to have reached terminal status, meaning it cannot transition back to a current status. The model does not allow for cures from default, as this is rare and would complicate the model. Therefore, the transition from current to default can occur relatively quickly, as it depends on the borrower falling into delinquency first, which can happen within 90 days of missed payments.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.2730 | CR: 1.0000 | AC: 0.0245 | NS: 0.0000

I don't know.

---

## Question 5: What studies and academic literature does the first lien model draw on?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 0.0000 | AC: 0.1294 | NS: 0.0000

The first lien model draws on studies and academic literature including Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), An, Deng and Gabriel (2021), and von Furstenberg (1969).

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.7307 | CP: 0.2500 | CR: 0.0000 | AC: 0.1301 | NS: 0.0000

The First Lien Model draws on a large body of literature that provides useful context for developing an accurate, robust model of first lien probability of default (PD) and loss given default (LGD). It is informed by a review of relevant literature and industry best practices, as well as statistical fit and the Board’s experience and expertise. The literature review includes research that focuses on first lien mortgages, which is a much larger market compared to home equity exposures, and it also considers advanced modeling techniques for bounding LGD estimates.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9175 | CP: 0.0000 | CR: 0.0000 | AC: 0.1460 | NS: 0.0000

The first lien model draws on studies and academic literature including Gupton, Finger, & Bhatia's CreditMetrics (1997), KMV’s PortfolioManager, and the actuarial approach employed by Credit Suisse First Boston’s CreditRisk+. Detailed comparisons of these approaches are provided in works by Crouhy, Galai, & Mark (2000); Gordy (2000); and Allen & Saunders (2003).

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.7697 | CP: 0.6250 | CR: 0.2500 | AC: 0.3324 | NS: 0.4444

The First Lien Model draws on several studies and academic literature, including:

1. von Furstenberg (1969) - developed the first academic default risk model showing that the borrower’s level of home equity at the time of origination was the most important predictor of mortgage default.
2. Demyanyk and Van Hemert (2011).
3. Elul, Souleles, et al. (2010).
4. An, Deng and Gabriel (2021).
5. Bhutta, Dokko, and Shan (2010) - distinguished between defaults induced by job losses and those induced by negative equity.
6. Elul (2009) - found that low credit score borrowers have a higher risk of becoming delinquent.

These studies contribute to the development and design of the First Lien PD Model.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9487 | CP: 0.3750 | CR: 0.0000 | AC: 0.3814 | NS: 0.0909

The First Lien Model draws on various studies and academic literature, including:

1. Von Furstenberg's work from the late 1960s, which developed the first academic default risk model and identified the borrower's level of home equity as a key predictor of mortgage default.
2. Studies by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng, and Gabriel (2021).
3. Research by Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss.
4. Elul (2009), which finds that low credit score borrowers have a higher risk of becoming delinquent, particularly affecting subprime low-doc loans.

These studies provide useful context for developing an accurate and robust model of first lien probability of default (PD).

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.7680 | CP: 0.7000 | CR: 0.2500 | AC: 0.3133 | NS: 0.0000

The first lien model draws on several studies and academic literature, including:

1. von Furstenberg (1969) - developed the first academic default risk model.
2. Demyanyk and Van Hemert (2011).
3. Elul, Souleles, et al. (2010).
4. An, Deng and Gabriel (2021).
5. Bhutta, Dokko, and Shan (2010) - distinguished between defaults induced by job losses and those induced by negative equity.
6. Elul (2009) - found that low credit score borrowers have a higher risk of becoming delinquent.
7. Mayer, Pence, and Sherlund (2009) - found that borrowers with piggyback second liens tend to default at a higher rate.
8. Calem and Sarama (2017) - explored borrower behavior regarding multiple liens.
9. Jagtiani and Lang (2011) - provided explanations for default decisions related to larger first-lien mortgage monthly payments. 

These studies contribute to the understanding and development of the First Lien PD Model.

### 7. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8539 | CP: 0.5139 | CR: 0.3750 | AC: 0.7500 | NS: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and other income shocks from those induced purely by negative equity.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent and notes the greater impact of credit scores on subprime low-doc delinquency rates compared to similar full-doc loans.
3. Krainer and Laderman (2011) - This study finds that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest academic default risk models, showing that the borrower’s level of home equity at the time of origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - Another example of mortgage PD models referenced in the literature.
6. Elul, Souleles, et al. (2010) - This paper is also cited as part of the literature informing the model.
7. An, Deng, and Gabriel (2021) - This study is mentioned as part of the academic literature that the Board draws upon.

These studies collectively inform the design and specification of the First Lien Model, particularly regarding factors influencing mortgage defaults.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.7855 | CP: 0.7042 | CR: 0.3750 | AC: 0.3968 | NS: 0.1667

The first lien model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the roles of LTV and job loss in mortgage defaults.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent and notes the greater impact of credit scores on subprime low-doc delinquency rates compared to full-doc loans.
3. Krainer and Laderman (2011) - This study indicates that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest studies that developed a default risk model, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - Another example of research contributing to mortgage PD models.
6. Elul, Souleles, et al. (2010) - This study is also referenced in the context of mortgage modeling.
7. An, Deng, and Gabriel (2021) - This is another example of literature that informs the first lien model.

These studies collectively inform the model's design, variables, and transformations.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9143 | CP: 0.6458 | CR: 0.3750 | AC: 0.5326 | NS: 0.4000

The first lien model draws on various studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the roles of LTV and job loss in mortgage defaults.
2. Elul (2009), which finds that low credit score borrowers have a higher risk of becoming delinquent and notes the greater impact of credit scores on subprime low-doc delinquency rates compared to full-doc loans.
3. Krainer and Laderman (2011), which indicates that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg's work from the late 1960s, which developed the first academic default risk model, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Other examples of mortgage PD models include Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng, and Gabriel (2021).

These studies provide useful context for developing an accurate and robust model of first lien probability of default (PD).

### 10. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.7959 | CP: 0.8833 | CR: 0.3750 | AC: n/a | NS: 0.2500

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and other income shocks from those induced purely by negative equity.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent and notes the impact of credit scores on subprime low-doc delinquency rates.
3. Krainer and Laderman (2011) - This study finds that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - Developed the first academic default risk model, showing that the borrower’s level of home equity at the time of origination was the most important predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - Analyzed the subprime mortgage crisis.
6. Elul, Souleles, et al. (2010) - Investigated what triggers mortgage default.
7. An, Deng, and Gabriel (2021) - Studied default option exercise over the financial crisis and beyond.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, job loss, credit scores, and borrower characteristics.

### 11. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.7853 | CP: 0.8722 | CR: 0.3750 | AC: 0.4191 | NS: 0.5714

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," which distinguishes between defaults induced by job losses and those induced by negative equity.
2. Elul (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," which finds that low credit score borrowers have a higher risk of becoming delinquent.
3. Krainer and Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," which discusses the increase in mortgage defaults among borrowers with low credit scores during the financial crisis.
4. von Furstenberg (1969) - developed the first academic default risk model, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - "Understanding the Subprime Mortgage Crisis."
6. Elul, Souleles, et al. (2010) - "What ‘Triggers’ Mortgage Default?"
7. An, Deng, and Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond."

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, job loss, credit scores, and borrower equity.

### 12. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7853 | CP: 0.8711 | CR: 0.3750 | AC: 0.4195 | NS: 0.5000

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," which distinguishes between defaults induced by job losses and those induced purely by negative equity.
2. Elul (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," which finds that low credit score borrowers have a higher risk of becoming delinquent.
3. Krainer and Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," which discusses the increase in mortgage defaults among borrowers with low credit scores during the financial crisis.
4. von Furstenberg (1969) - developed the first academic default risk model, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - "Understanding the Subprime Mortgage Crisis."
6. Elul, Souleles, et al. (2010) - "What ‘Triggers’ Mortgage Default?"
7. An, Deng, and Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond."

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios (LTV), job loss, credit scores, and borrower equity positions.

### 13. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.7854 | CP: 0.6595 | CR: 0.3750 | AC: n/a | NS: 0.4000

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.

These studies provide insights into the factors influencing mortgage defaults, including loan-to-value ratios (LTV), job loss, credit scores, and borrower equity.

### 14. `chunk_size_500_chunk_overlap_300` — F: 0.5556 | AR: 0.9313 | CP: 0.3333 | CR: 0.0000 | AC: 0.1522 | NS: 0.0000

The first lien model draws on various studies and academic literature, including:

1. von Furstenberg, G. (1969). “Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis,” Journal of Finance 24(2): 459-77.
2. von Furstenberg, G. (1970a). “Interstate.”
3. Demyanyk and Van Hemert (2011).
4. Elul, Souleles, et al. (2010).
5. An, Deng and Gabriel (2021).

Additionally, it is informed by a review of the relevant literature and industry best practices, as well as statistical fit and modeler expert judgment.

### 15. `chunk_size_1000_chunk_overlap_300` — F: n/a | AR: 0.9487 | CP: 0.4583 | CR: 0.2500 | AC: n/a | NS: n/a

The First Lien Model draws on several studies and academic literature, including:

1. von Furstenberg's work from the late 1960s, which developed the first academic default risk model and identified the borrower's level of home equity at origination as a key predictor of mortgage default.
2. Demyanyk and Van Hemert (2011), which discusses the subprime mortgage crisis.
3. Elul, Souleles, et al. (2010), which examines various factors influencing mortgage defaults.
4. An, Deng, and Gabriel (2021), which contributes to the understanding of mortgage default risk.
5. Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of loan-to-value (LTV) ratios and unemployment rates.
6. Elul (2009), which finds that low credit score borrowers have a higher risk of delinquency.

These studies provide insights into the factors influencing mortgage default risk, which the Board incorporates into the First Lien PD Model.

### 16. `chunk_size_2000_chunk_overlap_200` — F: n/a | AR: 0.7927 | CP: 0.4028 | CR: 0.3750 | AC: n/a | NS: n/a

The first lien model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and other income shocks from those induced purely by negative equity.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent and notes the greater impact of credit scores on subprime low-doc delinquency rates compared to similar full-doc loans.
3. Krainer and Laderman (2011) - This study finds that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - Developed the first academic default risk model, showing that the borrower’s level of home equity at the time of origination was the most important predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - Another example of mortgage PD models developed and estimated.
6. Elul, Souleles, et al. (2010) - Contributes to the body of literature on mortgage defaults.
7. An, Deng, and Gabriel (2021) - Also part of the literature informing the model.

These studies provide useful context for developing an accurate and robust model of first lien probability of default (PD).

---

## Question 6: How does the home equity model leverage the Zillow price database?

### 1. `chunk_size_500_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 2. `chunk_size_500_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 3. `chunk_size_500_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 4. `chunk_size_500_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

---

## Question 7: What did Alan Greenspan say about the stress test reform announcement?

### 1. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 2. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 3. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 4. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

---

## Question 8: What was Michael Jackson's top selling album?

### 1. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 2. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 3. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 4. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: n/a | AC: n/a | NS: n/a

I don't know.

---

## Question 9: Under the expected loss approach, what three components are used to estimate expected loan losses?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9473 | CP: 0.6726 | CR: 1.0000 | AC: 0.5658 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are the probability of default (PD), loss given default (LGD), and exposure at default (EAD).

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9473 | CP: 0.5833 | CR: 1.0000 | AC: 0.9126 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are: 

1. Estimated probability of default (𝑃𝑃𝐷𝐷𝑖𝑖,𝑡𝑡)
2. Estimated loss given default (𝐿𝐿𝐿𝐿𝐷𝐷𝑖𝑖,𝑡𝑡)
3. Exposure at default (𝐸𝐸𝐸𝐸𝐷𝐷𝑖𝑖)

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.8969 | CP: 0.6361 | CR: 1.0000 | AC: 0.9219 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are the probability of default, loss given default, and exposure at default.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9473 | CP: 0.6042 | CR: 1.0000 | AC: 0.5648 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are Probability of Default (PD), Loss Given Default (LGD), and Exposure at Default (EAD).

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9473 | CP: 0.9107 | CR: 1.0000 | AC: 0.8337 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are the probability of default (PD), loss given default (LGD), and exposure at default (EAD).

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9473 | CP: 0.8708 | CR: 1.0000 | AC: 0.4051 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are the probability of default (PD), loss given default (LGD), and exposure at default (EAD).

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9473 | CP: 0.5422 | CR: 1.0000 | AC: 0.8315 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are: 

1. Probability of Default (PD)
2. Loss Given Default (LGD)
3. Exposure at Default (EAD)

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9473 | CP: 0.8560 | CR: 1.0000 | AC: 0.8565 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are Probability of Default (PD), Loss Given Default (LGD), and Exposure at Default (EAD).

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9473 | CP: 0.5099 | CR: 1.0000 | AC: 0.8318 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are:

1. Probability of Default (PD)
2. Loss Given Default (LGD)
3. Exposure at Default (EAD)

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9473 | CP: 0.5099 | CR: 1.0000 | AC: 0.8318 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are:

1. Probability of Default (PD)
2. Loss Given Default (LGD)
3. Exposure at Default (EAD)

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9473 | CP: 0.4988 | CR: 1.0000 | AC: 0.8318 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are:

1. Probability of Default (PD)
2. Loss Given Default (LGD)
3. Exposure at Default (EAD)

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9473 | CP: 0.4965 | CR: 1.0000 | AC: 0.8318 | NS: 0.0000

The three components used to estimate expected loan losses under the expected loss approach are:

1. Probability of Default (PD)
2. Loss Given Default (LGD)
3. Exposure at Default (EAD)

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9304 | CP: 0.7183 | CR: 1.0000 | AC: 0.8145 | NS: 0.0000

Under the expected loss approach, the three components used to estimate expected loan losses are the probability of default, loss given default, and exposure at default.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8969 | CP: 0.7183 | CR: 1.0000 | AC: 0.8145 | NS: 0.0000

Under the expected loss approach, the three components used to estimate expected loan losses are the probability of default, loss given default, and exposure at default.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8969 | CP: 0.7183 | CR: 1.0000 | AC: 0.8145 | NS: 0.0000

Under the expected loss approach, the three components used to estimate expected loan losses are the probability of default, loss given default, and exposure at default.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8969 | CP: 0.7183 | CR: 1.0000 | AC: 0.8145 | NS: 0.0000

Under the expected loss approach, the three components used to estimate expected loan losses are the probability of default, loss given default, and exposure at default.

---

## Question 10: What is the primary function of the operational-risk loss model in the supervisory stress test?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.7470 | CR: 1.0000 | AC: 0.3165 | NS: 0.8000

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly losses over the projection horizon for each supervisory stress test scenario, comprehensively stress testing firms to operational risk and producing stressful operational losses that could be systemic, correlated among several firms, or specific to individual firms.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.7278 | CR: 1.0000 | AC: 0.5765 | NS: 0.8333

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses over the projection horizon for each supervisory stress test scenario, taking into account key firm characteristics such as the size of the firm and its historical operational losses.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.8179 | CR: 1.0000 | AC: 0.3358 | NS: 0.6000

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses over the projection horizon for each supervisory stress test scenario. It aims to produce stressful operational losses that could be systemic for many firms, correlated among several firms, or specific to individual firms.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.5250 | CR: 1.0000 | AC: 0.4633 | NS: 0.0000

The primary function of the operational-risk loss model in the supervisory stress test is to estimate potential operational losses over hypothetical stress scenarios.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.4333 | CR: 0.0000 | AC: 0.4424 | NS: 0.5000

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in hypothetical stress scenarios. It aims to comprehensively assess potential operational losses that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.6042 | CR: 1.0000 | AC: 0.4422 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in various stress scenarios. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.6042 | CR: 0.0000 | AC: 0.5010 | NS: 0.8000

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over the projection horizon under various stress test scenarios. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated across several firms, or specific to individual firms.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.6389 | CR: 1.0000 | AC: 0.7633 | NS: 0.0000

The primary function of the operational-risk loss model in the supervisory stress test is to estimate potential operational losses over a hypothetical stress scenario.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5889 | CR: 1.0000 | AC: 0.7633 | NS: 0.0000

The primary function of the operational-risk loss model in the supervisory stress test is to estimate potential operational losses over a hypothetical stress scenario.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.4413 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in various stress scenarios. It aims to comprehensively assess potential operational losses that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.6201 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in a hypothetical stress scenario. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.4429 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in a hypothetical stress scenario. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.4429 | NS: 1.0000

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in a hypothetical stress scenario. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9994 | CP: 0.5000 | CR: 1.0000 | AC: 0.5032 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in a hypothetical stress scenario. It aims to comprehensively assess potential operational losses that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.4429 | NS: 0.6667

The primary function of the operational-risk loss model in the supervisory stress test is to project quarterly operational losses for firms over a projection horizon in a hypothetical stress scenario. It aims to comprehensively assess potential operational losses, including those that could be systemic, correlated among several firms, or specific to individual firms, particularly during stressful periods.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 1.0000 | AC: 0.0266 | NS: 0.0000

I don't know.

---

## Question 11: Why does the Federal Reserve model operational risk losses separately from pre-provision net revenue (PPNR)?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.9762 | CR: 1.0000 | AC: 0.3967 | NS: 0.6000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational losses tend to exhibit distinct characteristics, such as a heavy-tailed distribution. This separation allows for a more accurate estimation of operational losses, which include losses from events like fraud, computer system failures, process errors, and lawsuits. By treating operational risk as a separate component, the Federal Reserve can better capture the unique nature of these losses and improve the transparency of the model.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.7087 | CR: 1.0000 | AC: 0.5532 | NS: 0.4000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that are idiosyncratic in nature. These losses stem from events such as fraud, computer system failures, process errors, and lawsuits, which are sufficiently different from the remaining PPNR components. As a result, the Board judged that separate modeling approaches for operational risk losses and other PPNR components are justified.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5687 | CR: 1.0000 | AC: 0.6037 | NS: 0.8000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that are idiosyncratic in nature. These losses stem from events such as fraud, computer system failures, process errors, and lawsuits, which are sufficiently different from the remaining PPNR components. This justifies the use of separate modeling approaches for operational risk losses and other components of PPNR.

### 4. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.4972 | CR: 1.0000 | AC: 0.6663 | NS: 0.6000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that differentiate them from other components of PPNR. Operational risk losses arise from events such as fraud, computer system failures, process errors, and lawsuits, which are inherently idiosyncratic and challenging to capture within the broader PPNR framework. This separation allows for a more accurate estimation of potential operational losses over the hypothetical stress scenario.

### 5. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.6807 | CR: 1.0000 | AC: 0.5026 | NS: 0.6667

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that differentiate them from other components of PPNR. Operational risk losses arise from events such as fraud, computer system failures, process errors, and lawsuits, which are inherently idiosyncratic and challenging to capture under stress scenarios. This separation allows for a more accurate estimation of potential operational losses over the hypothetical stress scenario, as these losses have unique behaviors that may not correlate with the overall revenue and expense components of PPNR.

### 6. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.6605 | CR: 1.0000 | AC: 0.4446 | NS: 0.8750

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses "tend to exhibit distinct characteristics." This separation is necessary due to the idiosyncratic nature of operational risk losses, which can arise from events such as fraud, computer system failures, process errors, and lawsuits, making them inherently challenging to capture under stress scenarios.

### 7. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.6883 | CR: 1.0000 | AC: 0.4708 | NS: 0.8571

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses "tend to exhibit distinct characteristics." This separation is necessary due to the idiosyncratic nature of operational risk losses, which can stem from events such as fraud, computer system failures, process errors, and lawsuits. These characteristics make it challenging to capture their behavior under stress within the broader PPNR framework, which includes various revenue and expense components that are influenced by macroeconomic variables.

### 8. `chunk_size_500_chunk_overlap_300` — F: 0.9000 | AR: 1.0000 | CP: 0.5704 | CR: 1.0000 | AC: 0.3947 | NS: 0.8000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational losses tend to exhibit distinct characteristics, such as a heavy-tailed distribution. This separation allows for a more accurate estimation of potential operational losses, which stem from events like fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 9. `chunk_size_3000_chunk_overlap_50` — F: 0.8571 | AR: 1.0000 | CP: 0.6605 | CR: 1.0000 | AC: 0.3227 | NS: 0.6667

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that are different from other components of PPNR. This separation is necessary due to the idiosyncratic nature of operational risk losses, which can stem from events such as fraud, computer system failures, process errors, and lawsuits. These losses are inherently challenging to capture under stress, even when robust historical data are available, necessitating a distinct modeling approach.

### 10. `chunk_size_3000_chunk_overlap_200` — F: 0.8571 | AR: 1.0000 | CP: 0.6726 | CR: 1.0000 | AC: 0.5061 | NS: 0.8571

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that are different from other components of PPNR. This separation is necessary due to the idiosyncratic nature of operational risk losses, which can arise from events such as fraud, computer system failures, process errors, and lawsuits. These losses are inherently challenging to capture under stress, even when robust historical data are available, necessitating a distinct modeling approach.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.8333 | AR: 1.0000 | CP: 0.4750 | CR: 1.0000 | AC: 0.4706 | NS: 0.5000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses are judged to be sufficiently different in nature from the remaining components of PPNR. This separation allows for distinct modeling approaches that can better capture the unique characteristics and risks associated with operational losses, which may not be directly related to the bank's overall revenue or performance metrics used in PPNR.

### 12. `chunk_size_1000_chunk_overlap_300` — F: 0.8000 | AR: 1.0000 | CP: 0.4444 | CR: 1.0000 | AC: 0.5457 | NS: 0.6000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses tend to exhibit distinct characteristics that are idiosyncratic in nature. This separation allows for a more accurate estimation of potential operational losses over hypothetical stress scenarios, as operational risk losses stem from events such as fraud, computer system failures, process errors, and lawsuits, which require specific modeling approaches to capture their behavior under stress.

### 13. `chunk_size_500_chunk_overlap_200` — F: 0.7500 | AR: 0.9751 | CP: 1.0000 | CR: 1.0000 | AC: 0.4382 | NS: 0.6250

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses "tend to exhibit distinct characteristics." This separation allows for a more accurate assessment of operational risk, which includes losses stemming from events such as fraud, computer system failures, process errors, and lawsuits, rather than conflating these losses with the broader PPNR projections.

### 14. `chunk_size_500_chunk_overlap_50` — F: 0.7000 | AR: 1.0000 | CP: 0.6083 | CR: 1.0000 | AC: 0.3963 | NS: 0.6000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational losses tend to exhibit distinct characteristics, such as a heavy-tailed distribution. This separation allows for a more accurate estimation of these losses, which stem from events like fraud, computer system failures, process errors, and lawsuits. By treating operational risk losses independently, the Federal Reserve can better capture the unique nature of these risks compared to other components of PPNR.

### 15. `chunk_size_2000_chunk_overlap_300` — F: 0.6667 | AR: 1.0000 | CP: 0.3833 | CR: 1.0000 | AC: 0.9248 | NS: 0.3333

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) because operational risk losses and other components of PPNR, such as net interest income and noninterest income, are judged to be sufficiently different in nature. This separation allows for more accurate modeling approaches, as operational risk events and other real estate owned expenses are distinct from the remaining PPNR components. Additionally, the Board makes adjustments to eliminate or minimize potential double-counting of losses, further justifying the separate modeling of operational risk.

### 16. `chunk_size_1000_chunk_overlap_200` — F: 0.5714 | AR: 1.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.3069 | NS: 0.0000

The Federal Reserve models operational risk losses separately from pre-provision net revenue (PPNR) to improve the measure of operational risk exposure and to mitigate certain assumptions regarding the timing of operational loss events. This separation allows for a more accurate assessment of operational risks without the influence of the broader PPNR projections, which can be heavily influenced by backward-looking terms and may not adequately capture the dynamics of operational risk.

---

## Question 12: What specific types of events are captured by the Operational Risk Model?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8617 | CP: 0.2296 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9086 | CP: 0.1825 | CR: 1.0000 | AC: 0.3251 | NS: 0.8750

The Operational Risk Model captures losses from the following event types:

1. Clients, Products, and Business Practices (CPBP) - 72.5%
2. Execution, Delivery, and Process Management (EDPM) - 14.8%
3. External Fraud (EF) - 4.9%
4. Employment Practices and Worker Safety (EPWS) - 3.0%
5. Internal Fraud (IF) - 2.3%
6. Business Disruption and System Failures (BDSF) - 1.3%
7. Damage to Physical Assets (DPA) - 1.2%

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.8617 | CP: 0.6333 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8617 | CP: 0.2619 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9648 | CP: 0.2000 | CR: 0.7500 | AC: 0.3291 | NS: 0.8750

The Operational Risk Model captures the following specific types of events:

1. Clients, Products, and Business Practices (CPBP) - 72.5% of total losses
2. Execution, Delivery, and Process Management (EDPM) - 14.8% of total losses
3. External Fraud (EF) - 4.9% of total losses
4. Employment Practices and Worker Safety (EPWS) - 3.0% of total losses
5. Internal Fraud (IF) - 2.3% of total losses
6. Business Disruption and System Failures (BDSF) - 1.3% of total losses
7. Damage to Physical Assets (DPA) - 1.2% of total losses

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8617 | CP: 0.2917 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8617 | CP: 0.2250 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8617 | CP: 0.7500 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8617 | CP: 0.4028 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8617 | CP: 0.5139 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8617 | CP: 0.5833 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8617 | CP: 0.5833 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8617 | CP: 0.5833 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8617 | CP: 0.5833 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8617 | CP: 0.5556 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8617 | CP: 0.5833 | CR: 1.0000 | AC: 0.9323 | NS: 0.0000

The Operational Risk Model captures losses stemming from events such as fraud, computer system failures, process errors, and lawsuits by employees, customers, or other parties.

---

## Question 13: What is the time horizon for the projection of net income and capital components?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.5238 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.7778 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.4157 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.7500 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.8218 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5405 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.7611 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.6089 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.6726 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.9367 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.5250 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.4768 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.5629 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5629 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.5629 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.7345 | CR: 1.0000 | AC: 0.6721 | NS: 0.0000

The time horizon for the projection of net income and capital components is nine quarters.

---

## Question 14: What notable update will be made to the Fair Value Option model for the 2026 stress test?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9743 | CP: 0.5000 | CR: 0.0000 | AC: 0.1294 | NS: 0.0000

The notable update to the Fair Value Option model for the 2026 stress test is that it will project gains and losses on loans subject to fair value accounting, and these projections will enter as “other losses/gains” into the Board’s calculation of pre-tax net income in the stress test.

### 2. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9745 | CP: 0.3611 | CR: 0.5000 | AC: 0.8131 | NS: 0.0000

The notable update to the Fair Value Option model for the 2026 stress test will be to lower the loss given default assumption amount and loan equivalent factor parameter.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9513 | CP: 0.3651 | CR: 1.0000 | AC: 0.9498 | NS: 0.2500

For the 2026 stress test, the Fair Value Option model will be adjusted to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions, with the model assuming a constant LGD of 50 percent.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9745 | CP: 0.2111 | CR: 1.0000 | AC: 0.6239 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.6695 | CP: 0.4028 | CR: 1.0000 | AC: 0.7109 | NS: 0.4000

The Fair Value Option model will be adjusted to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. Specifically, the model will assume a constant LGD of 50 percent and set the LEQ for corporate loans at 65 percent.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9745 | CP: 0.4028 | CR: 1.0000 | AC: 0.7938 | NS: 0.8000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt a lower loss given default (LGD) assumption, which will be set to a constant 50 percent, calibrated to historical loan recovery outcomes. Additionally, the loan-equivalent-factor (LEQ) for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9730 | CP: 0.4021 | CR: 1.0000 | AC: 0.6238 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9745 | CP: 0.1429 | CR: 1.0000 | AC: 0.6239 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9715 | CP: 0.1250 | CR: 1.0000 | AC: 0.6238 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9745 | CP: 0.1667 | CR: 1.0000 | AC: 0.6239 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adjustment to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9513 | CP: 0.1667 | CR: 1.0000 | AC: 0.6530 | NS: 0.7143

For the 2026 stress test, the Fair Value Option model will be adjusted to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9700 | CP: 0.2000 | CR: 1.0000 | AC: 0.6246 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adoption of lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9700 | CP: 0.2000 | CR: 1.0000 | AC: 0.8628 | NS: 0.6000

The notable update to the Fair Value Option model for the 2026 stress test will be the adoption of lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.6699 | CP: 0.2000 | CR: 1.0000 | AC: 0.7111 | NS: 0.6000

The Fair Value Option model will be adjusted to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.6695 | CP: 0.2000 | CR: 1.0000 | AC: 0.6202 | NS: 0.6000

The Fair Value Option model will be adjusted to adopt lower loss given default (LGD) and loan-equivalent-factor (LEQ) assumptions. The model will assume a constant LGD of 50 percent, calibrated to historical loan recovery outcomes, and the LEQ for corporate loans will be set at 65 percent to better reflect historical patterns of utilization rates.

### 16. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0185 | NS: 0.0000

I don't know.

---

## Question 15: How will the compensation model be enhanced in the 2026 supervisory stress test?

### 1. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.2361 | CR: 1.0000 | AC: 0.6165 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 2. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.2917 | CR: 1.0000 | AC: 0.7504 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 3. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.2917 | CR: 1.0000 | AC: 0.6165 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 4. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.2917 | CR: 1.0000 | AC: 0.7504 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 5. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.3095 | CR: 1.0000 | AC: 0.6165 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 6. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.3095 | CR: 1.0000 | AC: 0.7507 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement aims to account for the heterogeneity of business lines and compensation practices across firms.

### 7. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.3095 | CR: 1.0000 | AC: 0.7507 | NS: 0.6000

The compensation model will be enhanced in the 2026 supervisory stress test by adjusting the projections of compensation expenses to condition them on the share of compensation paid in commissions and stocks. This enhancement aims to account for the heterogeneity of business lines and compensation practices across firms.

### 8. `chunk_size_3000_chunk_overlap_100` — F: 0.7500 | AR: 1.0000 | CP: 0.3095 | CR: 1.0000 | AC: 0.6959 | NS: 0.7500

The compensation model will be enhanced in the 2026 supervisory stress test by conditioning the projections of compensation expenses on the share of compensation paid in commissions and stocks. This enhancement is intended to account for the heterogeneity of business lines and compensation practices across firms.

### 9. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.8125 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 10. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.7611 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 11. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.8333 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 12. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.8333 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 13. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.7117 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 14. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.6783 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 15. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.6644 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

### 16. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.6644 | CR: 0.0000 | AC: 0.0158 | NS: 0.0000

I don't know.

---

## Question 16: What is the 'constant balance sheet assumption' used by the Board in its projections?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9724 | CP: 0.8783 | CR: 1.0000 | AC: 0.1775 | NS: 0.0000

The 'constant balance sheet assumption' used by the Board in its projections means that the Board assumes a firm's balance sheet will remain unchanged throughout the projection horizon. This includes holding the values of total assets, risk-weighted assets, and leverage ratio denominators constant, except for adjustments related to regulatory capital calculations or changes in the Board's regulations. The assumption simplifies the modeling process and ensures consistency across projections.

### 2. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.5861 | NS: 0.2857

The 'constant balance sheet assumption' used by the Board in its projections refers to the practice of holding a firm's total assets, risk-weighted assets, and leverage ratio denominators constant over the projection horizon. This assumption is intended to promote consistency and comparability across firms, prevent firms from assuming they could "shrink to health," and ensure that firms remain sufficiently capitalized to accommodate credit demand during severe downturns.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9690 | CP: 0.9068 | CR: 1.0000 | AC: 0.5484 | NS: 0.5000

The 'constant balance sheet assumption' used by the Board in its projections refers to maintaining a flat balance sheet for each quarter of the stress test horizon. This means that the Board assumes a firm's total assets remain unchanged over the projection period, implicitly assuming that a firm originates new bonds each quarter with the same security type and broad rating to ensure that each quarter's portfolio is identical.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9718 | CP: 0.7714 | CR: 1.0000 | AC: 0.5989 | NS: 0.4286

The 'constant balance sheet assumption' used by the Board in its projections means that the Board assumes that a firm's balance sheet will remain unchanged throughout the projection horizon. This includes maintaining the current level of assets, such as investment securities, trading assets, and loans, as well as keeping risk-weighted assets and leverage ratio denominators constant, except for changes related to regulatory capital calculations or changes to the Board's regulations. This assumption promotes consistency and comparability across firms and helps ensure that firms remain sufficiently capitalized to accommodate credit demand during economic stress.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.7838 | CP: 0.7968 | CR: 1.0000 | AC: 0.6525 | NS: 0.2857

The 'constant balance sheet assumption' used by the Board in its projections means that the Board assumes a firm takes actions to maintain its current level of assets, including investment securities, trading assets, and loans, over the projection horizon. This assumption implies that a firm's total assets do not change during the projection period, and it allows for consistency and comparability across firms. To maintain this assumption, firms must purchase new securities to offset the impact of maturing or decreasing balances due to partial paydowns.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.9594 | CR: 1.0000 | AC: 0.5137 | NS: 0.3000

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm will maintain its current level of assets, including investment securities, trading assets, and loans, throughout the projection horizon. This means that the firm's risk-weighted assets and leverage ratio denominators are also assumed to remain unchanged, except for changes related to regulatory capital calculations or changes to the Board's regulations. This assumption is intended to promote consistency and comparability across firms and to ensure that firms remain sufficiently capitalized to accommodate credit demand during severe economic downturns. It prevents firms from assuming they could "shrink to health" and allows supervisors to evaluate the health of the banking sector as firms continue to lend during times of economic stress.

### 7. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.9750 | CR: 1.0000 | AC: 0.6442 | NS: 0.6250

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm will take actions to maintain its current level of assets, including investment securities, trading assets, and loans, over the projection horizon. This means that the firm's risk-weighted assets and leverage ratio denominators are assumed to remain unchanged throughout the projection period, except for changes related to regulatory capital calculations or changes to the Board's regulations. This assumption promotes consistency and comparability across firms and simplifies the modeling process by avoiding predictions about how each firm's balance sheet would change under stressful economic conditions.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.9478 | CR: 1.0000 | AC: 0.5693 | NS: 0.6250

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm takes actions to maintain its current level of assets, including investment securities, trading assets, and loans, over the projection horizon. This means that the firm's risk-weighted assets and leverage ratio denominators are assumed to remain unchanged, promoting consistency and comparability across firms and simplifying the modeling process. The assumption prevents firms from assuming they could "shrink to health" and helps ensure they remain sufficiently capitalized to accommodate credit demand during severe downturns.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.9821 | CR: 1.0000 | AC: 0.3513 | NS: 0.6667

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm takes actions to maintain, but not grow, its current level of assets over the planning horizon under stress. This approach promotes consistency and comparability across firms and reduces the complexity of the model. It prevents firms from assuming they could "shrink to health" and helps ensure that firms remain sufficiently capitalized to accommodate credit demand in a severe downturn.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.8722 | CR: 1.0000 | AC: 0.3504 | NS: 0.5714

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm takes actions to maintain, but not grow, its current level of assets over the planning horizon under stress. This assumption promotes consistency and comparability across firms and reduces the complexity of the model. It prevents firms from assuming they could "shrink to health" and helps ensure that firms remain sufficiently capitalized to accommodate credit demand in a severe downturn.

### 11. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.7282 | CR: 1.0000 | AC: 0.4846 | NS: 0.6667

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm takes actions to maintain, but not grow, its current level of assets over the planning horizon under stress. This approach promotes consistency and comparability across firms and reduces the complexity of the model. It prevents firms from assuming they could "shrink to health" and helps ensure that firms remain sufficiently capitalized to accommodate credit demand in a severe downturn.

### 12. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.5050 | CR: 1.0000 | AC: 0.3513 | NS: 0.6667

The 'constant balance sheet assumption' used by the Board in its projections is the assumption that a firm takes actions to maintain, but not grow, its current level of assets over the planning horizon under stress. This approach promotes consistency and comparability across firms and reduces the complexity of the model. It prevents firms from assuming they could "shrink to health" and helps ensure that firms remain sufficiently capitalized to accommodate credit demand in a severe downturn.

### 13. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9793 | CP: 0.7440 | CR: 1.0000 | AC: 0.7777 | NS: 0.7143

The 'constant balance sheet assumption' used by the Board in its projections refers to the methodology where a firm is assumed to maintain, but not grow, its current level of assets over the projection horizon under stress. This assumption promotes consistency and comparability across firms and simplifies the model by avoiding the complexities of predicting how each firm's balance sheet would change under stressful economic conditions. It prevents firms from assuming they could "shrink to health" and helps ensure that they remain sufficiently capitalized to accommodate credit demand in a severe downturn.

### 14. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9690 | CP: 0.9240 | CR: 1.0000 | AC: 0.8371 | NS: 0.4286

The 'constant balance sheet assumption' used by the Board in its projections refers to the methodology where a firm's total assets are assumed to remain unchanged over the projection horizon. This means that the Board expects firms to maintain, but not grow, their current level of assets during stress testing. This approach promotes consistency and comparability across firms and simplifies the modeling process by avoiding the complexities of predicting how each firm's balance sheet would change under stressful economic conditions.

### 15. `chunk_size_500_chunk_overlap_100` — F: 0.8000 | AR: 0.7603 | CP: 0.7114 | CR: 1.0000 | AC: 0.3576 | NS: 0.0000

The 'constant balance sheet assumption' used by the Board in its projections means that a firm's total assets are assumed to remain unchanged over the projection horizon. To maintain this assumption, firms must purchase new securities during the projection period to offset the impact of securities maturing or decreasing in balance due to partial paydowns. This approach is intended to be simple and broadly applicable across all firms, as outlined in the Policy Statement.

### 16. `chunk_size_1000_chunk_overlap_100` — F: 0.5714 | AR: 0.9724 | CP: 0.8553 | CR: 1.0000 | AC: 0.1827 | NS: 0.5714

The 'constant balance sheet assumption' used by the Board in its projections means that the Board assumes a firm's total assets, risk-weighted assets, and leverage ratio denominators remain unchanged over the projection horizon. This assumption allows the Board to evaluate the health of the banking sector as firms continue to lend during times of economic stress, without needing to make assumptions about how underwriting standards might change across firms. The Board uses this assumption to facilitate the projections and ensure consistency and comparability across firms.

---

## Question 17: What is the 'look-ahead period' mentioned in the aggregation model documentation?

### 1. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9869 | CP: 0.5000 | CR: 1.0000 | AC: 0.1415 | NS: 0.8333

The 'look-ahead period' mentioned in the aggregation model documentation refers to the time frame that firms consider when estimating allowance for credit losses, specifically in relation to the difference between the supervisory calculation of allowances and the firm’s reported allowance as of the effective date of the stress test exercise. This period can range from a one-quarter look-ahead, which assumes firms have perfect foresight into their expected losses, to a longer look-ahead that allows for the time firms may need to adapt their expectations to meet stressful conditions.

### 2. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9869 | CP: 0.5000 | CR: 1.0000 | AC: 0.2999 | NS: 1.0000

The 'look-ahead period' mentioned in the aggregation model documentation refers to the time frame that firms consider for estimating allowance for credit losses under the CECL methodology. It can range from a one-quarter look-ahead, which assumes firms have perfect foresight into their expected losses, to a longer look-ahead period that assumes firms take time to adapt their expectations to meet the stressful conditions of a severely adverse scenario.

### 3. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9869 | CP: 0.5000 | CR: 1.0000 | AC: 0.3066 | NS: 1.0000

The 'look-ahead period' mentioned in the aggregation model documentation refers to the time frame used to incorporate forward-looking information for estimating allowance for credit losses. It could range from a one-quarter look-ahead, which assumes firms have perfect foresight into their expected losses, to a look-ahead lasting several quarters, which assumes firms take time to adapt their expectations to meet the stressful conditions of a severely adverse scenario.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9869 | CP: 0.5833 | CR: 1.0000 | AC: 0.2980 | NS: 1.0000

The 'look-ahead period' mentioned in the aggregation model documentation refers to the time frame that firms consider when estimating allowances for credit losses under the CECL methodology. It can range from a one-quarter look-ahead, which assumes firms have perfect foresight into their expected losses, to a longer look-ahead period that assumes firms take time to adapt their expectations to meet stressful conditions.

### 5. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 6. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 7. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 8. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.3333 | CR: 1.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 16. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

---

## Question 18: What is the 'Projections Calculator' in the aggregation framework?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9612 | CP: 0.6333 | CR: 1.0000 | AC: 0.3211 | NS: 1.0000

The 'Projections Calculator' in the aggregation framework is a tool that sources data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It aggregates and renames regulatory reporting items for use in supervisory stress testing models, constructs scaling factors to ensure loan values are accurately reported, and produces final projections of loss dollars for firms in the portfolio across different quarters. The calculator also makes modifications to the data to ensure compatibility with downstream models and holds aggregated values constant throughout the projection horizon.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9612 | CP: 0.7250 | CR: 1.0000 | AC: 0.2786 | NS: 0.5833

The 'Projections Calculator' in the aggregation framework is a tool that renames and aggregates regulatory reporting items for use in supervisory stress testing models. It aggregates total domestic first lien residential mortgages from corresponding items on FR Y-14Q, Schedule M (Balances), and applies a scaling factor to ensure that the loan values reported are consistent with the projected values. The Projections Calculator methodology does not capture the actual reported balances but instead holds aggregated values constant throughout the projection horizon. It is used to calculate inputs for supervisory credit risk models and to project total loss dollars by summing projected losses on the existing portfolio and projected new origination balances.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9612 | CP: 0.5333 | CR: 1.0000 | AC: 0.3280 | NS: 0.7000

The 'Projections Calculator' in the aggregation framework is a tool that replaces missing values in regulatory reports with zeroes, renames and aggregates regulatory reporting items for use in supervisory stress testing models, and collects a comprehensive set of balance sheet and risk-weighted asset items from firms’ regulatory reports. It serves as an input for the Board’s supervisory stress testing models by holding aggregated values constant throughout the projection horizon, without capturing the actual expected evolution of balances at individual firms or in the banking industry under stress.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9707 | CP: 0.5978 | CR: 1.0000 | AC: 0.2764 | NS: 0.7500

The 'Projections Calculator' in the aggregation framework is a tool that replaces missing values in regulatory reports with zeroes, renames and aggregates regulatory reporting items for use in supervisory stress testing models, and calculates inputs for supervisory credit risk models. It sources data from various regulatory reports, such as the FR Y-9C and FR Y-14Q, and applies a scaling factor to ensure consistency in the dollar values of loan portfolios used for projecting revenue and loan losses. The Projections Calculator also projects total loss dollars by summing projected losses on existing portfolios and new origination balances during the projection period.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9612 | CP: 0.3780 | CR: 1.0000 | AC: 0.2485 | NS: 0.7857

The 'Projections Calculator' in the aggregation framework is a tool that sources data from various regulatory reports, including the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It makes modifications to the data to ensure compatibility with downstream models, such as converting data from thousands of U.S. dollars to millions and replacing missing values with zeroes. The Projections Calculator is used to project loss dollars by applying model parameters to specific loans and producing loss rates, which are then utilized in the Retail Loss Aggregation process to project total loss dollars for each firm in the portfolio across different sub-portfolios and quarters.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9612 | CP: 0.5857 | CR: 1.0000 | AC: 0.2698 | NS: 0.2667

The 'Projections Calculator' in the aggregation framework is a tool that sources data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It renames and aggregates regulatory reporting items for use in supervisory stress testing models, facilitating compatibility with downstream models by making modifications to the data, such as converting values from thousands to millions of U.S. dollars and replacing missing values with zeroes. The Projections Calculator is used to project loss dollars for firms in a portfolio over a series of quarters, applying a top-down modeling approach and ensuring consistency in the dollar values of loans used for projecting revenue and loan losses.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.7219 | CP: 0.5426 | CR: 1.0000 | AC: 0.3013 | NS: 0.8750

The 'Projections Calculator' is a tool that collects a comprehensive set of balance sheet and risk-weighted asset items from firms’ regulatory reports and aggregates them to serve as inputs to the Board’s supervisory stress testing models. It replaces missing values in regulatory reports with zeroes, renames and aggregates regulatory reporting items, and holds aggregated values constant throughout the projection horizon. The Projections Calculator is designed to facilitate compatibility with downstream models and ensures that the dollar values of portfolios used for projecting revenue and loan losses are consistent.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9612 | CP: 0.9627 | CR: 1.0000 | AC: 0.2720 | NS: 1.0000

The 'Projections Calculator' in the aggregation framework is a methodology used to calculate inputs for supervisory credit risk models by aggregating loan balances from the FR Y-14Q, Schedule M (Balances) and applying a scaling factor to ensure consistency with total loans reported on the FR Y-9C. It does not capture the actual expected evolution of balances under stress and holds aggregated values constant throughout the projection horizon. The calculator also modifies data from various regulatory reports to facilitate compatibility with downstream models and projects total loss dollars by summing projected losses on the existing portfolio and projected new origination balances.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9612 | CP: 0.2250 | CR: 1.0000 | AC: 0.1705 | NS: 1.0000

The 'Projections Calculator' in the aggregation framework is a methodology used to aggregate line-items together and hold those values constant in each quarter of the projection horizon. It does not capture or reflect the actual expected evolution of balances at individual firms or in the banking industry under stress, as it lacks statistically calibrated parameters and does not perform back testing or sensitivity testing to monitor performance over time. The calculator uses a scaling factor to adjust aggregated loan balances from regulatory reports for supervisory credit risk models. If the scaling factor deviates significantly from 1, the Board may require a firm to resubmit its reports.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9612 | CP: 0.6111 | CR: 1.0000 | AC: 0.2594 | NS: 0.6667

The 'Projections Calculator' in the aggregation framework is a tool that renames and aggregates regulatory reporting items for use in supervisory stress testing models. It produces a path of noninterest income over the projection horizon by aggregating line-items together and holding those values constant in each quarter of the projection horizon. The calculator uses a scaling factor to monitor the alignment of reported loan balances across different regulatory reports and calculates inputs for supervisory credit risk models based on aggregated loan balances. However, it does not capture the actual expected evolution of balances at individual firms or in the banking industry under stress, as it lacks statistically calibrated parameters and does not perform back testing or sensitivity testing.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9612 | CP: 0.6667 | CR: 1.0000 | AC: 0.3765 | NS: 0.5714

The 'Projections Calculator' in the aggregation framework is a tool used to aggregate regulatory reporting items for supervisory stress testing models. It produces projections for various financial components, such as noninterest income, by using aggregate bank projections from the FR Y-14A schedules. The calculator holds these aggregated values constant throughout the projection horizon and does not capture the actual expected evolution of balances at individual firms or in the banking industry under stress. It also employs a scaling factor to monitor the alignment between reported loan balances on regulatory reports. If discrepancies arise, the Board may require firms to resubmit their reports.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9612 | CP: 0.6000 | CR: 1.0000 | AC: 0.3803 | NS: 0.9000

The 'Projections Calculator' in the aggregation framework is a tool used to source data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It makes modifications to the data to ensure compatibility with downstream models. The Projections Calculator aggregates line-items together and holds those values constant in each quarter of the projection horizon. It also calculates inputs for supervisory credit risk models by multiplying aggregated loan balances from FR Y-14Q, Schedule M (Balances) by a scaling factor, which is used as a monitoring tool. The scaling factor is expected to be close to 1, and deviations may require firms to resubmit their reports.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9612 | CP: 0.6000 | CR: 1.0000 | AC: 0.3052 | NS: 0.7500

The 'Projections Calculator' in the aggregation framework is a tool used to source data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It makes modifications to the data to ensure compatibility with downstream models. The Projections Calculator aggregates line-items together and holds those values constant in each quarter of the projection horizon, facilitating the calculation of inputs for supervisory credit risk models and the overall stress testing process. It also uses a scaling factor to monitor the alignment of reported loan balances across different regulatory reports.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9612 | CP: 0.5516 | CR: 1.0000 | AC: 0.2576 | NS: 0.8462

The 'Projections Calculator' is a tool used in the aggregation framework to source data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It makes modifications to the data to ensure compatibility with downstream models, such as converting data from thousands of U.S. dollars to millions of U.S. dollars and replacing missing values with zeroes. The Projections Calculator aggregates regulatory reporting items and holds these values constant over the projection horizon to facilitate the calculation of losses and revenue used for supervisory stress test projections.

### 15. `chunk_size_2000_chunk_overlap_50` — F: 0.8750 | AR: 0.9612 | CP: 0.2250 | CR: 1.0000 | AC: 0.2962 | NS: 0.6250

The 'Projections Calculator' in the aggregation framework is a tool used to aggregate line-items together and hold those values constant in each quarter of the projection horizon. It serves as a monitoring tool for the Projections Calculator methodology, which does not capture or reflect the actual expected evolution of balances at individual firms or in the banking industry under stress. The scaling factor, which is used in conjunction with the Projections Calculator, helps to ensure that aggregated loan balances from regulatory reports are aligned, and if it deviates significantly from 1, the Board may require a firm to resubmit its reports.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.6667 | AR: 0.9612 | CP: 0.6000 | CR: 1.0000 | AC: 0.2932 | NS: 0.5556

The 'Projections Calculator' in the aggregation framework is a tool used to source data from various regulatory reports, such as the Consolidated Financial Statements for Holding Companies (FR Y-9C), Regulatory Capital Reporting for Institutions Subject to the Advanced Capital Adequacy Framework (FFIEC 101), and FR Y-14Q, Schedule M (Balances). It makes modifications to the data to ensure compatibility with downstream models. The Projections Calculator aggregates line-items together and holds those values constant in each quarter of the projection horizon, facilitating the calculation of inputs for supervisory credit risk models and other projections used in stress testing. It also serves as a monitoring tool by calculating a scaling factor based on reported loan balances across different regulatory reports.

---

## Question 19: How is the national aggregate building stock constructed in the Corporate Model?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8660 | CP: 1.0000 | CR: 1.0000 | AC: 0.9696 | NS: 0.0000

The national aggregate building stock is constructed as a weighted average across individual markets, with weights based on the size of the market as measured in square feet of the building stock.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8660 | CP: 1.0000 | CR: 1.0000 | AC: 0.9696 | NS: 0.0000

The national aggregate building stock is constructed as a weighted average across individual markets, with weights being the size of the market as measured in square feet of the building stock.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8660 | CP: 1.0000 | CR: 1.0000 | AC: 0.9696 | NS: 0.0000

The national aggregate building stock is constructed as a weighted average across individual markets, with weights based on the size of the market as measured in square feet of the building stock.

### 4. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 5. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0291 | NS: 0.0000

I don't know.

### 6. `chunk_size_500_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 7. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 9. `chunk_size_1000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 10. `chunk_size_1000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.3333 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 13. `chunk_size_2000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.2500 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 14. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.3333 | CR: 1.0000 | AC: 0.7790 | NS: 0.0000

I don't know.

---

## Question 20: How are seasonal adjustments for the Corporate Model independent variables obtained?

### 1. `chunk_size_500_chunk_overlap_50` — F: 0.6667 | AR: 1.0000 | CP: 0.1667 | CR: 0.0000 | AC: 0.1252 | NS: 0.0000

Seasonal adjustments for the Corporate Model independent variables are obtained by including quarterly indicator variables in the regression model to capture regular seasonal variation in compensation expenses and trading revenues. These seasonal indicators help account for fluctuations driven by seasonal factors.

### 2. `chunk_size_500_chunk_overlap_100` — F: 0.6667 | AR: 0.9725 | CP: 0.0000 | CR: 0.0000 | AC: 0.1250 | NS: 0.0000

Seasonal adjustments for the Corporate Model independent variables are obtained by including quarterly indicator variables in the regression model to capture regular seasonal variation. This approach helps to account for fluctuations driven by seasonal factors.

### 3. `chunk_size_1000_chunk_overlap_300` — F: 0.6667 | AR: 0.9883 | CP: 0.2000 | CR: 1.0000 | AC: 0.7868 | NS: 0.0000

The seasonal adjustments for the Corporate Model independent variables are obtained by first seasonally adjusting each of the time series provided by the vendor according to the X11 procedure.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 0.3333 | AR: 1.0000 | CP: 0.3333 | CR: 1.0000 | AC: 0.7828 | NS: 0.0000

Seasonal adjustments for the Corporate Model independent variables are obtained by seasonally adjusting each of the time series provided by the vendor according to the X11 procedure.

### 5. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.1429 | CR: 1.0000 | AC: 0.0370 | NS: 0.0000

I don't know.

### 6. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.1429 | CR: 1.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 7. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.1250 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.1250 | CR: 0.0000 | AC: 0.0370 | NS: 0.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0370 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0369 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 1.0000 | AC: 0.0370 | NS: 0.0000

I don't know.

---

## Question 21: How is the 'weighted average' calculated for market size in square feet in the Corporate Model?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9627 | CP: 1.0000 | CR: 1.0000 | AC: 0.8051 | NS: 0.3333

The 'weighted average' for market size in square feet in the Corporate Model is calculated as a weighted average across individual markets, where the weights are the size of the market as measured in square feet of the building stock.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9059 | CP: 1.0000 | CR: 1.0000 | AC: 0.7623 | NS: 0.0000

The 'weighted average' for market size in square feet in the Corporate Model is calculated as a weighted average across individual markets, where the weights are determined by the size of the market as measured in square feet of the building stock.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9059 | CP: 0.7000 | CR: 1.0000 | AC: 0.8051 | NS: 0.0000

The 'weighted average' for market size in square feet in the Corporate Model is calculated as a weighted average across individual markets, where the weights are the size of the market as measured in square feet of the building stock.

### 4. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.1429 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.4111 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.1667 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.3206 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.6042 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.6220 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.4028 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.6042 | CR: 1.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

---

## Question 22: How does the Board handle newly originated loans in its constant balance sheet projections?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9502 | CP: 0.9167 | CR: 1.0000 | AC: 0.3166 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the 9 projection quarters, consistent with the constant balance assumption for the stress test exercise.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.7429 | CP: 0.7679 | CR: 1.0000 | AC: 0.4938 | NS: 0.5455

The Board assumes that newly originated loans have the same characteristics as those in the existing portfolio, consistent with the constant balance sheet assumption applied across the supervisory stress test models. Newly originated loans are considered unseasoned and should have zero months on book, meaning they are assumed to have been originated during the projection period and cannot be older vintages. Additionally, loans are assumed to be in current status at origination, and new HELOCs are assumed to have open lines, as open-endedness is a key feature of these loans. Any reduction in exposure from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter, ensuring that the portfolio balance remains unchanged.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9503 | CP: 0.8095 | CR: 1.0000 | AC: 0.1504 | NS: 0.4000

The Board handles newly originated loans in its constant balance sheet projections by adding them to replenish any reduction in exposure arising from default, prepayment, or amortization. This ensures that the portfolio balance remains unchanged throughout the projection horizon, consistent with the constant balance assumption for the stress test exercise. Newly originated loans are treated similarly to loan re-origination done for credit loss projections across the loan portfolio.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9503 | CP: 0.4444 | CR: 1.0000 | AC: 0.5400 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by adding them to replenish any reduction in exposure arising from default, prepayment, or amortization. This ensures that the portfolio balance remains unchanged throughout the projection quarters. Newly originated loans are treated as current (not delinquent), and their loan age and vintage fields are reset to zero.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.7685 | CP: 0.4746 | CR: 1.0000 | AC: 0.4950 | NS: 0.5000

The Board assumes that newly originated loans have the same characteristics as those in the existing portfolio, consistent with the constant balance sheet assumption applied across the supervisory stress test models. Newly originated loans are considered unseasoned and are assumed to have zero months on book. They are also assumed to have been originated during the projection period and cannot be older vintages. Any reduction in exposure from default, prepayment, or amortization is replenished by these newly originated loans within the same projection quarter, ensuring that the portfolio balance remains unchanged.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.5053 | CP: 0.3068 | CR: 1.0000 | AC: 0.1232 | NS: 0.7500

The Board assumes that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter, such that the portfolio balance remains unchanged. This approach is similar to loan re-origination done for the credit loss projections across the loan portfolio.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9503 | CP: 0.6444 | CR: 1.0000 | AC: 0.1381 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by adding them to the portfolio to replenish any reduction in exposure arising from default, prepayment, or amortization. This approach ensures that the portfolio balance remains unchanged throughout the projection horizon, consistent with the assumption that firms maintain constant balance sheets.

### 8. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9503 | CP: 0.7889 | CR: 1.0000 | AC: 0.1366 | NS: 0.7500

The Board handles newly originated loans in its constant balance sheet projections by adding them to replenish any reduction in exposure arising from default, prepayment, or amortization. This ensures that the portfolio balance remains unchanged throughout the projection horizon, consistent with the constant balance assumption for the stress test exercise.

### 9. `chunk_size_500_chunk_overlap_50` — F: 0.8750 | AR: 0.9502 | CP: 0.9889 | CR: 1.0000 | AC: 0.4519 | NS: 0.6000

The Board handles newly originated loans in its constant balance sheet projections by assuming that these loans are current (not delinquent) at the time of origination. The loan age field for these new originations is reset to zero, and the "vintage" fields, which are used to assess the enhanced risk of loans originated in certain years, are also reset to zero. This approach facilitates the flat balance sheet assumption while projecting loan-level balances.

### 10. `chunk_size_3000_chunk_overlap_50` — F: 0.8000 | AR: 0.9503 | CP: 0.8042 | CR: 1.0000 | AC: 0.3166 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the 9 projection quarters, consistent with the constant balance assumption for the stress test exercise.

### 11. `chunk_size_3000_chunk_overlap_100` — F: 0.8000 | AR: 0.9502 | CP: 0.8042 | CR: 1.0000 | AC: 0.3182 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the projection period, consistent with the assumption of maintaining constant balance sheets over the projection horizon.

### 12. `chunk_size_3000_chunk_overlap_300` — F: 0.8000 | AR: 0.9503 | CP: 0.7683 | CR: 1.0000 | AC: 0.1500 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the 9 projection quarters, consistent with the constant balance assumption for the stress test exercise.

### 13. `chunk_size_500_chunk_overlap_300` — F: 0.7500 | AR: 0.9366 | CP: 0.5549 | CR: 1.0000 | AC: 0.3334 | NS: 0.0000

The Board handles newly originated loans in its constant balance sheet projections by replenishing any reduction in exposure arising from default, prepayment, or amortization with newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the 9 projection quarters, consistent with the constant balance assumption for the stress test exercise.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 0.6000 | AR: 0.9503 | CP: 0.7683 | CR: 1.0000 | AC: 0.3182 | NS: 0.2000

The Board handles newly originated loans in its constant balance sheet projections by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged throughout the projection period, consistent with the assumption of maintaining constant balance sheets over the projection horizon.

### 15. `chunk_size_2000_chunk_overlap_200` — F: 0.5000 | AR: 0.7266 | CP: 0.7045 | CR: 1.0000 | AC: 0.1592 | NS: 0.8000

The Board handles newly originated loans by assuming that any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter. This approach ensures that the portfolio balance remains unchanged, consistent with the constant balance assumption for the stress test exercise. Newly originated loans are added in a manner similar to loan re-origination done for credit loss projections across the loan portfolio.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0215 | NS: 0.0000

I don't know.

---

## Question 23: What are the key cross-sectional and time-series inputs to the Corporate PD Model?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8777 | CP: 0.5000 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8777 | CP: 0.3333 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.8777 | CP: 0.4762 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8777 | CP: 0.4167 | CR: 1.0000 | AC: 0.7925 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which is a holistic measure summarizing a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.9658 | NS: 0.0000

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, and the key time-series input is the BBB spread.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8777 | CP: 0.3333 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.9658 | NS: 0.0000

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, and the key time-series input is the BBB spread.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.9658 | NS: 0.0000

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, and the key time-series input is the BBB spread.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.9658 | NS: 0.0000

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, and the key time-series input is the BBB spread.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8777 | CP: 1.0000 | CR: 1.0000 | AC: 0.7965 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8777 | CP: 0.3333 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8777 | CP: 0.5556 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8777 | CP: 0.5444 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8777 | CP: 0.6333 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8777 | CP: 0.5556 | CR: 1.0000 | AC: 0.7964 | NS: 0.3333

The key cross-sectional input to the Corporate PD Model is the obligor internal risk rating, which summarizes a wide range of hard and soft credit-relevant information. The key time-series input to the model is the BBB spread.

---

## Question 24: What is the significance of 'obligor internal risk rating' in the Corporate Model?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9961 | CP: 0.3333 | CR: 1.0000 | AC: 0.8858 | NS: 0.1111

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a holistic measure that summarizes a wide range of hard and soft credit-relevant information about an obligor. It is a key cross-sectional input used to project the default probability for corporate exposures, allowing for the assessment of credit quality across different firms' loan portfolios. These internal ratings are standardized to a common scale, which facilitates the comparison and application of risk measures for both estimation samples and firms' loans. The model assumes that these internal ratings accurately and consistently reflect salient credit risk factors, making them essential for effective credit quality measurement and risk assessment.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9961 | CP: 0.5524 | CR: 1.0000 | AC: 0.3229 | NS: 0.4167

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for projecting the default probability of corporate exposures. It is a holistic measure that summarizes a wide range of hard and soft credit-relevant information, allowing for the assessment of credit quality. The internal risk ratings are mapped to a common aggregate rating scale used for probability of default (PD) estimation, which helps ensure consistency in evaluating the creditworthiness of obligors. This approach assumes that the internal ratings assigned by firms accurately and consistently reflect the relevant credit risk factors, thereby facilitating more accurate projections of default probabilities and risk profiles for firms' loan portfolios.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9961 | CP: 0.1556 | CR: 1.0000 | AC: 0.1148 | NS: 0.6250

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for estimating the probability of default (PD) for corporate exposures. These internal ratings, which are mapped to a common rating scale, are assumed to accurately and consistently summarize important credit risk factors. They are used to assess credit quality and are crucial for generating stressed projections that reflect firms' risk profiles. The model relies on these ratings to evaluate the sensitivity to macroeconomic factors across different rating categories, and they play a key role in the overall assessment of credit risk for both publicly rated and non-publicly rated obligors.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9961 | CP: 0.7222 | CR: 1.0000 | AC: 0.1135 | NS: 0.3636

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring credit quality. These internal ratings are mapped to a common rating scale, which allows for the effective assessment of credit risk across different obligors. The model assumes that these ratings accurately and consistently summarize important credit risk factors, and they are used to project the probability of default (PD) for corporate exposures. This approach helps in differentiating risk based on industry and ensures that the model can effectively estimate default probabilities for various obligors. Additionally, the ongoing monitoring of the model's performance indicates that these internal ratings are effective at measuring credit quality, further underscoring their importance in the model's framework.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9961 | CP: 0.6667 | CR: 1.0000 | AC: 0.1112 | NS: 0.2000

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for projecting default probabilities (PDs) for corporate exposures. These internal ratings, which are determined by firms' proprietary rating systems, are standardized to a common rating scale that aligns with vendor PDs. This mapping allows for a consistent assessment of credit risk factors across different firms and facilitates the projection of PDs based on these ratings. The model assumes that these internal ratings accurately and consistently summarize the relevant credit risk, and they are crucial for determining the credit quality of firms' corporate loans. Additionally, the model's effectiveness in measuring credit quality is supported by the Board's monitoring, which finds no material difference in performance between publicly rated and non-publicly rated obligors when using these internal ratings.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9961 | CP: 0.6454 | CR: 0.0000 | AC: 0.1129 | NS: 0.5000

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for projecting default probabilities (PDs) for corporate exposures. These internal ratings, which are standardized to a common rating scale, are assumed to accurately and consistently summarize key credit risk factors. The model relies on these ratings to assess the credit quality of obligors and to project how their default probabilities may vary based on macroeconomic conditions. Additionally, the mapping of internal ratings to a common scale enhances the efficiency and transparency of the risk assessment process, allowing for better measurement and comparison of credit risk across different firms and industries.

### 7. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9961 | CP: 0.7611 | CR: 0.0000 | AC: 0.1142 | NS: 0.6364

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different obligors. The model uses these ratings to project default probabilities (PD) and to differentiate risk based on credit quality, thereby enabling more accurate loss estimates. Additionally, the internal risk ratings help in segmenting the model by industry and rating, which is crucial for capturing variations in default risk and sensitivity to macroeconomic factors. Overall, the internal risk ratings are essential for ensuring that the model effectively reflects the credit risk associated with corporate exposures.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9961 | CP: 0.8762 | CR: 1.0000 | AC: 0.1141 | NS: 0.5556

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different firms and obligors. The model assumes that these internal ratings accurately and consistently summarize key credit risk factors, enabling effective projections of default probabilities (PD) and loss estimates. Additionally, the internal risk ratings facilitate the differentiation of risk based on industry and rating, which is crucial for capturing variations in default risk and ensuring that loss estimates reflect the credit quality differences across portfolios.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9961 | CP: 0.8262 | CR: 1.0000 | AC: 0.1131 | NS: 0.3636

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different firms and obligors. The model assumes that these internal ratings accurately and consistently summarize key credit risk factors, enabling effective estimation of probabilities of default (PD) and loss given default. Additionally, the mapping of internal risk ratings to standardized ratings facilitates the projection of default probabilities and helps in differentiating risk across various industries and rating categories, ultimately contributing to more precise loss estimates and risk management.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9961 | CP: 0.7893 | CR: 1.0000 | AC: 0.1179 | NS: 0.3750

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different firms and loan portfolios. The model assumes that these internal ratings accurately and consistently summarize key credit risk factors, enabling the projection of default probabilities (PD) and loss estimates. Additionally, the mapping of internal risk ratings to standardized ratings facilitates the integration of qualitative and quantitative data, enhancing the model's robustness and stability in estimating credit risk.

### 11. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9961 | CP: 0.7333 | CR: 1.0000 | AC: 0.1136 | NS: 0.6250

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different obligors. The model assumes that these ratings accurately and consistently summarize key credit risk factors, enabling effective estimation of default probabilities (PD) and loss projections. Additionally, the internal risk ratings facilitate the segmentation of the Corporate PD Model by industry and rating, which helps account for variations in default risk and sensitivity to macroeconomic factors across different credit quality levels.

### 12. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9961 | CP: 0.7333 | CR: 1.0000 | AC: 0.1136 | NS: 0.7500

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different obligors. The model assumes that these ratings accurately and consistently summarize key credit risk factors, enabling effective estimation of default probabilities (PD) and loss projections. Additionally, the internal risk ratings facilitate the segmentation of the Corporate PD Model by industry and rating, which helps account for variations in default risk and sensitivity to macroeconomic factors across different credit quality levels.

### 13. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9961 | CP: 0.7333 | CR: 1.0000 | AC: 0.1157 | NS: 0.8750

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different obligors. The model assumes that these ratings accurately and consistently summarize key credit risk factors, enabling effective estimation of default probabilities (PD) and loss projections. Additionally, the internal risk ratings facilitate the segmentation of the model by industry and rating, which helps account for variations in default risk and sensitivity to macroeconomic factors across different credit quality levels.

### 14. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9961 | CP: 0.7333 | CR: 1.0000 | AC: 0.1154 | NS: 0.5000

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for measuring the credit quality of corporate loans. These internal ratings are mapped to a common rating scale, which allows for consistent assessment and comparison of credit risk across different firms and obligors. The model assumes that these internal ratings accurately and consistently summarize important credit risk factors, enabling effective estimation of default probabilities (PD) and loss projections. Additionally, the internal risk ratings facilitate the segmentation of the model by industry and rating, which helps account for variations in default risk and sensitivity to macroeconomic factors across different credit quality levels.

### 15. `chunk_size_1000_chunk_overlap_50` — F: 0.8750 | AR: 0.9961 | CP: 0.7750 | CR: 1.0000 | AC: 0.1101 | NS: 0.5000

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver for estimating the probability of default (PD). These internal ratings are mapped to a common rating scale, which allows for a consistent assessment of credit quality across different obligors. The model assumes that these internal ratings accurately and consistently summarize key credit risk factors, and they are used to project default probabilities for corporate exposures. Additionally, the internal risk ratings help in differentiating model specifications according to industry, thereby enhancing the model's effectiveness in measuring credit risk.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.8182 | AR: 0.9961 | CP: 0.4546 | CR: 1.0000 | AC: 0.2340 | NS: 0.4545

The 'obligor internal risk rating' is significant in the Corporate Model as it serves as a primary risk driver, summarizing a wide range of hard and soft credit-relevant information to assess the credit quality of obligors. These internal ratings are mapped to a common scale, which enhances the efficiency and transparency of the risk assessment process. The model assumes that these ratings accurately and consistently reflect the salient credit risk factors, allowing for effective measurement of credit quality across different obligors. Additionally, the internal risk ratings are used in conjunction with macroeconomic factors to project default probabilities for corporate exposures.

---

## Question 25: Which regulatory report provides the granular position data used in the First Lien Mortgage Model?

### 1. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9786 | CP: 0.4988 | CR: 1.0000 | AC: 0.1869 | NS: 0.0000

The regulatory report that provides the granular position data used in the First Lien Mortgage Model is the FR Y-14Q, Schedule M (Balances).

### 2. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9484 | CP: 0.9705 | CR: 1.0000 | AC: 0.6883 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided in the FR Y-14M report.

### 3. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9484 | CP: 0.6494 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 0.5000 | AR: 0.9786 | CP: 0.8441 | CR: 1.0000 | AC: 0.5618 | NS: 0.0000

The regulatory report that provides the granular position data used in the First Lien Mortgage Model is the FR Y-14M.

### 5. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.9484 | CP: 0.8037 | CR: 1.0000 | AC: 0.5597 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 6. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.9484 | CP: 0.9468 | CR: 1.0000 | AC: 0.4863 | NS: 0.5000

The regulatory report that provides the granular position data used in the First Lien Mortgage Model is the FR Y-14M report.

### 7. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.9484 | CP: 0.9283 | CR: 1.0000 | AC: 0.4883 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided in the FR Y-14M report.

### 8. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.9484 | CP: 0.6211 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 9. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.9484 | CP: 0.9468 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 10. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.9484 | CP: 0.9060 | CR: 1.0000 | AC: 0.4883 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided in the FR Y-14M report.

### 11. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.9786 | CP: 0.7972 | CR: 1.0000 | AC: 0.4868 | NS: 0.0000

The regulatory report that provides the granular position data used in the First Lien Mortgage Model is the FR Y-14M.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.9484 | CP: 0.7579 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.9484 | CP: 0.8701 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.9484 | CP: 0.9060 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.9484 | CP: 0.9060 | CR: 1.0000 | AC: 0.6847 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided by the FR Y-14M report.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.9484 | CP: 0.9060 | CR: 1.0000 | AC: 0.6883 | NS: 0.0000

The granular position data used in the First Lien Mortgage Model is provided in the FR Y-14M report.

---

## Question 26: How does the Board ensure that differences in credit classes are not driven by subjective determination?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.8762 | CR: 1.0000 | AC: 0.6414 | NS: 0.6667

The Board ensures that differences in credit classes are not driven by subjective determination by using algorithmic definitions based on observable loan characteristics. This approach aligns the credit class definitions with the reported credit class in the PLS data while maintaining simplicity. By relying on algorithmic definitions rather than directly reported classifications, the Board ensures consistent treatment of loans across firms and reporters in the sample.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9767 | CP: 0.6681 | CR: 1.0000 | AC: 0.6861 | NS: 0.5000

The Board ensures that differences in credit classes are not driven by subjective determination by using algorithmic categorizations that align closely with reported credit classes in the PLS data, while keeping the definitions simple. This approach relies on observable loan characteristics, such as original loan-to-value (LTV), origination credit score, and documentation type, rather than on imputed or subjective information. By using these consistent definitions, the Board maintains uniformity between the data used to estimate model parameters and the data used to project losses.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8283 | CP: 0.9627 | CR: 1.0000 | AC: 0.5654 | NS: 0.5000

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8283 | CP: 0.5799 | CR: 1.0000 | AC: 0.8710 | NS: 0.4000

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses, thereby minimizing the influence of individual servicers' subjective assessments.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8283 | CP: 0.6321 | CR: 1.0000 | AC: 0.7048 | NS: 0.4000

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definition of credit classes used to estimate model parameters and the data used to project losses, thereby minimizing the influence of individual servicers' subjective assessments.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9032 | CP: 0.8260 | CR: 1.0000 | AC: 0.9517 | NS: 0.2000

The Board ensures that differences in credit classes are not driven by the subjective determination of individual servicers by using a consistent approach based on observable loan characteristics, such as original loan-to-value (LTV), origination credit score, and documentation type. This method allows for a standardized classification of credit classes, which helps maintain consistency across the data used for modeling and projections.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9303 | CP: 0.8556 | CR: 1.0000 | AC: 0.6384 | NS: 0.6000

The Board ensures that differences in credit classes are not driven by subjective determination by using observable loan characteristics, such as original loan-to-value (LTV) ratio, origination credit score, and documentation type, to assign credit classes. This approach maintains consistency between the definitions of credit classes across the data used to estimate model parameters and the data used to project losses.

### 8. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8283 | CP: 0.8644 | CR: 1.0000 | AC: 0.5654 | NS: 0.2500

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses.

### 9. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8252 | CP: 0.9318 | CR: 1.0000 | AC: 0.5392 | NS: 0.3333

The Board ensures that differences in credit classes are not driven by subjective determination by relying on observable loan characteristics to assign credit class. This approach ensures consistency between the definition of credit classes in the data used to estimate the model parameters and the data used to project losses. By using observable characteristics rather than subjective determinations made by individual servicers, the Board maintains objectivity in the classification of loans into credit classes.

### 10. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8252 | CP: 0.9889 | CR: 1.0000 | AC: 0.5392 | NS: 0.3333

The Board ensures that differences in credit classes are not driven by subjective determination by relying on observable loan characteristics to assign credit class. This approach ensures consistency between the definition of credit classes in the data used to estimate the model parameters and the data used to project losses. By using observable characteristics rather than subjective determinations made by individual servicers, the Board maintains objectivity in the classification of loans into credit classes.

### 11. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8761 | CP: 0.8844 | CR: 1.0000 | AC: 0.5066 | NS: 0.3333

The Board ensures that differences in credit classes are not driven by subjective determination by relying on observable loan characteristics to assign credit class. This approach ensures consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses. By using observable characteristics rather than subjective determinations by individual servicers, the Board maintains objectivity in the classification process.

### 12. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8252 | CP: 1.0000 | CR: 1.0000 | AC: 0.5398 | NS: 0.3333

The Board ensures that differences in credit classes are not driven by subjective determination by relying on observable loan characteristics to assign credit class. This approach ensures consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses. By using observable characteristics rather than subjective determinations made by individual servicers, the Board maintains objectivity in the classification of loans into credit classes.

### 13. `chunk_size_1000_chunk_overlap_50` — F: 0.8750 | AR: 0.8808 | CP: 0.5807 | CR: 1.0000 | AC: 0.3173 | NS: 0.6250

The Board ensures that differences in credit classes are not driven by the subjective determination of individual servicers by estimating probability of default (PD) by aggregate credit rating category. This approach utilizes credit ratings, which provide a single summary metric of obligor credit quality, and reflects a wide range of information about an obligor, including both quantitative data and qualitative elements. By relying on standardized credit ratings from independent credit rating agencies, the Board aims to maintain objectivity in the assessment of credit classes.

### 14. `chunk_size_1000_chunk_overlap_100` — F: 0.8000 | AR: 0.8282 | CP: 0.5444 | CR: 1.0000 | AC: 0.8717 | NS: 0.4000

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definition of credit classes in the data used to estimate model parameters and the data used to project losses, thereby minimizing the influence of individual servicers' subjective determinations.

### 15. `chunk_size_500_chunk_overlap_200` — F: 0.7778 | AR: 1.0000 | CP: 0.5889 | CR: 1.0000 | AC: 0.1563 | NS: 0.1111

The Board ensures that differences in credit classes are not driven by subjective determination by using a standardized approach to credit ratings, which includes the use of median internal ratings from firms' internal risk rating systems when discrepancies among firms' ratings occur. This method aims to generate stressed projections that more appropriately reflect firms' risk profiles, thereby minimizing the influence of subjective assessments. Additionally, credit ratings from independent credit rating agencies provide an external, objective measure of obligor credit quality, incorporating a wide range of quantitative and qualitative information.

### 16. `chunk_size_2000_chunk_overlap_200` — F: 0.6000 | AR: 0.8283 | CP: 0.6333 | CR: 1.0000 | AC: 0.9557 | NS: 0.2000

The Board ensures that differences in credit classes are not driven by subjective determination by relying on credit class definitions based on observable loan characteristics. This approach guarantees consistency between the definitions of credit classes in the data used to estimate model parameters and the data used to project losses, thereby minimizing the influence of individual servicers' subjective determinations.

---

## Question 27: In the context of retail credit models, what are payoff rates?

### 1. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9143 | CP: 0.2250 | CR: 1.0000 | AC: 0.3466 | NS: 0.8750

Payoff rates in the context of retail credit models refer to the rates at which borrowers pay off their loan balances. These rates can vary depending on the macroeconomic environment and the characteristics of the loan. The modeling approach allows for these factors to be internalized in the model, and payoff rates are used in supervisory stress tests to determine the amount of run-off balance, which in turn helps to assess the level of new originations.

### 2. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 3. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 4. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0258 | NS: 0.0000

I don't know.

---

## Question 28: In the First Lien Mortgage Model, what does the PD model produce in addition to loss rates?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.7694 | CP: 0.3556 | CR: 1.0000 | AC: 0.5078 | NS: 1.0000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 2. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.6104 | CP: 0.4968 | CR: 1.0000 | AC: 0.6973 | NS: 0.6667

The PD model produces payoff rates in addition to loss rates.

### 3. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.6104 | CP: 0.3388 | CR: 1.0000 | AC: 0.4973 | NS: 0.5000

The PD model produces payoff rates in addition to loss rates.

### 4. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.6104 | CP: 0.2958 | CR: 1.0000 | AC: 0.6973 | NS: 0.5000

The PD model produces payoff rates in addition to loss rates.

### 5. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8252 | CP: 0.1833 | CR: 1.0000 | AC: 0.9542 | NS: 0.6667

The PD model also produces payoff rates in addition to loss rates.

### 6. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.6104 | CP: 0.4968 | CR: 1.0000 | AC: 0.6973 | NS: 0.6667

The PD model produces payoff rates in addition to loss rates.

### 7. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.6104 | CP: 0.4968 | CR: 1.0000 | AC: 0.6973 | NS: 0.6667

The PD model produces payoff rates in addition to loss rates.

### 8. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.6104 | CP: 0.4968 | CR: 1.0000 | AC: 0.6973 | NS: 0.6667

The PD model produces payoff rates in addition to loss rates.

### 9. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.6104 | CP: 0.4968 | CR: 1.0000 | AC: 0.6973 | NS: 0.5000

The PD model produces payoff rates in addition to loss rates.

### 10. `chunk_size_500_chunk_overlap_100` — F: 0.5000 | AR: 0.7694 | CP: 0.3333 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 11. `chunk_size_500_chunk_overlap_300` — F: 0.5000 | AR: 0.7694 | CP: 0.1429 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 12. `chunk_size_1000_chunk_overlap_50` — F: 0.5000 | AR: 0.7694 | CP: 0.2500 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 13. `chunk_size_1000_chunk_overlap_100` — F: 0.5000 | AR: 0.7694 | CP: 0.2111 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 14. `chunk_size_1000_chunk_overlap_200` — F: 0.5000 | AR: 0.7694 | CP: 0.1736 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 15. `chunk_size_1000_chunk_overlap_300` — F: 0.5000 | AR: 0.7694 | CP: 0.2897 | CR: 1.0000 | AC: 0.5078 | NS: 0.5000

The PD model produces a probability of payoff for each loan in addition to loss rates.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0189 | NS: 0.0000

I don't know.

---

## Question 29: Why does the Board choose a loan-level approach rather than an aggregate approach for retail portfolios?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9596 | CP: 0.4929 | CR: 1.0000 | AC: 0.3439 | NS: 0.2857

The Board chooses a loan-level approach rather than an aggregate approach for retail portfolios because it intends to increase the interpretability of the model results. Additionally, the loan-level model is assessed as being most consistent with modeling best practices and best suited for the context of the portfolios, which encompass a wide range of lending. The decision is also influenced by the large number of loan and borrower characteristics that impact default and payoff risk, as well as the availability of loan-level data reported on the FR Y-14M.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.7680 | CP: 0.6656 | CR: 1.0000 | AC: 0.6958 | NS: 0.3333

The Board chooses a loan-level approach rather than an aggregate approach for retail portfolios to increase the interpretability of the model results. Additionally, this approach is assessed as being most consistent with modeling best practices and is better suited for the context of the portfolios, as it allows for a more detailed analysis of the large number of loan and borrower characteristics that impact default and payoff risk.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9597 | CP: 0.9472 | CR: 1.0000 | AC: 0.8459 | NS: 0.6250

The Board chooses a loan-level approach rather than an aggregate approach for retail portfolios because it allows for much more granular differentiation compared to a top-down approach that does not consider individual loan characteristics. This approach is intended to increase the interpretability of the model results and is assessed as most consistent with modeling best practices, making it better suited for use in the context of the supervisory stress test. Additionally, the loan-level model can account for variations in risk levels among individual loans, which is important for accurately projecting loan losses and provisions.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 0.8333 | AR: 0.7681 | CP: 0.7798 | CR: 1.0000 | AC: 0.8282 | NS: 0.6667

The Board chooses a loan-level approach rather than an aggregate approach for retail portfolios to increase the interpretability of the model results. This approach is assessed as most consistent with modeling best practices and is best suited for use in the context of the supervisory stress test. Additionally, the loan-level model allows for a more accurate representation of the individual loans' performance and risk characteristics, which is important for effective risk assessment.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 0.3333 | AR: 0.9437 | CP: 0.9068 | CR: 1.0000 | AC: 0.8063 | NS: 0.0000

The Board chose a loan-level approach rather than an aggregate approach for retail portfolios because it allows for maintaining consistency in the firm’s portfolio composition while directly accounting for the maturity profile of the individual loans. This approach achieves a balance of simplicity, flexibility, and accuracy, which were key factors in the Board's decision.

### 6. `chunk_size_500_chunk_overlap_200` — F: 0.1429 | AR: 0.9597 | CP: 0.6050 | CR: 1.0000 | AC: 0.3491 | NS: 0.2857

The Board chooses a loan-level approach rather than an aggregate approach for retail portfolios because more granular models are generally better suited to capture the range of risk profiles among the firm portfolios. This allows for a more detailed evaluation of individual loan characteristics, borrower characteristics, and macroeconomic conditions, which can lead to more accurate estimations of default risk and expected losses.

### 7. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.6893 | CR: 1.0000 | AC: 0.0224 | NS: 0.5000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.7878 | CR: 1.0000 | AC: 0.3224 | NS: 0.5000

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.6931 | CR: 1.0000 | AC: 0.0224 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.4921 | CR: 1.0000 | AC: 0.3224 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.6441 | CR: 1.0000 | AC: 0.2724 | NS: 1.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.3882 | CR: 1.0000 | AC: 0.2724 | NS: 1.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.9060 | CR: 1.0000 | AC: 0.0224 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.9060 | CR: 1.0000 | AC: 0.2724 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.9060 | CR: 1.0000 | AC: 0.2724 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.9060 | CR: 1.0000 | AC: 0.0224 | NS: 0.0000

I don't know.

---

## Question 30: What is the 'Retail Loss Aggregation' process in the retail credit risk models?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8546 | CP: 0.9306 | CR: 1.0000 | AC: 0.4718 | NS: 0.4444

The 'Retail Loss Aggregation' process refers to the method by which the Board produces final projections of loss dollars for each firm in various sub-portfolios (such as bank cards, charge cards, HELs, and HELOCs) on a quarterly basis. This process involves applying projected loss rates to the balances of the respective categories of accounts, which are generated by a balance sheet line-item projections calculator based on data reported in FR Y-14Q. The Retail Loss Aggregation process ensures a simple, consistent, and robust approach across all retail portfolios, adhering to principles of supervisory stress testing. The outputs from this process are used in downstream calculations to estimate provisions.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8546 | CP: 1.0000 | CR: 0.0000 | AC: 0.3123 | NS: 0.5714

The 'Retail Loss Aggregation' process refers to the method by which the Board produces final projections of loss dollars for firms participating in the supervisory stress test. It begins with reported portfolio balances and projected loss rates and payoff rates for each quarter. The process involves applying a series of calculations and adjustments to generate final loss projections for each firm in various sub-portfolios, such as bank cards and charge cards. The output of this process is used in the downstream Provisions Model to estimate provisions, ensuring a consistent approach across all retail portfolios while adhering to principles of simplicity, consistency, and robustness.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8546 | CP: 1.0000 | CR: 1.0000 | AC: 0.1690 | NS: 0.5714

The 'Retail Loss Aggregation' process refers to the method by which the Board produces final projections of loss dollars for retail portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process ensures consistency across all retail portfolios and adheres to principles such as simplicity, consistency, robustness, and the assumption of a constant balance sheet. It involves calculating total loss dollars by summing losses on existing portfolios and projected new origination balances, while also adjusting for revenue and loss sharing agreements. The output of this process is used in downstream models to estimate provisions.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8546 | CP: 0.9415 | CR: 0.0000 | AC: 0.2934 | NS: 1.0000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from previous sections to produce final projections of loss dollars for retail credit portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test, specifically those reporting data on FR Y-14M, Schedule D.1 (Credit Cards). The process involves applying a series of calculations to estimate losses on both existing portfolios and projected new origination portfolios. The output is a final projection of loss dollars for each firm in each sub-portfolio (bank cards and charge cards) for each quarter. This process is designed to be simple, consistent, and robust, adhering to principles of the supervisory stress test, and generally does not require data adjustments unless the submitted data is deficient.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8546 | CP: 0.6357 | CR: 1.0000 | AC: 0.7889 | NS: 0.7143

The 'Retail Loss Aggregation' process refers to the method by which the Board produces final projections of loss dollars for each firm in the portfolio for each quarter. It begins with the reported portfolio balances and projected loss rates for each firm participating in the supervisory stress test. The process involves applying a series of calculations and adjustments to these inputs to generate loss estimates in a consistent manner across all retail portfolios. The output includes total loss projections for existing portfolios as well as for two projected new origination portfolios, ensuring adherence to principles of simplicity, consistency, and robustness in the modeling process.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8546 | CP: 0.7163 | CR: 0.0000 | AC: 0.7708 | NS: 0.7143

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various sections to produce final projections of loss dollars for retail portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process involves applying a series of calculations and adjustments to generate a final projection of loss dollars for each firm in each sub-portfolio (such as bank cards and charge cards) across the projection period. This process ensures consistency and adherence to principles of the supervisory stress test, including simplicity, robustness, and the assumption of a constant balance sheet throughout the forecast period. The output of the Retail Loss Aggregation process is used in downstream calculations to produce estimates of provisions.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8546 | CP: 0.8153 | CR: 1.0000 | AC: 0.2765 | NS: 0.8182

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from previous sections to produce final projections of loss dollars. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process involves applying calculations to these balances, which are derived from data reported in FR Y-14M, Schedule D.1 (Credit Cards), for both the existing portfolio and two projected new origination portfolios. The output of this process is a final projection of loss dollars for each firm in each sub-portfolio (bank cards and charge cards) for each quarter. The projected loss rates are assigned to the respective account balances, and total losses generated are used in the downstream Provisions Model to estimate provisions. The process is designed to be simple, consistent, and robust, adhering to principles of the supervisory stress test.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8546 | CP: 0.7087 | CR: 1.0000 | AC: 0.1720 | NS: 1.0000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process involves applying a series of calculations and adjustments to these inputs to generate final loss projections for each firm in different sub-portfolios, such as bank cards and charge cards for credit cards, or HEL and HELOC for home equity. The projected loss rates are assigned to the respective account balances, and the total loss dollars are calculated as the sum of losses on the existing portfolio and projected new origination balances during the projection period. This process ensures consistency and adherence to supervisory stress test principles.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8546 | CP: 0.7994 | CR: 1.0000 | AC: 0.8067 | NS: 0.7500

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process involves applying a series of calculations and adjustments to these inputs to generate final loss projections for each firm in different sub-portfolios (such as bank cards and charge cards). The projected loss rates are assigned to the balances of the respective account categories based on data reported in regulatory schedules. The output of this process is a final projection of loss dollars for each firm in each sub-portfolio for each quarter.

### 10. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8546 | CP: 0.8951 | CR: 0.0000 | AC: 0.1727 | NS: 0.8571

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various model components to produce final projections of loss dollars for retail credit portfolios. This process begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. It involves applying a series of calculations and adjustments to these inputs to generate final loss projections for each firm in each sub-portfolio (such as bank cards and charge cards, or home equity loans and lines of credit) across the projection period. The output of this process is a comprehensive estimate of loss dollars for the existing portfolio as well as projected new origination portfolios.

### 11. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8546 | CP: 0.8951 | CR: 0.0000 | AC: 0.1729 | NS: 0.6000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various model components to produce final projections of loss dollars for retail credit portfolios. This process begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. It involves applying a series of calculations and adjustments to these inputs to generate final projections of loss dollars for each firm in each sub-portfolio (such as bank cards and charge cards, or home equity loans and lines of credit) across the projection period. The output reflects the total projected losses, which include losses from both existing portfolios and projected new origination portfolios.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.9167 | AR: 0.8546 | CP: 0.8819 | CR: 1.0000 | AC: 0.8143 | NS: 0.7000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. It begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. The process involves applying a series of calculations and adjustments to these inputs to generate final loss projections for each firm in different sub-portfolios (such as bank cards and charge cards, or home equity loans and lines of credit) across the projection period. The output includes total loss dollars projected from both existing portfolios and new origination portfolios, ensuring consistency and adherence to supervisory stress test principles.

### 13. `chunk_size_2000_chunk_overlap_100` — F: 0.8333 | AR: 0.8546 | CP: 0.8000 | CR: 1.0000 | AC: 0.1707 | NS: 0.7273

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. This process begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. It involves applying a series of calculations and adjustments to these inputs to generate final loss projections for each firm in different sub-portfolios, such as bank cards and charge cards for the Credit Card Model, or Home Equity Loans (HEL) and Home Equity Lines of Credit (HELOC) for the Home Equity Model. The projected loss rates are assigned to the respective balances of accounts, and the total loss dollars are calculated as the sum of losses on the existing portfolio and projected new origination balances during the projection period. The process ensures consistency and adherence to supervisory stress test principles.

### 14. `chunk_size_3000_chunk_overlap_50` — F: 0.8000 | AR: 0.8545 | CP: 0.8951 | CR: 0.0000 | AC: 0.8162 | NS: 0.7000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. This process begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. It involves applying a series of calculations and adjustments to these inputs to generate final projections of loss dollars for each firm in each sub-portfolio (such as bank cards and charge cards, or home equity loans and lines of credit) across the projection period. The output of this process is a comprehensive estimate of losses that incorporates existing portfolios as well as projected new origination portfolios.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.8000 | AR: 0.8546 | CP: 0.8951 | CR: 1.0000 | AC: 0.1735 | NS: 0.6000

The 'Retail Loss Aggregation' process refers to the method by which the Board uses outputs from various models to produce final projections of loss dollars for retail credit portfolios. This process begins with reported portfolio balances and projected loss rates for each quarter for firms participating in the supervisory stress test. It involves applying a series of calculations and adjustments to these inputs to generate final projections of loss dollars for each firm in each sub-portfolio (such as bank cards and charge cards, or home equity loans and lines of credit) across the projection period. The output reflects the total projected losses, which include losses from both existing portfolios and projected new origination portfolios.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0281 | NS: 0.0000

I don't know.

---

## Question 31: How does the Board handle missing or immaterial portfolios in the retail credit risk models?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8442 | CP: 0.0000 | CR: 1.0000 | AC: 0.1160 | NS: 0.5000

The Board handles missing or immaterial portfolios by using a process that is consistent with other models throughout the supervisory stress test. For firms with portfolio balances that are below the materiality threshold, they have the option of submitting or not submitting the relevant schedule. This approach aims to produce reasonable estimates while limiting the operational burden for both reporters and the Board.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9925 | CP: 0.0000 | CR: 0.5000 | AC: 0.0947 | NS: 0.7000

The Board handles missing or immaterial portfolios in the retail credit risk models by using a Retail Loss Aggregation framework to produce reasonable and consistent projections. For immaterial portfolios, which are defined as those that are not material, the Board applies a fifty percent adjustment. For firms with large credit card portfolios, a 10 percent sample is considered reasonable, while for firms with smaller credit card portfolios, using all reported data is preferred to avoid reliability issues with sampling. The Board also maintains a general constant portfolio assumption across all sub-models and uses a shared framework to reflect variation in risk levels while limiting complexity and reporting burdens.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8442 | CP: 0.0000 | CR: 0.0000 | AC: 0.1035 | NS: 0.6667

The Board handles missing or immaterial portfolios by assigning a high loss rate (90th percentile) to the portfolio balances based on supervisory projections of losses for other firms if the submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate. This approach is consistent with other models throughout the supervisory stress test to produce reasonable projections while mitigating the impact of missing data. Additionally, for firms with portfolio balances below the materiality threshold, there is an option to submit or not submit the relevant schedule.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8442 | CP: 0.0000 | CR: 0.0000 | AC: 0.0886 | NS: 0.7143

The Board handles missing or immaterial portfolios by allowing firms with portfolio balances below the materiality threshold the option of submitting or not submitting the relevant schedule (FR Y-14M, Schedule D for Credit Cards). If a firm's submitted data in a sub-portfolio is too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms. This approach is consistent with other models and aims to limit the operational burden for both reporters and the Board.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.5430 | CP: 0.0000 | CR: 1.0000 | AC: 0.1145 | NS: 0.8889

The Board uses all available data to project losses for firms with credit card accounts totaling less than $10 billion in balance, as this approach is not operationally burdensome and reduces costs. For missing and immaterial portfolios, the process is consistent with other models throughout the supervisory stress test to produce reasonable projections while mitigating the risks associated with relying on insufficient data. The Board also employs a top-down approach for modeling these portfolios, which is a well-established method in regulatory modeling that assesses systemic risk using aggregated data.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.3841 | NS: 0.5000

The Board handles missing or immaterial portfolios in the retail credit risk models by allowing firms with portfolio balances below the materiality threshold the option of submitting or not submitting the relevant schedule (FR Y-14M, Schedule D). Additionally, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms.

### 7. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.1011 | NS: 0.8571

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of such portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and avoids the risks associated with using a sample that may not be representative. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, including the assumption of a constant balance sheet through the projection period.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 0.8750 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.1029 | NS: 0.4286

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of such portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of losses for other firms. Additionally, for firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and avoids the risks associated with using a sample that may not be representative. The chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, including the assumption of a constant balance sheet through the projection period.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 0.8750 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.1007 | NS: 0.8750

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of such portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and avoids the risks associated with using a sample that may not be representative. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 0.8750 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.0988 | NS: 0.5000

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of these portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and avoids the risks associated with using a sample that may not be representative. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period.

### 11. `chunk_size_3000_chunk_overlap_50` — F: 0.8750 | AR: 0.9925 | CP: 0.2000 | CR: 1.0000 | AC: 0.0985 | NS: 0.8571

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of such portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and ensures reliability. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period.

### 12. `chunk_size_3000_chunk_overlap_100` — F: 0.8750 | AR: 0.9925 | CP: 0.2000 | CR: 1.0000 | AC: 0.0984 | NS: 0.8571

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of these portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and ensures reliability. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period.

### 13. `chunk_size_3000_chunk_overlap_200` — F: 0.8750 | AR: 0.9925 | CP: 0.2000 | CR: 1.0000 | AC: 0.0984 | NS: 0.8571

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of these portfolios. Specifically, if a firm’s submitted data in a sub-portfolio are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate to the portfolio balances based on supervisory projections of bank card or charge card losses for other firms. For firms with relatively small credit card portfolios, the Board uses all available data to project losses, as this approach is less operationally burdensome and ensures reliability. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period.

### 14. `chunk_size_500_chunk_overlap_100` — F: 0.8333 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.0896 | NS: 0.8333

The Board handles missing or immaterial portfolios in the retail credit risk models by using the Retail Loss Aggregation framework to produce reasonable and consistent projections. For portfolios that are below the materiality threshold, firms have the option of submitting or not submitting the required data on FR Y-14M, Schedule D (Credit Cards). Additionally, for portfolios with less material balances, the Board opts for simpler modeling approaches to reduce complexity and operational burdens, as the impact on capital requirements is minimal.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 0.8333 | AR: 0.9925 | CP: 0.2000 | CR: 1.0000 | AC: 0.1036 | NS: 0.7143

The Board handles missing or immaterial portfolios in the retail credit risk models by applying a range of alternatives for determining the level of new originations and the treatment of these portfolios. Specifically, for portfolios that are too deficient to produce a supervisory loss estimate, the Board assigns a high (90th percentile) loss rate based on supervisory projections of losses for other firms. Additionally, the chosen approach is consistent with certain assumptions applied broadly in the supervisory stress test, such as the assumption of a constant balance sheet through the projection period. For firms with smaller credit card portfolios, the Board uses all available data to project losses, as this is less operationally burdensome and ensures reliability in the projections.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.6667 | AR: 0.9925 | CP: 0.0000 | CR: 1.0000 | AC: 0.1004 | NS: 0.6667

The Board handles missing or immaterial portfolios in the retail credit risk models by applying assumptions that are consistent with the Board's principle of conservatism and policies on the treatment of such portfolios.

---

## Question 32: What type of model does the Credit Card PD Model use to project default rates?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8481 | CP: 0.3530 | CR: 1.0000 | AC: 0.7326 | NS: 0.5000

The Credit Card PD Model uses an account-level, multi-period, discrete-time hazard approach to project the likelihood that an account will default in each period.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9654 | CP: 0.7333 | CR: 1.0000 | AC: 0.5224 | NS: 0.5000

The Credit Card PD Model uses a hazard model to project the path of default rates.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9331 | CP: 0.0000 | CR: 0.0000 | AC: 0.2082 | NS: 0.0000

The Credit Card PD Model uses historical data, payment status and loan losses, account characteristics, and economic conditions to project default rates.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9821 | CP: 0.9000 | CR: 1.0000 | AC: 0.5225 | NS: 0.5000

The Credit Card PD Model uses a hazard model to project the path of default rates.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9319 | CP: 0.1625 | CR: 1.0000 | AC: 0.5224 | NS: 0.5000

The Credit Card PD Model uses a hazard model to project the path of default rates.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9326 | CP: 0.1944 | CR: 0.0000 | AC: 0.1944 | NS: 0.0000

The Credit Card PD Model uses a binomial logit regression framework to project default rates.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9654 | CP: 0.2083 | CR: 1.0000 | AC: 0.5224 | NS: 0.5000

The Credit Card PD Model uses a hazard model to project the path of default rates.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9319 | CP: 0.3333 | CR: 1.0000 | AC: 0.5224 | NS: 0.5000

The Credit Card PD Model uses a hazard model to project the path of default rates.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9821 | CP: 0.1250 | CR: 1.0000 | AC: 0.5198 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure to project default rates. It employs a binomial logit regression framework for its equations.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9821 | CP: 0.1964 | CR: 1.0000 | AC: 0.4370 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure to project default rates.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7974 | CP: 0.2500 | CR: 1.0000 | AC: 0.2189 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure, specifically employing a binomial logit regression framework to project default rates.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8590 | CP: 0.2217 | CR: 1.0000 | AC: 0.2189 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure, specifically employing a binomial logit regression framework to project default rates.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9821 | CP: 0.1429 | CR: 1.0000 | AC: 0.4370 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure to project default rates.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9821 | CP: 0.2262 | CR: 1.0000 | AC: 0.2199 | NS: 0.0000

The Credit Card PD Model uses a conditional default probability model to project default rates, specifically employing an account-level, multi-period, hazard model structure with a binomial logit regression framework.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9821 | CP: 0.3611 | CR: 1.0000 | AC: 0.4370 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure to project default rates.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9821 | CP: 0.3405 | CR: 1.0000 | AC: 0.4370 | NS: 0.0000

The Credit Card PD Model uses an account-level, multi-period, hazard model structure to project default rates.

---

## Question 33: Why are competing outcomes like prepayment excluded from certain retail default models?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.2500 | CR: 1.0000 | AC: 0.6657 | NS: 0.6000

Competing outcomes like prepayment are excluded from certain retail default models to simplify the modeling framework. By considering only one outcome variable, default, the model does not require the development of additional specifications to account for prepayment. This choice reduces complexity and the reporting burden on firms, although it limits the model's ability to account for account-specific variations in the probability of default.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.6000 | CR: 1.0000 | AC: 0.5415 | NS: 0.7500

Competing outcomes like prepayment are excluded from certain retail default models to simplify the modeling framework. This choice avoids the need for developing additional specifications to account for prepayment, allowing the model to focus solely on default without the complexity introduced by including prepayment as a competing risk.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 0.8750 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0851 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because the models typically assume a symmetrical response of the outcome variables to changes in independent variables. This means that the projections will react equally to both upward and downward movements in these independent variables, which may not accurately reflect the empirical reality where prepayments are often restricted or penalized. Additionally, the focus on default probabilities without accounting for prepayment can lead to a lack of consideration for the complexities involved in the behavior of loans, particularly in the context of residential mortgage-backed securities where prepayment characteristics are more significant.

### 4. `chunk_size_3000_chunk_overlap_100` — F: 0.8750 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0739 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because they are treated as seemingly unrelated risks that can be predicted independently of one another. The literature suggests that an increase in prepayment probability has no impact on default probability; however, in practice, these factors are not independent. Therefore, modeling them simultaneously is necessary to accurately capture their interrelationship and the dynamics of loan performance.

### 5. `chunk_size_3000_chunk_overlap_200` — F: 0.8750 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0739 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because they are treated as seemingly unrelated risks that can be predicted independently of one another. The literature suggests that an increase in prepayment probability has no impact on default probability; however, in practice, these factors are not independent. Therefore, modeling them simultaneously is necessary to accurately capture their interrelationship and the dynamics of loan performance.

### 6. `chunk_size_500_chunk_overlap_200` — F: 0.8571 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0731 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because ignoring prepayments would artificially increase the number of loans exposed to default risk, leading to an overstatement of losses. This is particularly pronounced for loans nearing maturity, as the models may not accurately account for the risks associated with non-default attrition, which can bias the projections upward by underestimating the expected survival probability of accounts.

### 7. `chunk_size_1000_chunk_overlap_50` — F: 0.8571 | AR: 1.0000 | CP: 0.1429 | CR: 0.0000 | AC: 0.2474 | NS: 0.2857

Competing outcomes like prepayment are excluded from certain retail default models because the models treat prepayment and default as seemingly unrelated risks that can be predicted independently of one another. This approach simplifies the modeling process, but it may not accurately reflect the interdependencies between these factors in practice. The documentation suggests that while this one-outcome approach has drawbacks, the Board believes that its simplicity outweighs these issues.

### 8. `chunk_size_2000_chunk_overlap_200` — F: 0.8000 | AR: 1.0000 | CP: 0.3333 | CR: 0.0000 | AC: 0.0679 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because the Board recognizes that default and prepayment are not independent in practice. While some studies treat them as unrelated risks that can be predicted independently, the reality is that an increase in prepayment probability can impact default probability. Therefore, the models must account for these competing risks to accurately reflect the relationship between default and prepayment.

### 9. `chunk_size_3000_chunk_overlap_50` — F: 0.8000 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.2027 | NS: 0.1818

Competing outcomes like prepayment are excluded from certain retail default models because the models treat default and prepayment as seemingly unrelated risks that can be predicted independently of one another. This approach simplifies the modeling process, but it may not accurately reflect the practical reality where these factors are not independent. In practice, an increase in prepayment probability can impact default probability, and thus, modeling them simultaneously is often necessary to capture their interrelationship accurately. However, the decision to exclude them may stem from the desire to maintain a simpler model structure or due to limitations in data availability.

### 10. `chunk_size_1000_chunk_overlap_200` — F: 0.7500 | AR: 1.0000 | CP: 0.1714 | CR: 0.0000 | AC: 0.0853 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because the models focus on specific outcomes such as default and payoff, where the combined probability of all outcomes sums to one. In particular, for loans that are already in default (e.g., those that are 180 or more days past due), the probability of further transitions from default is not applicable, as these loans have reached terminal status. Additionally, the models may prioritize simplicity and consistency in projections, which can lead to the exclusion of competing risks like prepayment to maintain a straightforward approach.

### 11. `chunk_size_2000_chunk_overlap_50` — F: 0.7143 | AR: 1.0000 | CP: 0.2000 | CR: 0.0000 | AC: 0.0749 | NS: 0.4286

Competing outcomes like prepayment are excluded from certain retail default models because they are treated as seemingly unrelated risks that can be predicted independently of one another. This means that an increase in prepayment probability is assumed to have no impact on default probability. However, in practice, these factors are not independent, and modeling them simultaneously is necessary to accurately capture their interactions and effects on mortgage performance.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.7143 | AR: 1.0000 | CP: 0.1667 | CR: 0.0000 | AC: 0.2251 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because these models treat default and prepayment as independent risks. However, in practice, these factors are not independent, and modeling them simultaneously is necessary to accurately capture their interactions. The exclusion simplifies the model structure but may not reflect the true dynamics of loan performance, where an increase in prepayment probability can impact default probability.

### 13. `chunk_size_3000_chunk_overlap_300` — F: 0.6250 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0731 | NS: 0.0000

Competing outcomes like prepayment are excluded from certain retail default models because they are treated as seemingly unrelated risks that can be predicted independently of one another. The literature suggests that while some studies may treat prepayment and default as independent, in practice, these factors are not independent. Therefore, modeling them simultaneously is important to accurately capture their interrelationship and the impact they have on each other.

### 14. `chunk_size_500_chunk_overlap_50` — F: 0.5714 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.3823 | NS: 0.4286

Competing outcomes like prepayment are excluded from certain retail default models to simplify the modeling framework, as their inclusion would require the development of additional specifications to account for prepayment. Instead, the models assume stable paydown rates, which avoids the complexity of directly modeling prepayment. This choice allows the model to focus on default without the complications introduced by prepayment dynamics.

### 15. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 0.0000 | AC: 0.0072 | NS: 0.0000

I don't know.

### 16. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.1429 | CR: 0.0000 | AC: 0.0072 | NS: 0.0000

I don't know.

---

## Question 34: How is the 'International Cards Model' defined in the documentation?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8857 | CP: 0.7497 | CR: 1.0000 | AC: 0.2924 | NS: 0.5000

The 'International Cards Model' is defined as a model used to project losses on loans located around the world. It accounts for significant variations in economic conditions across different regions by incorporating variables that capture both global and local macroeconomic environments. The model employs a linear regression framework and segments data by product type (such as "Bank card," "Charge card," and "Corporate, SME, and Business cards") and geography to differentiate risks associated with individual-purpose cards versus business-purpose cards. It aims to provide accurate projections of net charge-off rates while maintaining a manageable level of complexity.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8857 | CP: 0.7343 | CR: 1.0000 | AC: 0.1587 | NS: 0.1250

The 'International Cards Model' is defined in the documentation as a model used to project net charge-off rates for the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It incorporates measures of both local and global macroeconomic environments to account for changes in region-specific conditions and the interconnectedness of the global economy. The model segments data by product type and geography, dividing the International Card model into four regions: Canada, EMEA (Europe, Middle East, and Africa), LATAM (Latin America and Caribbean), and APAC (Asia Pacific). It uses a single model structure to project losses while maintaining a balance between complexity and the ability to capture additional differences across firms not explained by observable data.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8856 | CP: 0.9333 | CR: 1.0000 | AC: 0.1686 | NS: 0.0000

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It incorporates a two-equation structure to account for additional differences across firms not captured by other data fields, while maintaining interpretability. The model segments data by product type and geography, considering global economic conditions and region-specific macroeconomic variables. It is designed to project losses on loans located around the world, acknowledging significant variations in economic conditions across different regions.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8857 | CP: 0.7329 | CR: 1.0000 | AC: 0.3048 | NS: 0.7143

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card portfolio and the International Small Business and Corporate Credit Card portfolio. It employs a slightly more complex model structure compared to the Domestic Models, utilizing a linear regression framework that projects net charge-off rates in a two-equation structure. This model accounts for differences in historical net charge-off rates and delinquency rates, allowing for forward-looking projections while differentiating balances between the two portfolios. The model segments data by product type and geography to capture key differences in risks and is supported by performance testing measures.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8857 | CP: 0.6496 | CR: 1.0000 | AC: 0.1707 | NS: 0.5455

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It employs a single model to project losses on these two portfolios, calibrated to produce reasonable projections by leveraging historical relationships between variables. The model includes variables to differentiate balances between the two portfolios, capturing persistent differences in net charge-off rates. It uses a linear regression framework with a two-equation structure, allowing it to account for differences in historical net charge-off and delinquency rates. The model is estimated using data from both international cards portfolios and incorporates additional features to account for differences across firms without adding excessive complexity. Delinquency is defined as 60 days or more past due, although there are suggestions to align this definition with a 90-day threshold used in domestic models.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8857 | CP: 0.8802 | CR: 1.0000 | AC: 0.1699 | NS: 0.5000

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card portfolios and the International Small Business and Corporate Credit Card portfolios. It employs a slightly more complex model structure compared to the Domestic Models, utilizing a linear regression framework that projects net charge-off rates in two steps using two linear regressions. The first equation projects the delinquency rate, while the second projects the net charge-off rate. The model incorporates measures of both local and global macroeconomic conditions, differentiates between product types and geographic regions, and includes features to account for differences across firms without adding excessive complexity.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8856 | CP: 0.8125 | CR: 1.0000 | AC: 0.1634 | NS: 0.0000

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It employs a slightly more complex model structure compared to the Domestic Models, as the latter's approach is unable to reliably project net charge-off rates for the International portfolios. The model segments data by product type and geography, differentiating between individual-purpose cards and business-purpose cards, and accounts for regional economic conditions through measures of both local and global macroeconomic environments. The model includes a two-equation structure to capture the persistence of historical net charge-off and delinquency rates, and it incorporates additional portfolio characteristics to account for differences across firms without adding excessive complexity.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8857 | CP: 0.8556 | CR: 1.0000 | AC: 0.1667 | NS: 0.6667

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It employs a slightly more complex structure compared to Domestic Models, incorporating a two-equation model that simultaneously projects delinquency rates and net charge-off rates. The model segments data by product type and geography, allowing it to account for differences in risks and regional economic shocks. It includes variables such as the share of accounts within different credit score categories and flags for specific card types in different regions. The model aims to produce reasonable and reliable projections of net charge-off rates while minimizing complexity and maintaining interpretability.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8857 | CP: 0.7190 | CR: 1.0000 | AC: 0.1697 | NS: 0.6250

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It employs a two-equation structure that separately projects delinquency rates and net charge-off rates simultaneously. This model is calibrated using data segmented by product type and geography, allowing it to account for regional economic shocks and differences in risk levels across firms. The model incorporates various variables, including the share of accounts within different credit score categories, to enhance its predictive capabilities. The model is estimated once using data from both international cards portfolios, and it includes region-specific macroeconomic variables to reflect the impacts of the global macroeconomic environment.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8856 | CP: 0.5121 | CR: 1.0000 | AC: 0.1653 | NS: 0.7143

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card portfolio and the International Small Business and Corporate Credit Card portfolio. It employs a two-equation structure that separately projects delinquency rates and net charge-off rates simultaneously. The model incorporates additional portfolio characteristics and segments data by product type and geography, allowing it to account for regional economic shocks and differences in risk levels across firms. The model uses various variables, including delinquency rates, macroeconomic factors, and the share of accounts within different credit score categories, to produce accurate projections of net charge-off rates.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8857 | CP: 0.7028 | CR: 1.0000 | AC: 0.1668 | NS: 0.7778

The 'International Cards Model' is defined as a model used to project net charge-off rates for both the International Bank and Charge Card and International Small Business and Corporate Credit Card portfolios. It employs a slightly more complex model structure compared to the Domestic Models, utilizing a two-equation approach that separately projects delinquency rates and net charge-off rates simultaneously. This model incorporates regional economic conditions by segmenting data into four geographic regions (Canada, EMEA, LATAM, and APAC) and includes macroeconomic variables specific to these regions. Additionally, it accounts for differences in risk levels across firms by incorporating portfolio characteristics and the share of accounts within different credit score categories, although it does not segment the model by credit score due to potential sparsity in certain risk segments. The model aims to capture key differences in risks while maintaining interpretability and producing reasonable projections of net charge-off rates.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8020 | CP: 0.6117 | CR: 1.0000 | AC: 0.1659 | NS: 1.0000

The 'International Cards Model' is defined as a model that segments data by both product type and geography. It categorizes loans into three product types: “Bank card,” “Charge card,” and “Corporate, SME, and Business cards.” The model combines “Bank card” and “Charge card” into a single segment based on borrower type, while keeping corporate, SME, and business cards separate. This segmentation helps differentiate individual-purpose cards from business-purpose cards and captures key differences in risks while maintaining a less complex model structure.

Geographically, the model divides the International Card data into four regions: “Region 1: Canada,” “Region 2: EMEA — Europe, Middle East, and Africa,” “Region 3: LATAM — Latin America and Caribbean,” and “Region 4: APAC — Asia Pacific.” The model interacts these regions with region-specific macroeconomic variables to account for regional economic shocks. 

Credit score is not used to segment the model due to the risk of sparsity in certain segments, but the share of accounts within three credit score categories is included as a variable to project losses for bank and charge cards. The model employs a two-equation structure to simultaneously project delinquency rates and net charge-off rates, allowing it to incorporate additional information about risk levels across firms. This structure is deemed valuable for capturing persistent differences in delinquency and net charge-off rates across regions and portfolio types.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8020 | CP: 0.5667 | CR: 1.0000 | AC: 0.1635 | NS: 0.9167

The 'International Cards Model' is defined as a model that segments data by both product type and geography. It categorizes loans into three product types: “Bank card,” “Charge card,” and “Corporate, SME, and Business cards.” The model combines “Bank card” and “Charge card” into a single segment based on borrower type, while keeping corporate, SME, and business cards separate. This segmentation helps differentiate individual-purpose cards from business-purpose cards and captures key differences in risks while maintaining a less complex model structure.

Geographically, the model divides into four regions: “Region 1: Canada,” “Region 2: EMEA — Europe, Middle East, and Africa,” “Region 3: LATAM — Latin America and Caribbean,” and “Region 4: APAC — Asia Pacific.” The model interacts these regions with region-specific macroeconomic variables to account for regional economic shocks. Credit scores are not used to segment the model due to the risk of sparsity in certain segments, but the share of accounts within three credit score categories is included as a variable to project losses for bank and charge cards. The model employs a two-equation structure to project delinquency rates and net charge-off rates simultaneously, allowing for a more nuanced understanding of risk across different firms and regions.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7759 | CP: 0.5587 | CR: 1.0000 | AC: 0.1638 | NS: 0.8889

The 'International Cards Model' is defined as a model that segments data by both product type and geography. It categorizes loans into three product types: “Bank card,” “Charge card,” and “Corporate, SME, and Business cards.” The model combines “Bank card” and “Charge card” into a single segment while keeping corporate, SME, and business cards separate to differentiate individual-purpose cards from business-purpose cards. The model is further divided into four geographic regions: Canada, EMEA (Europe, Middle East, and Africa), LATAM (Latin America and Caribbean), and APAC (Asia Pacific). It incorporates region-specific macroeconomic variables to account for regional economic shocks and uses a two-equation structure to project delinquency rates and net charge-off rates simultaneously. The model also includes the share of accounts within three credit score categories as a variable to project losses for bank and charge cards, although credit score is not used to segment the model due to potential sparsity in certain risk segments.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8020 | CP: 0.6607 | CR: 0.0000 | AC: 0.1663 | NS: 0.7692

The 'International Cards Model' is defined as a model that segments data by both product type and geography. It categorizes loans into three product types: “Bank card,” “Charge card,” and “Corporate, SME, and Business cards.” The model combines “Bank card” and “Charge card” into a single segment based on borrower type, while keeping corporate, SME, and business cards separate. This segmentation helps differentiate individual-purpose cards from business-purpose cards and captures key differences in risks while maintaining a less complex model structure.

Geographically, the model divides into four regions: “Region 1: Canada,” “Region 2: EMEA — Europe, Middle East, and Africa,” “Region 3: LATAM — Latin America and Caribbean,” and “Region 4: APAC — Asia Pacific.” The model interacts these regions with region-specific macroeconomic variables to account for regional economic shocks. 

The model employs a two-equation structure that separately projects delinquency rates and net charge-off rates simultaneously, allowing it to incorporate additional information about differences in risk levels across firms. It includes portfolio characteristics and the share of accounts within three credit score categories as variables to project losses, although credit score is not used to segment the model due to the risk of sparsity in certain segments. Overall, the model aims to produce reliable projections of net charge-off rates while accounting for various risk factors and macroeconomic conditions.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.8571 | AR: 0.7036 | CP: 0.0000 | CR: 0.0000 | AC: 0.1474 | NS: 0.2857

The 'International Cards Model' is defined in the documentation as a model that delineates differences in geographies through coarse fixed effects by region (e.g., Canada, EMEA, LATAM, APAC) to measure regional economic conditions. It is used to define delinquency based on a threshold of 60 days or more past due, although there is a suggestion that the Federal Reserve should consider a threshold of 90 days or more past due. The model does not account for any geographic variation in the International Scalar Models, despite the importance of geographic factors.

---

## Question 35: What are 'scalar models' in the context of retail credit risk?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9807 | CP: 0.6250 | CR: 0.5000 | AC: 0.1722 | NS: 0.8750

Scalar models in the context of retail credit risk refer to a modeling approach that applies a single loss rate path to all firms reporting balance for a given portfolio. This method is characterized by its operational simplicity and consistent treatment across covered firms. However, it does not account for true differences in riskiness among the loans, as it treats loans identically regardless of observable risk characteristics. Scalar models are used when there is sparseness of reported data or limited balances in the portfolio, which reduces the impact of loss projections on stress testing results.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9065 | CP: 0.2000 | CR: 0.5000 | AC: 0.3858 | NS: 0.2222

Scalar models in the context of retail credit risk are an approach that applies a single loss rate path to all firms reporting balance for a given portfolio. This method contrasts with more complex bottom-up models and is currently used for a subset of portfolios within the Other Retail models. The advantages of scalar models include operational simplicity, consistent application across portfolios, and the production of robust and stable outcomes. They are particularly useful in situations where there is sparseness of reported data and limited balances, which can reduce the impact of loss projections on stress testing results.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9807 | CP: 0.1250 | CR: 0.0000 | AC: 0.3039 | NS: 0.0000

Scalar models in the context of retail credit risk are approaches that apply a single loss rate path to all firms reporting balance for a given portfolio. This method contrasts with more complex bottom-up models and is currently used for a subset of portfolios within the Other Retail models. Scalar models are operationally simple and provide a consistent framework for assessing credit risk across different portfolios. However, they may have limitations in differentiating loss rates based on observable risk characteristics, such as product type and credit score.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9408 | CP: 0.9500 | CR: 1.0000 | AC: 0.3997 | NS: 0.5000

Scalar models are a simplified approach used in retail credit risk modeling, particularly for portfolios with limited data and balances. They apply a single loss rate path to all firms reporting balance for a given portfolio, which allows for operational simplicity and consistent treatment across covered firms. This approach is utilized when there is sparseness of reported data and limited balances, reducing the impact of loss projections on stress testing results. Scalar models are designed to produce robust and stable outcomes driven by underlying risk factors and macroeconomic scenarios, while also allowing for conservative assumptions when necessary.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9535 | CP: 0.6829 | CR: 1.0000 | AC: 0.6131 | NS: 0.7778

Scalar models in the context of retail credit risk are approaches used to project net charge-off rates for various portfolios by assuming a constant net charge-off rate for each portfolio. This method applies a single loss rate path to all firms reporting balance for a given portfolio, which simplifies the modeling process and provides consistent treatment across covered firms. Scalar models are particularly useful in situations where there is limited historical data or sparse reporting, making it challenging to use more complex regression models. While they do not account for differences in riskiness among portfolios, their simplicity and operational efficiency make them a practical choice for certain retail credit risk assessments.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9535 | CP: 0.5179 | CR: 1.0000 | AC: 0.2561 | NS: 0.8125

Scalar models are used in the context of retail credit risk to project net charge-off rates for various portfolios by applying a constant net charge-off rate to each portfolio. This approach is operationally simple and provides consistent treatment across covered firms, but it does not account for differences in riskiness among the portfolios. Scalar models are typically employed when there is limited historical data or small balances in the portfolios, which reduces the impact of loss projections on stress testing results. They are straightforward applications of credit risk modeling practices that minimize operational challenges and allow for explainable results. However, they may lack the precision of more complex models, such as regression models, due to the sparseness of reported data.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9535 | CP: 0.6883 | CR: 1.0000 | AC: 0.4414 | NS: 0.5385

Scalar models are a type of modeling approach used in the context of retail credit risk to project net charge-off rates for various portfolios. They apply a single loss rate path to all firms reporting balance for a given portfolio, which simplifies the modeling process. This approach is operationally simple, provides consistent treatment across covered firms, and minimizes operational challenges. Scalar models pool loans from all firms without including firm-specific fixed effects, meaning differences in results are driven by variations in input data rather than firm-specific characteristics. They are particularly useful in situations where there is limited historical data or small balances in the portfolio, making more complex models like regression less effective. Scalar models are designed to produce robust and stable outcomes driven by underlying risk factors and macroeconomic scenarios.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9535 | CP: 0.7611 | CR: 1.0000 | AC: 0.2902 | NS: 0.7500

Scalar models in the context of retail credit risk are a simplified modeling approach used to assess loss projections across various portfolios. They apply a single loss rate path to all firms reporting balance for a given portfolio, which allows for operational simplicity and consistent treatment across covered firms. However, scalar models do not account for true differences in riskiness among firms or variations based on the severity of economic scenarios. They are often used in portfolios where there is limited historical data or where the balances are small, making more complex modeling techniques, like regression models, less effective or justified. The use of scalar models is particularly noted for their ability to reduce implementation costs and align with stress testing principles of simplicity.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9807 | CP: 0.6042 | CR: 1.0000 | AC: 0.2746 | NS: 0.7273

Scalar models in the context of retail credit risk refer to a modeling approach that applies a single loss rate path to all firms reporting balance for a given portfolio. This approach is characterized by its operational simplicity and consistent treatment across covered firms. However, it has limitations, as it does not account for true differences in riskiness across covered firms or variations based on the severity of different scenarios. Scalar models are used particularly in portfolios where there is sparseness of reported data and limited balances, which reduces the impact of loss projections on stress testing results. They are justified in certain portfolios due to the limited historical data available, making more complex modeling techniques, like regression models, less effective.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7399 | CP: 0.4750 | CR: 1.0000 | AC: 0.2850 | NS: 0.8333

Scalar models are used to project net charge-off rates for various portfolios within the Other Retail model. They assume a constant net charge-off rate for each portfolio, applying a single loss rate path to all firms reporting balance for a given portfolio. This approach is operationally simple and provides consistent treatment across covered firms; however, it does not account for differences in riskiness across firms or variations based on the severity of economic scenarios. Scalar models are chosen for certain portfolios due to factors such as the sparseness of reported data, limited balances, and the reduced impact of loss projections on stress testing results. They are justified in cases where historical data is limited, making more complex regression models less precise or feasible.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9716 | CP: 0.6433 | CR: 0.5000 | AC: 0.2782 | NS: 0.9167

Scalar models in the context of retail credit risk are approaches used to project net charge-off rates for various portfolios by applying a single loss rate path to all firms reporting balance for a given portfolio. These models assume a constant net charge-off rate for each portfolio, which simplifies implementation and provides consistent treatment across covered firms. However, scalar models do not account for differences in riskiness across firms or variations based on the severity of economic scenarios, leading to less precise projections compared to more complex regression models that incorporate segmentation and other risk characteristics. Scalar models are often used in situations where there is limited historical data or where the portfolios are small, making more complex modeling techniques less beneficial.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9807 | CP: 0.8929 | CR: 1.0000 | AC: 0.2611 | NS: 1.0000

Scalar models in the context of retail credit risk refer to a modeling approach that applies a single loss rate path to all firms reporting balance for a given portfolio. This approach is characterized by its operational simplicity and consistent treatment across covered firms. However, it does not account for true differences in riskiness across firms or variations based on the severity of different scenarios. Scalar models are used for certain portfolios within the Other Retail model due to factors such as the sparseness of reported data and limited balances, which reduce the impact of loss projections on stress testing results. While scalar models provide a straightforward method for assigning net charge-off rates, they are generally considered to produce less precise projections compared to more complex regression models that incorporate additional variables and segmentation.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9807 | CP: 0.8929 | CR: 1.0000 | AC: 0.2566 | NS: 0.9231

Scalar models in the context of retail credit risk refer to a modeling approach that applies a single loss rate path to all firms reporting balance for a given portfolio. This approach is characterized by its operational simplicity and consistent treatment across covered firms. However, it does not account for true differences in riskiness across firms or variations based on the severity of different scenarios. Scalar models are used for certain portfolios within the Other Retail model due to factors such as the sparseness of reported data and limited balances, which reduce the impact of loss projections on stress testing results. While scalar models are simpler and reduce implementation costs, they may produce less precise projections compared to more complex regression models that incorporate more granular information and allow for differentiation in riskiness across firms.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9535 | CP: 0.8929 | CR: 1.0000 | AC: 0.2666 | NS: 0.8000

Scalar models in the context of retail credit risk are a simplified modeling approach used to assess loss rates across various portfolios within the Other Retail model. These models apply a single loss rate path to all firms reporting balance for a given portfolio, which makes them operationally simple and provides consistent treatment across covered firms. However, scalar models do not account for true differences in riskiness among covered firms or variations based on the severity of different scenarios. They are used primarily due to the sparseness of reported data and limited balances in certain portfolios, which reduces the impact of loss projections on stress testing results. Scalar models are justified in cases where historical data is limited, making more complex regression models less feasible.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9626 | CP: 0.8929 | CR: 1.0000 | AC: 0.5293 | NS: 0.8462

Scalar models in the context of retail credit risk are a simplified modeling approach used to assess loss rates across various portfolios within the Other Retail model. This approach applies a single loss rate path to all firms reporting balance for a given portfolio, which makes it operationally simple and provides consistent treatment across covered firms. However, scalar models do not account for true differences in riskiness among covered firms or variations based on the severity of different scenarios. They are used primarily due to the sparseness of reported data and limited balances in certain portfolios, which reduces the impact of loss projections on stress testing results. Scalar models are justified when the historical data available is insufficient for more complex regression models, allowing for a straightforward assignment of net charge-off rates while maintaining simplicity in implementation.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0187 | NS: 0.0000

I don't know.

---

## Question 36: What is the rationale for using monthly data in some market risk models?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9391 | CP: 0.5074 | CR: 1.0000 | AC: 0.5468 | NS: 0.5000

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis. Additionally, using monthly data helps maintain a sufficient volume of data points to support a stable estimate.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9391 | CP: 0.3889 | CR: 1.0000 | AC: 0.5102 | NS: 0.5714

The rationale for using monthly data in some market risk models is to achieve estimate stability associated with higher frequency data and increasing numbers of observations. Monthly data helps to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test. Additionally, using monthly data maintains a sufficient volume of data points to support stable estimates and ensures sufficient resolution to capture the peaks and troughs of relevant stress events occurring in the calibration.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9391 | CP: 0.5593 | CR: 1.0000 | AC: 0.5560 | NS: 0.5000

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test. Additionally, monthly data maintains a sufficient volume of data points to support a stable estimate and ensures sufficient resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This approach strikes a balance between capturing market trends and avoiding overreaction to short-term fluctuations.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9391 | CP: 0.4125 | CR: 1.0000 | AC: 0.4287 | NS: 0.5556

The rationale for using monthly data in some market risk models is to achieve estimate stability while avoiding the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations. Monthly data allows the model to maintain a sufficient volume of data points to support stable estimates and ensures enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance is important for the forecast horizon of the stress test, where losses are projected on a quarterly basis.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9391 | CP: 0.3889 | CR: 1.0000 | AC: 0.4067 | NS: 0.5556

The rationale for using monthly data in some market risk models is to achieve estimate stability associated with higher frequency data and increasing numbers of observations, while also utilizing a time interval relevant to the stress test horizon and the macroeconomic shocks depicted. By using monthly data, the model aims to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test. Additionally, monthly data allows for maintaining a sufficient volume of data points to support a stable estimate and ensures sufficient resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9391 | CP: 0.3667 | CR: 1.0000 | AC: 0.5086 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test (where losses are projected on a quarterly basis). Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also capturing the peaks and troughs of relevant stress events occurring in the calibration window. This approach achieves a reasonable balance between avoiding noise and ensuring enough data for reliable modeling.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9391 | CP: 0.4167 | CR: 1.0000 | AC: 0.5095 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test (where losses are projected on a quarterly basis). Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate modeling.

### 8. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9391 | CP: 0.8167 | CR: 1.0000 | AC: 0.5106 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test (where losses are projected on a quarterly basis). Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate forecasting in stress tests.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9391 | CP: 0.9762 | CR: 1.0000 | AC: 0.5126 | NS: 0.6250

The rationale for using monthly data in some market risk models is twofold: (i) it helps avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis; and (ii) it maintains a sufficient volume of data points to support a stable estimate while also capturing the peaks and troughs of relevant stress events occurring in the calibration window. Monthly time series data thus achieve a reasonable balance between these two objectives.

### 10. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9391 | CP: 0.7577 | CR: 1.0000 | AC: 0.5094 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis. Additionally, using monthly data maintains a sufficient volume of data points to support stable estimates while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate modeling in stress tests.

### 11. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9391 | CP: 0.7893 | CR: 1.0000 | AC: 0.5095 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis. Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate modeling in stress tests.

### 12. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9391 | CP: 0.7611 | CR: 1.0000 | AC: 0.5094 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis. Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate modeling.

### 13. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9391 | CP: 0.7893 | CR: 1.0000 | AC: 0.5095 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test, where losses are projected on a quarterly basis. Additionally, using monthly data maintains a sufficient volume of data points to support a stable estimate while also providing enough resolution to capture the peaks and troughs of relevant stress events occurring in the calibration window. This balance between avoiding noise and ensuring data stability is crucial for accurate modeling in stress tests.

### 14. `chunk_size_500_chunk_overlap_300` — F: 0.8571 | AR: 0.9391 | CP: 0.7917 | CR: 1.0000 | AC: 0.6275 | NS: 0.5714

The rationale for using monthly data in some market risk models is to avoid the confounding effects of transient or short-term market microstructure noise, which is more prevalent in higher frequency observations and less relevant to the forecast horizon of the stress test. Additionally, using monthly data helps maintain a sufficient volume of data points to support stable estimates while being relevant to the stress test horizon and the macroeconomic shocks depicted.

### 15. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.3500 | CR: 0.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.1429 | CR: 0.0000 | AC: 0.0201 | NS: 0.0000

I don't know.

---

## Question 37: Which event type accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022?

### 1. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8990 | CP: 0.5556 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 2. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8990 | CP: 0.4778 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 3. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8991 | CP: 0.8056 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8990 | CP: 0.4667 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 5. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 6. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 7. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8990 | CP: 0.3333 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 8. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 9. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8991 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 10. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 11. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 12. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8990 | CP: 1.0000 | CR: 1.0000 | AC: 0.6082 | NS: 0.6667

Clients, Products, and Business Practices (CPBP) accounts for the largest proportion (72.5%) of gross operational losses incurred between 2000 and 2022.

### 13. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.0274 | NS: 0.0000

I don't know.

### 14. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.8333 | CR: 1.0000 | AC: 0.0274 | NS: 0.0000

I don't know.

### 15. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.4444 | CR: 0.0000 | AC: 0.0274 | NS: 0.0000

I don't know.

### 16. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.5444 | CR: 1.0000 | AC: 0.0274 | NS: 0.0000

I don't know.

---

## Question 38: Why does the Operational Risk Model estimate losses using gross amounts rather than losses net of recoveries?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.7519 | CP: 0.5556 | CR: 1.0000 | AC: 0.9085 | NS: 0.2500

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries due to the lower chance of recovery during stressful periods and the uncertainty over when recoveries will materialize.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9340 | CP: 0.4571 | CR: 1.0000 | AC: 0.7995 | NS: 0.2500

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because, during stressful periods, there is a lower chance of recovery, and there is uncertainty over when recoveries will materialize. Therefore, the model conservatively estimates losses by using the gross loss amount.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9183 | CP: 0.7333 | CR: 1.0000 | AC: 0.9101 | NS: 0.0000

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries because there is a lower chance of recovery during stressful periods and uncertainty over when recoveries will materialize.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9183 | CP: 0.7000 | CR: 1.0000 | AC: 0.9105 | NS: 0.5000

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9160 | CP: 0.5861 | CR: 1.0000 | AC: 0.9099 | NS: 0.5000

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries because there is a lower chance of recovery during stressful periods and there is uncertainty over when recoveries will materialize.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.7519 | CP: 0.6330 | CR: 1.0000 | AC: 0.9085 | NS: 0.2500

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries due to the lower chance of recovery during stressful periods and the uncertainty over when recoveries will materialize.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.7519 | CP: 0.6568 | CR: 1.0000 | AC: 0.9085 | NS: 0.2500

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries due to the lower chance of recovery during stressful periods and the uncertainty over when recoveries will materialize.

### 8. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9186 | CP: 0.7481 | CR: 1.0000 | AC: 0.9105 | NS: 0.5000

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9160 | CP: 0.6568 | CR: 1.0000 | AC: 0.9105 | NS: 0.2500

The Operational Risk Model conservatively estimates losses using the gross loss amount rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize.

### 10. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9340 | CP: 0.7857 | CR: 1.0000 | AC: 0.8020 | NS: 0.0000

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize. Therefore, the model conservatively estimates losses by using the gross loss amount.

### 11. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9340 | CP: 0.7857 | CR: 1.0000 | AC: 0.7591 | NS: 0.0000

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize. Therefore, the model conservatively estimates losses by using the gross loss amount.

### 12. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9305 | CP: 0.7857 | CR: 1.0000 | AC: 0.9091 | NS: 0.2500

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize. Therefore, the model conservatively estimates losses by using the gross loss amount.

### 13. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9305 | CP: 1.0000 | CR: 1.0000 | AC: 0.7216 | NS: 0.2500

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because there is a lower chance of recovery during stressful periods, and there is uncertainty over when recoveries will materialize. Therefore, the model conservatively estimates losses by using the gross loss amount.

### 14. `chunk_size_500_chunk_overlap_300` — F: 0.8000 | AR: 0.9340 | CP: 0.6349 | CR: 1.0000 | AC: 0.7236 | NS: 0.0000

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because there is a lower chance of recovery during stressful periods and uncertainty over when recoveries will materialize. This conservative approach ensures that the model accounts for the full extent of potential losses without relying on uncertain recovery amounts.

### 15. `chunk_size_500_chunk_overlap_50` — F: 0.5000 | AR: 0.9340 | CP: 0.2778 | CR: 1.0000 | AC: 0.6564 | NS: 0.1667

The Operational Risk Model estimates losses using gross amounts rather than losses net of recoveries because a small share of operational loss events allows firms to recover a portion of the loss amount, and the chance of recovery diminishes during stressful periods. Additionally, there is uncertainty over when recoveries will occur, making it more appropriate to project losses based on gross amounts to account for the full extent of potential operational losses.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.3222 | CR: 0.0000 | AC: 0.0330 | NS: 0.0000

I don't know.

---

## Question 39: What are 'idiosyncratic loss events' in operational risk?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9823 | CP: 0.4444 | CR: 1.0000 | AC: 0.6884 | NS: 0.5000

Idiosyncratic loss events in operational risk are losses that are specific to individual firms, as opposed to systemic events that affect multiple firms. An example of an idiosyncratic loss event is a cybersecurity attack that impacts only a single firm.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9823 | CP: 0.5533 | CR: 1.0000 | AC: 0.7939 | NS: 0.3333

Idiosyncratic loss events in operational risk are those losses that are specific to individual firms and are not correlated with broader market events or trends. These events can arise from unique circumstances affecting a single firm, such as cybersecurity attacks or rogue trading incidents, which do not necessarily reflect the operational risks faced by other firms in the industry.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9823 | CP: 0.3333 | CR: 1.0000 | AC: 0.5228 | NS: 0.2500

Idiosyncratic loss events in operational risk are those loss events that are specific to individual firms, meaning they do not affect the broader industry or market but rather impact a single organization. An example of such an event could be a cybersecurity attack that targets only one firm.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9823 | CP: 0.5833 | CR: 1.0000 | AC: 0.8334 | NS: 0.2500

Idiosyncratic loss events in operational risk are those loss events that are specific to individual firms, as opposed to being correlated with broader market or economic factors. These events can arise from unique circumstances or incidents affecting a single firm, such as cybersecurity attacks that impact only that firm.

### 5. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9744 | CP: 0.6089 | CR: 1.0000 | AC: 0.8565 | NS: 0.2000

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not correlate with broader market or economic conditions. These events can arise from unique circumstances or failures within a particular firm, such as cybersecurity attacks that impact only that firm, rather than events that affect multiple firms simultaneously.

### 6. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9743 | CP: 0.7878 | CR: 1.0000 | AC: 0.8150 | NS: 0.2857

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not necessarily correlate with broader economic factors or events affecting multiple firms. These events can include unique incidents such as cybersecurity attacks that impact only a single firm, as opposed to correlated events that affect several firms simultaneously. The term highlights the distinct and unpredictable nature of certain operational risks that may arise from a firm's specific circumstances or vulnerabilities.

### 7. `chunk_size_3000_chunk_overlap_200` — F: 0.8571 | AR: 0.9743 | CP: 0.8105 | CR: 1.0000 | AC: 0.6518 | NS: 0.5714

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not necessarily correlate with broader economic factors or events affecting multiple firms. These events can include unique incidents such as cybersecurity attacks that impact only a single firm, as opposed to systemic events that affect many firms simultaneously. The term highlights the distinct and unpredictable nature of certain operational risks that can arise from a firm's specific circumstances or vulnerabilities.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 0.8000 | AR: 0.9743 | CP: 0.6089 | CR: 1.0000 | AC: 0.8579 | NS: 0.2000

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not correlate with broader economic factors or events affecting multiple firms. These events can arise from unique circumstances or failures within a particular firm, such as cybersecurity attacks that impact only that firm, rather than systemic issues that affect the industry as a whole.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 0.8000 | AR: 0.9744 | CP: 0.8500 | CR: 1.0000 | AC: 0.5648 | NS: 0.2000

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not correlate with broader market or economic conditions. These events can arise from unique circumstances or failures within a particular firm, such as cybersecurity attacks that impact only that firm, rather than events that affect multiple firms simultaneously.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 0.8000 | AR: 0.9743 | CP: 0.8611 | CR: 1.0000 | AC: 0.8565 | NS: 0.2000

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not correlate with broader market or economic conditions. These events can arise from unique circumstances or failures within a particular firm, such as cybersecurity attacks that impact only that firm, rather than events that affect multiple firms simultaneously.

### 11. `chunk_size_3000_chunk_overlap_300` — F: 0.8000 | AR: 0.9744 | CP: 0.8105 | CR: 1.0000 | AC: 0.6912 | NS: 0.4000

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not necessarily correlate with broader economic factors or events affecting multiple firms. These events can arise from unique circumstances or vulnerabilities within a particular firm, such as cybersecurity attacks that impact only that firm, rather than systemic issues that affect the industry as a whole.

### 12. `chunk_size_1000_chunk_overlap_300` — F: 0.7500 | AR: 0.9823 | CP: 0.6683 | CR: 1.0000 | AC: 0.6579 | NS: 0.4444

Idiosyncratic loss events in operational risk are specific loss events that are unique to a single firm, as opposed to systemic events that affect multiple firms simultaneously. These events can arise from various factors, such as internal processes, systems, or incidents that do not correlate with broader economic conditions or events affecting the industry as a whole. Examples include cybersecurity attacks that impact only one firm.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 0.7143 | AR: 0.9744 | CP: 0.7878 | CR: 1.0000 | AC: 0.5215 | NS: 0.2857

Idiosyncratic loss events in operational risk refer to loss events that are specific to individual firms and do not correlate with broader market or economic conditions. These events can arise from unique circumstances or failures within a particular firm, such as cybersecurity attacks that impact only that firm, rather than events that affect multiple firms simultaneously. The term highlights the distinct and unpredictable nature of certain operational risks that may not be influenced by external factors.

### 14. `chunk_size_1000_chunk_overlap_200` — F: 0.6667 | AR: 0.9823 | CP: 0.6389 | CR: 1.0000 | AC: 0.6016 | NS: 0.3333

Idiosyncratic loss events in operational risk are those loss events that are specific to individual firms and are disconnected from broader economic conditions or trends. An example provided in the context is a rogue trading event, which may not be influenced by the overall amount of trading happening at a firm. These events are unique to a particular firm and do not correlate with losses experienced by other firms.

### 15. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.7183 | CR: 1.0000 | AC: 0.0254 | NS: 0.0000

I don't know.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.4167 | CR: 0.0000 | AC: 0.0254 | NS: 0.0000

I don't know.

---

## Question 40: Why is revenue generally not used as the primary risk indicator for operational risk in the Board's model?

### 1. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9881 | CP: 0.9500 | CR: 1.0000 | AC: 0.3061 | NS: 0.8750

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to decrease dramatically during recessions, which could lead to a sudden decrease in operational loss projections during periods of economic stress. This is not aligned with historical data and experiences, such as those from the 2008 financial crisis. Additionally, total income exhibits much higher volatility over time compared to asset-based measures, which would introduce greater volatility to operational loss projections. As a result, the Board determined that total assets were preferable to total income for scaling historical operational losses.

### 2. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9881 | CP: 0.6944 | CR: 1.0000 | AC: 0.6469 | NS: 0.6000

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size, which can lead to unstable loss projections. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. Additionally, during recessions, firm revenue can decrease dramatically, which could result in operational loss projections that do not align with historical data and experiences, such as those observed during the 2008 financial crisis. Therefore, the Board determined that total assets, which provide a more stable measure of operational risk exposure, is preferable to total income for scaling historical operational losses.

### 3. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9881 | CP: 0.8254 | CR: 1.0000 | AC: 0.6493 | NS: 0.7273

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size, which can lead to instability in loss projections. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. Additionally, during recessions, firm revenue can decrease dramatically, which could result in operational loss projections that do not align with historical data and experiences, such as those observed during the 2008 financial crisis. Therefore, the Board determined that total assets, which provide a more stable measure of exposure to operational risk, is preferable for scaling historical operational losses.

### 4. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9881 | CP: 0.8254 | CR: 1.0000 | AC: 0.6193 | NS: 0.7778

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. As a result, using revenue-based measures can lead to unstable loss projections, which is undesirable for stress testing models, particularly when the volatility may arise from unintuitive reasons. The Board determined that total assets, which provide a more stable measure of exposure to operational risk, is preferable for scaling historical operational losses.

### 5. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9881 | CP: 0.8635 | CR: 1.0000 | AC: 0.9407 | NS: 0.6667

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. As a result, using revenue-based measures could lead to unstable loss projections, which is undesirable for stress testing models, particularly when the volatility may arise from unintuitive reasons. The Board has determined that total assets, which provide a more stable measure of exposure to operational risk, is preferable for scaling historical operational losses.

### 6. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9881 | CP: 0.8254 | CR: 1.0000 | AC: 0.5993 | NS: 0.7778

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. As a result, using revenue-based measures could lead to unstable loss projections, which is undesirable for stress testing models, especially when the volatility may arise from unintuitive reasons. The Board determined that total assets, which provide a more stable measure of exposure to operational risk, is preferable for scaling historical operational losses.

### 7. `chunk_size_2000_chunk_overlap_300` — F: 0.9091 | AR: 0.9881 | CP: 0.8350 | CR: 1.0000 | AC: 0.6588 | NS: 0.6000

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size, which can lead to instability in loss projections. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and economic conditions. Additionally, during recessions, firm revenue can decrease dramatically, which could result in operational loss projections dropping unexpectedly, contrary to historical data trends. Therefore, the Board determined that total assets, which provide a more stable measure, are preferable for scaling historical operational losses.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 0.9000 | AR: 0.9881 | CP: 0.8611 | CR: 1.0000 | AC: 0.5873 | NS: 0.6000

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and the interest rate environment. As a result, using revenue-based scaling variables can lead to more unstable loss projections, which is undesirable for stress testing models, particularly when the volatility may arise from unintuitive reasons. Additionally, many operational loss events are idiosyncratic and may not correlate with the amount of business activity, making it difficult to select appropriate risk indicators based solely on revenue.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 0.9000 | AR: 0.9881 | CP: 0.8500 | CR: 1.0000 | AC: 0.5645 | NS: 0.5556

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size. This volatility can be influenced by factors that have little association with operational risk, such as monetary policy and the interest rate environment. As a result, using revenue-based scaling variables can lead to more unstable loss projections, which is undesirable for stress testing models, especially when the volatility may arise from unintuitive reasons. Additionally, many operational loss events are idiosyncratic and may not correlate with the amount of business activity reflected in revenue.

### 10. `chunk_size_1000_chunk_overlap_300` — F: 0.8750 | AR: 0.9881 | CP: 0.9500 | CR: 1.0000 | AC: 0.6755 | NS: 0.8750

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to decrease dramatically during recessions, which could lead to a sudden decrease in operational loss projections during periods of economic stress. This behavior is not aligned with historical data and the experiences from events like the 2008 financial crisis. Additionally, total income exhibits much higher volatility over time compared to asset-based measures, which would introduce greater volatility to operational loss projections, making it an undesirable feature for stress testing models.

### 11. `chunk_size_500_chunk_overlap_100` — F: 0.8333 | AR: 0.9881 | CP: 0.2500 | CR: 1.0000 | AC: 0.3144 | NS: 0.3333

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to decrease dramatically during recessions, which could lead to circumstances where operational loss projections also decrease. Additionally, operational losses can arise for reasons that are idiosyncratic and may not correlate with the amount of business activity, making revenue-based measures less reliable as indicators of operational risk exposure.

### 12. `chunk_size_1000_chunk_overlap_50` — F: 0.8333 | AR: 0.9881 | CP: 0.8056 | CR: 1.0000 | AC: 0.9550 | NS: 0.3333

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it is more volatile than asset size, and this volatility can be driven by factors that have little association with operational risk, such as monetary policy and the interest rate environment. This instability in revenue components can lead to less reliable projections of operational-risk losses compared to using asset size, which is shown to be more stable and significant in explaining operational risk exposure.

### 13. `chunk_size_1000_chunk_overlap_100` — F: 0.7778 | AR: 0.9881 | CP: 0.7200 | CR: 1.0000 | AC: 0.6004 | NS: 0.4444

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because it tends to be more volatile than asset size and can decrease dramatically during recessions, which may lead to sudden decreases in operational loss projections that do not align with historical data. Additionally, revenue measures can be influenced by economic factors that have little association with operational risk, such as monetary policy, making them less stable and reliable for projecting operational losses compared to asset-based measures.

### 14. `chunk_size_500_chunk_overlap_50` — F: 0.7500 | AR: 0.9881 | CP: 0.0000 | CR: 0.0000 | AC: 0.3955 | NS: 0.2500

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because operational losses can arise for reasons that are idiosyncratic and may not be directly related to the amount of business activity within a specific area. Many operational loss events have distinct characteristics and can be influenced by various economic and non-economic factors, making it difficult to establish a direct correlation between revenue and operational risk. Additionally, the model is driven heavily by different revenue components, which are treated separately to avoid potential double-counting of losses.

### 15. `chunk_size_500_chunk_overlap_300` — F: 0.6000 | AR: 0.9881 | CP: 0.3778 | CR: 0.0000 | AC: 0.3277 | NS: 0.0000

Revenue is generally not used as the primary risk indicator for operational risk in the Board's model because firm revenue tends to decrease dramatically during recessions. This could lead to circumstances where operational loss projections decrease suddenly during periods of economic stress, which is not aligned with historical data and the characteristics of operational losses.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0137 | NS: 0.0000

I don't know.

---

## Question 41: In the Operational Risk Model, what does the 'small-loss component model' project?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9057 | CP: 0.4854 | CR: 1.0000 | AC: 0.3885 | NS: 0.7500

The 'small-loss component model' in the Operational Risk Model estimates losses below the $20,000 threshold. It accounts for losses that are not included in the input data for the distributional model, utilizing data from firms that report operational loss data without any threshold or with a threshold lower than $20,000.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.7985 | CP: 0.7929 | CR: 1.0000 | AC: 0.1574 | NS: 0.7500

The 'small-loss component model' projects losses below the $20,000 threshold. It estimates loss events below this threshold based on the observation that the share of smaller loss events does not vary much between firms, but that firms’ total losses below this threshold are proportional to total assets.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.7985 | CP: 0.4444 | CR: 1.0000 | AC: 0.4490 | NS: 1.0000

The 'small-loss component model' projects loss events of less than $20,000.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9384 | CP: 0.8056 | CR: 1.0000 | AC: 0.5826 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events of less than $20,000.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9384 | CP: 0.8056 | CR: 1.0000 | AC: 0.5826 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events of less than $20,000.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.7985 | CP: 0.7708 | CR: 1.0000 | AC: 0.1544 | NS: 1.0000

The 'small-loss component model' projects loss events of less than $20,000. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a threshold lower than $20,000, and it averages asset-scaled aggregate losses from below-threshold events over time and across firms to project associated loss events based on asset size.

### 7. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.7985 | CP: 0.5222 | CR: 1.0000 | AC: 0.4256 | NS: 1.0000

The 'small-loss component model' projects loss events below the $20,000 modeling threshold. It estimates losses that are not included in the input data for the distributional model by averaging asset-scaled aggregate losses from below-threshold events over time and across firms.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9384 | CP: 0.6222 | CR: 1.0000 | AC: 0.3750 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000, and it is based on the observation that the share of smaller loss events does not vary much between firms, while total losses below this threshold are proportional to firm size, as measured by total assets.

### 9. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7834 | CP: 0.6222 | CR: 1.0000 | AC: 0.3449 | NS: 1.0000

The 'small-loss component model' projects loss events below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000, and it is based on the observation that the share of smaller loss events does not vary much between firms, while total losses below this threshold are proportional to firm size, as measured by total assets.

### 10. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9384 | CP: 0.6222 | CR: 1.0000 | AC: 0.3748 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000, and it is based on the observation that the share of smaller loss events does not vary much between firms, but total losses below this threshold are proportional to firm size, as measured by total assets.

### 11. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9384 | CP: 0.7093 | CR: 1.0000 | AC: 0.3482 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000, and it is based on the observation that the share of smaller loss events does not vary much between firms, while total losses below this threshold are proportional to firm size, as measured by total assets.

### 12. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9384 | CP: 0.7093 | CR: 1.0000 | AC: 0.3739 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000. The model is based on the observation that the share of smaller loss events does not vary much between firms, and that total losses below this threshold are proportional to firm size, as measured by total assets.

### 13. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9384 | CP: 0.7093 | CR: 1.0000 | AC: 0.1596 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000. The model is based on the observation that the share of smaller loss events does not vary much between firms, and that total losses below this threshold are proportional to firm size, as measured by total assets.

### 14. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9384 | CP: 0.7093 | CR: 1.0000 | AC: 0.1596 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model projects loss events that are below the $20,000 modeling threshold. It estimates these losses by utilizing data from firms that report operational loss data without any threshold or with a lower threshold than $20,000. The model is based on the observation that the share of smaller loss events does not vary much between firms, and that total losses below this threshold are proportional to firm size, as measured by total assets.

### 15. `chunk_size_500_chunk_overlap_50` — F: 0.6667 | AR: 0.9057 | CP: 0.3750 | CR: 1.0000 | AC: 0.1567 | NS: 1.0000

The 'small-loss component model' in the Operational Risk Model estimates losses below the $20,000 threshold. It utilizes operational loss data reported by several firms that either do not have a threshold or have one that is lower than this threshold.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0275 | NS: 0.0000

I don't know.

---

## Question 42: What is the primary objective of the distributional model in operational risk?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.7736 | CR: 0.0000 | AC: 0.3344 | NS: 0.7500

The primary objective of the distributional model in operational risk is to estimate potential operational losses over hypothetical stress scenarios by capturing a wide range of operational loss events influenced by various economic and non-economic factors. It aims to provide a robust, consistent, and comparable approach to projecting operational losses, particularly accounting for large loss events that may arise from different underlying causes.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.8560 | CR: 1.0000 | AC: 0.7855 | NS: 0.4000

The primary objective of the distributional model in operational risk is to produce stressed operational loss projections that could be either systemic, correlated across several firms, or specific to individual firms. It aims to capture the idiosyncratic nature of operational risk and the wide range of causes that underlie operational losses.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.8560 | CR: 1.0000 | AC: 0.9433 | NS: 0.0000

The primary objective of the distributional model in operational risk is to produce stressed operational loss projections that could be either systemic, correlated across several firms, or specific to individual firms.

### 4. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.3833 | CR: 0.0000 | AC: 0.3164 | NS: 0.2000

The primary objective of the distributional model in operational risk is to estimate potential operational losses over hypothetical stress scenarios by reflecting a severe and rare outcome based on the unconditional properties of the historical operational loss event distribution. It aims to provide a conservative loss estimate that accounts for a range of different risks that firms may face, informed by industry experience across firms.

### 5. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.7292 | CR: 1.0000 | AC: 0.2919 | NS: 0.8333

The primary objective of the distributional model in operational risk is to produce conservative loss estimates that account for a range of different risks that firms may face, by taking a tail percentile of the unconditional aggregate loss distribution. This model is informed by industry experience across firms and is designed to reflect the idiosyncratic nature of operational risk and the wide range of causes underlying operational losses.

### 6. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.6429 | CR: 1.0000 | AC: 0.1569 | NS: 0.4000

The primary objective of the distributional model in operational risk is to produce conservative loss estimates that account for a range of different risks that firms may face, by using an unconditional aggregate loss distribution informed by industry experience across firms. This model is designed to reflect the idiosyncratic nature of operational risk and the wide range of causes underlying operational losses.

### 7. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.7222 | CR: 1.0000 | AC: 0.9433 | NS: 0.0000

The primary objective of the distributional model in operational risk is to produce stressed operational loss projections that could be either systemic, correlated across several firms, or specific to individual firms.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.6844 | CR: 1.0000 | AC: 0.3189 | NS: 0.8000

The primary objective of the distributional model in operational risk is to estimate potential operational losses over hypothetical stress scenarios by capturing the idiosyncratic nature of operational risk and accounting for a wide range of causes that underlie operational losses. It produces loss projections that reflect severe and rare outcomes, informed by the unconditional distribution of historical operational loss events across firms.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.8214 | CR: 1.0000 | AC: 0.3028 | NS: 0.8750

The primary objective of the distributional model in operational risk is to produce loss projections that reflect severe and rare outcomes resulting from a broad range of different operational loss events. It captures the idiosyncratic nature of operational risk and accounts for large loss events that may arise from various factors, including those coinciding with severe macroeconomic downturns. The model is driven by the unconditional properties of the historical operational loss event distribution, allowing it to provide conservative loss estimates based on a standard set of assumptions applicable to all firms.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.9095 | CR: 1.0000 | AC: 0.3030 | NS: 0.7143

The primary objective of the distributional model in operational risk is to produce loss projections that reflect severe and rare outcomes resulting from a broad range of different operational loss events. It captures the idiosyncratic nature of operational risk and accounts for large loss events that may arise from various factors, including those coinciding with severe macroeconomic downturns. The model is driven by the unconditional properties of the historical operational loss event distribution, allowing it to provide a conservative loss estimate based on industry experience across firms.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.7440 | CR: 1.0000 | AC: 0.2808 | NS: 0.8750

The primary objective of the distributional model in operational risk is to produce loss projections that reflect severe and rare outcomes resulting from a broad range of different operational loss events. It captures the idiosyncratic nature of operational risk and accounts for large loss events that may arise from various factors, including those coinciding with severe macroeconomic downturns. The model is driven by the unconditional properties of the historical operational loss event distribution, allowing it to provide a conservative loss estimate that considers a wide range of risks faced by firms.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.9094 | CR: 1.0000 | AC: 0.1601 | NS: 0.8571

The primary objective of the distributional model in operational risk is to produce an unconditional distribution of operational loss amounts, which reflects a severe and rare outcome that could result from a broad range of different loss events. This model captures the idiosyncratic nature of operational risk and accounts for large loss events that might arise from various factors, including those that may coincide with severe macroeconomic downturns. It aims to provide a conservative loss estimate by taking a tail percentile of the unconditional aggregate loss distribution.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.1601 | NS: 0.8571

The primary objective of the distributional model in operational risk is to produce an unconditional distribution of operational loss amounts, which reflects a severe and rare outcome that could result from a broad range of different loss events. This model captures the idiosyncratic nature of operational risk and accounts for large loss events that might arise from various factors, including those that may coincide with severe macroeconomic downturns. It aims to provide a conservative loss estimate by taking a tail percentile of the unconditional aggregate loss distribution.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.9094 | CR: 1.0000 | AC: 0.1655 | NS: 0.7143

The primary objective of the distributional model in operational risk is to produce an unconditional distribution of operational loss amounts, which reflects a severe and rare outcome that could result from a broad range of different loss events. It aims to capture the idiosyncratic nature of operational risk and account for large loss events that might arise from various factors, including those that may coincide with severe macroeconomic downturns. The model generates loss projections based on a selected tail percentile of the distribution, informed by the frequency of historical recessions.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 1.0000 | CR: 1.0000 | AC: 0.1601 | NS: 0.8571

The primary objective of the distributional model in operational risk is to produce an unconditional distribution of operational loss amounts, which reflects a severe and rare outcome that could result from a broad range of different loss events. This model captures the idiosyncratic nature of operational risk and accounts for large loss events that might arise from various factors, including those that may coincide with severe macroeconomic downturns. It aims to provide a conservative loss estimate by taking a tail percentile of the unconditional aggregate loss distribution.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.4286 | AR: 1.0000 | CP: 0.2917 | CR: 1.0000 | AC: 0.2884 | NS: 0.0000

The primary objective of the distributional model in operational risk is to project operational losses in a way that is less sensitive to assumptions about the timing and impact of large loss events. This approach aims to improve the measure of operational risk exposure and enhance the stability, robustness, consistency, and comparability across firms.

---

## Question 43: What specific 2024 event is cited as an example of an operational loss caused by system outages?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.7646 | CP: 0.6095 | CR: 1.0000 | AC: 0.5884 | NS: 0.0000

The widespread system outages caused by a faulty CrowdStrike update in 2024 is cited as an example of an operational loss caused by system outages.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9685 | CP: 0.7611 | CR: 1.0000 | AC: 0.5011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9514 | CP: 0.8333 | CR: 1.0000 | AC: 0.7011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9685 | CP: 0.8095 | CR: 1.0000 | AC: 0.7011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9685 | CP: 1.0000 | CR: 1.0000 | AC: 0.5761 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9685 | CP: 0.7778 | CR: 1.0000 | AC: 0.5011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 7. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9685 | CP: 0.8333 | CR: 1.0000 | AC: 0.7011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 8. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9628 | CP: 1.0000 | CR: 1.0000 | AC: 0.9511 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9685 | CP: 1.0000 | CR: 1.0000 | AC: 0.7011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 10. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9685 | CP: 1.0000 | CR: 1.0000 | AC: 0.5011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 11. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9628 | CP: 1.0000 | CR: 1.0000 | AC: 0.7011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 12. `chunk_size_500_chunk_overlap_50` — F: 0.5000 | AR: 0.9012 | CP: 0.7000 | CR: 1.0000 | AC: 0.5027 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is a faulty CrowdStrike update.

### 13. `chunk_size_2000_chunk_overlap_200` — F: 0.5000 | AR: 0.9628 | CP: 1.0000 | CR: 1.0000 | AC: 0.5011 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 14. `chunk_size_3000_chunk_overlap_50` — F: 0.5000 | AR: 0.9685 | CP: 1.0000 | CR: 1.0000 | AC: 0.9511 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 15. `chunk_size_3000_chunk_overlap_100` — F: 0.5000 | AR: 0.9685 | CP: 1.0000 | CR: 1.0000 | AC: 0.9511 | NS: 0.5000

The specific 2024 event cited as an example of an operational loss caused by system outages is the widespread system outages caused by a faulty CrowdStrike update.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0191 | NS: 0.0000

I don't know.

---

## Question 44: What does the Bayesian Information Criterion (BIC) measure according to the glossary?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9150 | CP: 1.0000 | CR: 1.0000 | AC: 0.8046 | NS: 0.3333

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity. It favors increased complexity only if the resulting improvement in fit sufficiently compensates for the loss of simplicity.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9150 | CP: 0.8500 | CR: 1.0000 | AC: 0.5068 | NS: 0.0000

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity.

### 3. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9150 | CP: 0.8708 | CR: 1.0000 | AC: 0.8068 | NS: 0.0000

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8750 | CP: 1.0000 | CR: 1.0000 | AC: 0.9508 | NS: 0.6000

The Bayesian Information Criterion (BIC) is a statistical measure typically used in model selection to avoid overfitting a regression model. It prioritizes goodness of fit but penalizes complexity.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8750 | CP: 1.0000 | CR: 1.0000 | AC: 0.9489 | NS: 0.8571

The Bayesian Information Criterion (BIC) is a statistical measure typically used in model selection to avoid overfitting a regression model. It prioritizes goodness of fit but penalizes complexity. A lower BIC indicates the preferred model specification, as it suggests either a higher likelihood, a lower number of parameters, or both.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8750 | CP: 1.0000 | CR: 1.0000 | AC: 0.9485 | NS: 0.2857

The Bayesian Information Criterion (BIC) is a statistical measure typically used in model selection to avoid overfitting a regression model. It prioritizes goodness of fit but penalizes complexity. A lower BIC indicates the preferred specification when comparing two models, as it suggests either a higher likelihood, a lower number of parameters, or both.

### 7. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8750 | CP: 1.0000 | CR: 1.0000 | AC: 0.9486 | NS: 0.7143

The Bayesian Information Criterion (BIC) is a statistical measure typically used in model selection to avoid overfitting a regression model. It prioritizes goodness of fit but penalizes complexity. A lower BIC indicates the preferred specification when comparing two models, as it suggests either a higher likelihood, a lower number of parameters, or both.

### 8. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9149 | CP: 0.5000 | CR: 1.0000 | AC: 0.8047 | NS: 0.3333

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity. It favors increased complexity only if the resulting improvement in fit sufficiently compensates for the loss of simplicity.

### 9. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9150 | CP: 1.0000 | CR: 1.0000 | AC: 0.8051 | NS: 0.3333

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity. BIC will favor increased complexity only if the resulting improvement in fit sufficiently compensates for the loss of simplicity.

### 10. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9150 | CP: 1.0000 | CR: 1.0000 | AC: 0.8046 | NS: 0.3333

The Bayesian Information Criterion (BIC) measures a model’s goodness of fit while penalizing complexity. It favors increased complexity only if the resulting improvement in fit sufficiently compensates for the loss of simplicity.

### 11. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0255 | NS: 0.0000

I don't know.

### 12. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.7755 | NS: 0.0000

I don't know.

### 13. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0255 | NS: 0.0000

I don't know.

### 14. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7755 | NS: n/a

I don't know.

### 15. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0255 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.7755 | NS: 0.0000

I don't know.

---

## Question 45: How is the 'Projected Interest Income Rate' handled in the PPNR model revisions?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0811 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by modeling the interest rate path differently for fixed-rate and variable-rate products over the projection periods. Interest income consists of interest income from existing portfolios and from new originations during the projection periods under a flat balance assumption, with both wholesale and retail portfolios re-originating based on different runoff rates at each projection quarter.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0788 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by considering interest income from existing portfolios and from new originations during the projection periods under a flat balance assumption. This approach ensures consistency while maintaining a conservative and supportable basis for interest income projections.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.1000 | CR: 0.0000 | AC: 0.0804 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by modeling the interest rate path differently for fixed-rate and variable-rate products over the projection window. Interest income consists of interest from existing portfolios and new originations under a flat balance assumption. For variable-rate products, projected interest rates are determined using base rate-related variables from the scenario file combined with an estimated spread. Most variable rates reset quarterly while balances remain unchanged under the flat balance assumption. Additionally, all portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to that floor.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9818 | CP: 0.0000 | CR: 0.0000 | AC: 0.0820 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is determined using the base rate-related variables from the scenario file, combined with an estimated spread. For variable-rate products, projected interest rates are calculated while assuming that balances remain unchanged under a flat balance assumption. The approach ensures consistency and maintains a conservative and supportable basis for interest income projections. Additionally, the projected interest rate path is modeled differently for fixed-rate and variable-rate products over the projection window, with all portfolios having a portfolio-specific interest rate floor that binds if the projected interest rate decreases to that floor.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0861 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by modeling the interest rate path differently for fixed-rate and variable-rate products over the projection window. For variable-rate products, projected interest rates are determined using a base rate-related approach with data from the FR Y-14M and FR Y-14Q regulatory reports. This granular approach allows for deriving changes in interest income directly from loan characteristics, specifically the type of interest rate variability. The model incorporates a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to that floor. Overall, the approach aims to provide a more accurate reflection of the income impact of loan characteristics within a scenario, enhancing the model's sensitivity to projected scenarios.

### 6. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0828 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by modeling interest income from existing portfolios and new originations during the projection periods under a flat balance assumption. The Board proposes to model the interest rate path differently for fixed-rate and variable-rate products over the projection window. All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor. For variable-rate products, projected interest rates are determined using base rate-related variables from the scenario file, combined with an estimated spread. Most variable rates reset quarterly while balances of variable-rate products remain unchanged under the flat balance assumption.

### 7. `chunk_size_500_chunk_overlap_100` — F: 0.8000 | AR: 1.0000 | CP: 1.0000 | CR: 0.0000 | AC: 0.0814 | NS: 0.0000

The 'Projected Interest Income Rate' in the PPNR model revisions is handled by ensuring that interest income consists of interest income from existing portfolios and from new originations during the projection periods under a flat balance assumption. This approach maintains a conservative and supportable basis for interest income projections while holding the jump-off interest rate and Prime Rate constant over projection quarters.

### 8. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 9. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 1.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0243 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0244 | NS: 0.0000

I don't know.

---

## Question 46: How many components of PPNR does the Board model separately?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9735 | CP: 0.4444 | CR: 1.0000 | AC: 0.6611 | NS: 0.0000

The Board models 23 components of PPNR separately.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9735 | CP: 0.5833 | CR: 1.0000 | AC: 0.6611 | NS: 0.0000

The Board models 23 components of PPNR separately.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9735 | CP: 1.0000 | CR: 1.0000 | AC: 0.6611 | NS: 0.0000

The Board models 23 components of PPNR separately.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9735 | CP: 0.9029 | CR: 1.0000 | AC: 0.6611 | NS: 0.0000

The Board models 23 components of PPNR separately.

### 5. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.7582 | CP: 0.2917 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 6. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.7582 | CP: 0.4821 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 7. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7582 | CP: 0.3929 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 8. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.7582 | CP: 0.2500 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 9. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7582 | CP: 0.5595 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 10. `chunk_size_1000_chunk_overlap_100` — F: 0.7500 | AR: 0.6296 | CP: 0.1000 | CR: 0.0000 | AC: 0.2039 | NS: 0.0000

The Board models a total of 20 components of pre-provision net revenue (PPNR) separately: 8 components of interest income, 6 components of interest expense, and 6 components of noninterest income.

### 11. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0310 | NS: 0.0000

I don't know.

### 12. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.9571 | CP: 0.1000 | CR: 0.0000 | AC: 0.1604 | NS: 0.0000

The Board models three components of PPNR separately: interest income, interest expense, and noninterest income.

### 13. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 1.0000 | CP: 0.3611 | CR: 0.0000 | AC: 0.1614 | NS: 0.0000

The Board models a total of 20 components of PPNR separately.

### 14. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.7582 | CP: 0.3333 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 15. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.7582 | CP: 0.2778 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.7582 | CP: 0.5000 | CR: 1.0000 | AC: 0.9754 | NS: 0.0000

The Board models 23 components of pre-provision net revenue (PPNR) separately.

---

## Question 47: Why are capital-neutral items like goodwill impairment excluded from PPNR models?

### 1. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.2000 | CR: 1.0000 | AC: 0.3765 | NS: 0.0000

Capital-neutral items like goodwill impairment are excluded from PPNR models to prevent the model from punitively assigning losses against balances that are not included in capital. This exclusion helps avoid a double-counting scenario, where losses to the carry value of a deduction item are mechanically offset by a reduced capital deduction in respect of that item.

### 2. `chunk_size_1000_chunk_overlap_100` — F: 0.7500 | AR: 1.0000 | CP: 0.3611 | CR: 1.0000 | AC: 0.6763 | NS: 0.2500

Capital-neutral items like goodwill impairment are excluded from PPNR models because projecting capital-neutral flows would not impact stress testing outcomes. This means that including these items would not affect the overall capital assessment during stress tests, so they are omitted to simplify the modeling process.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 0.6667 | AR: 1.0000 | CP: 0.1825 | CR: 1.0000 | AC: 0.7777 | NS: 0.3333

Capital-neutral items like goodwill impairment are excluded from PPNR models because projecting capital-neutral flows would not impact stress testing outcomes. This means that including these items would not provide relevant information for assessing the capital adequacy of firms during stress tests.

### 4. `chunk_size_500_chunk_overlap_100` — F: 0.3333 | AR: 1.0000 | CP: 0.2429 | CR: 0.0000 | AC: 0.2926 | NS: 0.5000

Capital-neutral items like goodwill impairment are excluded from PPNR models because they do not reflect the ongoing operational performance of a firm. These items are considered non-recurring or non-operational in nature, and their exclusion helps to provide a clearer picture of a firm's core earnings and financial health. By removing these items, the PPNR models can focus on more stable and predictable revenue and expense components that are relevant for assessing capital adequacy and performance.

### 5. `chunk_size_500_chunk_overlap_300` — F: 0.1667 | AR: 1.0000 | CP: 0.5079 | CR: 0.0000 | AC: 0.3123 | NS: 0.0000

Capital-neutral items like goodwill impairment are excluded from PPNR models because they do not impact the core earnings or operational performance of a firm. These items are considered non-recurring or non-operational in nature, and their exclusion helps to provide a clearer picture of the firm's ongoing profitability and financial health. By removing such items, the models can focus on more stable and predictable revenue streams, allowing for better forecasting and analysis of the firm's performance.

### 6. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 7. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.5000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 8. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 9. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 10. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 11. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 12. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.5000 | CR: 1.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 13. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 14. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.2000 | CR: 1.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.2500 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.2250 | CR: 0.0000 | AC: 0.0411 | NS: 0.0000

I don't know.

---

## Question 48: What does the term 'Autocorrelation' mean in the context of the supervisory stress test models?

### 1. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 2. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 3. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 4. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 5. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 6. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.6856 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 7. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.6855 | CP: 1.0000 | CR: 1.0000 | AC: 0.7951 | NS: 0.3333

Autocorrelation refers to the correlation between the errors in different time periods within a time series or panel data model.

### 8. `chunk_size_500_chunk_overlap_50` — F: 0.6667 | AR: 0.9782 | CP: 1.0000 | CR: 1.0000 | AC: 0.4672 | NS: 0.2500

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 9. `chunk_size_500_chunk_overlap_100` — F: 0.6667 | AR: 0.9782 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 10. `chunk_size_500_chunk_overlap_300` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 11. `chunk_size_1000_chunk_overlap_100` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 0.6667 | AR: 0.9809 | CP: 1.0000 | CR: 1.0000 | AC: 0.5422 | NS: 0.0000

In the context of the supervisory stress test models, 'Autocorrelation' refers to the correlation between the errors in different time periods within a time series or panel data model.

### 16. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 0.0000 | AC: 0.0178 | NS: 0.0000

I don't know.

---

## Question 49: What is an 'Autoregressive process' according to the model glossary?

### 1. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.8056 | CP: 0.4860 | CR: 1.0000 | AC: 0.9251 | NS: 0.0000

An 'Autoregressive process' is a time series model whose current value depends linearly on one or more of its previous values plus an unpredictable disturbance.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.7933 | CP: 0.1944 | CR: 1.0000 | AC: 0.8927 | NS: 0.0000

An 'Autoregressive process' is a statistical model where the current value of a variable is expressed as a linear function of its own past values, plus a stochastic error term. It is commonly used in time series analysis to predict future outcomes based on past performance, as past values are informative for forecasting.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.7526 | CP: 0.2667 | CR: 1.0000 | AC: 0.8277 | NS: 0.1667

An autoregressive process is a time series process in which its current value is a linear function of its own observations in the previous periods, plus a white noise process. Specifically, an autoregressive representation of order 2 means that the current value depends on its own observations from the previous two periods. Autoregressive terms are included in time series models when past performance is informative in predicting future outcomes.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.7933 | CP: 0.6111 | CR: 1.0000 | AC: 0.6339 | NS: 0.0000

An 'Autoregressive process' is a statistical model where the current value of a variable is regressed on its own past values. It reflects the recent past performance of the dependent variable and is used to account for persistence in the variable's behavior over time. In the context of the models discussed, it helps in predicting future values based on historical data.

### 5. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7933 | CP: 0.5148 | CR: 1.0000 | AC: 0.9251 | NS: 0.0000

An 'Autoregressive process' is a time series model whose current value depends linearly on one or more of its previous values plus an unpredictable disturbance.

### 6. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.7269 | CP: 0.6726 | CR: 1.0000 | AC: 0.8335 | NS: 0.5000

An 'autoregressive process' is a statistical model used in time series analysis where the current value of a variable is regressed on its own previous values. It is commonly included in models when past performance is informative in predicting future outcomes. In the context of the models discussed, autoregressive terms improve forecast performance by capturing persistence in the data, allowing for better predictions based on historical values.

### 7. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.7633 | CP: 0.9094 | CR: 1.0000 | AC: 0.8901 | NS: 0.6250

An 'Autoregressive process' is a statistical model where the current value of a variable is regressed on its own past values. It is commonly used in time series models to predict future outcomes based on past performance, as past values are informative in forecasting future behavior. In the context provided, autoregressive terms improve model forecast performance by capturing persistence in the data and reducing volatility from seasonal effects.

### 8. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8055 | CP: 0.9068 | CR: 1.0000 | AC: 0.9251 | NS: 0.0000

An 'Autoregressive process' is a time series model whose current value depends linearly on one or more of its previous values plus an unpredictable disturbance.

### 9. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7269 | CP: 0.9094 | CR: 1.0000 | AC: 0.6393 | NS: 0.2857

An 'Autoregressive process' is a statistical model where the current value of a variable is regressed on its own past values. It is commonly used in time series analysis to predict future values based on historical data, as past performance is informative in predicting future outcomes. In the context provided, autoregressive terms improve model forecast performance by capturing the persistence of the dependent variable over time.

### 10. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.7934 | CP: 0.8552 | CR: 1.0000 | AC: 0.6429 | NS: 0.5714

An 'Autoregressive process' is a statistical model where the current value of a variable is regressed on its own past values. It is commonly used in time series analysis to capture the relationship between a variable and its previous values, allowing for persistence in the variable's behavior over time. This structure is justified as it accounts for the correlation between the observed value of a component in a certain quarter and the observed value for the same component in the previous quarter.

### 11. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.1667 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

### 12. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.1667 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

### 13. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

### 14. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.3500 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

### 15. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.4694 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

### 16. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.5148 | CR: 1.0000 | AC: 0.0210 | NS: 0.0000

I don't know.

---

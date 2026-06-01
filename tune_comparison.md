# RAG Hyperparameter Tune Comparison

Generated from 32 log files in `logs/`.

## Summary Table

> - **Faithfulness (F)**: Measures whether every claim in the generated answer is supported by the retrieved context. The judge LLM extracts atomic statements from the answer and verifies each one against the chunks. A score of 1.0 means nothing was hallucinated; 0.0 means the answer is entirely unsupported. Low faithfulness usually signals the LLM is drawing on parametric knowledge instead of the retrieved documents. *Example: if the answer states "the stress test threshold is 4.5%" but no retrieved chunk mentions that figure, that claim is unfaithful and lowers the score.*
> - **Answer Relevancy (AR)**: Measures how directly the answer addresses the question — penalising vague, incomplete, or off-topic responses. It works by prompting the LLM to generate several questions that the answer could plausibly answer, then computing the average cosine similarity of those synthetic questions back to the original. High AR means the answer is focused and on-point; low AR means it drifted or hedged excessively. *Example: if the question asks "what is the purpose of stress testing?" and the answer spends most of its content describing who conducts stress tests rather than why, the synthetic questions generated from it will not closely match the original, pulling AR down.*
> - **Context Precision (CP)**: Measures whether the most relevant chunks appear near the top of the retrieved set. The judge LLM decides for each chunk whether it actually contributed to answering the question, then computes a precision-at-k style score that rewards relevant chunks ranked early and penalises relevant chunks buried at the bottom. Low CP suggests the retriever is returning a lot of noise before the useful material. *Example: if the single chunk that contains the answer is ranked 9th out of 10, CP will be low even though the answer was technically reachable — a better embedding or smaller chunk size would surface it earlier.*
> 
> Collections sorted by F mean (descending). `n/a` = eval disabled or scoring failed.

| Collection | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | **F Mean** | **AR Mean** | **CP Mean** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chunk_size_1000_chunk_overlap_100` | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.9000** | **0.7209** | **0.6169** |
| `chunk_size_2000_chunk_overlap_300` | 1.0000 | n/a | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8889** | **n/a** | **n/a** |
| `chunk_size_1000_chunk_overlap_300` | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8125 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8812** | **0.7249** | **0.6605** |
| `chunk_size_1000_chunk_overlap_50` | 1.0000 | n/a | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.8750** | **n/a** | **n/a** |
| `chunk_size_2000_chunk_overlap_300` | 1.0000 | n/a | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.8750** | **0.6683** | **0.6846** |
| `chunk_size_1000_chunk_overlap_300` | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.7000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8700** | **n/a** | **n/a** |
| `chunk_size_3000_chunk_overlap_50` | 1.0000 | n/a | 1.0000 | 1.0000 | 0.7273 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8586** | **0.6446** | **0.7005** |
| `chunk_size_1000_chunk_overlap_100` | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.8519** | **n/a** | **n/a** |
| `chunk_size_3000_chunk_overlap_100` | 1.0000 | n/a | 1.0000 | 1.0000 | 0.7500 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.8438** | **n/a** | **n/a** |
| `chunk_size_1000_chunk_overlap_200` | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8333** | **n/a** | **n/a** |
| `chunk_size_2000_chunk_overlap_200` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8000** | **n/a** | **n/a** |
| `chunk_size_2000_chunk_overlap_100` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8000** | **0.6650** | **0.5658** |
| `chunk_size_2000_chunk_overlap_200` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.8000** | **0.6543** | **0.6011** |
| `chunk_size_3000_chunk_overlap_50` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7800** | **n/a** | **n/a** |
| `chunk_size_1000_chunk_overlap_50` | 1.0000 | 0.0000 | 1.0000 | 0.7500 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7750** | **0.6666** | **0.5343** |
| `chunk_size_1000_chunk_overlap_200` | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7576** | **0.7131** | **0.6270** |
| `chunk_size_2000_chunk_overlap_100` | 1.0000 | 0.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.7556** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_300` | 0.8750 | 0.7500 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7458** | **n/a** | **n/a** |
| `chunk_size_2000_chunk_overlap_50` | 1.0000 | n/a | 0.8333 | 1.0000 | 0.8000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | n/a | **0.7370** | **0.6221** | **0.5342** |
| `chunk_size_3000_chunk_overlap_200` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7000** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_50` | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7000** | **0.5893** | **0.5464** |
| `chunk_size_500_chunk_overlap_100` | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.7000** | **0.5668** | **0.5196** |
| `chunk_size_3000_chunk_overlap_100` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7000** | **0.5776** | **0.6063** |
| `chunk_size_3000_chunk_overlap_200` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | 1.0000 | **0.7000** | **0.5776** | **0.5793** |
| `chunk_size_3000_chunk_overlap_300` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9091 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.6909** | **0.5683** | **0.6240** |
| `chunk_size_500_chunk_overlap_100` | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 0.8667 | **0.6867** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_300` | 0.9000 | 0.6667 | 1.0000 | 1.0000 | 0.8000 | 0.5000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.6867** | **0.6436** | **0.6005** |
| `chunk_size_3000_chunk_overlap_300` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.7500 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.6750** | **n/a** | **n/a** |
| `chunk_size_2000_chunk_overlap_50` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 1.0000 | 1.0000 | n/a | **0.6667** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_50` | 0.6667 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | n/a | **0.6296** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_200` | 0.8750 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.5875** | **n/a** | **n/a** |
| `chunk_size_500_chunk_overlap_200` | 0.8571 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.0000 | n/a | 0.0000 | 0.0000 | 1.0000 | 1.0000 | **0.5857** | **0.5085** | **0.3811** |

---

## Question 1: What changes to model disclosure were proposed in the stress test transparency rule?

### 1. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes that it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation with respect to the stress test models and scenarios.
4. The disclosure process would create a new mechanism for obtaining feedback from the public, including academics, financial analysts, and firms, on the design and specifications of the models.
5. The Board would publish model changes by May 15 of the year in which the stress test is performed if those changes are not deemed material.

These changes aim to enhance transparency, public accountability, and the overall credibility of the stress tests.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. An enhanced disclosure process that would require the Board to annually disclose the model documentation and scenarios.
2. The Board would invite public comment on the scenarios and any material changes to the models before such changes are implemented in the supervisory stress test.
3. The jump-off date for the stress test would be shifted from December 31 to September 30 to accommodate the public comment process.
4. The Board would publish comprehensive documentation on the stress test models, including equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
5. The proposal would also solicit public comment on revisions to the Stress Testing Policy Statement and alternative thresholds for model changes.
6. The Board would disclose and invite public input on any material model changes before implementing them in the stress test.

### 3. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. An enhanced disclosure process that would require the Board to annually disclose the model documentation and scenarios.
2. The Board would invite public comment on the scenarios and any material changes to the models before such changes are implemented in the supervisory stress test.
3. The jump-off date for the stress test would be shifted from December 31 to September 30 to accommodate the public comment process.
4. The Board would publicly disclose the models used for the stress test by May 15 of the calendar year in which the stress test was performed.
5. The Board would disclose and invite public input on any material model changes before implementing them in the stress test.
6. Comprehensive documentation of the stress test models would include equations, variables, coefficients, assumptions, limitations, and discussions of alternative models, which would be published on the Board's website. 

These changes aim to increase transparency, public accountability, and facilitate public participation regarding the stress test models and scenarios.

### 4. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual disclosure of the models used for the stress test by May 15 of the calendar year in which the stress test was performed.
2. Disclosure and invitation for public input on any material model changes before implementing them in the stress test.
3. Comprehensive documentation of the stress test models, including coefficients, assumptions, limitations, and rationale for modeling decisions, to be published for public comment.
4. A commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
5. Shifting the jump-off date of the stress test from December 31 to September 30 to accommodate public comment on the scenarios and any material changes to the models before implementation.

### 5. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual disclosure of the models used for the stress test by May 15 of the calendar year in which the stress test was conducted.
2. Disclosure and invitation for public input on any material model changes before implementing them in the stress test.
3. Comprehensive documentation of the stress test models, including equations, variables, coefficients, assumptions, limitations, rationale for modeling decisions, and discussions of alternative models, to be published for public comment.
4. A commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
5. The proposal to revise the Stress Testing Policy Statement to facilitate disclosing additional information directly to firms about their own stress test results. 

These changes aim to enhance transparency, public accountability, and public feedback on the stress test models and scenarios.

### 6. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. A commitment to respond to substantive public comments on any material model changes prior to their implementation.
5. A shift in the jump-off date for the stress test from December 31 to September 30 to accommodate the public comment process. 

These changes aim to enhance transparency and public accountability regarding the supervisory stress test framework.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. A commitment to respond to substantive public comments on any material model changes prior to implementation.
5. Revision of the Stress Testing Policy Statement to align with the enhanced disclosure process.
6. Shifting the jump-off date of the supervisory stress tests from December 31 to September 30 to accommodate the public comment process.

### 8. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. A commitment to respond to substantive public comments on any material model changes prior to their implementation.
5. A shift in the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process. 

These changes aim to enhance transparency and public accountability regarding the supervisory stress test framework.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. A commitment to invite public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. A shift in the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process.
4. An invitation for public comment on proposed amendments to the Board’s Stress Testing Policy Statement and the Scenario Design Policy Statement, including guides for additional domestic scenario variables.

These changes aim to enhance transparency and public accountability regarding the models used in the supervisory stress tests.

### 10. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before they are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process in the Board’s regulations, committing to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that the Board will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to other participating firms.

6. **Increased Predictability and Transparency**: The revised Scenario Design Policy Statement would include additional guides for certain macroeconomic variables and a more transparent process for determining the paths of scenario variables.

These changes aim to improve the transparency and public accountability of the supervisory stress test framework.

### 11. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before they are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process in the Board’s regulations, committing to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that the Board will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to all participating firms.

6. **Increased Predictability and Transparency**: The revised Scenario Design Policy Statement would include additional guides for certain macroeconomic variables and a more transparent process for determining the paths of scenario variables.

These changes aim to improve the transparency and public accountability of the supervisory stress test framework.

### 12. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before such changes are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process in the Board’s regulations, committing to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that non-public information about a firm's results would generally be shared directly with that firm, provided similar information is disclosed to other participating firms.

These changes aim to improve transparency, public accountability, and the overall credibility of the supervisory stress tests.

### 13. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before they are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process that requires the Board to maintain transparency and facilitate public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that the Board will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to all participating firms.

6. **Increased Predictability and Transparency**: The revised Scenario Design Policy Statement would include additional guides for scenario variables and a description of the annual process for seeking feedback on the supervisory stress test scenarios prior to their finalization.

These changes aim to improve transparency, public accountability, and the overall credibility of the stress testing framework.

### 14. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9625 | CP: 0.8783

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models.
2. Invitation for public comment on any material changes that the Board seeks to make to those models.
3. A commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
4. The Board would publish model changes by May 15 of the year in which the stress test is performed if those changes are not deemed material.
5. The proposal aims to codify an enhanced disclosure process in the Board’s regulations to improve public accountability and transparency.

### 15. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9625 | CP: 0.7657

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
4. The disclosure process would create a new mechanism for obtaining feedback from the public, including academics, financial analysts, and firms, on the design and specifications of the models.
5. The Board would publish model changes that are not considered material by May 15 of the year in which the stress test is performed, without formally inviting public comment on these non-material changes.

### 16. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. An enhanced disclosure process that would require the Board to annually disclose the model documentation and scenarios.
2. The Board would invite public comment on the scenarios and any material changes to the models before such changes are implemented in the supervisory stress test.
3. The jump-off date for the stress test would be shifted from December 31 to September 30 to accommodate the public comment process.
4. The Board would publish comprehensive documentation on the stress test models, including equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
5. The proposal would also solicit public comment on revisions to the Stress Testing Policy Statement in accordance with the enhanced disclosure process.
6. The Board would disclose and invite public input on any material model changes before implementing them in the stress test.

### 17. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. An enhanced disclosure process that would require the Board to annually disclose the model documentation and scenarios.
2. The invitation for public comment on the scenarios and any material changes to the models before such changes are implemented in the supervisory stress test.
3. The shift of the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process.
4. The annual publication of comprehensive documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and discussions of alternative models.
5. The identification of any non-material changes made to the models as part of the annual publication.
6. The solicitation of public comment on revisions to the Stress Testing Policy Statement in accordance with the proposed enhanced disclosure process.

### 18. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual disclosure of the models used for the stress test by May 15 of the calendar year in which the stress test was performed.
2. Disclosure and invitation for public input on any material model changes before implementing them in the stress test.
3. A commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
4. The requirement for the Board to annually disclose model documentation and scenarios and invite public comment on these scenarios and any material changes to the models before such changes are implemented.
5. The proposal to revise the Stress Testing Policy Statement to facilitate disclosing additional information directly to firms about their own stress test results. 

These changes aim to enhance transparency, public accountability, and public participation in the stress testing process.

### 19. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual disclosure of the models used to conduct the stress test by May 15 of the calendar year in which the stress test is performed.
2. Disclosure and invitation for public input on any material model changes before implementing them in the stress test.
3. Comprehensive documentation of the stress test models, including equations, variables, coefficients, assumptions, limitations, rationale for modeling decisions, and discussions of alternative models, to be published for public comment.
4. A commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
5. The proposal to revise the Stress Testing Policy Statement to facilitate disclosing additional information directly to firms about their own stress test results. 

These changes aim to enhance transparency, public accountability, and public feedback on the stress test models and scenarios.

### 20. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9625 | CP: 0.9060

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. A commitment to respond to substantive public comments on any material model changes prior to their implementation.
5. A shift in the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process. 

These changes aim to enhance transparency and public accountability regarding the stress test models and scenarios.

### 21. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9625 | CP: 0.9060

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. A commitment to respond to substantive public comments on any material model changes prior to their implementation.
5. A proposed shift of the jump-off date for the stress test from December 31 to September 30 to accommodate the public comment process. 

These changes aim to enhance transparency and public accountability regarding the stress testing framework.

### 22. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9625 | CP: 0.9060

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. Invitation for public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. Annual publication of the stress test scenarios for public comment.
4. Revision of the Stress Testing Policy Statement to align with the enhanced disclosure process.
5. Shifting the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process on the scenarios. 

These changes aim to enhance transparency and public accountability regarding the models used in the supervisory stress tests.

### 23. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9625 | CP: 0.9060

The proposed changes to model disclosure in the stress test transparency rule include:

1. Annual publication of comprehensive model documentation, which would include equations, variables, coefficients, assumptions, limitations, and rationale for modeling decisions.
2. A commitment to invite public comment on any material changes to the models before they are implemented in the supervisory stress test.
3. A shift in the jump-off date of the stress test from December 31 to September 30 to accommodate the public comment process.
4. An invitation for public comment on proposed amendments to the Board’s Stress Testing Policy Statement and the Scenario Design Policy Statement, including guides for additional domestic scenario variables.

These changes aim to enhance transparency and public accountability regarding the models used in the supervisory stress tests.

### 24. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before they are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process in the Board’s regulations, committing to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that the Board will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to other participating firms.

6. **Increased Predictability and Transparency**: The revised Scenario Design Policy Statement would include additional guides for certain macroeconomic variables and a description of the annual process for seeking feedback on the supervisory stress test scenarios prior to their finalization.

These changes aim to improve transparency, public accountability, and the overall credibility of the stress testing framework.

### 25. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before such changes are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process in the Board’s regulations, committing to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including provisions for sharing non-public information about a firm's results directly with that firm, provided similar information is disclosed to all participating firms.

6. **Additional Guides for Scenario Variables**: The proposal includes providing additional guides for seven domestic scenario variables and a detailed description of the approaches for producing the scenario variable paths.

These changes aim to improve transparency, public accountability, and the overall credibility of the stress testing framework.

### 26. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before such changes are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process that facilitates public participation and transparency regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Direct Disclosure to Firms**: The Board would clarify that it will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to other participating firms.

These changes aim to improve transparency, public accountability, and the overall credibility of the supervisory stress tests.

### 27. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9625 | CP: 1.0000

The proposed changes to model disclosure in the stress test transparency rule include:

1. **Annual Publication of Comprehensive Model Documentation**: The Board would annually publish detailed documentation on the stress test models, which would include equations, variables, coefficients, assumptions, limitations, rationales for modeling decisions, and discussions of alternative models.

2. **Public Comment on Material Changes**: The Board would invite public comment on any material changes to the models before such changes are implemented in the supervisory stress test.

3. **Enhanced Disclosure Process**: The proposal would codify an enhanced disclosure process that requires the Board to maintain transparency and facilitate public participation regarding the stress test models and scenarios.

4. **Shift in Jump-Off Date**: To accommodate the public comment process on the stress test scenarios, the jump-off date for the stress test would be shifted from December 31 to September 30.

5. **Revisions to the Stress Testing Policy Statement**: The Board would propose amendments to the Stress Testing Policy Statement to align it with the enhanced disclosure process, including clarifying that the Board will generally share non-public information about a firm's results directly with that firm, provided similar information is disclosed to all participating firms.

6. **Increased Predictability and Transparency**: The revised Scenario Design Policy Statement would include additional guides for scenario variables and a more transparent process for scenario design, allowing for public feedback prior to finalization.

These changes aim to improve transparency, public accountability, and the overall credibility of the stress testing framework.

### 28. `chunk_size_500_chunk_overlap_300` — F: 0.9000 | AR: 0.9625 | CP: 0.8835

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation with respect to the stress test models and scenarios.
4. The disclosure process would create a new mechanism for obtaining feedback from the public, including academics, financial analysts, and firms, on the design and specifications of the stress test models.
5. The Board would also disclose additional information directly to firms about their own stress test results.

These changes aim to enhance transparency and public accountability, instill confidence in the fairness of the supervisory stress tests, and improve the credibility of the stress test process.

### 29. `chunk_size_500_chunk_overlap_200` — F: 0.8750 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes that it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
4. The Board would publish model changes by May 15 of the year in which the stress test is performed if those changes are not deemed material.
5. The proposal aims to codify an enhanced disclosure process in the Board’s regulations to increase public accountability and instill confidence in the fairness of the supervisory stress tests.

### 30. `chunk_size_500_chunk_overlap_300` — F: 0.8750 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes that it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation with respect to the stress test models and scenarios.
4. The disclosure process would create a new mechanism for obtaining feedback from the public, including academics, financial analysts, and firms, on the design and specifications of the stress test models.

These changes aim to enhance transparency and public accountability, instilling confidence in the fairness of the supervisory stress tests.

### 31. `chunk_size_500_chunk_overlap_200` — F: 0.8571 | AR: 0.9625 | CP: 0.8553

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes that it seeks to make to those models.
3. The Board would commit to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
4. The Board would publish model changes by May 15 of the year in which the stress test is performed if those changes are not considered material.
5. The proposal aims to enhance the disclosure process by codifying it in the Board’s regulations, building on previous efforts to increase transparency and public accountability.

### 32. `chunk_size_500_chunk_overlap_50` — F: 0.6667 | AR: n/a | CP: n/a

The proposed changes to model disclosure in the stress test transparency rule include the following:

1. The Board would annually publish comprehensive model documentation on the stress test models.
2. The Board would invite public comment on any material changes that it seeks to make to those models.
3. The Board would publish the stress test results annually.
4. The proposed enhanced disclosure process would codify a commitment to maintaining transparency and facilitating public participation regarding the stress test models and scenarios.
5. The Board would seek public comment on revisions to the Stress Testing Policy Statement in accordance with the proposed enhanced disclosure process.

Additionally, if changes to the models are not material, the Board would publish these model changes by May 15 of the year in which the stress test is performed, without formally inviting public comment on these non-material changes.

---

## Question 2: How did stress testing start, and how has it evolved?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing in the U.S. began with the Federal Reserve’s supervisory stress testing in 2009. Historically, individual banks measured and managed risk using their own internal stress tests, but the introduction of supervisory stress testing marked a significant evolution in the approach to assessing potential vulnerabilities and ensuring that banks have sufficient capital to withstand severe economic shocks.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing in the U.S. began with the Federal Reserve’s supervisory stress testing in 2009. Historically, individual banks have measured and managed risk using their own internal stress tests, but the supervisory approach was introduced to help identify potential vulnerabilities and ensure that banks have sufficient capital to withstand severe economic shocks.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This program evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011. Historically, individual banks have measured and managed risk using their own internal stress tests.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing began as a response to the reforms following the Global Financial Crisis and has been an important element of the Federal Reserve Board's regulatory framework and supervisory program since 2009. Over the years, there has been a commitment to improving the transparency of stress tests and reducing the volatility of the resulting capital buffer requirements. This evolution reflects a continuous effort to enhance the understanding of how to maintain the financial system's strength and ensure that large supervised institutions have sufficient capital to absorb losses and continue lending during economic downturns.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing began as a response to the Global Financial Crisis, with its implementation starting in 2009 as part of the regulatory framework and supervisory program of the Federal Reserve Board. Over the years, it has evolved to enhance transparency and public accountability, with ongoing modifications to the capital planning and stress capital buffer requirements. The process has been refined to ensure that large supervised institutions maintain sufficient capital to absorb losses and continue lending, even during economic downturns.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

Stress testing began as a response to the reforms following the Global Financial Crisis, becoming an important element of the Federal Reserve Board's regulatory framework and supervisory program since 2009. Over the years, there has been a commitment to improving the transparency of stress tests and reducing the volatility of the resulting capital buffer requirements. This evolution reflects a continuous effort to enhance the understanding of how to maintain the strength of the financial system by ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending, even during economic downturns.

### 7. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8194 | CP: 0.5000

Stress testing in the U.S. began with the Federal Reserve’s supervisory stress testing in 2009. Historically, individual banks measured and managed risk using their own internal stress tests, but the introduction of supervisory stress testing marked a significant evolution in the approach to assessing potential vulnerabilities and ensuring that banks have sufficient capital to withstand severe economic shocks.

### 8. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8194 | CP: 0.5000

Stress testing in the U.S. began with the Federal Reserve’s supervisory stress testing in 2009. Historically, individual banks measured and managed risk using their own internal stress tests, but the introduction of supervisory stress testing marked a significant evolution in the approach to assessing potential vulnerabilities and ensuring that banks have sufficient capital to withstand severe economic shocks.

### 9. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.8194 | CP: 0.6000

Stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This program evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011. Historically, individual banks have measured and managed risk using their own internal stress tests. Stress testing has become an important risk management tool for banks and supervisors, helping to identify potential vulnerabilities and ensuring that banks have sufficient capital to withstand severe economic shocks.

### 10. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.6365 | CP: 0.1111

Stress testing began as a response to the reforms following the Global Financial Crisis and has been an important element of the Federal Reserve Board's regulatory framework and supervisory program since 2009. Over the years, there has been a commitment to improving the transparency of stress tests and reducing the volatility of the resulting capital buffer requirements. This evolution reflects a continuous effort to enhance the understanding of how to maintain the strength of the financial system by ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during economic downturns.

### 11. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.6511 | CP: 0.1667

Stress testing started as a response to the Global Financial Crisis and has been an important element of the Board's regulatory framework and supervisory program since 2009. It was designed to ensure that large supervised institutions have sufficient capital to absorb losses and continue lending even during economic downturns. Over time, there has been a commitment to improving the transparency of stress tests and reducing the volatility of resulting capital buffer requirements, indicating an evolution towards greater accountability and clarity in the stress testing process.

### 12. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.6366 | CP: 0.2000

Stress testing began as a response to the reforms following the Global Financial Crisis, becoming an important element of the Federal Reserve Board's regulatory framework and supervisory program since 2009. Over time, there has been a commitment to improving the transparency of stress tests and reducing the volatility of the resulting capital buffer requirements. This evolution reflects a continuous effort to enhance the understanding of how to maintain the strength of the financial system by ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending, even during economic downturns.

### 13. `chunk_size_500_chunk_overlap_300` — F: 0.7500 | AR: n/a | CP: n/a

Stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This program evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011. Historically, individual banks have gauged risk using their own internal stress tests, but supervisory stress testing has become a standardized practice to measure and manage risk across the banking sector.

### 14. `chunk_size_500_chunk_overlap_300` — F: 0.6667 | AR: 0.8193 | CP: 0.7556

Stress testing in the U.S. began with the Federal Reserve’s 2009 Supervisory Capital Assessment Program during the Global Financial Crisis. This program evolved into the annual Comprehensive Capital Analysis and Review (CCAR) program in 2011. Historically, individual banks have gauged risk using their own internal stress tests, but supervisory stress testing has become a standardized practice to measure and manage risk across the banking sector.

### 15. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 16. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 17. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 18. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 19. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 20. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 21. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 22. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 23. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 24. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 25. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 26. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 27. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 28. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 29. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 30. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 3: How does the Projections Calculator handle missing values in regulatory reports?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. It also converts data obtained from the FR Y-9C and FFIEC 101, which is originally reported in thousands of U.S. dollars, into millions of U.S. dollars. Additionally, the Projections Calculator renames and aggregates regulatory reporting items for use in other supervisory stress testing models.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 14. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 15. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 16. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 17. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 18. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 19. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 20. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 21. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 22. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 23. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 24. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 0.3333

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. It also converts data obtained from the FR Y-9C and FFIEC 101, which is originally reported in thousands of U.S. dollars, into millions of U.S. dollars. Additionally, the instructions for the FR Y-9C, FFIEC 101, and FR Y-14Q regulatory reports require firms to report certain items as blank if they do not apply for a given firm.

### 25. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 0.2500

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 26. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 0.7500

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 27. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 28. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 29. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 30. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9601 | CP: 1.0000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed.

### 31. `chunk_size_2000_chunk_overlap_50` — F: 0.8333 | AR: 0.5822 | CP: 0.2000

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. It also converts data obtained from the FR Y-9C and FFIEC 101, which is originally reported in thousands of U.S. dollars, into millions of U.S. dollars. Additionally, the Projections Calculator renames and aggregates regulatory reporting items for use in other supervisory stress testing models.

### 32. `chunk_size_2000_chunk_overlap_100` — F: 0.8000 | AR: n/a | CP: n/a

The Projections Calculator replaces missing values in any of the regulatory reports with zeroes, as needed. It also converts data obtained from the FR Y-9C and FFIEC 101, which is originally reported in thousands of U.S. dollars, into millions of U.S. dollars. Additionally, if certain items do not apply for a given firm, the instructions for the FR Y-9C, FFIEC 101, and FR Y-14Q regulatory reports require firms to report these items as blank.

---

## Question 4: In the first lien model, how are 2008 and after vintages are combined

### 1. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

2008 and after vintages are combined if any of the following criteria are met:
- FRMs with original credit score less than 680, or ARMs with original credit score less than 720
- FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent
- All loans greater than 30 days past due or in foreclosure.

### 2. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are categorized based on their characteristics, such as property state, loan status, and origination year. Specifically, the vintages are grouped to avoid categories becoming too sparse, with 2005 and earlier vintages combined, and for Option ARMs, 2007 and after vintages are combined.

### 3. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are categorized based on their characteristics, such as property state, loan status, and origination year. Specifically, for Option ARMs, vintages from 2007 and after are combined, and for other loans, the 2008 and after vintages are grouped to avoid categories becoming too sparse.

### 4. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 5. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 
1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 6. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 7. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 8. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 9. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 10. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 11. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 12. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.7217 | CP: 0.4021

2008 and after vintages are combined if any of the following criteria are met:
- FRMs with original credit score less than 680, or ARMs with original credit score less than 720
- FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent
- All loans greater than 30 days past due or in foreclosure

Otherwise, the origination year is applied directly.

### 13. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8608 | CP: 0.5000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are categorized based on their characteristics, such as property state, loan status, and origination year. Specifically, for Option ARMs, vintages from 2007 and after are combined. This approach is taken to avoid categories becoming too sparse.

### 14. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8608 | CP: 0.5000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are categorized based on their delinquency status, property state, and other characteristics to avoid categories becoming too sparse.

### 15. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8907 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met:
- FRMs with original credit score less than 680, or ARMs with original credit score less than 720
- FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent
- All loans greater than 30 days past due or in foreclosure.

### 16. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8907 | CP: 0.5444

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs (Fixed Rate Mortgages) with original credit score less than 680, or ARMs (Adjustable Rate Mortgages) with original credit score less than 720.
2. FRMs with original LTV (Loan-to-Value) above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 17. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8907 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 18. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8907 | CP: 0.9167

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

### 19. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8907 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 
1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure. 

This approach is taken to avoid categories becoming too sparse.

### 20. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8879 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 21. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8879 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure.

This approach is taken to avoid categories becoming too sparse.

### 22. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.8879 | CP: 1.0000

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: 

1. FRMs with original credit score less than 680, or ARMs with original credit score less than 720.
2. FRMs with original LTV above 90 percent, or ARMs with original LTV above 80 percent.
3. All loans greater than 30 days past due or in foreclosure. 

This approach is taken to avoid categories becoming too sparse.

### 23. `chunk_size_1000_chunk_overlap_50` — F: 0.7500 | AR: 0.8530 | CP: 0.4762

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are categorized based on their characteristics, such as property state, loan status, and vintage. Specifically, for Option ARMs, vintages from 2007 and after are combined.

### 24. `chunk_size_1000_chunk_overlap_100` — F: 0.6667 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are of a certain status or characteristic that aligns with the model's requirements. However, the specific criteria for combining these vintages are not detailed in the provided context.

### 25. `chunk_size_1000_chunk_overlap_200` — F: 0.3333 | AR: n/a | CP: n/a

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are Option ARMs, or to avoid categories becoming too sparse.

### 26. `chunk_size_1000_chunk_overlap_200` — F: 0.3333 | AR: 0.8907 | CP: 0.3333

In the first lien model, 2008 and after vintages are combined if any of the following criteria are met: the loans are Option ARMs, or the categories become too sparse.

### 27. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 28. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 29. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 30. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 5: Tell me about how quickly first lien model can transition current loans to default

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The first lien mortgage model assumes that current loans, defined as less than 90 days past due, cannot directly transition to default, which is defined as greater than 180 days past due. The model requires two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, about 0.01 percent of observations, loans may transition directly from current to default, but this is not the norm.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model assumes that current loans cannot directly transition to default. According to the model's definitions, current loans are classified as being less than 90 days past due, while defaulted loans are those greater than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, loans may transition directly from current to default, but this occurs in about 0.01 percent of observations in the estimation data.

### 3. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model assumes that current loans cannot directly transition to default. Instead, it requires two quarters for a loan to transition from current to delinquent and then to default. This is based on the model's definitions, where current loans are defined as being less than 90 days past due, and defaulted loans are those that are greater than 180 days past due. In extremely rare circumstances, about 0.01 percent of observations in the data, loans may transition directly from current to default, but the model does not account for this rare transition as it found that projected loss rates remained unchanged.

### 4. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Current loans cannot directly transition to default according to the model's definitions. A loan is considered current if it is less than 90 days past due, while a loan is classified as defaulted if it is more than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In very rare cases, about 0.01 percent of observations, loans may transition directly from current to default, but this is not modeled due to its infrequency and the principle of simplicity in the stress testing policy.

### 5. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Current loans cannot directly transition to default in the first lien model. The model defines current loans as those that are less than 90 days past due, while defaulted loans are defined as being greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, loans may transition directly from current to default, but these cases are not modeled due to their infrequency.

### 6. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model assumes that current loans cannot directly transition to default. According to the model's definitions, current loans are classified as being less than 90 days past due, while defaulted loans are those that are more than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In rare circumstances, loans may transition directly from current to default, but such instances are removed from the estimation sample and ignored.

### 7. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Mortgage Model assumes that two quarters are needed for a loan to transition from current to delinquent to default. In extremely rare circumstances, loans can transition directly from current to default, but this accounts for approximately 0.01 percent of observations in the data used to calibrate the model. The model does not specifically model this rare transition, as testing showed that projected loss rates remained unchanged when allowing for direct transitions from current to default.

### 8. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model assumes that two quarters are needed for a loan to transition from current to delinquent to default. Specifically, loans are defined as current if they are less than 90 days past due, and they are considered defaulted if they are greater than 180 days past due. In extremely rare circumstances, loans may transition directly from current to default, but this is not modeled due to its rarity and the principle of simplicity in the stress testing policy.

### 9. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

Current loans cannot directly transition to default in the First Lien PD Model. The model defines current loans as those that are less than 90 days past due, while defaulted loans are defined as those that are greater than 180 days past due. Therefore, the model assumes that two quarters (approximately six months) are needed for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, loans may transition directly from current to default, but this occurs in about 0.01 percent of observations and is not modeled due to the principle of simplicity. The Board tested this direct transition and found that projected loss rates remained unchanged.

### 10. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another, including from current to default. A borrower must first fall into delinquency before they can transition to default. Specifically, loans are defined as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan reaches 180 days past due, it is considered in default. The model captures the flows between these payment statuses during the projection period, making it particularly well-suited for stress testing, especially when a significant share of loans are delinquent at the start of the projection horizon.

### 11. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.8410 | CP: 0.9526

The first lien mortgage model assumes that current loans, defined as less than 90 days past due, cannot directly transition to default, which is defined as greater than 180 days past due. The model requires two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, approximately 0.01 percent of observations, loans may transition directly from current to default, but this is not the norm.

### 12. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.8512 | CP: 0.5689

The first lien model assumes that current loans cannot directly transition to default. According to the model's definitions, current loans are classified as being less than 90 days past due, while defaulted loans are those greater than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, about 0.01 percent of observations, loans may transition directly from current to default, but this is not the norm.

### 13. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8498 | CP: 0.8644

The First Lien Model assumes that current loans cannot directly transition to default. Instead, it requires two quarters for a loan to transition from current to delinquent and then to default. This is based on the definitions used in the model, where current loans are defined as being less than 90 days past due, and defaulted loans are those that are greater than 180 days past due. In extremely rare circumstances, about 0.01 percent of observations, loans may transition directly from current to default, but the model does not account for this rare transition as it was found to have no significant impact on projected loss rates.

### 14. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8031 | CP: 1.0000

Current loans cannot directly transition to default in the First Lien PD Model. This is due to the model's definition of current loans as being less than 90 days past due, while defaulted loans are defined as being greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In very rare cases, approximately 0.01 percent of observations, loans may transition directly from current to default, but this is not modeled due to the principle of simplicity and because it was found that allowing such transitions did not change projected loss rates.

### 15. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.7763 | CP: 1.0000

Current loans cannot directly transition to default in the first lien model. The model defines current loans as those that are less than 90 days past due, while defaulted loans are defined as those that are greater than 180 days past due. Therefore, the model assumes that it takes two quarters for a loan to transition from current to delinquent and then to default. In extremely rare circumstances, loans may transition directly from current to default, but these cases are not modeled due to their infrequency.

### 16. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8475 | CP: 0.9627

The First Lien Model assumes that current loans cannot directly transition to default. Instead, it defines current loans as those that are less than 90 days past due, while defaulted loans are those that are greater than 180 days past due. Therefore, the model assumes that it takes two quarters (approximately six months) for a loan to transition from current to delinquent and then to default. In rare circumstances, loans may transition directly from current to default, but such observations are removed from the estimation sample and ignored.

### 17. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.7668 | CP: 1.0000

The First Lien Mortgage Model assumes that two quarters are needed for a loan to transition from current to delinquent to default. In extremely rare circumstances, loans can transition directly from current to default, but this occurs in approximately 0.01 percent of observations in the data used to calibrate the model. However, the model does not account for this rare transition, as testing showed that projected loss rates remained unchanged. Therefore, the model primarily follows the two-quarter transition from current to delinquent before reaching default.

### 18. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8313 | CP: 1.0000

The First Lien Model assumes that two quarters are needed for a loan to transition from current to delinquent to default. Specifically, loans are defined as current if they are less than 90 days past due, and they are considered defaulted if they are greater than 180 days past due. In extremely rare circumstances, loans can transition directly from current to default, but this is not modeled due to its rarity, as it covers approximately 0.01 percent of observations in the data used to calibrate the model coefficients. The model does not account for this direct transition, as testing showed that projected loss rates remained unchanged when this transition was excluded.

### 19. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8031 | CP: 1.0000

Current loans cannot directly transition to default in the First Lien PD Model. This is due to the model's definition of current loans as being less than 90 days past due, while defaulted loans are defined as being greater than 180 days past due. Therefore, the model assumes that two quarters (approximately six months) are needed for a loan to transition from current to delinquent and then to default. In extremely rare cases, loans may transition directly from current to default, but this occurs in about 0.01 percent of observations and is not modeled due to the principle of simplicity.

### 20. `chunk_size_3000_chunk_overlap_300` — F: 0.9091 | AR: 0.7336 | CP: 1.0000

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another, including from current to default. A borrower must first fall into delinquency before they can transition to default. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan reaches 180 days past due, it is considered in default. Therefore, the transition from current to default can occur relatively quickly, but it requires the loan to first become delinquent. The model captures the flows between these statuses during the projection period, making it particularly suited for stress testing, especially when a significant share of loans are delinquent at the start of the projection horizon.

### 21. `chunk_size_500_chunk_overlap_300` — F: 0.8333 | AR: n/a | CP: n/a

The first lien mortgage model defines current loans as those that are less than 90 days past due and defaulted loans as those greater than 180 days past due. According to the model, it assumes that two quarters are needed for a loan to transition from current to delinquent and then to default. Therefore, current loans cannot directly transition to default. In extremely rare circumstances, covering approximately 0.01 percent of observations in the data used to calibrate the model coefficients, loans may transition directly from current to default.

### 22. `chunk_size_3000_chunk_overlap_50` — F: 0.8000 | AR: n/a | CP: n/a

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning between different payment statuses, including from current to default. A borrower must first fall into delinquency before they can transition to default. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan reaches 180 days past due, it is considered in default. Therefore, the transition from current to default can occur relatively quickly, as it requires the loan to first become delinquent for a period before reaching the default status. The model captures these transitions based on the prior status of the loan and various loan and macroeconomic characteristics.

### 23. `chunk_size_500_chunk_overlap_300` — F: 0.8000 | AR: 0.7475 | CP: 0.8389

The first lien mortgage model defines current loans as those that are less than 90 days past due and defaulted loans as those greater than 180 days past due. Due to these definitions, the model assumes that two quarters are needed for a loan to transition from current to delinquent and then to default. Therefore, current loans cannot directly transition to default.

### 24. `chunk_size_2000_chunk_overlap_50` — F: 0.8000 | AR: 0.7322 | CP: 1.0000

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning to different payment statuses, including default. To reach default, a borrower must first fall into delinquency. The model indicates that once a loan is marked as default, it is considered to have reached terminal status, meaning it cannot transition back to a current status. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Additionally, loans that have triggered default conditions (e.g., are 180 or more days past due) are not run through the PD model, as they have already reached default status. Therefore, the transition from current to default can occur relatively quickly, depending on the borrower's payment behavior and the specific circumstances leading to delinquency.

### 25. `chunk_size_3000_chunk_overlap_100` — F: 0.7500 | AR: n/a | CP: n/a

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning between various payment statuses, including from current to default. A borrower must first fall into delinquency before potentially transitioning to default. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan reaches 180 days past due, it is classified as in default. Therefore, the transition from current to default can occur relatively quickly, as it requires the loan to first become delinquent for a period before reaching the default status at 180 days past due.

### 26. `chunk_size_3000_chunk_overlap_300` — F: 0.7500 | AR: n/a | CP: n/a

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another, including from current to default. To reach default, a borrower must first fall into delinquency. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan is marked as default, it is treated as a terminal status, meaning it cannot transition back to a different status. The model does not allow for cures from default, as this is rare and would complicate the model. Therefore, the transition from current to default can occur relatively quickly, depending on the borrower's payment behavior and the macroeconomic environment, but it is contingent upon the borrower first becoming delinquent.

### 27. `chunk_size_3000_chunk_overlap_50` — F: 0.7273 | AR: 0.7336 | CP: 1.0000

The First Lien PD Model uses a loan-level, state transition model approach to project the probability of a loan transitioning from one payment status to another, including from current to default. A borrower must first fall into delinquency before they can transition to default. The model defines loans as delinquent if they are 90-179 days past due or in foreclosure proceedings. Once a loan reaches 180 days past due, it is considered in default. Therefore, the transition from current to default can occur relatively quickly, depending on the borrower's payment behavior and the time it takes for them to become delinquent. The model captures these transitions and the associated probabilities based on historical data and macroeconomic conditions.

### 28. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 29. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 30. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 6: What studies and academic literature does the first lien model draw on?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on studies and academic literature including works by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng and Gabriel (2021). It also incorporates findings from the literature on mortgage modeling, particularly regarding default risk on FHA-insured home mortgages.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on a large body of literature that provides useful context for developing an accurate, robust model of first lien probability of default (PD). It is informed by a review of relevant literature and industry best practices, as well as statistical fit and the Board’s experience and expertise. Additionally, the model documentation mentions that most research on residential real estate focuses on first lien mortgages rather than home equity exposures, given that first lien mortgages are a much larger market and are associated with more widely available data.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on studies and academic literature including Gupton, Finger, & Bhatia's CreditMetrics (1997), KMV’s PortfolioManager, and the actuarial approach employed by Credit Suisse First Boston’s CreditRisk+. Detailed comparisons of these approaches are provided in works by Crouhy, Galai, & Mark (2000); Gordy (2000); and Allen & Saunders (2003).

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on various studies and academic literature, including the work of von Furstenberg, G. (1969) on default risk related to FHA-insured home mortgages, and subsequent studies such as those by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng and Gabriel (2021). Additionally, it incorporates findings that indicate the borrower's level of home equity at the time of origination as a significant predictor of mortgage default.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on various studies and academic literature, including:

1. von Furstenberg's work from the late 1960s, which developed the first academic default risk model, highlighting the importance of the borrower’s level of home equity at origination as a predictor of mortgage default.
2. Research by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng, and Gabriel (2021).
3. A study by Bhutta, Dokko, and Shan (2010) that distinguishes between defaults induced by job losses and those induced by negative equity, emphasizing the roles of loan-to-value (LTV) ratios and job loss in mortgage defaults.
4. Elul's (2009) findings that low credit score borrowers have a higher risk of delinquency, particularly affecting subprime low-documentation loans.

These studies inform the model's design and the inclusion of factors such as updated LTV and unemployment rates.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on various studies and academic literature, including:

1. Von Furstenberg's work from the late 1960s, which developed the first academic default risk model, highlighting the importance of the borrower’s level of home equity at origination as a predictor of mortgage default.
2. Studies by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng, and Gabriel (2021).
3. Research by Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, emphasizing the roles of loan-to-value (LTV) ratios and job loss.
4. Elul (2009), which finds that low credit score borrowers have a higher risk of delinquency, particularly affecting subprime low-documentation loans.

These studies inform the model's design, including the incorporation of updated LTV measures and proxies for job loss, as well as the use of credit scores as predictors of mortgage default risk.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien PD Model draws on various studies and academic literature, including:

1. Von Furstenberg (1969), who developed the first academic default risk model focusing on the borrower's level of home equity at origination as a predictor of mortgage default.
2. Demyanyk and Van Hemert (2011).
3. Elul, Souleles, et al. (2010).
4. An, Deng, and Gabriel (2021).
5. Bhutta, Dokko, and Shan (2010), who distinguished between defaults induced by job losses and those induced by negative equity.
6. Elul (2009), who found that low credit score borrowers have a higher risk of becoming delinquent.

These studies provide context and support for the model's design and the variables included in it.

### 8. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the roles of LTV (Loan-to-Value) and job loss in mortgage defaults.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores impact subprime low-doc delinquency rates more than full-doc loans.
3. Krainer and Laderman (2011) - This study indicates that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest academic default risk models, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011); Elul, Souleles, et al. (2010); An, Deng, and Gabriel (2021) - These are additional examples of mortgage PD models referenced in the literature review.

These studies collectively inform the design and specification of the First Lien Model, particularly regarding the predictors of mortgage defaults.

### 9. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss in mortgage defaults.

2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores have a greater impact on subprime low-documentation loans compared to full-documentation loans.

3. Krainer and Laderman (2011) - Their findings indicate that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.

4. von Furstenberg (1969) - This is one of the earliest studies that developed a default risk model, showing that the borrower’s level of home equity at the time of origination is a key predictor of mortgage default.

5. Demyanyk and Van Hemert (2011) and Elul, Souleles, et al. (2010) - These studies are also referenced as part of the literature informing the development of the first lien model.

Overall, the model incorporates findings related to debt burden, equity position, income uncertainty, and credit scores in assessing the risk of mortgage defaults.

### 10. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on various studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss in mortgage defaults.

2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores have a greater impact on subprime low-documentation delinquency rates compared to full-documentation loans.

3. Krainer and Laderman (2011) - Their findings indicate that borrowers with low credit scores experienced a relatively larger increase in mortgage defaults during the financial crisis.

4. von Furstenberg (1969) - This early work developed the first academic default risk model, emphasizing the borrower's level of home equity at origination as a key predictor of mortgage default.

5. Demyanyk and Van Hemert (2011) and Elul, Souleles, et al. (2010) - These studies are also referenced as part of the literature informing the development of the first lien PD model.

6. An, Deng, and Gabriel (2021) - Another example of research that contributes to the understanding of mortgage default risk.

These studies collectively support the model's design and the specific variables included in the first lien PD model.

### 11. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The first lien model draws on various studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced purely by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss in mortgage defaults.

2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores significantly impact subprime low-documentation delinquency rates compared to full-documentation loans.

3. Krainer and Laderman (2011) - Their findings indicate that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.

4. von Furstenberg (1969) - This is cited as one of the first academic default risk models, showing that a borrower's level of home equity at origination is a key predictor of mortgage default.

5. Demyanyk and Van Hemert (2011) and Elul, Souleles, et al. (2010) - These studies are also referenced in the context of developing the first lien model.

6. An, Deng, and Gabriel (2021) - Another example of literature that informs the model.

These studies collectively provide a foundation for understanding the factors influencing mortgage defaults and the design of the first lien model.

### 12. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.
8. Lekkas, V., J. M. Quigley, and R. Van Order (1993) - "Loan loss severity and optimal mortgage default," Journal of the American Real Estate and Urban Economics Association.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, credit scores, and economic conditions.

### 13. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010). “The Depth of Negative Equity and Mortgage Default Decisions,” Federal Reserve Board Working Paper.
2. Elul, R. (2009). “Securitization and Mortgage Default: Reputation vs. Adverse Selection,” Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011). “Prepayment and Default in the Mortgage Crisis Period,” Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969). “Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis,” Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. “Understanding the Subprime Mortgage Crisis,” The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010). “What ‘Triggers’ Mortgage Default?” American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021). “Default Option Exercise over the Financial Crisis and beyond,” Review of Finance.
8. Lekkas, V., J. M. Quigley, and R. Van Order (1993). “Loan loss severity and optimal mortgage default,” Journal of the American Real Estate and Urban Economics Association.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, credit scores, and borrower behavior.

### 14. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.

These studies provide insights into the factors influencing mortgage defaults, including loan-to-value ratios (LTV), job loss, credit scores, and borrower behavior.

### 15. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9770 | CP: 0.9029

The first lien model draws on studies and academic literature including works by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng and Gabriel (2021). Additionally, it incorporates findings related to mortgage modeling, particularly those that inform the development of the First Lien PD Model.

### 16. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.7401 | CP: 0.9379

The first lien model draws on a large body of literature that provides useful context for developing an accurate, robust model of first lien probability of default (PD). It is informed by a review of relevant literature and industry best practices, as well as statistical fit and the Board’s experience and expertise. Additionally, the model documentation mentions that most research on residential real estate focuses on first lien mortgages rather than home equity exposures, due to the larger market size and more widely available data for first lien mortgages.

### 17. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9501 | CP: 0.1250

The first lien model draws on studies and academic literature including Gupton, Finger, & Bhatia's CreditMetrics (1997), KMV’s PortfolioManager, and the actuarial approach employed by Credit Suisse First Boston’s CreditRisk+. Detailed comparisons of these approaches are provided in works by Crouhy, Galai, & Mark (2000); Gordy (2000); and Allen & Saunders (2003).

### 18. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9487 | CP: 0.2500

The First Lien Model draws on various studies and academic literature, including:

1. von Furstenberg's work from the late 1960s, which developed the first academic default risk model, highlighting the importance of the borrower’s level of home equity at origination as a predictor of mortgage default.
2. Research by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng, and Gabriel (2021).
3. A study by Bhutta, Dokko, and Shan (2010) that distinguishes between defaults induced by job losses and those induced by negative equity, emphasizing the roles of loan-to-value (LTV) ratios and job loss in mortgage defaults.
4. Elul's 2009 study, which finds that low credit score borrowers have a higher risk of becoming delinquent, particularly affecting subprime low-documentation loans.

These studies inform the model's design and the inclusion of factors such as updated LTV and unemployment rates.

### 19. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9487 | CP: 0.9379

The First Lien Model draws on a variety of studies and academic literature, including:

1. The work of von Furstenberg, who developed the first academic default risk model in the late 1960s, showing that the borrower’s level of home equity at the time of origination was a key predictor of mortgage default.
2. Studies by Demyanyk and Van Hemert (2011), Elul, Souleles, et al. (2010), and An, Deng and Gabriel (2021).
3. Research by Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss in mortgage defaults.
4. Findings from Elul (2009), which indicate that low credit score borrowers have a higher risk of becoming delinquent, particularly affecting subprime low-documentation loans.

These studies provide useful context for developing an accurate and robust model of first lien probability of default (PD).

### 20. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8456 | CP: 0.9583

The First Lien PD Model draws on various studies and academic literature, including:

1. von Furstenberg (1969) - developed the first academic default risk model focusing on the borrower's level of home equity at origination as a predictor of mortgage default.
2. Demyanyk and Van Hemert (2011).
3. Elul, Souleles, et al. (2010).
4. An, Deng and Gabriel (2021).
5. Bhutta, Dokko, and Shan (2010) - distinguished between defaults induced by job losses and those induced by negative equity.
6. Elul (2009) - found that low credit score borrowers have a higher risk of becoming delinquent.

Additionally, the model incorporates findings from Mayer, Pence, and Sherlund (2009) regarding borrowers with piggyback second liens and Calem and Sarama (2017) on borrowers with multiple liens.

### 21. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9174 | CP: 0.5667

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the roles of LTV (Loan-to-Value) and job loss in mortgage defaults.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores impact subprime low-doc delinquency rates more than full-doc loans.
3. Krainer and Laderman (2011) - This study indicates that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest academic default risk models, showing that the borrower’s level of home equity at the time of origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) - Another example of mortgage PD models developed and estimated.
6. Elul, Souleles, et al. (2010) - This research contributes to the understanding of mortgage default risk.
7. An, Deng, and Gabriel (2021) - This study is also referenced in the context of mortgage modeling.

These studies collectively inform the design and specification of the First Lien Model, emphasizing the importance of factors such as debt burden, equity position, income uncertainty, and credit scores in assessing mortgage default risk.

### 22. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9770 | CP: 0.7042

The first lien model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced purely by negative equity, highlighting the roles of loan-to-value (LTV) ratios and job loss in mortgage defaults.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores impact subprime low-documentation delinquency rates more than similar full-documentation loans.
3. Krainer and Laderman (2011) - This study indicates that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest academic default risk models, showing that the borrower’s level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011) and Elul, Souleles, et al. (2010) - These studies are also referenced in the context of developing the first lien PD model.

Overall, the model incorporates findings related to debt burden, equity position, income uncertainty, and credit scores in assessing mortgage default risk.

### 23. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.7949 | CP: 0.7022

The first lien model draws on various studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of both loan-to-value (LTV) ratios and job loss in mortgage defaults.

2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, particularly noting that credit scores have a greater impact on subprime low-documentation loans compared to full-documentation loans.

3. Krainer and Laderman (2011) - Their findings indicate that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.

4. von Furstenberg (1969) - This early work developed the first academic default risk model, emphasizing the borrower's level of home equity at origination as a key predictor of mortgage default.

5. Demyanyk and Van Hemert (2011) and Elul, Souleles, et al. (2010) - These studies are also referenced as part of the literature informing the development of the first lien PD model.

6. An, Deng, and Gabriel (2021) - Another example of literature that contributes to the understanding of mortgage default risk.

These studies collectively inform the model's design, variables, and transformations used in assessing the risk of mortgage defaults.

### 24. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9770 | CP: 1.0000

The first lien model draws on various studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - This study distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the roles of loan-to-value (LTV) ratios and job loss in mortgage defaults.
2. Elul (2009) - This research finds that low credit score borrowers have a higher risk of becoming delinquent, noting that credit scores impact subprime low-documentation delinquency rates more than full-documentation loans.
3. Krainer and Laderman (2011) - This study indicates that borrowers with low credit scores experienced a larger increase in mortgage defaults during the financial crisis.
4. von Furstenberg (1969) - This is one of the earliest academic default risk models, showing that a borrower's level of home equity at origination is a key predictor of mortgage default.
5. Demyanyk and Van Hemert (2011); Elul, Souleles, et al. (2010); An, Deng, and Gabriel (2021) - These are additional examples of mortgage PD models referenced in the literature review.

The model also incorporates findings from a broad body of literature that provides context for developing an accurate and robust model of first lien probability of default (PD).

### 25. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.7853 | CP: 0.8711

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.
8. Lekkas, V., J. M. Quigley, and R. Van Order (1993) - "Loan loss severity and optimal mortgage default," Journal of the American Real Estate and Urban Economics Association.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, credit scores, and borrower behavior.

### 26. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.7853 | CP: 0.9214

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010). “The Depth of Negative Equity and Mortgage Default Decisions,” Federal Reserve Board Working Paper.
2. Elul, R. (2009). “Securitization and Mortgage Default: Reputation vs. Adverse Selection,” Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011). “Prepayment and Default in the Mortgage Crisis Period,” Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969). “Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis,” Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. “Understanding the Subprime Mortgage Crisis,” The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010). “What ‘Triggers’ Mortgage Default?” American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021). “Default Option Exercise over the Financial Crisis and beyond,” Review of Finance.
8. Lekkas, V., J. M. Quigley, and R. Van Order (1993). “Loan loss severity and optimal mortgage default,” Journal of the American Real Estate and Urban Economics Association.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, credit scores, and economic conditions.

### 27. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.7853 | CP: 0.9444

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, Dokko, and Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," which distinguishes between defaults induced by job losses and those induced by negative equity.
2. Elul (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," which finds that low credit score borrowers have a higher risk of becoming delinquent.
3. Krainer and Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," which discusses the increase in mortgage defaults among borrowers with low credit scores during the financial crisis.
4. von Furstenberg (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing," which developed the first academic default risk model.
5. Demyanyk and Van Hemert (2011) - "Understanding the Subprime Mortgage Crisis."
6. Elul, Souleles, et al. (2010) - "What ‘Triggers’ Mortgage Default?"
7. An, Deng, and Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond."

These studies provide insights into various factors influencing mortgage defaults, such as loan-to-value ratios (LTV), job loss, credit scores, and borrower equity.

### 28. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.7853 | CP: 0.9056

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.

These studies provide insights into the factors influencing mortgage defaults, including loan-to-value (LTV) ratios, credit scores, and economic conditions.

### 29. `chunk_size_1000_chunk_overlap_300` — F: 0.8125 | AR: 0.9487 | CP: 0.7736

The First Lien Model draws on various studies and academic literature, including:

1. von Furstenberg's work from the late 1960s, which developed the first academic default risk model and identified the borrower's level of home equity at origination as a key predictor of mortgage default.
2. Demyanyk and Van Hemert (2011), which discusses the subprime mortgage crisis.
3. Elul, Souleles, et al. (2010), which examines factors influencing mortgage defaults.
4. An, Deng, and Gabriel (2021), which contributes to the understanding of mortgage default risk.
5. Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of loan-to-value (LTV) ratios and job loss in mortgage defaults.
6. Elul (2009), which finds that low credit score borrowers have a higher risk of delinquency.

These studies provide insights into the variables and transformations included in the First Lien PD Model.

### 30. `chunk_size_1000_chunk_overlap_300` — F: 0.7000 | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Von Furstenberg's work from the late 1960s, which developed the first academic default risk model and identified the borrower's level of home equity at origination as a key predictor of mortgage default.
2. Demyanyk and Van Hemert (2011), which discusses the subprime mortgage crisis.
3. Elul, Souleles, et al. (2010), which examines various factors influencing mortgage defaults.
4. An, Deng, and Gabriel (2021), which contributes to the understanding of mortgage default risk.
5. Bhutta, Dokko, and Shan (2010), which distinguishes between defaults induced by job losses and those induced by negative equity, highlighting the importance of loan-to-value (LTV) ratios and job loss in mortgage defaults.
6. Elul (2009), which finds that low credit score borrowers have a higher risk of delinquency.

These studies provide insights into the design and variables included in the First Lien PD Model.

### 31. `chunk_size_500_chunk_overlap_300` — F: 0.5000 | AR: 0.9770 | CP: 0.8955

The first lien model draws on various studies and academic literature, including:

1. von Furstenberg, G. (1969). “Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis,” Journal of Finance 24(2): 459-77.
2. von Furstenberg, G. (1970a).
3. Demyanyk and Van Hemert (2011).
4. Elul, Souleles, et al. (2010).
5. An, Deng and Gabriel (2021).

Additionally, it incorporates findings from the first academic default risk model, which indicated that the borrower’s level of home equity at the time of origination was the most important predictor of mortgage default.

### 32. `chunk_size_3000_chunk_overlap_200` — F: n/a | AR: n/a | CP: n/a

The First Lien Model draws on several studies and academic literature, including:

1. Bhutta, N., J. Dokko, and H. Shan (2010) - "The Depth of Negative Equity and Mortgage Default Decisions," Federal Reserve Board Working Paper.
2. Elul, R. (2009) - "Securitization and Mortgage Default: Reputation vs. Adverse Selection," Federal Reserve Bank of Philadelphia, Working Paper No. 9-21.
3. Krainer, J. and E. Laderman (2011) - "Prepayment and Default in the Mortgage Crisis Period," Federal Reserve Bank of San Francisco Working Paper.
4. von Furstenberg, G. (1969) - "Default Risk on FHA-Insured Home Mortgage as a Function of the Term of Financing: A Quantitative Analysis," Journal of Finance.
5. Demyanyk, Y., and Van Hemert, O. - "Understanding the Subprime Mortgage Crisis," The Review of Financial Studies.
6. Elul, R., N. S. Souleles, S. Chomsisengphet, D. Glennon, and R. Hunt (2010) - "What ‘Triggers’ Mortgage Default?" American Economic Review Papers & Proceedings.
7. An, X., Y. Deng, S.A. Gabriel (2021) - "Default Option Exercise over the Financial Crisis and beyond," Review of Finance.
8. Lekkas, V., J. M. Quigley, and R. Van Order (1993) - "Loan loss severity and optimal mortgage default," Journal of the American Real Estate and Urban Economics Association.

These studies provide insights into various factors influencing mortgage defaults, including loan-to-value ratios, credit scores, and borrower behavior.

---

## Question 7: How does the home equity model leverage the zillow price database?

### 1. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 2. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 3. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 4. `chunk_size_500_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 5. `chunk_size_500_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 6. `chunk_size_500_chunk_overlap_200` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 7. `chunk_size_500_chunk_overlap_300` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 8. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 9. `chunk_size_1000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 10. `chunk_size_1000_chunk_overlap_200` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 11. `chunk_size_1000_chunk_overlap_300` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 12. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 13. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 14. `chunk_size_2000_chunk_overlap_200` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 15. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 16. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 17. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 18. `chunk_size_3000_chunk_overlap_300` — F: n/a | AR: n/a | CP: n/a

I don't know.

### 19. `chunk_size_500_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 20. `chunk_size_500_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 21. `chunk_size_500_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 22. `chunk_size_500_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 23. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 24. `chunk_size_1000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 25. `chunk_size_1000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 26. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 27. `chunk_size_2000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 28. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 29. `chunk_size_3000_chunk_overlap_50` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 30. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_3000_chunk_overlap_200` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_3000_chunk_overlap_300` — F: n/a | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 8: What did Alan Greenspan say about the stress test reform announcement?

### 1. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 2. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 3. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 4. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 17. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 18. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 19. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 20. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 21. `chunk_size_1000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 22. `chunk_size_1000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 23. `chunk_size_1000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 24. `chunk_size_1000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 25. `chunk_size_2000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 26. `chunk_size_2000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 27. `chunk_size_2000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 28. `chunk_size_2000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 29. `chunk_size_3000_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 30. `chunk_size_3000_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_3000_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 9: What did Chair Powell say about the stress test reform announcement?

### 1. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps maintain that strength by ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the stress testing program has been an important element of the Board's regulatory framework since 2009 and that the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 2. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps maintain that strength by ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 3. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps ensure that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that last December, the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps ensure large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that last December, the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 5. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting are a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following a commitment made in December to enhance these aspects.

### 6. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements. He emphasized the importance of seeking public comment on the stress test models and the design of hypothetical scenarios, indicating a commitment to follow through on the Board's previous announcement to enhance transparency.

### 7. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is important for ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step in following through on the Board's commitment to improve the transparency of the stress tests and reduce the volatility of capital buffer requirements. He expressed gratitude to the staff for their work on the proposals and looked forward to the presentations.

### 8. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following a commitment made in December 2024 to enhance the transparency of the stress tests.

### 9. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed were a step in following through on the Board's commitment to improve the transparency of the stress tests and reduce the volatility of resulting capital buffer requirements. He emphasized the importance of seeking public comment on the stress test models and the design of hypothetical scenarios for the upcoming stress test.

### 10. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed were a step in following through on the Board's commitment to improve the transparency of the stress tests and reduce the volatility of capital buffer requirements. He emphasized the importance of seeking public comment on the stress test models and the design of hypothetical scenarios for the upcoming stress test.

### 11. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step toward improving the transparency of the stress tests and reducing the volatility of capital buffer requirements. He emphasized the importance of seeking comment on the stress test models and the design of hypothetical scenarios, indicating a commitment to follow through on the Board's prior announcement to enhance transparency.

### 12. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.8360 | CP: 0.6676

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps maintain that strength by ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 13. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.8361 | CP: 0.6349

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps maintain that strength by ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that last December, the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 14. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.8361 | CP: 0.6215

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps maintain that strength by ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that last December, the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 15. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.8361 | CP: 0.9111

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps ensure large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that stress testing has been an important element of the Board's regulatory framework since 2009 and that last December, the Board committed to improving the transparency of the stress tests and reducing the volatility of resulting capital buffer requirements. He described the meeting as a step in following through on that commitment.

### 16. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.8360 | CP: 0.3333

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is important for ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following the Board's commitment to enhance transparency made in December 2024.

### 17. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.8361 | CP: 0.8333

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following a commitment made in December 2024 to enhance these aspects.

### 18. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.8361 | CP: 0.8333

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following a commitment made in December 2024 to enhance the transparency of the stress tests.

### 19. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.8360 | CP: 1.0000

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps ensure that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step toward improving the transparency of the stress tests and reducing the volatility of capital buffer requirements, following a commitment made in December 2024 to enhance the stress testing framework.

### 20. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.8360 | CP: 0.9167

Chair Powell stated that the financial system remains sound and resilient, and that stress testing helps ensure that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed were a step in following through on the Board's commitment to improve the transparency of the stress tests and reduce the volatility of resulting capital buffer requirements. He expressed gratitude to the staff for their presentations and acknowledged the importance of stress testing as part of the Board's regulatory framework since 2009.

### 21. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.8360 | CP: 0.9167

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed were a step in following through on the Board's commitment to improve the transparency of the stress tests and reduce the volatility of capital buffer requirements. He expressed gratitude to the staff for their presentations and emphasized the importance of the stress testing framework since its inception in 2009, particularly as a response to reforms following the Global Financial Crisis.

### 22. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.8360 | CP: 0.6000

Chair Powell stated that the financial system remains sound and resilient, and that stress testing is crucial for ensuring that large supervised institutions have sufficient capital to absorb losses and continue lending during a recession. He mentioned that the proposals discussed in the meeting were a step towards improving the transparency of the stress tests and reducing the volatility of capital buffer requirements. He emphasized the importance of seeking comment on the stress test models, changes to the framework governing the design of hypothetical scenarios, and the scenario for the upcoming stress test.

### 23. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 24. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 25. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 26. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 27. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: n/a | CP: n/a

I don't know.

### 28. `chunk_size_500_chunk_overlap_50` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 29. `chunk_size_500_chunk_overlap_100` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 30. `chunk_size_500_chunk_overlap_200` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 31. `chunk_size_500_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

### 32. `chunk_size_3000_chunk_overlap_300` — F: 0.0000 | AR: 0.0000 | CP: 0.0000

I don't know.

---

## Question 10: What is the purpose of the Dodd-Frank Act stress tests and who must participate?

### 1. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms, specifically bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board, have the capital necessary to absorb losses as a result of adverse economic conditions. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 2. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms, specifically bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board, have the capital necessary to absorb losses as a result of adverse economic conditions. These tests help assess a firm's capital adequacy, identify downside risks, and contribute to financial stability goals. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 3. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial firms have the capital necessary to absorb losses as a result of adverse economic conditions, thereby helping to achieve financial stability goals. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 4. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms, specifically bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board, have the capital necessary to absorb losses as a result of adverse economic conditions. These stress tests help improve firms' stress testing practices and assist in achieving financial stability goals. Participants must include bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board.

### 5. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks and the potential impact of adverse outcomes on the firm's capital adequacy, and assist in achieving the financial stability goals of the Dodd-Frank Act. Additionally, these stress tests help improve firms' stress testing practices regarding their internal assessments of capital adequacy and overall capital planning.

Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to conduct company-run stress tests on a periodic basis. Furthermore, the Board conducts annual supervisory stress tests for these large firms and for bank holding companies with total consolidated assets between $100 billion and $250 billion.

### 6. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks, assess the potential impact of adverse outcomes on a firm's capital adequacy, and achieve the financial stability goals of the Dodd-Frank Act. The firms that must participate in these stress tests include bank holding companies with $250 billion or more in total consolidated assets, nonbank financial companies supervised by the Board, and bank holding companies with total consolidated assets between $100 billion and $250 billion.

### 7. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks and the potential impact of adverse outcomes on the firm's capital adequacy, and assist in achieving the financial stability goals of the Dodd-Frank Act. The firms that must participate in these stress tests include bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are required to conduct periodic stress tests.

### 8. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks, and evaluate the potential impact of adverse outcomes on a firm's capital adequacy. These tests also aim to achieve the financial stability goals of the Dodd-Frank Act and improve firms' stress testing practices regarding their internal assessments of capital adequacy and overall capital planning.

Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to conduct company-run stress tests on a periodic basis. Additionally, the Board conducts annual supervisory stress tests for these large firms and for bank holding companies with total consolidated assets between $100 billion and $250 billion.

### 9. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses resulting from adverse economic conditions, thereby ensuring their financial stability and ability to lend during severe recessions. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 10. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby ensuring their financial stability and ability to lend to households and businesses even in a severe recession. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, must participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are required to conduct periodic stress tests.

### 11. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby promoting financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 12. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby promoting financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 13. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies supervised by the Board have sufficient capital to absorb losses during adverse economic conditions. These tests help ensure that these firms are adequately capitalized and able to lend to households and businesses even in a severe recession.

Participants in the stress tests include bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 14. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies supervised by the Board have the capital necessary to absorb losses as a result of adverse economic conditions. These stress tests help ensure that these firms are sufficiently capitalized and able to lend to households and businesses even in a severe recession.

Participation is required for bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 15. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies supervised by the Board have the capital necessary to absorb losses during adverse economic conditions. These tests help ensure that these firms are sufficiently capitalized and able to lend to households and businesses even in a severe recession.

Participants in the stress tests include bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 16. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies have the capital necessary to absorb losses during adverse economic conditions, thereby helping to ensure financial stability in the United States. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 17. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 0.9220 | CP: 0.8556

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial firms have the capital necessary to absorb losses as a result of adverse economic conditions. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to conduct these stress tests on a periodic basis. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests as mandated by the Economic Growth, Regulatory Relief, and Consumer Protection Act.

### 18. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9220 | CP: 0.9750

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms, specifically bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board, have the capital necessary to absorb losses as a result of adverse economic conditions. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 19. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9220 | CP: 0.6746

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms have the capital necessary to absorb losses as a result of adverse economic conditions, thereby contributing to financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to conduct these company-run stress tests on a periodic basis. Additionally, the Board must conduct annual supervisory stress tests for these firms.

### 20. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9220 | CP: 0.8412

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large firms, specifically bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board, have the capital necessary to absorb losses as a result of adverse economic conditions. These stress tests help improve firms' stress testing practices and assist in achieving financial stability goals. Participants must include bank holding companies with $250 billion or more in total consolidated assets and nonbank financial companies supervised by the Board. Additionally, firms subject to Category I, II, or III standards must conduct company-run stress tests.

### 21. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 0.9220 | CP: 0.8339

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks, and evaluate the potential impact of adverse outcomes on a firm's capital adequacy. These tests also aim to achieve the financial stability goals of the Dodd-Frank Act and improve firms' stress testing practices regarding their internal assessments of capital adequacy and overall capital planning.

Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to conduct company-run stress tests on a periodic basis. Additionally, the Board conducts annual supervisory stress tests for these large firms and for bank holding companies with total consolidated assets between $100 billion and $250 billion.

### 22. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 0.9220 | CP: 0.6722

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks and the potential impact of adverse outcomes on the firm's capital adequacy, and assist in achieving the financial stability goals of the Dodd-Frank Act. The firms that must participate in these stress tests include bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are required to conduct periodic stress tests.

### 23. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 0.9220 | CP: 0.9478

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks and the potential impact of adverse outcomes on the firm's capital adequacy, and assist in achieving the financial stability goals of the Dodd-Frank Act. 

Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, must participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 24. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 0.9220 | CP: 0.9325

The purpose of the Dodd-Frank Act stress tests is to provide forward-looking information to supervisors to assist in their overall assessments of a firm's capital adequacy, help identify downside risks and the potential impact of adverse outcomes on the firm's capital adequacy, and assist in achieving the financial stability goals of the Dodd-Frank Act. 

Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, must participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are also required to conduct periodic stress tests.

### 25. `chunk_size_2000_chunk_overlap_50` — F: 1.0000 | AR: 0.9220 | CP: 0.9750

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby ensuring their financial stability and ability to lend to households and businesses even in a severe recession. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, must participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are required to conduct periodic stress tests.

### 26. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 0.9220 | CP: 0.9861

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby ensuring their financial stability and ability to lend to households and businesses even in a severe recession. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, must participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion are required to conduct periodic stress tests.

### 27. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 0.9220 | CP: 0.9617

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby promoting financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 28. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: 0.9220 | CP: 1.0000

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have the capital necessary to absorb losses during adverse economic conditions, thereby promoting financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 29. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 0.9220 | CP: 0.9705

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large financial institutions have sufficient capital to absorb losses during adverse economic conditions, thereby promoting financial stability. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 30. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 0.9220 | CP: 0.9472

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies supervised by the Board have sufficient capital to absorb losses during adverse economic conditions. These tests help ensure that these firms are adequately capitalized and can continue to lend to households and businesses even in a severe recession.

Participation is required for bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 31. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 0.9220 | CP: 0.9325

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies supervised by the Board have the capital necessary to absorb losses during adverse economic conditions. These tests help ensure that these institutions are sufficiently capitalized and able to lend to households and businesses even in a severe recession.

Participation is required for bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

### 32. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 0.9220 | CP: 0.9583

The purpose of the Dodd-Frank Act stress tests is to evaluate whether large bank holding companies and nonbank financial companies have the capital necessary to absorb losses during adverse economic conditions, thereby helping to ensure financial stability in the United States. Bank holding companies with $250 billion or more in total consolidated assets, as well as nonbank financial companies supervised by the Board, are required to participate in these stress tests. Additionally, bank holding companies with total consolidated assets between $100 billion and $250 billion must also conduct periodic stress tests.

---

## Question 11: What criticisms did the BPI raise about the Fed's stress test methodology?

### 1. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The BPI criticized the Fed's stress test methodology for producing inaccurate results, stating that the tests often yield counterintuitive and nonsensical outcomes that are inconsistent with more accurate bank models and recent market experiences. They also highlighted concerns about the lack of transparency in the stress testing process and the substantial fluctuations in capital requirements resulting from the Fed's methodological changes.

### 2. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

BPI criticized the Fed's stress test methodology for producing inaccurate results. They argued that the tests fail to project how much a bank's capital would be depleted under severely adverse scenarios, often yielding counterintuitive and nonsensical results that are inconsistent with more accurate bank models and recent market experiences. Additionally, BPI has claimed that the Fed's stress tests violate the law by lacking transparency, which the public has a legal right to see, understand, and comment on.

### 3. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy**: The stress tests produce inaccurate results, often yielding counterintuitive and nonsensical outcomes that are inconsistent with more accurate bank models and recent market experiences.

2. **Opacity**: The models used by the Fed are described as one-size-fits-all and opaque, making it difficult for banks to understand the basis of the results.

3. **Volatility**: The results of the stress tests are characterized by excessive volatility, which raises questions about the consistency and predictability of the stress testing process.

4. **Impact on Business Decisions**: The stress test framework creates uncertainty that negatively affects banks' business decisions, potentially harming the economy and U.S. business growth.

5. **Appeals Process**: The appeals process for challenging test results is deemed broken, as nearly every public appeal has been denied with little explanation, and only one appeal was granted in 2024.

6. **Discouragement of Certain Lines of Business**: The stress tests discourage banks from engaging in certain lines of business, such as mortgages and small business loans, due to higher capital requirements associated with these areas.

Overall, BPI argues that the Fed's stress tests violate legal transparency requirements and that the current methodology needs significant reform to improve its effectiveness and fairness.

### 4. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy of Results**: The stress tests produce inaccurate results that are often counterintuitive and inconsistent with more granular and accurate bank models and recent market experiences.

2. **Opacity and Lack of Transparency**: BPI has challenged the opacity of the Fed’s stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned for transparency, which has largely been ignored.

3. **Volatility and Inconsistency**: The reliance on aggregated models and recent bank performance in projections leads to excessive volatility in capital requirements, making it difficult for banks to plan effectively.

4. **Broken Appeals Process**: The appeals process for challenging test results is described as broken, with nearly all public appeals being denied without sufficient explanation.

5. **Discouragement of Certain Business Lines**: The stress tests treat certain lines of business, such as mortgages and small business loans, as riskier, which can lead to higher capital requirements and discourage banks from engaging in these areas.

6. **One-Size-Fits-All Approach**: The Fed's models are criticized for being one-size-fits-all and opaque, which does not adequately address the diverse risks faced by different banks.

7. **Need for Public Comment**: BPI emphasized that allowing public comment on scenarios and supervisory models would enhance transparency and improve model accuracy, ultimately fostering a more effective financial system.

### 5. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted the opacity of the Fed's stress test models and called for public access to understand and comment on these models.

2. **Inconsistency and Fairness**: They questioned the consistency and fairness of the stress testing process across different types of banking institutions, particularly in light of substantial increases in capital requirements for Intermediate Holding Companies (IHCs).

3. **Volatility in Capital Requirements**: BPI pointed out significant volatility in stress capital buffers, especially for IHCs of foreign banks, which raises concerns about predictability in capital requirements.

4. **Reliance on Aggregated Models**: The Fed's reliance on aggregated models that assign disproportionate weight to recent bank performance in projections was criticized. This approach often leads to excessive variability in stress test projections.

5. **Inaccurate Revenue Projections**: BPI noted that the Fed's revenue models, based on aggregated pre-provision net revenue (PPNR) components, often downplayed macroeconomic scenario variables, resulting in inaccurate and volatile projections.

6. **Need for Public Comment**: They emphasized that allowing public comment on scenarios and supervisory models would enhance transparency and improve model accuracy, ultimately fostering a more effective financial system.

### 6. `chunk_size_2000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Opacity and Lack of Transparency**: BPI criticized the Fed for the opaque nature of its stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned the Fed for years to make the stress tests transparent, but their efforts have been ignored.

2. **Inconsistency and Fairness**: The BPI highlighted concerns about the consistency and fairness of the stress testing process across different types of banking institutions, particularly in light of substantial increases in capital requirements for Intermediate Holding Companies (IHCs).

3. **Volatility in Capital Requirements**: The BPI pointed out that the Fed's reliance on aggregated models and recent bank performance in projections leads to significant volatility in stress capital buffers, raising concerns about predictability and fairness.

4. **Lack of Granularity**: They noted that the Fed's revenue projections lack granularity, which contributes to excessive variability in capital requirements. The models often assign disproportionate weight to past bank performance rather than macroeconomic scenario variables.

5. **Need for Public Comment**: BPI emphasized that allowing public comment on scenarios and supervisory models would enable expert review and improve model accuracy, thereby fostering a more effective financial system.

Overall, BPI's criticisms focus on the need for greater transparency, consistency, and fairness in the Fed's stress testing methodology.

### 7. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The Fed's stress testing process has been described as obscure, lacking transparency which affects trust and predictability for regulated entities.

2. **Inaccuracies and Volatility**: BPI highlighted inaccuracies and excessive volatility in the supervisory stress-testing models used to determine capital requirements, particularly due to the reliance on aggregated models that disproportionately weight recent bank performance.

3. **Granularity in Revenue Projections**: There is a concern about the lack of granularity in the Fed's revenue projections, which contributes to excessive variability in capital requirements.

4. **Backward-Looking Models**: The Fed's models are heavily influenced by backward-looking terms, which can distort projections and lead to inconsistencies in assessing banks' capital needs.

5. **Need for Public Comment**: BPI emphasized the importance of allowing public comment on scenarios and supervisory models to enhance transparency and improve model accuracy.

6. **Impact on Credit Availability**: The lack of transparency and predictability in the stress testing process can negatively impact bank credit availability and cost, ultimately affecting the broader economy. 

Overall, BPI called for reforms to improve the transparency and effectiveness of the stress testing framework.

### 8. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress testing process, which affects banks' ability to anticipate and plan for changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out inaccuracies and excessive volatility in the supervisory stress-testing models used to determine the stress capital buffer, particularly due to the Fed's reliance on aggregated models that disproportionately weight bank performance from the preceding year.

3. **Granularity of Models**: BPI criticized the Fed for not providing sufficient granularity in their revenue projections, which contributes to excessive variability in stress test projections.

4. **Public Comment on Models**: They advocated for allowing public comment on scenarios and supervisory models to enable expert review, which would improve transparency and model accuracy.

5. **Impact on Capital Requirements**: The substantial increases in capital requirements for intermediate holding companies (IHCs) of foreign banks were noted as a significant concern, raising questions about the consistency and fairness of the stress testing process across different types of banking institutions.

Overall, BPI emphasized the need for reforms to enhance the transparency and effectiveness of the stress testing framework.

### 9. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress testing process, which makes it difficult for banks to anticipate and plan for changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out inaccuracies and excessive volatility in the supervisory stress-testing models used to determine the stress capital buffer, particularly due to the Fed's reliance on aggregated models that assign disproportionate weight to bank performance in the preceding year.

3. **Granularity of Models**: The BPI criticized the Fed for not providing sufficient granularity in their revenue projections, which contributes to excessive variability in stress test projections.

4. **Public Comment and Review**: They advocated for allowing public comment on scenarios and supervisory models to enable extensive review by experts, academics, and banks, which would improve model accuracy and transparency.

5. **Impact on Capital Requirements**: The BPI noted that the Fed's methodological changes have led to significant increases in capital requirements for intermediate holding companies (IHCs) of foreign banks, raising questions about the consistency and fairness of the stress testing process across different types of banking institutions. 

Overall, the BPI emphasized the need for reforms to enhance the transparency and effectiveness of the stress testing framework.

### 10. `chunk_size_500_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.9207

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccurate Results**: The Fed's models produce inaccurate results that do not effectively project how much a bank's capital would be depleted under severely adverse scenarios. The stress tests often yield counterintuitive and nonsensical results that are inconsistent with more accurate bank models and recent market experiences.

2. **Lack of Transparency**: BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress tests, arguing that the public has a legal right to see, understand, and comment on the Fed's stress test models.

3. **Volatility in Capital Requirements**: BPI pointed out that there is excess volatility in capital requirements due to the lack of granularity in the Fed's revenue projections, which contributes to significant fluctuations in capital requirements.

4. **Methodological Changes**: The substantial increases in capital requirements for Intermediate Holding Companies (IHCs) raised questions about the consistency and fairness of the stress testing process across different types of banking institutions, indicating that the Fed's methodological changes have a significant impact. 

Overall, BPI called for increased transparency and notice and comment on the supervisory models used in stress testing.

### 11. `chunk_size_500_chunk_overlap_100` — F: 1.0000 | AR: 0.9799 | CP: 0.9683

The BPI criticized the Fed's stress test methodology for producing inaccurate results, stating that the tests often yield counterintuitive and nonsensical outcomes that are inconsistent with more accurate bank models and recent market experiences. They also highlighted concerns about the lack of transparency in the stress testing process and the significant impact of the Fed's methodological changes on capital requirements for banks.

### 12. `chunk_size_500_chunk_overlap_200` — F: 1.0000 | AR: 0.9799 | CP: 0.9367

The BPI criticized the Fed's stress test methodology for producing inaccurate results, stating that the tests often yield counterintuitive and nonsensical outcomes that are inconsistent with more accurate bank models and recent market experiences. They argued that the Fed's models perform poorly in projecting how much a bank's capital would be depleted under severely adverse scenarios. Additionally, BPI highlighted concerns about the lack of transparency in the Fed's stress tests and the substantial fluctuations in capital requirements resulting from the tests, which raised questions about the consistency and fairness of the stress testing process across different types of banking institutions.

### 13. `chunk_size_500_chunk_overlap_300` — F: 1.0000 | AR: 0.9693 | CP: 0.9889

BPI criticized the Fed's stress test methodology for producing inaccurate results. They argued that the tests poorly project how much a bank's capital would be depleted under severely adverse scenarios, leading to counterintuitive and sometimes nonsensical results that are inconsistent with more accurate bank models and recent market experience. Additionally, BPI has challenged the opacity of the Fed's stress test models, claiming that the public has a legal right to see, understand, and comment on them.

### 14. `chunk_size_1000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.7847

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccurate Results**: The stress tests produce counterintuitive and sometimes nonsensical results that are inconsistent with more granular and accurate bank models and recent market experience.

2. **Broken Appeals Process**: The appeals process for challenging the results is deemed broken, as nearly every public appeal has been denied with little explanation, and the Fed only granted an appeal for the first time in 2024.

3. **Discouragement of Certain Business Lines**: The stress tests treat certain lines of business, such as mortgages and small business loans, as riskier, leading to higher capital requirements that discourage banks from engaging in these areas.

4. **Excessive Volatility in Capital Requirements**: The substantial fluctuations in capital requirements highlighted by the stress test results raise questions about the consistency and predictability of the stress testing process, which could affect banks' ability to manage their capital effectively and impact their lending capacity.

### 15. `chunk_size_1000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.9294

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccurate Results**: The stress tests produce counterintuitive and sometimes nonsensical results that are inconsistent with more accurate bank models and recent market experience.

2. **Broken Appeals Process**: The appeals process for challenging the results is deemed insufficient, as nearly every public appeal has been denied with little explanation, and the Fed only granted an appeal for the first time in 2024.

3. **Discouragement of Certain Business Lines**: The stress tests treat certain lines of business, such as mortgages and small business loans, as riskier, leading to higher capital requirements that could discourage banks from engaging in these areas.

4. **Lack of Transparency**: BPI has challenged the opacity of the Fed’s stress test models, arguing that the public has a legal right to see, understand, and comment on them.

5. **Uncertainty Affecting Economic Growth**: The stress test framework creates uncertainty that negatively impacts the economy and U.S. business growth.

6. **Excessive Volatility in Capital Requirements**: The substantial fluctuations in capital requirements highlighted by the stress test results raise questions about the consistency and predictability of the stress testing process, which could affect banks' ability to manage their capital effectively.

### 16. `chunk_size_1000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.8690

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted concerns about the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models.

2. **Inaccurate Results**: The stress tests were criticized for producing inaccurate and sometimes nonsensical results that are inconsistent with more granular and accurate bank models and recent market experiences.

3. **Volatility**: The results of the stress tests were described as volatile, leading to excessive fluctuations in capital requirements, which could affect banks' ability to manage their capital effectively.

4. **Discouragement of Certain Business Lines**: The stress tests were said to discourage banks from engaging in certain lines of business, such as mortgages and small business loans, due to their treatment as riskier and the resulting higher capital requirements.

5. **Broken Appeals Process**: BPI pointed out that the appeals process for challenging test results is ineffective, as nearly every public appeal has been denied with little explanation.

6. **One-Size-Fits-All Approach**: The methodology was criticized for being a one-size-fits-all approach that does not adequately account for the unique circumstances of different banks.

These criticisms were part of BPI's broader efforts to advocate for reforms and greater transparency in the stress testing process.

### 17. `chunk_size_1000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 0.9861

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy of Results**: The stress tests produce inaccurate results that are often counterintuitive and inconsistent with more granular bank models and recent market experiences. The Fed's models are said to perform poorly in projecting capital depletion under adverse scenarios.

2. **Opacity and Lack of Transparency**: BPI criticized the lack of transparency in the Fed's stress test models and methodologies, arguing that the public has a legal right to see, understand, and comment on these models. They believe that allowing public comment would improve transparency and model accuracy.

3. **Volatility and Inconsistency**: The stress tests lead to substantial fluctuations in capital requirements, raising concerns about the consistency and predictability of the testing process. This volatility can significantly impact banks' ability to manage their capital effectively.

4. **Discouragement of Certain Business Lines**: The stress tests treat certain lines of business, such as mortgages and small business loans, as riskier, which can lead to higher capital requirements and discourage banks from engaging in these activities.

5. **Broken Appeals Process**: BPI pointed out that the appeals process for challenging stress test results is ineffective, with most public appeals being denied without sufficient explanation. 

Overall, BPI argues that these issues hinder banks' ability to plan and manage their capital effectively, potentially affecting their lending capacity and market participation.

### 18. `chunk_size_2000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.9167

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. Lack of Transparency: BPI highlighted the opacity of the Fed's stress test models and called for public access to understand and comment on these models.

2. Inconsistency and Fairness: They questioned the consistency and fairness of the stress testing process across different types of banking institutions, particularly in light of substantial increases in capital requirements for Intermediate Holding Companies (IHCs).

3. Volatility in Capital Requirements: BPI pointed out significant volatility in stress capital buffers, especially for IHCs of foreign banks, which raises concerns about predictability and fairness.

4. Reliance on Aggregated Models: The Fed's reliance on aggregated models and recent bank performance in projections was criticized for making it difficult for banks to anticipate and plan for changes in capital requirements.

5. Insufficient Reforms: Although the Fed has taken some steps to improve model granularity, BPI deemed these efforts insufficient to address the underlying issues.

6. Need for Public Comment: BPI emphasized that allowing public comment on scenarios and supervisory models would enhance transparency and improve model accuracy, ultimately fostering a more effective financial system.

### 19. `chunk_size_2000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.9594

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted the opacity of the Fed's stress test models and called for increased transparency and public comment on the scenarios and supervisory models used in the stress tests.

2. **Inconsistency and Fairness**: They questioned the consistency and fairness of the stress testing process across different types of banking institutions, particularly in light of substantial increases in capital requirements for Intermediate Holding Companies (IHCs).

3. **Volatility in Capital Requirements**: BPI pointed out significant volatility in stress capital buffers, especially for IHCs of foreign banks, which raises concerns about the predictability and stability of capital requirements.

4. **Reliance on Aggregated Models**: The Fed's reliance on aggregated models and recent bank performance in projections was criticized for making it difficult for banks to anticipate and plan for changes in capital requirements.

5. **Excessive Variability**: BPI noted that excessive variability in stress test projections is driven by the Fed's use of backward-looking terms in their revenue models, which often prioritize past performance over macroeconomic scenario variables.

6. **Need for Granularity**: They emphasized the need for more granularity in the Fed's revenue projections to reduce volatility and improve the accuracy of the stress tests.

Overall, BPI argued that these issues hinder the effectiveness of the stress testing framework and negatively impact banks' ability to manage their capital and lending practices.

### 20. `chunk_size_3000_chunk_overlap_50` — F: 1.0000 | AR: 1.0000 | CP: 0.9468

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress testing process, which makes it difficult for banks to anticipate and plan for changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out inaccuracies and excessive volatility in the supervisory stress-testing models used to determine the stress capital buffer, particularly due to the Fed's reliance on aggregated models that assign disproportionate weight to bank performance in the preceding year.

3. **Granularity of Models**: The BPI criticized the Fed for not providing sufficient granularity in their revenue projections, which contributes to excessive variability in capital requirements.

4. **Public Comment and Review**: They suggested that allowing public comment on scenarios and supervisory models would enable extensive review by experts, academics, and banks, thereby increasing transparency and improving model accuracy.

5. **Methodological Changes**: The BPI expressed concerns about the significant increases in capital requirements for intermediate holding companies (IHCs) of foreign banks and the lack of understanding regarding the factors driving these changes due to the Fed's opaque methodology.

Overall, the BPI emphasized the need for increased transparency, predictability, and fairness in the stress testing process to better serve the needs of the U.S. economy.

### 21. `chunk_size_3000_chunk_overlap_100` — F: 1.0000 | AR: 1.0000 | CP: 0.8835

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The BPI highlighted concerns about the opacity of the Fed's stress testing process, which makes it difficult for banks to understand and anticipate changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out the inaccuracies and excessive volatility inherent in the supervisory stress-testing models used to determine the stress capital buffer.

3. **Reliance on Aggregated Models**: The BPI criticized the Fed's reliance on aggregated models that disproportionately weight bank performance from the preceding year, which leads to projections that are heavily influenced by backward-looking data rather than current macroeconomic conditions.

4. **Granularity of Revenue Projections**: They noted that the lack of granularity in the Fed's revenue projections contributes to excessive variability in capital requirements.

5. **Need for Public Comment**: The BPI suggested that allowing public comment on scenarios and supervisory models would enhance transparency and improve model accuracy, ultimately fostering a more effective financial system.

Overall, the BPI expressed that the Fed's methodology raises serious concerns about the consistency, predictability, and fairness of the stress testing process across different types of banking institutions.

### 22. `chunk_size_3000_chunk_overlap_200` — F: 1.0000 | AR: 1.0000 | CP: 0.8957

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress testing process, which makes it difficult for banks to anticipate and plan for changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out inaccuracies and excessive volatility in the supervisory stress-testing models used to determine the stress capital buffer, particularly due to the Fed's reliance on aggregated models that assign disproportionate weight to bank performance in the preceding year.

3. **Granularity of Models**: BPI criticized the Fed for the lack of granularity in their revenue projections, which contributes to excessive variability in stress test projections.

4. **Public Comment on Models**: They suggested that allowing public comment on scenarios and supervisory models would enable extensive review by experts, academics, and banks, thereby increasing transparency and improving model accuracy.

5. **Impact on Capital Requirements**: The substantial increases in capital requirements for intermediate holding companies (IHCs) of foreign banks raised concerns about the consistency and fairness of the stress testing process across different types of banking institutions.

Overall, BPI emphasized the need for improved transparency and more effective modeling to better serve the needs of the U.S. economy.

### 23. `chunk_size_3000_chunk_overlap_300` — F: 1.0000 | AR: 1.0000 | CP: 1.0000

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress testing process, which makes it difficult for banks to anticipate and plan for changes in capital requirements.

2. **Inaccuracies and Volatility**: They pointed out inaccuracies and excessive volatility in the supervisory stress-testing models used to determine the stress capital buffer, particularly due to the Fed's reliance on aggregated models that assign disproportionate weight to bank performance in the preceding year.

3. **Granularity of Models**: The BPI criticized the Fed for insufficient granularity in their revenue projections, which contributes to excessive variability in capital requirements.

4. **Modeling of PPNR**: They specifically noted challenges in the modeling of pre-provision net revenue (PPNR) and its impact on banks' capital requirements, indicating that the Fed's methodology lacks clarity and consistency.

5. **Need for Public Comment**: The BPI suggested that allowing public comment on scenarios and supervisory models would enable extensive review by experts and improve model accuracy, thereby fostering a more effective financial system.

Overall, the BPI's testimony emphasized the need for reforms to enhance the transparency and reliability of the stress testing framework.

### 24. `chunk_size_500_chunk_overlap_100` — F: 0.8667 | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy of Results**: The stress tests produce inaccurate results, failing to project how much a bank's capital would be depleted under severely adverse scenarios. The models perform poorly and yield counterintuitive or nonsensical results that are inconsistent with more accurate bank models and recent market experiences.

2. **Lack of Transparency**: BPI has challenged the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned the Fed for transparency, which has been ignored.

3. **Methodological Changes**: The substantial fluctuations in capital requirements highlighted by the stress test results raise questions about the consistency and fairness of the stress testing process across different types of banking institutions.

4. **Discretionary Changes**: Changes to stress testing scenarios and models are made at the Fed's discretion and are not subject to notice and comment, which limits public accountability.

These criticisms indicate a broader concern about the effectiveness and fairness of the Fed's stress testing framework.

### 25. `chunk_size_500_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy**: The stress tests produce inaccurate results, projecting how much a bank’s capital would be depleted under adverse scenarios poorly. The results are often counterintuitive and inconsistent with more accurate bank models and recent market experiences.

2. **Lack of Transparency**: BPI highlighted concerns about the lack of transparency in the Federal Reserve's stress tests, arguing that the public has a legal right to see, understand, and comment on the Fed’s stress test models.

3. **Volatility in Capital Requirements**: BPI pointed out that there is excess volatility in capital requirements due to the lack of granularity in the Fed's revenue projections, which contributes to significant fluctuations in capital requirements.

4. **Methodological Changes**: The substantial increases in capital requirements for Intermediate Holding Companies (IHCs) raised questions about the consistency and fairness of the stress testing process across different types of banking institutions.

5. **Discretionary Changes**: Changes to stress testing scenarios and models are made at the Fed's discretion and are not subject to notice and comment, which BPI criticized as undermining accountability.

### 26. `chunk_size_1000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccuracy of Results**: The stress tests produce inaccurate results that are often counterintuitive and inconsistent with more granular and accurate bank models and recent market experiences.

2. **Broken Appeals Process**: The appeals process for challenging the results is deemed broken, as nearly every public appeal has been denied with little explanation, and only one appeal was granted in 2024.

3. **Discouragement of Certain Business Lines**: The stress tests discourage certain lines of business, such as mortgages and small business loans, which are treated as riskier and can lead to higher capital requirements due to their close link to the unemployment rate.

4. **Lack of Transparency**: BPI has consistently challenged the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models.

5. **Excessive Volatility in Capital Requirements**: The substantial fluctuations in capital requirements highlighted by the stress test results raise questions about the consistency and predictability of the stress testing process, which could affect banks' ability to manage their capital effectively and impact their lending capacity.

### 27. `chunk_size_1000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Inaccurate Results**: The stress tests produce counterintuitive and sometimes nonsensical results that are inconsistent with more accurate bank models and recent market experiences.

2. **Poor Performance of Models**: The Fed's models are said to perform poorly in projecting how much a bank's capital would be depleted under severely adverse scenarios.

3. **Broken Appeals Process**: The appeals process for challenging the results is described as broken, with nearly every public appeal being denied without sufficient explanation. The Fed only granted an appeal for the first time in 2024.

4. **Discouragement of Certain Business Lines**: The stress tests are said to discourage certain lines of business, such as mortgages and small business loans, which are treated as riskier and can lead to higher capital requirements.

5. **Lack of Transparency**: BPI has challenged the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on them.

6. **Uncertainty Affecting Economic Growth**: The stress test framework creates uncertainty that negatively impacts the economy and U.S. business growth.

7. **Excessive Volatility in Capital Requirements**: The substantial fluctuations in capital requirements highlighted by the stress test results raise questions about the consistency and predictability of the stress testing process, potentially affecting banks' lending capacity and market participation.

### 28. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. Lack of Transparency: BPI highlighted the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models.

2. Inconsistency and Fairness: The substantial increases in capital requirements for Intermediate Holding Companies (IHCs) raised questions about the consistency and fairness of the stress testing process across different types of banking institutions.

3. Volatility in Capital Requirements: BPI pointed out significant volatility in stress capital buffers, particularly for IHCs of foreign banks, which raises concerns about the predictability and fairness of the stress testing process.

4. Reliance on Aggregated Models: The Fed's reliance on aggregated models and recent bank performance in projections of Pre-Provision Net Revenue (PPNR) was criticized for making it difficult for banks to anticipate and plan for changes in capital requirements.

5. Insufficient Steps for Improvement: Although the Fed has taken some steps to improve the granularity of their models, BPI deemed these efforts insufficient to address the underlying issues.

6. Need for Public Comment: BPI emphasized that allowing public comment on scenarios and supervisory models would enable extensive review by experts, academics, and banks, thereby increasing transparency and improving model accuracy. 

Overall, BPI argued that these issues contribute to uncertainty that negatively impacts the economy and U.S. business growth.

### 29. `chunk_size_2000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned the Fed for years to make the stress tests transparent, but their efforts have been ignored.

2. **Inconsistency and Fairness**: The substantial increases in capital requirements for Intermediate Holding Companies (IHCs) raised questions about the consistency and fairness of the stress testing process across different types of banking institutions.

3. **Volatility in Capital Requirements**: The 2024 stress test results revealed significant volatility in stress capital buffers, particularly for IHCs of foreign banks, which raised concerns about the predictability and fairness of the process.

4. **Reliance on Aggregated Models**: The Fed's reliance on aggregated models and recent bank performance in projections of pre-provision net revenue (PPNR) was criticized for making it difficult for banks to anticipate and plan for changes in capital requirements.

5. **Excessive Variability**: BPI noted that excessive variability in stress test projections was a significant issue, stemming from the Fed's reliance on backward-looking terms in their revenue models, which often downplayed macroeconomic scenario variables.

6. **Need for Public Comment**: BPI emphasized that allowing public comment on scenarios and supervisory models would enable extensive review by experts and improve model accuracy, thereby fostering a more effective financial system.

Overall, BPI's criticisms centered on the need for greater transparency, consistency, and predictability in the Fed's stress testing framework.

### 30. `chunk_size_3000_chunk_overlap_100` — F: n/a | AR: n/a | CP: n/a

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: The Fed's stress testing process has been described as obscure, making it difficult for banks to understand the factors driving capital requirements.

2. **Inaccuracies and Volatility**: BPI highlighted the inaccuracies and excessive volatility inherent in the supervisory stress-testing models, particularly in the modeling of pre-provision net revenue (PPNR) and its impact on banks' capital requirements.

3. **Reliance on Aggregated Models**: The Fed's reliance on aggregated models that assign disproportionate weight to bank performance in the preceding year leads to projections that are heavily influenced by backward-looking data, which can create a "momentum" effect.

4. **Increased Capital Requirements**: The 2024 stress test results revealed higher capital depletions under stress scenarios, leading to increased capital requirements for many banks, which BPI argued were driven by lower projections of net revenues.

5. **Need for Public Comment**: BPI emphasized the importance of allowing public comment on scenarios and supervisory models to enhance transparency and improve model accuracy.

6. **Insufficient Steps for Improvement**: Although the Fed has taken some steps to improve the granularity of their models, BPI believes these efforts are insufficient to address the underlying issues in the stress testing process.

### 31. `chunk_size_2000_chunk_overlap_50` — F: n/a | AR: 1.0000 | CP: 0.8951

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Lack of Transparency**: BPI highlighted the opacity of the Fed's stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned the Fed for transparency, which they claim has been ignored.

2. **Inconsistency and Fairness**: The substantial increases in capital requirements for Intermediate Holding Companies (IHCs) raised questions about the consistency and fairness of the stress testing process across different types of banking institutions.

3. **Volatility in Capital Requirements**: BPI pointed out significant volatility in stress capital buffers, particularly for IHCs of foreign banks, which raises concerns about the predictability and stability of the stress testing process.

4. **Reliance on Aggregated Models**: The Fed's reliance on aggregated models and recent bank performance in projections of Pre-Provision Net Revenue (PPNR) was criticized for making it difficult for banks to anticipate and plan for changes in capital requirements.

5. **Excessive Variability**: BPI noted that excessive variability in stress test projections is driven by the Fed's reliance on backward-looking terms in their models, which can distort the accuracy of projections.

6. **Need for Public Comment**: They emphasized that allowing public comment on scenarios and supervisory models would enable expert review and improve model accuracy, fostering a more effective financial system.

Overall, BPI argued that these issues contribute to uncertainty that negatively impacts the economy and U.S. business growth.

### 32. `chunk_size_2000_chunk_overlap_300` — F: n/a | AR: 1.0000 | CP: 0.9583

The BPI raised several criticisms about the Fed's stress test methodology, including:

1. **Opacity and Lack of Transparency**: BPI criticized the Fed for the opaque nature of its stress test models, arguing that the public has a legal right to see, understand, and comment on these models. They have petitioned the Fed for years to make the stress tests transparent, but their efforts have been ignored.

2. **Inconsistency and Fairness**: The BPI highlighted concerns about the consistency and fairness of the stress testing process across different types of banking institutions, particularly in light of significant increases in capital requirements for Intermediate Holding Companies (IHCs).

3. **Volatility in Capital Requirements**: The BPI pointed out that the substantial volatility in stress capital buffers, especially for IHCs of foreign banks, raises serious concerns about the predictability and fairness of the stress testing process.

4. **Reliance on Aggregated Models**: They criticized the Fed's reliance on aggregated models and recent bank performance in Pre-Provision Net Revenue (PPNR) projections, which they argued makes it difficult for banks to anticipate and plan for changes in capital requirements.

5. **Need for Public Comment**: BPI emphasized the importance of allowing public comment on scenarios and supervisory models to enable extensive review by experts, academics, and banks, which would increase transparency and improve model accuracy.

6. **Excessive Variability**: They noted that excessive variability in capital requirements is driven by the lack of granularity in the Fed's revenue projections, which are heavily influenced by backward-looking terms in the models.

Overall, BPI's criticisms focus on the need for greater transparency, consistency, and fairness in the Fed's stress testing methodology to better serve the needs of the U.S. economy.

---

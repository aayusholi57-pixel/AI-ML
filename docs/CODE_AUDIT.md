# Code and Notebook Audit

This audit separates maintained portfolio code from historical learning material.

## Repository inventory

- Python files: 101
- Jupyter notebooks: 118
- The repository keeps the learning archive, so not every file is expected to be production-ready.

## Findings from the focused audit

### Repaired

- Exam RAG: removed import-time API-key failure, model/client side effects, and unstructured startup work. Added validation, deterministic file ordering, cached knowledge-base construction, and a FastAPI interface.
- PyTorch MLP API: removed working-directory assumptions for model weights, added an explicit missing-model response, deterministic dataset generation, and separated training from persistence.
- Empty RAG app: replaced the empty module with a usable FastAPI application.
- Portfolio documentation: added a curated project index and project-specific setup/architecture documentation.
- Dependency boundaries: added dedicated dependency files for the RAG and computer-vision applications.

### Notebook quality signals

The focused notebook review found several historical notebooks containing saved error outputs and empty code cells. Examples included:

- rag_again_full_pipeline.ipynb: 7 saved error outputs and 13 empty code cells
- sentiment_analysis.ipynb: 3 saved error outputs and 15 empty code cells
- Student rags/Exampreparation_RAG.ipynb: 3 saved error outputs and 57 empty code cells
- real_life_gemini_ai_agent.ipynb: 2 empty code cells
- project5.ipynb: a single empty code cell
- cnn/cnn10.ipynb: 9 empty code cells

These are treated as learning artifacts rather than silently rewritten experiments. The curated READMEs point reviewers toward maintained implementations.

## Duplicate/dead-code observations

There are repeated concepts and filenames across the learning archive, including multiple sentiment, RAG, student-analysis, and CNN notebooks. Some small scripts also duplicate introductory exercises. Because notebook-relative paths and imports can depend on the existing layout, wholesale renaming or deletion would be risky without a migration and execution pass.

The portfolio structure therefore promotes the strongest implementations while preserving the original learning evidence.

## Quality policy going forward

New portfolio projects should include:

- clear README and architecture
- explicit dependencies
- deterministic or documented data preparation
- input validation
- tests for important behaviour
- evaluation metrics and limitations
- no secrets or generated local artifacts

# ExamRAG — Vibes UI

## Run

```bash
pip install streamlit
streamlit run app.py
```

## Connect your RAG

Put your existing retrieval + Gemini code in `rag_engine.py`.

The UI expects:

```python
exam_rag(question, mode="explain", k=3)
```

For source cards, return:

```python
{
    "answer": answer,
    "sources": [
        {
            "source": result["source"],
            "page": result["page"],
            "score": result["score"]
        }
        for result in results
    ]
}
```

Modes:
- `explain`
- `short`
- `5-mark`
- `mcq`

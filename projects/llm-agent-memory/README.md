# LLM Agent with Persistent Memory

## Portfolio summary

An agent-engineering project centered on long-term conversational memory. The original Gemini + LangChain notebook remains as the learning/reference implementation, while this folder contains an **offline-first executable SQLite memory harness** that can be tested without an API key.

## Architecture

```text
User
 ↓
Agent harness
 ├── recent context
 └── SQLite memory → keyword retrieval
 ↓
Optional Gemini generation
```

## Execution

```bash
python demo.py
pytest -q
```

The demo stores memories, retrieves relevant context, and reports the stored-message count.

## Evaluation

The execution suite verifies SQLite persistence, relevant-memory retrieval, session isolation, and offline API-key configuration detection. These are **system-behavior tests**, not fabricated LLM quality scores.

Live generation quality should be evaluated separately with a labeled task set and a provider/API key.

## Live Gemini path

The historical `real_life_gemini_ai_agent.ipynb` contains the Gemini + LangChain implementation. Keep `GOOGLE_API_KEY` in the environment only; never commit secrets.

## Engineering focus

- Agent harness design
- Long-term memory
- SQLite persistence
- Retrieval tools
- Session isolation
- Offline testability
- Optional LLM integration

## Limitation

The current local retrieval layer is keyword based. For large archives, a production version should add FTS5 and/or semantic embeddings, then measure retrieval recall and downstream answer quality on a fixed evaluation set.

## LinkedIn framing

**Built an offline-testable LLM agent memory layer with SQLite persistence, session isolation, relevant-memory retrieval, and an optional Gemini/LangChain integration path. Added executable demos and CI tests so the system is demonstrable without relying on an API key.**

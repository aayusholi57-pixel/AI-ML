# LLM Agent with Persistent Memory

## Portfolio summary

An AI-agent experiment exploring tool use, conversational memory, SQLite persistence, and Gemini integration through LangChain and LangGraph.

## Architecture

User → Agent → Gemini
              ↓
        Memory tools
              ↓
            SQLite

The design separates recent conversation context from persisted notes and tasks.

## Engineering focus

- LLM application architecture
- Agent tool calling
- Persistent memory
- SQLite data access
- LangChain / LangGraph
- Environment-based API credentials

## Security note

Credentials must be supplied through environment variables. Historical notebooks are learning artifacts and should never contain real API keys.

## Recommended LinkedIn framing

**Built an LLM agent prototype with Gemini, LangChain/LangGraph, tool calling, and SQLite-backed memory. Explored how agents can retrieve and update persistent user context without sending an entire conversation history on every request.**

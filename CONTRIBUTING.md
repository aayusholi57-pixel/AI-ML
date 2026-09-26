# Contributing

Thanks for taking an interest in this AI/ML portfolio.

## Development workflow

1. Create a focused branch from `main`.
2. Keep changes scoped to one feature, bug fix, or documentation improvement.
3. Use Python 3.10+.
4. Add or update tests for behaviour that can be verified automatically.
5. Run the relevant project test suite and Ruff locally.
6. Update project documentation when commands, interfaces, or limitations change.
7. Open a pull request with a concise description of the problem, solution, and validation performed.

## Local quality checks

```bash
pytest tests/test_api.py -q
ruff check model.py route.py servermodel.py tests
```

For project-specific work, follow the dependency and test instructions in that project's README.

## Commit guidance

Prefer small, descriptive commits such as:

- `feat: add inference endpoint`
- `fix: validate model input`
- `test: cover retrieval ranking`
- `docs: clarify setup instructions`

Do not commit secrets, local databases, virtual environments, model checkpoints, or generated caches.

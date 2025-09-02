# 🚀 riil-py

**Lightweight, extensible AI workflow engine**  
Build and run AI pipelines with clean architecture, schema enforcement, and resilience.

> Inspired by [`FellouAI/eko`](https://github.com/FellouAI/eko), but designed for **Python-first**, **production-ready** AI workflows.

---

## 📁 Project Structure
```shell
riil-ai/
├── riil/
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── step.py
│   │   ├── workflow.py
│   │   ├── prompt.py
│   │   └── types.py
│   │
│   ├── usecases/
│   │   └── execute_workflow.py
│   │
│   ├── infrastructure/
│   │   ├── llms/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── openai.py
│   │   │   └── resolver.py
│   │   │
│   │   └── utils/
│   │       └── json_repair.py
│   │
│   └── interface/
│       └── cli.py
│
├── config/
│   └── rules/
│       └── default.md
│
├── tests/
│   ├── test_domain/
│   │   ├── test_step.py
│   │   ├── test_workflow.py
│   │   └── test_prompt.py
│   ├── test_infrastructure/
│   │   ├── test_openai.py
│   │   └── test_json_repair.py
│   └── conftest.py
│
├── pyproject.toml
├── README.md
└── .env.example
```


### 🔍 Layered Design (Clean Architecture)
- **`domain`**: Pure logic, no external dependencies
- **`usecases`**: Application workflows
- **`infrastructure`**: LLMs, utilities, external services
- **`interface`**: CLI entry point

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/pace-noge/riil-ai.git
cd rill-ai
```

### 2. Install Dependencies
We use Poetry for dependency management.

```bash
# Install poetry (if not installed)
pip install poetry

# Install dependencies
poetry install
```

### 3. Set Up Environment
Copy the example .env file and add your OpenAI API key.
```shell
cp .env.example .env
```

Edit .env
```shell
OPENAI_API_KEY=sk-your-actual-key-here
```

## 🧪 Running Tests
We use pytest with 90%+ coverage.
```shell
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Run specific test
poetry run pytest tests/test_infrastructure/test_openai.py
```

- ✅ Current coverage: 92%
- ✅ Tested features:
     - Workflow orchestration
     - Step execution
     - JSON repair
     - Schema validation
     - Retry logic
## 🚀 Usage
Run the Example Workflow
```shell
poetry run riil run-joke --topic="Python"
```
This runs:

```shell
"Tell me a joke about {topic}" → OpenAI → Output
```

You’ll see a real AI-generated joke.
___

## 🏗️ Core Features
| FEATURE | STATUS |
|---------| ------- |
|✅ Async execution | Built-in |
|✅ Prompt templating | {{var}} syntax |
|✅ Schema enforcement | Pydantic models |
|✅ JSON repair | Auto-fix malformed output |
| ✅ Retry on parse error | Configurable |
| ✅ Extensible LLMs | Open/Closed Principle |
|✅ Rule injection (future) | Ready for M2 |
|✅ Config-driven workflows | Ready for M2 |
___

## 🎯 Milestones & Achievements
✅ M1: Core Workflow Engine (CLI-Only)

`Run AI workflows without web bloat`

Achieved:
- Clean Architecture layers
- SOLID-compliant design
- Async Workflow engine
- OpenAIStep with schema, repair, retry
- CLI interface (riil run-joke)
- Unit tests (90%+ coverage)
- Future-ready for rules, RAG, FastAPI

Deliverables:
- Fully working core engine
- No external API keys required for testing (mock-ready)
- Extensible via register_step_type()
___

## 🔮 Future Roadmap

| MILESTONE | GOAL |
|-----------|------|
| M2 | Configurable workflows (YAML/JSON) |
| M3 | Streaming & real-time output |
| M4 | Rule system (role/tone/format presets) |
| M5 | FastAPI integration |
|M6 | RAG support (document → answer) |
|M7 |Event-driven workflows (callbacks, observability) |
___

## 📜 License
MIT
___
## 🤝 Contributing
1. Fork the repo
2. Create your feature branch (git checkout -b feat/my-feature)
3. Commit your changes (git commit -m 'feat: add my feature')
4. Push to the branch (git push origin feat/my-feature)
5. Open a Pull Request
6. See CONTRIBUTING.md for details.
___

## 🙏 Acknowledgments
- Inspired by FellouAI/eko
- Built with Python, Pydantic, OpenAI, and clean design principles
- Designed for extensibility and production use

___
>"riil-ai: Where AI workflows are simple, robust, and future-proof."

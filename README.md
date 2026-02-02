# SMART: Strategic Multi-Agent Red Teaming Framework

![SMART Architecture Diagram](./architecture.png)

## Introduction

**SMART** (Strategic Multi-Agent Red Teaming) is an autonomous adversarial framework designed to evaluate the safety and robustness of Large Language Models (LLMs). 

Unlike traditional "brute-force" red teaming tools that rely on static templates, SMART utilizes a **feedback-driven evolutionary engine**. It treats prompt injection as an optimization problem, employing a multi-agent system to plan, retrieve, attack, and—crucially—**mutate** attack strategies based on real-time defense feedback from the target model.

This project demonstrates a neuro-symbolic approach to AI safety, combining retrieval-augmented generation (RAG) with episodic memory to automate the discovery of "jailbreak" vectors in modern LLMs.

The ultimate goal of this project is beyond red teaming. It's automated prompt enhancing for every task.

## Test Results
Mainsteam 14b and less LLMs, including Llama3.2, Qwen3 and DeepSeek R1, takes up to 8 rounds. Larger models to be tested.

## System Architecture

The system follows a cyclic **Agentic Workflow**:

1.  **Strategist**: Analyzes the user's intent (e.g., "How to make X") and generates semantic search queries.
2.  **Assembler**: Retrieves templates from the Vector DB and intelligently embeds the payload using an LLM to ensure grammatical coherence.
3.  **Defender (Target)**: The local LLM under test (via Ollama) processes the prompt.
4.  **Judge**: Evaluates the response for harmful content.
5.  **Mutator (The Loop)**: If the attack fails, this agent reads the Judge's feedback and the session history to generate a novel, mutated prompt for the next round.

## Getting Started

### Prerequisites
* [Ollama](https://ollama.com/) installed and running locally.
* A Google AI Studio API Key (for Gemini).

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/emofun0/SMART-Red-Teaming.git
    cd SMART-Red-Teaming/
    ```

2.  **Install dependencies**
    ```bash
    conda create -n SMART python=3.12
    conda activate SMART
    pip install -r requirements.txt
    ```
    After that, create a .env file, and put your API key in it.
    ```
    GOOGLE_API_KEY=Your_Google_API_Key
    ```

3.  **Run the script**
    ```bash
    python main.py "Your malicious intent"
    ```
    Optional env vars: `TARGET_MODEL`, `OLLAMA_BASE_URL`, `MAX_ROUNDS`, `DB_PATH`, `LOG_FILE`, `RETRIEVAL_TOP_K`.

### Project Structure

```
smart/
  config.py           # AttackConfig, env loading
  models.py            # StrategyOutput, JudgeResult, AttemptRecord, RetrievedTemplate
  clients/             # LLM & target clients
    gemini_client.py   # GeminiLLMClient
    ollama_client.py   # OllamaTargetClient
  memory/
    vector_store.py   # JailbreakVectorStore (ChromaDB)
  agents/              # One class per agent
    strategist.py     # StrategistAgent
    assembler.py      # AssemblerAgent
    judge.py          # JudgeAgent
    mutator.py        # MutatorAgent
  workflow/
    orchestrator.py   # AttackOrchestrator (agentic loop)
  utils/
    session_logger.py # SessionLogger
main.py               # Entry: AttackOrchestrator().run(intent)
prebuilt_jailbreak_db.py  # Build vector DB (uses smart.config)
```

Layers are decoupled: config and models are shared; agents depend only on `GeminiLLMClient` and data types; the orchestrator wires agents, target client, and vector store into the attack workflow.

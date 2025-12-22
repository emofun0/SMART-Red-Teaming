# SMART: Strategic Multi-Agent Red Teaming Framework

![SMART Architecture Diagram](./architecture.png)

## Introduction

**SMART** (Strategic Multi-Agent Red Teaming) is an autonomous adversarial framework designed to evaluate the safety and robustness of Large Language Models (LLMs). 

Unlike traditional "brute-force" red teaming tools that rely on static templates, SMART utilizes a **feedback-driven evolutionary engine**. It treats prompt injection as an optimization problem, employing a multi-agent system to plan, retrieve, attack, and—crucially—**mutate** attack strategies based on real-time defense feedback from the target model.

This project demonstrates a neuro-symbolic approach to AI safety, combining retrieval-augmented generation (RAG) with episodic memory to automate the discovery of "jailbreak" vectors in modern LLMs.

The ultimate goal of this project is beyond red teaming. It's automated prompt enhancing for every task.

## Test Results
Mainsteam 8b and less LLMs, including Llama3.2 and Qwen3, takes up to 8 rounds. Larger models to be tested.

## System Architecture

The system follows a cyclic **Agentic Workflow**:

1.  **Strategist**: Analyzes the user's intent (e.g., "How to make X") and generates semantic search queries.
2.  **Assembler**: Retrieves templates from the Vector DB and intelligently embeds the payload using an LLM to ensure grammatical coherence.
3.  **Defender (Target)**: The local LLM under test (via Ollama) processes the prompt.
4.  **Judge**: Evaluates the response for harmful content.
5.  **Mutator (The Loop)**: If the attack fails, this agent reads the Judge's feedback and the session history to generate a novel, mutated prompt for the next round.

## Getting Started

### Prerequisites
* Python 3.8+
* [Ollama](https://ollama.com/) installed and running locally.
* A Google AI Studio API Key (for Gemini).

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/emofun0/SMART-Red-Teaming.git](https://github.com/emofun0/SMART-Red-Teaming.git)
    ```

2.  **Install dependencies**
    ```bash
    conda create -n SMART python=3.12
    conda activate SMART
    pip install -r requirements.txt
    ```

3.  **Run the script**
    ```bash
    python main.py
    ```
    
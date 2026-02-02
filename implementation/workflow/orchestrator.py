"""Agentic attack workflow: Strategist -> RAG -> Target -> Judge -> Mutator loop."""

from typing import Optional

from implementation.agents import AssemblerAgent, JudgeAgent, MutatorAgent, StrategistAgent
from implementation.clients import GeminiLLMClient, OllamaTargetClient
from implementation.config import AttackConfig
from implementation.memory import JailbreakVectorStore
from implementation.models import AttemptRecord
from implementation.utils import SessionLogger


class AttackOrchestrator:
    """
    Orchestrates the full attack workflow:
    1. Strategist: intent -> search keywords
    2. Vector store: keywords -> templates
    3. Assembler: template + intent -> final prompt
    4. Target (Ollama): prompt -> response
    5. Judge: (prompt, response) -> score
    6. On failure: Mutator (intent + history) -> new prompt, repeat until success or max_rounds
    """

    def __init__(self, config: Optional[AttackConfig] = None):
        self._config = config or AttackConfig.from_env()
        self._llm = GeminiLLMClient()
        self._target = OllamaTargetClient(self._config)
        self._store = JailbreakVectorStore(self._config)
        self._logger = SessionLogger(self._config)
        self._strategist = StrategistAgent(self._llm)
        self._assembler = AssemblerAgent(self._llm)
        self._judge = JudgeAgent(self._llm)
        self._mutator = MutatorAgent(self._llm)

    def run(self, intent: str) -> None:
        """Run full attack for given malicious intent. Logs and prints progress."""
        self._logger.start_session()
        print(f"\nTarget Intent: {intent}")
        print("=" * 60)

        mutation_history: list[AttemptRecord] = []

        # Phase 1: Strategist
        print("\nStrategist is thinking...")
        strategy = self._strategist.run(intent)
        print(f"   Thought: {strategy.thought}")
        print(f"   Keywords: [{strategy.search_keywords}]")

        # Phase 2: Retrieve templates
        print("Searching DB...")
        templates = self._store.search(strategy.search_keywords)
        if not templates:
            print("No templates found. Exiting.")
            return

        best_prompt: Optional[str] = None
        best_reason = "Initial retrieval failed"

        # Phase 3: Try each template
        for i, item in enumerate(templates):
            print(f"Attempt {i+1} (Type: {item.name})")
            final_prompt = self._assembler.run(item.document, intent)
            target_res = self._target.generate(final_prompt)
            eval_res = self._judge.run(final_prompt, target_res)
            self._logger.log_attempt(
                f"DB Template {i+1} ({item.name})",
                final_prompt,
                target_res,
                eval_res,
            )
            mutation_history.append(AttemptRecord(prompt=final_prompt, reason=eval_res.reason))
            if eval_res.score == 1:
                print("\nBREAKTHROUGH ACCOMPLISHED!")
                return
            best_prompt = final_prompt
            best_reason = eval_res.reason

        print("\nAll initial strategies failed.")
        current_prompt = best_prompt
        current_reason = best_reason

        # Phase 4: Mutation loop
        for round_num in range(self._config.max_rounds):
            print("-" * 50 + f"\nRound {round_num + 1}/{self._config.max_rounds} Mutating...", end=" ")
            mutated_prompt = self._mutator.run(intent, mutation_history)
            target_res = self._target.generate(mutated_prompt)
            eval_res = self._judge.run(mutated_prompt, target_res)
            self._logger.log_attempt(
                f"Mutation Round {round_num+1}",
                mutated_prompt,
                target_res,
                eval_res,
            )
            mutation_history.append(AttemptRecord(prompt=mutated_prompt, reason=eval_res.reason))
            if eval_res.score == 1:
                print("\nMUTATION SUCCESS!")
                return

        print("\nTarget is robust. Mutation failed.")

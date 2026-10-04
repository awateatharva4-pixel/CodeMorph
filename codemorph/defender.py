import os
import ast
from typing import Optional, List
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class VivaQuestion(BaseModel):
    id: int
    question: str = Field(description="The brutal technical interview question.")
    target_concept: str = Field(description="The underlying concept being tested (e.g. AST recursion depth, Big-O complexity).")
    model_answer: str = Field(description="The ideal, high-scoring answer a student should say to the professor or interviewer.")

class VivaEvaluation(BaseModel):
    score: int = Field(ge=0, le=10, description="Score from 0 to 10.")
    feedback: str = Field(description="Honest critique of what the student got right and wrong.")
    refined_answer: str = Field(description="How to phrase the answer for maximum points.")

class CodeDefender:
    """The Adversarial Code Defense & Viva Coach. Prepares developers to defend their codebase under brutal technical grilling."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def generate_defense_questions(self, code_content: str, filename: str) -> List[VivaQuestion]:
        """Analyzes code and generates the 3 most aggressive technical questions a professor or recruiter would ask."""
        if not self.client:
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                raise ValueError("GEMINI_API_KEY not configured.")
            self.client = genai.Client(api_key=key)

        prompt = f"""
You are an adversarial computer science professor and senior compiler engineer conducting an oral viva / technical defense.
The student claims they wrote this file: `{filename}`.

Inspect the code and generate the 3 MOST PROBING, BRUTAL technical questions to test whether the student truly understands the underlying computer science, data structures, and trade-offs, or whether they just copy-pasted from an AI.

Focus on:
1. Abstract Syntax Tree (AST) node traversal mechanics.
2. Big-O time and space complexity bottlenecks.
3. Edge cases, stack overflows, and memory trade-offs.

[CODE CONTENT]
```python
{code_content}
```
"""
        class VivaBatch(BaseModel):
            questions: List[VivaQuestion]

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VivaBatch,
                temperature=0.3,
            )
        )
        batch = VivaBatch.model_validate_json(response.text)
        return batch.questions

    def grade_student_answer(self, question: VivaQuestion, student_answer: str) -> VivaEvaluation:
        """Evaluates student's answer and provides feedback + ideal phrasing."""
        if not self.client:
            key = os.environ.get("GEMINI_API_KEY")
            self.client = genai.Client(api_key=key)

        prompt = f"""
You are evaluating a student's answer during a technical oral exam.

[QUESTION]
{question.question}

[TARGET CONCEPT]
{question.target_concept}

[MODEL ANSWER]
{question.model_answer}

[STUDENT'S ANSWER]
"{student_answer}"

Grade the student's answer strictly from 0 to 10.
Be honest and direct. Point out misconceptions. Give them the exact phrasing they should use to sound like a senior engineer.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VivaEvaluation,
                temperature=0.2,
            )
        )
        return VivaEvaluation.model_validate_json(response.text)

import os
import ast
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from codemorph.models import DeveloperDNA

class TranspileResult(BaseModel):
    transformed_code: str = Field(description="The code restyled to match the target DeveloperDNA stylometrics.")
    changes_made: list[str] = Field(description="List of specific transformations applied (e.g. unpacked list comprehension, removed type annotations).")

class CodeTransformer:
    """Restyles input code to match a target DeveloperDNA signature using AST-guided synthesis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def transform_code(self, source_code: str, dna: DeveloperDNA) -> Optional[TranspileResult]:
        """Transforms source code to match the target DeveloperDNA profile."""
        if not self.client:
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                raise ValueError("GEMINI_API_KEY not found in environment or arguments.")
            self.client = genai.Client(api_key=key)

        prompt = f"""
You are CodeMorph, an expert compiler and AST stylometric transpiler.
Transform the following SOURCE CODE so that its syntactic and structural patterns match the TARGET DEVELOPER DNA.

[TARGET DEVELOPER DNA]
- Average Variable Name Length: {dna.avg_var_name_length} characters
- Single-letter Variables Ratio (e.g. i, j, x): {int(dna.single_letter_var_ratio * 100)}%
- Snake_case vs CamelCase: {int(dna.snake_case_ratio * 100)}% snake_case, {int(dna.camel_case_ratio * 100)}% camelCase
- List Comprehensions vs Loops: {int(dna.comprehension_vs_loop_ratio * 100)}% comprehensions. (If low, unpack into standard for-loops with .append()).
- Type Annotations Ratio: {int(dna.type_annotation_ratio * 100)}% (If 0%, strip all type hints).
- Docstring Ratio: {int(dna.docstring_ratio * 100)}% (If 0%, remove formal multi-line docstrings).
- Comment Density: {int(dna.comment_density * 100)}% of lines should have brief, casual comments.
- Prefers Intermediate Variables: {dna.prefers_intermediate_variables} (Break down dense inlined expressions into procedural scratchpad variables).

[MANDATORY CONSTRAINTS]
1. ZERO FUNCTIONAL DIVERGENCE: The transformed code must produce 100% identical outputs for any valid input.
2. The code must be valid, executable Python syntax.
3. Do NOT make it look like a caricature or add intentional syntax bugs. Make it look like an authentic human engineer wrote it with their specific coding habits.

[SOURCE CODE]
```python
{source_code}
```
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TranspileResult,
                    temperature=0.2,
                )
            )
            result = TranspileResult.model_validate_json(response.text)

            # Sanity check: Ensure transformed code parses as valid Python AST
            ast.parse(result.transformed_code)
            return result
        except SyntaxError:
            return None
        except Exception:
            return None

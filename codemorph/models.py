from pydantic import BaseModel, Field
from typing import Dict, Any, List

class DeveloperDNA(BaseModel):
    developer_name: str = "Anonymous"
    sample_files_analyzed: int = 0
    total_lines_analyzed: int = 0
    
    # Naming Metrics
    avg_var_name_length: float = Field(default=0.0, description="Average character length of variable identifiers")
    single_letter_var_ratio: float = Field(default=0.0, description="Percentage of variables that are 1 character (e.g. i, j, x)")
    snake_case_ratio: float = Field(default=0.0, description="Percentage of snake_case identifiers")
    camel_case_ratio: float = Field(default=0.0, description="Percentage of camelCase identifiers")
    
    # Control Flow & Complexity
    max_nesting_depth: int = Field(default=0, description="Maximum observed nesting depth of control flow")
    avg_nesting_depth: float = Field(default=0.0, description="Average nesting depth across functions")
    comprehension_vs_loop_ratio: float = Field(default=0.0, description="Ratio of list/dict comprehensions to traditional for-loops")
    while_vs_for_ratio: float = Field(default=0.0, description="Ratio of while-loops to for-loops")
    
    # Typing & Structure
    type_annotation_ratio: float = Field(default=0.0, description="Percentage of function signatures with type hints")
    docstring_ratio: float = Field(default=0.0, description="Percentage of functions containing docstrings")
    comment_density: float = Field(default=0.0, description="Ratio of comment lines to executable code lines")
    
    # Behavioral Flags
    prefers_guard_clauses: bool = Field(default=False, description="Whether the developer prefers early returns over nested if-blocks")
    prefers_intermediate_variables: bool = Field(default=True, description="Whether the developer introduces scratchpad variables instead of inlining")

import ast
import re
from pathlib import Path
from typing import List, Optional

from codemorph.models import DeveloperDNA

class ASTStylometricVisitor(ast.NodeVisitor):
    """Walks the Abstract Syntax Tree and extracts granular stylometric statistics."""

    def __init__(self):
        self.var_names: List[str] = []
        self.for_count = 0
        self.while_count = 0
        self.comprehension_count = 0
        self.func_count = 0
        self.typed_func_count = 0
        self.docstring_count = 0
        self.current_depth = 0
        self.max_observed_depth = 0
        self.depth_samples: List[int] = []

    def visit(self, node):
        is_block = isinstance(node, (ast.For, ast.While, ast.If, ast.With, ast.Try, ast.FunctionDef, ast.ClassDef))
        if is_block:
            self.current_depth += 1
            if self.current_depth > self.max_observed_depth:
                self.max_observed_depth = self.current_depth
            self.depth_samples.append(self.current_depth)

        super().visit(node)

        if is_block:
            self.current_depth -= 1

    def visit_Name(self, node: ast.Name):
        # We only count store/parameter names, not built-in load names like print/len
        if isinstance(node.ctx, (ast.Store, ast.Param)):
            self.var_names.append(node.id)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.for_count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.while_count += 1
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        self.comprehension_count += 1
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp):
        self.comprehension_count += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.func_count += 1
        # Check for type annotations
        has_returns = node.returns is not None
        has_arg_types = any(arg.annotation is not None for arg in node.args.args)
        if has_returns or has_arg_types:
            self.typed_func_count += 1

        # Check for docstring
        if ast.get_docstring(node):
            self.docstring_count += 1

        self.generic_visit(node)


class CodeProfiler:
    """Profiles a collection of code files to build a DeveloperDNA profile."""

    def __init__(self, developer_name: str = "Atharva"):
        self.developer_name = developer_name

    def profile_files(self, file_paths: List[Path]) -> DeveloperDNA:
        visitor = ASTStylometricVisitor()
        total_lines = 0
        total_comments = 0
        valid_files = 0

        for path in file_paths:
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue

            lines = content.splitlines()
            total_lines += len(lines)
            total_comments += sum(1 for line in lines if line.strip().startswith("#"))

            try:
                tree = ast.parse(content)
                visitor.visit(tree)
                valid_files += 1
            except SyntaxError:
                continue

        # Compute metrics
        vars_count = len(visitor.var_names)
        avg_len = sum(len(v) for v in visitor.var_names) / vars_count if vars_count > 0 else 0.0
        single_letter = sum(1 for v in visitor.var_names if len(v) == 1) / vars_count if vars_count > 0 else 0.0

        # Casing ratios
        snake_case = sum(1 for v in visitor.var_names if "_" in v or v.islower()) / vars_count if vars_count > 0 else 0.0
        camel_case = sum(1 for v in visitor.var_names if re.match(r"^[a-z]+(?:[A-Z][a-z0-9]*)+$", v)) / vars_count if vars_count > 0 else 0.0

        total_loops = visitor.for_count + visitor.while_count
        comp_ratio = visitor.comprehension_count / total_loops if total_loops > 0 else 0.0
        while_ratio = visitor.while_count / visitor.for_count if visitor.for_count > 0 else 0.0

        typed_ratio = visitor.typed_func_count / visitor.func_count if visitor.func_count > 0 else 0.0
        doc_ratio = visitor.docstring_count / visitor.func_count if visitor.func_count > 0 else 0.0
        avg_depth = sum(visitor.depth_samples) / len(visitor.depth_samples) if visitor.depth_samples else 0.0

        return DeveloperDNA(
            developer_name=self.developer_name,
            sample_files_analyzed=valid_files,
            total_lines_analyzed=total_lines,
            avg_var_name_length=round(avg_len, 2),
            single_letter_var_ratio=round(single_letter, 2),
            snake_case_ratio=round(snake_case, 2),
            camel_case_ratio=round(camel_case, 2),
            max_nesting_depth=visitor.max_observed_depth,
            avg_nesting_depth=round(avg_depth, 2),
            comprehension_vs_loop_ratio=round(comp_ratio, 2),
            while_vs_for_ratio=round(while_ratio, 2),
            type_annotation_ratio=round(typed_ratio, 2),
            docstring_ratio=round(doc_ratio, 2),
            comment_density=round(total_comments / max(1, total_lines), 2)
        )

import os
import sys
import json
from pathlib import Path
from typing import Optional, List

# Windows console UTF-8 support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt

from codemorph.profiler import CodeProfiler
from codemorph.models import DeveloperDNA
from codemorph.transformer import CodeTransformer
from codemorph.defender import CodeDefender

app = typer.Typer(
    name="codemorph",
    help="🧬 AST-Driven Stylometric Transpiler & Developer Signature Emulator",
    add_completion=False
)
console = Console()

BANNER = r"""[bold magenta]
   ______          __        __  ___                 __  
  / ____/____  ___/ /___    /  |/  /____   _____ ____   / /_ 
 / /    / __ \/ __  // _ \  / /|_/ // __ \ / ___// __ \ / __ \
/ /___ / /_/ // /_/ //  __/ / /  / // /_/ // /   / /_/ // / / /
\____/ \____/ \__,_/ \___/ /_/  /_/ \____//_/   / .___//_/ /_/ 
                                               /_/             
[/bold magenta]
[bold white]AST-Driven Stylometric Transpiler & Code Defense Engine[/bold white]
"""

@app.command()
def profile(
    path: str = typer.Argument(..., help="Path to a file or directory containing your past code samples"),
    name: str = typer.Option("Atharva", "--name", "-n", help="Developer name"),
    output: str = typer.Option("developer_dna.json", "--output", "-o", help="Output JSON path"),
):
    """Analyze code samples using AST heuristics and generate a DeveloperDNA stylometric profile."""
    console.print(BANNER)
    target = Path(path).resolve()

    if target.is_file():
        files = [target]
    else:
        files = list(target.rglob("*.py"))

    if not files:
        console.print(f"[bold red]No Python files found in {target}[/bold red]")
        raise typer.Exit(code=1)

    console.print(f"[bold cyan]▶ Analyzing {len(files)} file(s) for developer '{name}'...[/bold cyan]\n")

    profiler = CodeProfiler(developer_name=name)
    dna = profiler.profile_files(files)

    # Save to disk
    out_path = Path(output)
    out_path.write_text(dna.model_dump_json(indent=2), encoding="utf-8")

    # Render metrics table
    table = Table(title=f"🧬 Developer DNA: {dna.developer_name}", show_header=True, header_style="bold magenta")
    table.add_column("Stylometric Metric", style="cyan")
    table.add_column("Observed Value", style="bold green", justify="right")

    table.add_row("Total Lines Analyzed", str(dna.total_lines_analyzed))
    table.add_row("Avg Variable Name Length", f"{dna.avg_var_name_length} chars")
    table.add_row("Single-Letter Variables Ratio", f"{int(dna.single_letter_var_ratio * 100)}%")
    table.add_row("Snake_case vs CamelCase", f"{int(dna.snake_case_ratio * 100)}% / {int(dna.camel_case_ratio * 100)}%")
    table.add_row("Max / Avg Nesting Depth", f"{dna.max_nesting_depth} / {dna.avg_nesting_depth}")
    table.add_row("Comprehension vs Loop Ratio", f"{int(dna.comprehension_vs_loop_ratio * 100)}%")
    table.add_row("Type Annotation Coverage", f"{int(dna.type_annotation_ratio * 100)}%")
    table.add_row("Docstring Coverage", f"{int(dna.docstring_ratio * 100)}%")
    table.add_row("Comment Density", f"{int(dna.comment_density * 100)}% of lines")

    console.print(table)
    console.print(f"\n[bold green]✔ Developer DNA saved to:[/bold green] [underline]{out_path.resolve()}[/underline]\n")

@app.command()
def morph(
    input_file: str = typer.Argument(..., help="Path to input code file to transform"),
    dna_file: str = typer.Option("developer_dna.json", "--dna", "-d", help="Path to DeveloperDNA JSON"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Path to save morphed code"),
):
    """Transpile source code to match the stylometric signature in DeveloperDNA."""
    console.print(BANNER)
    in_path = Path(input_file).resolve()
    dna_path = Path(dna_file).resolve()

    if not in_path.exists():
        console.print(f"[bold red]Input file not found: {in_path}[/bold red]")
        raise typer.Exit(code=1)

    if not dna_path.exists():
        console.print(f"[bold red]DeveloperDNA profile not found at {dna_path}. Run 'codemorph profile' first.[/bold red]")
        raise typer.Exit(code=1)

    dna = DeveloperDNA.model_validate_json(dna_path.read_text(encoding="utf-8"))
    source_code = in_path.read_text(encoding="utf-8")

    console.print(f"[bold cyan]▶ Morphing '{in_path.name}' to match signature of '{dna.developer_name}'...[/bold cyan]\n")

    transformer = CodeTransformer()
    result = transformer.transform_code(source_code, dna)

    if not result:
        console.print("[bold red]✖ Failed to transpile code while maintaining AST validity.[/bold red]")
        raise typer.Exit(code=1)

    console.print(Panel(
        "\n".join(f"• {change}" for change in result.changes_made),
        title="✨ Applied Stylometric Transformations",
        border_style="green"
    ))

    console.print(Panel(
        Syntax(result.transformed_code, "python", theme="monokai", line_numbers=True),
        title=f"Transpiled Code ({in_path.name})",
        border_style="magenta"
    ))

    if output:
        out_path = Path(output).resolve()
        out_path.write_text(result.transformed_code, encoding="utf-8")
        console.print(f"[bold green]✔ Saved to {out_path}[/bold green]")

@app.command()
def defend(
    file: str = typer.Argument(..., help="Path to code file you need to defend"),
):
    """Launch the Adversarial Viva Coach to practice defending your code."""
    console.print(BANNER)
    target_file = Path(file).resolve()

    if not target_file.exists():
        console.print(f"[bold red]File not found: {target_file}[/bold red]")
        raise typer.Exit(code=1)

    code_content = target_file.read_text(encoding="utf-8")

    console.print(Panel(
        f"[bold red]⚠ ADVERSARIAL ORAL EXAM ACTIVATED[/bold red]\n"
        f"You are defending: [bold cyan]{target_file.name}[/bold cyan]\n"
        f"The examiner will ask 3 brutal technical questions. Answer honestly.",
        border_style="red"
    ))

    defender = CodeDefender()
    questions = defender.generate_defense_questions(code_content, target_file.name)

    total_score = 0
    for q in questions:
        console.print(f"\n[bold yellow]Q{q.id}: {q.question}[/bold yellow]")
        console.print(f"[dim]Tested Concept: {q.target_concept}[/dim]\n")

        answer = Prompt.ask("[bold green]Your Answer[/bold green]")
        evaluation = defender.grade_student_answer(q, answer)

        color = "green" if evaluation.score >= 7 else "yellow" if evaluation.score >= 4 else "red"
        console.print(f"\n[bold {color}]Score: {evaluation.score}/10[/{color}]")
        console.print(f"[bold]Feedback:[/bold] {evaluation.feedback}")
        console.print(Panel(evaluation.refined_answer, title="🎓 How to Phrase in Viva", border_style="cyan"))
        total_score += evaluation.score

    avg = total_score / len(questions)
    console.print(f"\n[bold magenta]━━━━━━━━ Final Viva Score: {avg:.1f} / 10 ━━━━━━━━[/bold magenta]")

if __name__ == "__main__":
    app()

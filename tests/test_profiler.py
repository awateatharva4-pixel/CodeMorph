import ast
from pathlib import Path
from codemorph.profiler import CodeProfiler

def test_profiler_metrics(tmp_path: Path):
    sample = tmp_path / "sample.py"
    sample.write_text("""
# This is a sample calculation
def calculate_score(vals):
    total = 0
    for v in vals:
        if v > 10:
            total += v
    return total
""".strip(), encoding="utf-8")

    profiler = CodeProfiler(developer_name="TestUser")
    dna = profiler.profile_files([sample])

    assert dna.developer_name == "TestUser"
    assert dna.total_lines_analyzed > 0
    assert dna.max_nesting_depth >= 2
    assert dna.type_annotation_ratio == 0.0  # no type annotations in sample
    assert dna.comprehension_vs_loop_ratio == 0.0  # used for loop, not listcomp
    assert dna.comment_density > 0.0

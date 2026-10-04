<div align="center">

# 🧬 CodeMorph

### AST-Driven Stylometric Transpiler & Developer Signature Emulator

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![AST Analysis](https://img.shields.io/badge/engine-Abstract%20Syntax%20Tree-magenta.svg)](https://docs.python.org/3/library/ast.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CodeMorph** is a compiler and stylometric research engine that extracts a developer's unique syntactic signature and cognitive flow via Abstract Syntax Tree (AST) heuristics—and **transpiles foreign or AI-generated code to match their exact authentic programming DNA**.

[Quickstart](#-quickstart) • [How It Works](#-how-it-works) • [Commands](#-cli-commands) • [Adversarial Viva Defense](#-adversarial-code-defense)

---

</div>

## 🔬 The Science: Stylometric Fingerprinting
Every developer has an unmistakable subconscious syntax signature:
- **Identifier Morphology:** Average variable length, preference for single-letter indexing (`i`, `j`, `n`), and casing ratios.
- **Control Flow Topology:** Cyclomatic complexity, max nesting depth, and loops vs. list comprehensions.
- **Cognitive State:** Inline chaining vs. procedural scratchpad intermediate variables.

Machine-generated code is hyper-declarative and structurally sterile. **CodeMorph bridges the gap by mathematically extracting your code DNA and lowering abstract patterns into your personal imperative style.**

---

## ⚡ Architecture

```
  ┌────────────────────────┐
  │ Developer Code Samples │ ──▶ [ CodeProfiler (AST Visitor) ]
  └────────────────────────┘                     │
                                                 ▼
                                     ┌───────────────────────┐
                                     │   developer_dna.json  │
                                     │  (Stylometric Tensor) │
                                     └───────────┬───────────┘
                                                 │
  ┌────────────────────────┐                     ▼
  │ Foreign / AI Code      │ ──▶ [ CodeTransformer (AST-Guided) ] ──▶ [ Transpiled Code ]
  └────────────────────────┘                                                    │
                                                                                ▼
                                                                  [ CodeDefender Viva Coach ]
```

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/atharva/codemorph.git
cd codemorph

# Create and activate environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install package
pip install -e .
```

### 2. Extract Your Code DNA

Point CodeMorph at your past code files:

```bash
codemorph profile ./my_past_projects --name "Atharva" --output my_dna.json
```

Output:
```
            🧬 Developer DNA: Atharva             
┌───────────────────────────────┬────────────────┐
│ Stylometric Metric            │ Observed Value │
├───────────────────────────────┼────────────────┤
│ Total Lines Analyzed          │            520 │
│ Avg Variable Name Length      │      6.4 chars │
│ Single-Letter Variables Ratio │            18% │
│ Snake_case vs CamelCase       │       92% / 8% │
│ Max / Avg Nesting Depth       │       3 / 1.84 │
│ Comprehension vs Loop Ratio   │             0% │
│ Type Annotation Coverage      │             0% │
│ Comment Density               │    5% of lines │
└───────────────────────────────┴────────────────┘
```

### 3. Morph Foreign or AI Code

```bash
codemorph morph foreign_script.py --dna my_dna.json --output morphed_script.py
```

### 4. Practice Defending Your Code (Adversarial Viva Mode)

Never get caught off-guard in a lab viva or technical interview. CodeDefender acts as a strict compiler professor, inspects your code's AST, and grills you with brutal questions:

```bash
codemorph defend morphed_script.py
```

---

## 🛡 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
Built by <b>Atharva</b> • Researched with <b>Antigravity</b>
</div>

# File Size Refactoring Status

## Policy
Maximum 400 lines per source file.

## Completed ✅

### mock_llm.py (6,767 lines → Package with 7 files, each <400 lines)
**Status**: Complete and tested (all 177 tests pass)

**Structure**:
```
src/codebase_reviewer/mock_llm/
├── __init__.py (127 lines) - Main MockLLM class with routing
└── generators/
    ├── __init__.py (15 lines) - Package exports
    ├── base.py (203 lines) - Base class with shared utilities
    ├── readme.py (164 lines) - README analysis
    ├── architecture.py (288 lines) - Architecture validation
    ├── quality.py (395 lines) - Code quality assessment
    ├── security.py (213 lines) - Security analysis
    ├── testing.py (235 lines) - Testing strategy
    └── strategy.py (318 lines) - Strategic planning
```

**Commit**: `765cd6d` - "refactor: Split mock_llm.py (6,767 lines) into modular package structure"

## Remaining Work 🔄

### 1. cli.py (1,445 lines)
**Target**: Split into 4 modules of ~360 lines each

**Proposed Structure**:
```
src/codebase_reviewer/cli/
├── __init__.py - Main CLI group and entry point
├── commands/
│   ├── __init__.py
│   ├── core.py - review, prompts, web, simulate (~360 lines)
│   ├── tuning.py - tune group, evolve (~360 lines)
│   ├── analysis.py - analyze, ask, analyze_v2 (~360 lines)
│   └── enterprise.py - multi_repo, compliance, productivity, roi (~360 lines)
```

**Commands to Split**:
- `review` (lines 47-254) - 208 lines
- `prompts` (lines 256-314) - 59 lines
- `web` (lines 316-344) - 29 lines
- `simulate` (lines 346-396) - 51 lines
- `tune` group (lines 398-447) - 50 lines
  - `tune_init` (lines 404-435) - 32 lines
  - `tune_evaluate` (lines 437-447) - 11 lines
- `evolve` (lines 448-732) - 285 lines ⚠️ LARGEST
- `analyze` (lines 733-934) - 202 lines
- `ask` (lines 936-1023) - 88 lines
- `multi_repo` (lines 1025-1106) - 82 lines
- `compliance` (lines 1108-1185) - 78 lines
- `productivity` (lines 1187-1235) - 49 lines
- `roi` (lines 1237-1307) - 71 lines
- `analyze_v2` (lines 1309-1437) - 129 lines
- `main` (lines 1439-1445) - 7 lines

**Helper Functions**:
- `display_summary` (lines 187-253) - 67 lines

### 2. prompts/generator.py (745 lines)
**Target**: Split into 3 modules of ~250 lines each

**Proposed Structure**:
```
src/codebase_reviewer/prompts/
├── phase_generator.py - Main PhaseGenerator class (~150 lines)
├── context_builders_phase0_1.py - Phase 0-1 context builders (~300 lines)
└── context_builders_phase2_4.py - Phase 2-4 context builders (~300 lines)
```

**Methods to Split**:
- Main class (lines 11-87) - 77 lines
- Phase 0 builders (lines 126-174) - 49 lines
- Phase 1 builders (lines 175-287) - 113 lines
- Phase 2 builders (lines 288-483) - 196 lines
- Phase 3 builders (lines 484-548) - 65 lines
- Phase 4 builders (lines 489-548) - 60 lines
- Security builders (lines 549-562) - 14 lines
- Architecture builders (lines 563-726) - 164 lines
- Strategy builders (lines 727-745) - 19 lines

## Testing Requirements
After each refactoring:
1. Run full test suite: `pytest tests/ -v`
2. Verify all 177 tests pass
3. Check imports: `python -c "from codebase_reviewer.cli import cli; from codebase_reviewer.prompts.generator import PhaseGenerator"`
4. Run pre-commit hooks: `pre-commit run --all-files`

## Verification
```bash
# Check all files are under 400 lines
find src -name "*.py" -type f -exec wc -l {} + | awk '$1 > 400 {print}' | sort -rn
```

## Current Status
- ✅ mock_llm.py refactored (6,767 → 7 files, all <400 lines)
- ⏳ cli.py needs refactoring (1,445 lines)
- ⏳ prompts/generator.py needs refactoring (745 lines)

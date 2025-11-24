# Meta-Prompt for Phase 2 Tool Generation

**Generation**: {{generation}}  
**Codebase**: {{codebase_name}}  
**Date**: {{date}}

---

## 🎯 Mission

Generate a **self-contained Go tool** that:
1. Analyzes the codebase with **industry-standard security and quality analysis**
2. Generates comprehensive documentation with **visualizations and actionable insights**
3. Runs **offline** without requiring AI/LLM access
4. Tracks metrics and detects when it becomes obsolete
5. **Re-emits this meta-prompt** when regeneration is needed
6. Includes learnings from previous generations

## 🏆 Quality Standards

**Target**: Meet or exceed **Semgrep** and **SonarQube** industry standards.

### Required Capabilities

#### 1. **Security Analysis** (Critical)
- Detect OWASP Top 10 vulnerabilities:
  - SQL Injection (all variants)
  - XSS (reflected, stored, DOM-based)
  - Authentication/authorization flaws
  - Insecure cryptography
  - Command injection, path traversal, SSRF
  - Hardcoded secrets (API keys, passwords, tokens)
  - Insecure deserialization
  - CSRF vulnerabilities
- Minimum **50+ security rules** for B+ grade
- Minimum **200+ security rules** for A- grade
- Severity scoring: Critical/High/Medium/Low/Info
- Remediation guidance with code examples

#### 2. **Code Quality Analysis** (Critical)
- Complexity metrics:
  - Cyclomatic complexity
  - Cognitive complexity
  - Nesting depth
  - Function/method length
- Maintainability issues:
  - Code duplication
  - Dead code detection
  - Unused imports/variables
  - Magic numbers
  - Code smells (long methods, large classes, too many parameters)
- Technical debt calculation
- Test coverage integration (if available)

#### 3. **Visualization & Reporting** (Critical)
- Executive summary with key findings (✅/⚠️/❌ indicators)
- Mermaid diagrams:
  - Architecture diagrams
  - Data flow diagrams
  - Sequence diagrams
- Tables:
  - Technology stack
  - Quality metrics
  - Security findings
  - Comparison matrices
- Charts:
  - Language distribution
  - Issue trends
  - Complexity heatmaps
- Prioritized recommendations (High/Medium/Low)
- Grading system (A+/A/A-/B+/B/B-/C+/C/C-/D/F)

#### 4. **Dependency Analysis** (Important)
- Software Composition Analysis (SCA)
- Known CVEs in dependencies
- Outdated package detection
- License compliance checking
- Transitive dependency analysis

#### 5. **Integration & Export** (Important)
- JSON export for CI/CD integration
- HTML reports with interactive elements
- Markdown reports for documentation
- GitHub Actions / GitLab CI examples
- Quality gate support (pass/fail thresholds)

---

## 📊 Codebase Analysis

### Structure
{{codebase_structure}}

### Languages
{{languages}}

### Repositories
{{repositories}}

### Key Patterns
{{patterns}}

---

## 📋 User Requirements

### Documentation Needs
{{documentation_needs}}

### Quality Standards
{{quality_standards}}

### Update Frequency
{{update_frequency}}

---

## 🔧 Tool Generation Instructions

### 1. **Core Functionality**

Generate a Go tool with this structure:

```
phase2-tools-gen{{generation}}/
├── cmd/
│   └── generate-docs/
│       └── main.go          # Entry point
├── pkg/
│   ├── analyzer/            # Codebase analysis
│   ├── generator/           # Doc generation
│   ├── metrics/             # Metrics tracking
│   ├── obsolescence/        # Obsolescence detection
│   └── metaprompt/          # Meta-prompt management
├── go.mod
├── go.sum
└── README.md
```

### 2. **Meta-Prompt Embedding**

**CRITICAL**: Bake this entire meta-prompt into the tool as a constant:

```go
package metaprompt

// META_PROMPT is the DNA of this tool
// It will be re-emitted when regeneration is needed
const META_PROMPT = `
{{full_meta_prompt}}
`
```

### 3. **Obsolescence Detection**

Implement thresholds:

```go
type ObsolescenceThresholds struct {
    FilesChangedPercent float64  // {{files_changed_threshold}}%
    NewLanguages        bool     // Trigger if new language detected
    CoverageMin         float64  // {{coverage_threshold}}%
    StaleDaysMax        int      // {{staleness_threshold}} days
    ErrorRateMax        float64  // {{error_threshold}}%
}
```

### 4. **Regeneration Prompt Emission**

When obsolete, emit enhanced meta-prompt:

```go
func emitRegenerationPrompt(metrics Metrics) {
    // Load original meta-prompt
    original := metaprompt.META_PROMPT
    
    // Add learnings
    enhanced := addLearnings(original, metrics)
    
    // Save to file
    path := fmt.Sprintf("/tmp/codebase-reviewer/%s/regeneration-prompt-gen%d.md",
        codebaseName, generation+1)
    ioutil.WriteFile(path, []byte(enhanced), 0644)
    
    // Display instructions
    displayRegenerationInstructions(path)
}
```

---

## 📈 Metrics to Track

Track these metrics on every run:

```go
type Metrics struct {
    // Coverage
    FilesTotal          int
    FilesAnalyzed       int
    FilesDocumented     int
    CoveragePercent     float64
    
    // Change detection
    FilesChanged        int
    FilesChangedPercent float64
    FilesAdded          int
    FilesDeleted        int
    
    // Quality
    ErrorCount          int
    ErrorRate           float64
    WarningCount        int
    
    // Staleness
    LastRunDate         time.Time
    StaleDays           int
    
    // Patterns
    LanguagesDetected   []string
    NewLanguages        []string
    PatternsDetected    []string
    NewPatterns         []string
}
```

---

## 🔄 Self-Evolution Logic

### Learnings from Previous Generations

{{learnings}}

### Improvements for This Generation

{{improvements}}

---

## ✅ Success Criteria

The generated tool must:

- [ ] Compile successfully with `go build`
- [ ] Run offline without network access
- [ ] Generate documentation matching user requirements
- [ ] Track all required metrics
- [ ] Detect obsolescence correctly
- [ ] Re-emit meta-prompt when needed
- [ ] Include this meta-prompt in the binary
- [ ] Achieve ≥{{fidelity_target}}% fidelity vs AI-generated docs
- [ ] Achieve ≥{{coverage_target}}% coverage
- [ ] Run in <{{performance_target}} seconds

---

## 🎨 Code Generation Guidelines

### Style
- Idiomatic Go code
- Clear variable names
- Comprehensive comments
- Error handling on all operations

### Structure
- Modular packages
- Clear separation of concerns
- Testable functions
- Minimal dependencies

### Performance
- Concurrent analysis where possible
- Efficient file I/O
- Caching of expensive operations
- Progress indicators for long operations

---

## 📦 Deliverables

Generate the following files:

1. **cmd/generate-docs/main.go** - Entry point
2. **pkg/analyzer/** - Codebase analysis logic
3. **pkg/generator/** - Documentation generation
4. **pkg/metrics/** - Metrics tracking
5. **pkg/obsolescence/** - Obsolescence detection
6. **pkg/metaprompt/metaprompt.go** - Meta-prompt constant
7. **go.mod** - Go module definition
8. **README.md** - Tool documentation

---

## 🚀 Example Usage

The generated tool should work like this:

```bash
# Build
cd phase2-tools-gen{{generation}}
go build -o bin/generate-docs ./cmd/generate-docs

# Run
./bin/generate-docs /path/to/codebase

# Output
Analyzing codebase...
├── Found 1,234 files
├── Detected languages: Go, Python, JavaScript
├── Analyzing patterns...
└── Generating documentation...

Documentation generated: /tmp/codebase-reviewer/MyProject/

Metrics:
├── Coverage: 94% (1,160/1,234 files)
├── Files changed: 45 (3.6%)
├── Errors: 2 (0.2%)
└── Status: ✅ Healthy

Next run: ./bin/generate-docs /path/to/codebase
```

---

## 🎯 AI Assistant Instructions

**Dear AI Assistant** (that's you!),

Please generate the complete Go tool based on this meta-prompt.

**Include**:
- All source files with complete implementations
- This meta-prompt baked into `pkg/metaprompt/metaprompt.go`
- Comprehensive error handling
- Clear progress indicators
- Detailed README

**Format**:
- Use markdown code blocks with file paths
- Example: ` ```go\n# File: cmd/generate-docs/main.go\n... `
- Include all files needed for a working tool

**Quality**:
- Production-ready code
- No TODOs or placeholders
- Complete implementations
- Tested logic

Thank you! 🚀


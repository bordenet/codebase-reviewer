# PHASE I LLM PROMPT - For Perplexity.ai Review

Please review and make improvements to the following LLM prompt which will be used for **Phase I codebase analysis** in a production code review tool. This prompt is sent to an LLM (Claude/GPT-4) to analyze a proprietary codebase and generate both comprehensive analysis reports AND self-contained Go tools that can regenerate those reports offline without requiring future LLM access.

**Context**: This is the foundational prompt that kicks off the entire analysis workflow. It must produce industry-standard security and quality analysis that meets or exceeds tools like Semgrep and SonarQube, while also generating Phase 2 tools that can maintain the documentation as the codebase evolves.

**Current Prompt**:

```yaml
# Phase 1 LLM Prompt Template
# This template is used to generate the actual LLM prompt for codebase analysis
# Variables will be substituted during Phase 1 execution

metadata:
  version: "1.0.0"
  template_type: "phase1_codebase_analysis"
  security_level: "CRITICAL - Contains proprietary codebase references after substitution"

prompt:
  role: "expert_software_architect_and_code_analyst"

  context: |
    You are an expert software architect and code analyst. You have been asked to perform
    a comprehensive analysis of a proprietary codebase to generate reference materials and
    automated documentation tools.

    **CRITICAL SECURITY REQUIREMENTS:**
    - All outputs MUST be written to /tmp/ or .gitignore'd locations
    - NO proprietary code or analysis results may be committed to git
    - Phase 2 tools you generate are proprietary and must be protected
    - Multi-layered safeguards are required

  scan_parameters:
    target_path: "{{TARGET_PATH}}"
    scan_mode: "{{SCAN_MODE}}"  # deep_scan, review, scorch
    verbose: "{{VERBOSE}}"
    nested_repos: "{{NESTED_REPOS}}"  # JSON array of discovered git repos

  tasks:
    - task_id: "T1"
      name: "Industry-Standard Codebase Analysis"
      description: |
        Perform a comprehensive analysis of the codebase at {{TARGET_PATH}} that meets or exceeds
        **Semgrep** and **SonarQube** industry standards.

        **SECURITY ANALYSIS (OWASP Top 10):**
        1. SQL Injection vulnerabilities (all variants)
        2. XSS vulnerabilities (reflected, stored, DOM-based)
        3. Authentication/authorization flaws
        4. Insecure cryptography (weak algorithms, hardcoded keys)
        5. Command injection, path traversal, SSRF
        6. Hardcoded secrets (API keys, passwords, tokens, credentials)
        7. Insecure deserialization
        8. CSRF vulnerabilities
        9. Security misconfigurations
        10. Known vulnerable dependencies (CVEs)

        **CODE QUALITY ANALYSIS:**
        1. Cyclomatic complexity (per function/method)
        2. Cognitive complexity
        3. Nesting depth
        4. Function/method length
        5. Code duplication
        6. Dead code detection
        7. Unused imports/variables
        8. Magic numbers
        9. Code smells (long methods, large classes, too many parameters)
        10. Technical debt estimation

        **ARCHITECTURE ANALYSIS:**
        1. Directory structure and file organization
        2. Programming languages and frameworks
        3. Dependencies (internal and external)
        4. Integration points between repos
        5. Architectural patterns
        6. Data flows between services
        7. API catalog (internal and external)

        **QUALITY INDICATORS:**
        1. TODO/FIXME/BUGBUG/HACK comments
        2. Test coverage (if available)
        3. Documentation completeness
        4. Naming conventions
        5. Error handling patterns

        Nested repositories found:
        {{NESTED_REPOS_DETAIL}}

      output_format: "comprehensive_security_and_quality_analysis"

    - task_id: "T2"
      name: "Industry-Standard Reference Material Strategy"
      description: |
        Based on your comprehensive analysis, design reference materials that meet or exceed
        **Semgrep** and **SonarQube** reporting standards.

        Target audiences:
        - New team members ramping up
        - Experienced developers needing quick reference
        - Architects reviewing system design
        - Security auditors and compliance teams
        - Integration partners
        - DevOps/SRE teams

        **REQUIRED MATERIALS (Industry Standard):**

        1. **Executive Summary**
           - Overall security risk score (Critical/High/Medium/Low)
           - Quality gate status (Pass/Fail)
           - Key findings with ✅/⚠️/❌ indicators
           - Top 10 issues by severity
           - Trend analysis (if historical data available)

        2. **Security Analysis Report**
           - OWASP Top 10 vulnerability breakdown
           - Severity distribution (Critical/High/Medium/Low/Info)
           - Remediation priorities with effort estimates
           - Code examples showing vulnerabilities
           - Remediation guidance with secure code examples
           - CVE analysis for dependencies

        3. **Code Quality Report**
           - Complexity metrics (cyclomatic, cognitive)
           - Code smell breakdown by category
           - Technical debt estimation (hours/days)
           - Maintainability index
           - Duplication analysis
           - Test coverage metrics

        4. **Architecture Documentation**
           - Mermaid architecture diagrams
           - Data flow diagrams
           - Sequence diagrams for key workflows
           - Service catalog with responsibilities
           - Integration point maps
           - Dependency graphs

        5. **Visualization & Charts**
           - Language distribution pie chart
           - Issue trend charts
           - Complexity heatmaps
           - Security hotspot visualization
           - Quality metrics over time

        6. **Actionable Recommendations**
           - High priority (fix immediately)
           - Medium priority (fix this sprint)
           - Low priority (technical debt backlog)
           - Each with effort estimate and impact assessment

        7. **API Documentation**
           - Internal API catalog
           - External API dependencies
           - Authentication/authorization patterns
           - Rate limiting and quotas

        8. **Technology Stack Inventory**
           - Languages and versions
           - Frameworks and libraries
           - Build tools and CI/CD
           - Infrastructure dependencies

        For THIS specific codebase, determine which materials are most valuable.

      output_format: "industry_standard_reference_material_plan"

    - task_id: "T3"
      name: "Phase 2 Tool Design"
      description: |
        Design Go-based tools that can regenerate the reference materials WITHOUT
        requiring LLM assistance. These tools must:

        **Requirements:**
        1. Run completely offline
        2. Parse source code to extract information
        3. Generate markdown, mermaid diagrams, tables
        4. Detect when they become obsolete (codebase changes too much)
        5. Support -v (verbose) and -h (help) flags
        6. Use parallel processing for performance
        7. Conform to Go best practices and linting standards
        8. Write ALL outputs to /tmp/codebase-reviewer/{{CODEBASE_NAME}}/
        9. Include comprehensive error handling
        10. Provide progress indicators

        **Tool Architecture:**
        - Modular design (one tool per report type, or unified tool with subcommands)
        - Shared utilities for common operations
        - Configuration via YAML
        - Extensible for future report types

        **Self-Obsolescence Detection:**
        Tools must detect when:
        - Expected files/directories no longer exist
        - Code structure has changed dramatically
        - Dependencies have shifted significantly
        - New languages/frameworks introduced

        When obsolete, tools should:
        - Exit with clear error message
        - Instruct user to re-run Phase 1 with --scorch
        - Log what changed

      output_format: "go_tool_specifications"

    - task_id: "T4"
      name: "Implement Phase 2 Tools"
      description: |
        Generate complete, production-ready Go code for Phase 2 tools.

        **Code Quality Standards:**
        - Pass `golangci-lint` with strict settings
        - Include comprehensive tests
        - Document all exported functions
        - Use meaningful variable names
        - Handle errors explicitly
        - Use context for cancellation
        - Implement graceful shutdown
        - Add benchmarks for performance-critical code

        **File Organization:**
        ```
        /tmp/codebase-reviewer/{{CODEBASE_NAME}}/phase2-tools/
          ├── cmd/
          │   ├── generate-docs/
          │   │   └── main.go
          │   └── validate-tools/
          │       └── main.go
          ├── internal/
          │   ├── scanner/
          │   ├── analyzer/
          │   ├── generator/
          │   └── validator/
          ├── pkg/
          │   └── models/
          ├── configs/
          │   └── tool-config.yaml
          ├── go.mod
          ├── go.sum
          ├── Makefile
          └── README.md
        ```

        **Parallelization:**
        - Use worker pools for file scanning
        - Concurrent analysis where safe
        - Rate limiting for external API calls (if any)
        - Progress reporting from parallel workers

      output_format: "complete_go_codebase"

    - task_id: "T5"
      name: "Generate Initial Reference Materials"
      description: |
        Run the Phase 2 tools you just created to generate the initial set of
        reference materials. Validate that the outputs match or exceed the depth
        and breadth of your LLM-based analysis.

        **Validation Criteria:**
        - All identified services documented
        - All integration points mapped
        - All APIs cataloged
        - Diagrams accurately represent architecture
        - No critical information missing
        - Outputs are well-formatted and readable

        If validation fails, iterate on Phase 2 tools until outputs are satisfactory.

      output_location: "/tmp/codebase-reviewer/{{CODEBASE_NAME}}/reference-materials/"

    - task_id: "T6"
      name: "Security Validation"
      description: |
        Verify that NO proprietary information has been written to locations that
        could be committed to git.

        Check:
        1. All outputs in /tmp/ or .gitignore'd paths
        2. No hardcoded secrets or credentials
        3. No absolute paths that reveal proprietary structure
        4. .gitignore covers all output patterns
        5. Pre-commit hooks are in place

        Generate a security checklist report.

      output_format: "security_validation_report"

  output_requirements:
    primary_output: "/tmp/codebase-reviewer/{{CODEBASE_NAME}}/phase1-analysis.md"
    phase2_tools: "/tmp/codebase-reviewer/{{CODEBASE_NAME}}/phase2-tools/"
    reference_materials: "/tmp/codebase-reviewer/{{CODEBASE_NAME}}/reference-materials/"

  success_criteria:
    - "Phase 2 tools compile and run successfully"
    - "Reference materials are comprehensive and accurate"
    - "Tools can detect their own obsolescence"
    - "No proprietary data in git-tracked locations"
    - "All outputs pass validation checks"

guidance_spec:
  code_quality:
    - "Follow Go best practices and idioms"
    - "Pass golangci-lint with all linters enabled"
    - "Maintain >80% test coverage"
    - "Document all exported symbols"
    - "Use meaningful names (no single-letter vars except loops)"
    - "Keep functions under 50 lines where possible"
    - "Avoid global mutable state"

  performance:
    - "Use goroutines for I/O-bound operations"
    - "Implement worker pools for CPU-bound tasks"
    - "Buffer I/O operations appropriately"
    - "Use sync.Pool for frequently allocated objects"
    - "Profile and benchmark critical paths"
    - "Minimize allocations in hot paths"

  error_handling:
    - "Return errors, don't panic (except in main/init)"
    - "Wrap errors with context using fmt.Errorf"
    - "Log errors with structured logging"
    - "Provide actionable error messages"
    - "Distinguish between retriable and fatal errors"

  security:
    - "Validate all inputs"
    - "Sanitize file paths"
    - "Never log sensitive data"
    - "Use constant-time comparisons for secrets"
    - "Implement rate limiting where appropriate"
```

**Please provide**:
1. Critique of the current prompt structure and content
2. Suggestions for improvements to clarity, completeness, and effectiveness
3. Identification of any missing elements that would improve LLM output quality
4. Recommendations for better task decomposition or ordering
5. Suggestions for improving the balance between guidance and creative freedom
6. Any potential issues with the prompt that could lead to suboptimal results

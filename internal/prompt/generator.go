package prompt

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"text/template"

	"github.com/bordenet/codebase-reviewer/internal/scanner"
	"github.com/bordenet/codebase-reviewer/pkg/logger"
	"gopkg.in/yaml.v3"
)

// Generate creates the LLM prompt for Phase 1 analysis
func Generate(targetPath string, repos []scanner.Repository, outputDir string, verbose, scorch bool, log *logger.Logger) (string, error) {
	log.Info("Loading prompt template...")

	// Load template
	templatePath := "prompts/templates/phase1-prompt-template.yaml"
	templateData, err := os.ReadFile(templatePath)
	if err != nil {
		return "", fmt.Errorf("failed to read template: %w", err)
	}

	// Parse YAML template
	var promptTemplate map[string]interface{}
	if err := yaml.Unmarshal(templateData, &promptTemplate); err != nil {
		return "", fmt.Errorf("failed to parse template YAML: %w", err)
	}

	log.Info("Analyzing repositories...")

	// Analyze each repository
	var analyses []*scanner.RepositoryAnalysis
	for _, repo := range repos {
		analysis, err := scanner.AnalyzeRepository(repo, log)
		if err != nil {
			log.Warn("Failed to analyze %s: %v", repo.Name, err)
			continue
		}
		analyses = append(analyses, analysis)
	}

	log.Info("Building prompt context...")

	// Build substitution variables
	vars := buildTemplateVars(targetPath, repos, analyses, outputDir, verbose, scorch)

	// Render template
	rendered, err := renderTemplate(promptTemplate, vars)
	if err != nil {
		return "", fmt.Errorf("failed to render template: %w", err)
	}

	// Write prompt to output directory
	promptPath := filepath.Join(outputDir, "phase1-llm-prompt.md")
	if err := os.WriteFile(promptPath, []byte(rendered), 0644); err != nil {
		return "", fmt.Errorf("failed to write prompt: %w", err)
	}

	log.Info("Prompt generated: %s", promptPath)

	// Also write as YAML for programmatic access
	yamlPath := filepath.Join(outputDir, "phase1-llm-prompt.yaml")
	yamlData, err := yaml.Marshal(promptTemplate)
	if err != nil {
		return "", fmt.Errorf("failed to marshal YAML: %w", err)
	}
	if err := os.WriteFile(yamlPath, yamlData, 0644); err != nil {
		return "", fmt.Errorf("failed to write YAML prompt: %w", err)
	}

	return promptPath, nil
}

func buildTemplateVars(targetPath string, repos []scanner.Repository, analyses []*scanner.RepositoryAnalysis, outputDir string, verbose, scorch bool) map[string]string {
	codebaseName := filepath.Base(targetPath)

	// Build nested repos detail
	var reposDetail strings.Builder
	for i, analysis := range analyses {
		reposDetail.WriteString(fmt.Sprintf("\n### Repository %d: %s\n", i+1, analysis.Repository.Name))
		reposDetail.WriteString(fmt.Sprintf("- Path: %s\n", analysis.Repository.RelativePath))
		reposDetail.WriteString(fmt.Sprintf("- Primary Language: %s\n", analysis.PrimaryLanguage()))
		reposDetail.WriteString(fmt.Sprintf("- Total Files: %d\n", analysis.TotalFiles))
		reposDetail.WriteString("- Languages:\n")
		for lang, count := range analysis.Languages {
			reposDetail.WriteString(fmt.Sprintf("  - %s: %d files\n", lang, count))
		}
	}

	// Build repos JSON
	reposJSON, _ := json.Marshal(repos)

	scanMode := "deep_scan"
	if scorch {
		scanMode = "scorch"
	}

	return map[string]string{
		"TARGET_PATH":         targetPath,
		"CODEBASE_NAME":       codebaseName,
		"SCAN_MODE":           scanMode,
		"VERBOSE":             fmt.Sprintf("%v", verbose),
		"NESTED_REPOS":        string(reposJSON),
		"NESTED_REPOS_DETAIL": reposDetail.String(),
		"OUTPUT_DIR":          outputDir,
	}
}

func renderTemplate(templateData map[string]interface{}, vars map[string]string) (string, error) {
	// Convert template to YAML string
	yamlBytes, err := yaml.Marshal(templateData)
	if err != nil {
		return "", err
	}

	yamlStr := string(yamlBytes)

	// Replace variables
	for key, value := range vars {
		placeholder := "{{" + key + "}}"
		yamlStr = strings.ReplaceAll(yamlStr, placeholder, value)
	}

	// Convert to markdown for readability
	var buf bytes.Buffer
	buf.WriteString("# Phase 1 LLM Prompt - Codebase Analysis\n\n")
	buf.WriteString("**SECURITY NOTICE:** This prompt contains references to proprietary code.\n")
	buf.WriteString("All outputs must be written to /tmp or .gitignore'd locations.\n\n")
	buf.WriteString("---\n\n")
	buf.WriteString("```yaml\n")
	buf.WriteString(yamlStr)
	buf.WriteString("\n```\n\n")
	buf.WriteString("---\n\n")
	buf.WriteString("## Instructions for AI Assistant\n\n")
	buf.WriteString("Please process the above YAML prompt and:\n\n")
	buf.WriteString("1. Perform a deep scan of the codebase\n")
	buf.WriteString("2. Design reference materials strategy\n")
	buf.WriteString("3. Design Phase 2 tools\n")
	buf.WriteString("4. Implement Phase 2 tools in Go\n")
	buf.WriteString("5. Generate initial reference materials\n")
	buf.WriteString("6. Validate security compliance\n\n")
	buf.WriteString("All outputs must go to:\n")
	buf.WriteString(fmt.Sprintf("- %s\n\n", vars["OUTPUT_DIR"]))

	return buf.String(), nil
}

// RenderMarkdown converts the YAML prompt to a readable markdown format
func RenderMarkdown(yamlData map[string]interface{}) (string, error) {
	tmpl := `# Codebase Analysis Prompt

## Metadata
- Version: {{.metadata.version}}
- Type: {{.metadata.template_type}}
- Security Level: {{.metadata.security_level}}

## Context
{{.prompt.context}}

## Scan Parameters
- Target Path: {{.prompt.scan_parameters.target_path}}
- Scan Mode: {{.prompt.scan_parameters.scan_mode}}
- Verbose: {{.prompt.scan_parameters.verbose}}

## Nested Repositories
{{.prompt.scan_parameters.nested_repos_detail}}

## Tasks
{{range .prompt.tasks}}
### {{.name}} ({{.task_id}})
{{.description}}
{{end}}

## Output Requirements
- Primary Output: {{.prompt.output_requirements.primary_output}}
- Phase 2 Tools: {{.prompt.output_requirements.phase2_tools}}
- Reference Materials: {{.prompt.output_requirements.reference_materials}}

## Success Criteria
{{range .prompt.success_criteria}}
- {{.}}
{{end}}

## Guidance Specification

### Code Quality
{{range .guidance_spec.code_quality}}
- {{.}}
{{end}}

### Performance
{{range .guidance_spec.performance}}
- {{.}}
{{end}}

### Error Handling
{{range .guidance_spec.error_handling}}
- {{.}}
{{end}}

### Security
{{range .guidance_spec.security}}
- {{.}}
{{end}}
`

	t, err := template.New("prompt").Parse(tmpl)
	if err != nil {
		return "", err
	}

	var buf bytes.Buffer
	if err := t.Execute(&buf, yamlData); err != nil {
		return "", err
	}

	return buf.String(), nil
}

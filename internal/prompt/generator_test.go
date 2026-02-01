package prompt

import (
	"strings"
	"testing"

	"github.com/bordenet/codebase-reviewer/internal/scanner"
)

func TestBuildTemplateVars(t *testing.T) {
	tests := []struct {
		name     string
		target   string
		repos    []scanner.Repository
		analyses []*scanner.RepositoryAnalysis
		output   string
		verbose  bool
		scorch   bool
		wantKeys []string
	}{
		{
			name:     "basic variables",
			target:   "/path/to/my-project",
			repos:    []scanner.Repository{},
			analyses: []*scanner.RepositoryAnalysis{},
			output:   "/tmp/output",
			verbose:  false,
			scorch:   false,
			wantKeys: []string{"TARGET_PATH", "CODEBASE_NAME", "SCAN_MODE", "VERBOSE", "NESTED_REPOS", "OUTPUT_DIR"},
		},
		{
			name:   "with analyses",
			target: "/path/to/project",
			repos: []scanner.Repository{
				{Path: "/path/to/project", Name: "project", RelativePath: "."},
			},
			analyses: []*scanner.RepositoryAnalysis{
				{
					Repository: scanner.Repository{Name: "project", RelativePath: "."},
					Languages:  map[string]int{"Go": 10, "Python": 5},
					TotalFiles: 15,
				},
			},
			output:   "/tmp/out",
			verbose:  true,
			scorch:   false,
			wantKeys: []string{"TARGET_PATH", "CODEBASE_NAME", "NESTED_REPOS_DETAIL"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			vars := buildTemplateVars(tt.target, tt.repos, tt.analyses, tt.output, tt.verbose, tt.scorch)

			for _, key := range tt.wantKeys {
				if _, ok := vars[key]; !ok {
					t.Errorf("buildTemplateVars() missing key %q", key)
				}
			}
		})
	}
}

func TestBuildTemplateVars_CodebaseName(t *testing.T) {
	vars := buildTemplateVars("/home/user/my-project", nil, nil, "/tmp/out", false, false)
	if vars["CODEBASE_NAME"] != "my-project" {
		t.Errorf("CODEBASE_NAME = %q, want %q", vars["CODEBASE_NAME"], "my-project")
	}
}

func TestBuildTemplateVars_ScanMode(t *testing.T) {
	tests := []struct {
		scorch   bool
		wantMode string
	}{
		{false, "deep_scan"},
		{true, "scorch"},
	}

	for _, tt := range tests {
		vars := buildTemplateVars("/path", nil, nil, "/tmp", false, tt.scorch)
		if vars["SCAN_MODE"] != tt.wantMode {
			t.Errorf("SCAN_MODE with scorch=%v = %q, want %q", tt.scorch, vars["SCAN_MODE"], tt.wantMode)
		}
	}
}

func TestBuildTemplateVars_NestedReposDetail(t *testing.T) {
	analyses := []*scanner.RepositoryAnalysis{
		{
			Repository: scanner.Repository{Name: "sub-project", RelativePath: "sub"},
			Languages:  map[string]int{"Go": 20},
			TotalFiles: 20,
		},
	}

	vars := buildTemplateVars("/path", nil, analyses, "/tmp", false, false)
	detail := vars["NESTED_REPOS_DETAIL"]

	if !strings.Contains(detail, "sub-project") {
		t.Error("NESTED_REPOS_DETAIL should contain repository name")
	}
	if !strings.Contains(detail, "Go") {
		t.Error("NESTED_REPOS_DETAIL should contain language")
	}
	if !strings.Contains(detail, "20") {
		t.Error("NESTED_REPOS_DETAIL should contain file count")
	}
}

func TestRenderTemplate(t *testing.T) {
	tests := []struct {
		name     string
		template map[string]interface{}
		vars     map[string]string
		wantErr  bool
		contains []string
	}{
		{
			name:     "basic render",
			template: map[string]interface{}{"test": "{{VALUE}}"},
			vars:     map[string]string{"VALUE": "hello"},
			wantErr:  false,
			contains: []string{"hello", "Phase 1 LLM Prompt"},
		},
		{
			name:     "empty template",
			template: map[string]interface{}{},
			vars:     map[string]string{},
			wantErr:  false,
			contains: []string{"Phase 1 LLM Prompt"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := renderTemplate(tt.template, tt.vars)
			if (err != nil) != tt.wantErr {
				t.Errorf("renderTemplate() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			for _, s := range tt.contains {
				if !strings.Contains(result, s) {
					t.Errorf("renderTemplate() result should contain %q", s)
				}
			}
		})
	}
}

func TestRenderMarkdown(t *testing.T) {
	tests := []struct {
		name     string
		yamlData map[string]interface{}
		wantErr  bool
		contains []string
	}{
		{
			name: "complete template data",
			yamlData: map[string]interface{}{
				"metadata": map[string]interface{}{
					"version":        "1.0",
					"template_type":  "analysis",
					"security_level": "high",
				},
				"prompt": map[string]interface{}{
					"context": "Analyze the codebase",
					"scan_parameters": map[string]interface{}{
						"target_path":         "/path/to/code",
						"scan_mode":           "deep",
						"verbose":             true,
						"nested_repos_detail": "repo details here",
					},
					"tasks": []map[string]interface{}{
						{
							"name":        "Scan Files",
							"task_id":     "T1",
							"description": "Scan all source files",
						},
					},
					"output_requirements": map[string]interface{}{
						"primary_output":      "analysis.md",
						"phase2_tools":        "tools/",
						"reference_materials": "refs/",
					},
				},
				"success_criteria": []string{"Complete scan", "Generate report"},
				"guidance_spec": map[string]interface{}{
					"code_quality":   []string{"Follow conventions"},
					"performance":    []string{"Optimize for speed"},
					"error_handling": []string{"Handle all errors"},
					"security":       []string{"No secrets exposed"},
				},
			},
			wantErr:  false,
			contains: []string{"Codebase Analysis Prompt", "Metadata", "Context"},
		},
		{
			name: "partial template",
			yamlData: map[string]interface{}{
				"metadata": map[string]interface{}{
					"version": "2.0",
				},
			},
			wantErr:  false,
			contains: []string{"Codebase Analysis Prompt"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := RenderMarkdown(tt.yamlData)
			if (err != nil) != tt.wantErr {
				t.Errorf("RenderMarkdown() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if err != nil {
				return
			}
			for _, s := range tt.contains {
				if !strings.Contains(result, s) {
					t.Errorf("RenderMarkdown() result should contain %q", s)
				}
			}
		})
	}
}

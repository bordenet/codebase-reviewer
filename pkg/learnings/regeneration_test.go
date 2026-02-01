package learnings

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

func TestGenerateRegenerationPrompt(t *testing.T) {
	learnings := &Learnings{
		Metadata: Metadata{
			ToolName:    "test-tool",
			ToolVersion: "1.0.0",
			Generation:  1,
			RunDate:     time.Now().Add(-24 * time.Hour),
		},
		ExecutionMetrics: ExecutionMetrics{
			FilesProcessed: 100,
		},
		CodebaseChanges: CodebaseChanges{
			StructuralChanges: StructuralChanges{
				NewDirectories:     []string{"/new/dir1", "/new/dir2"},
				RemovedDirectories: []string{"/old/dir"},
			},
			LanguageChanges: LanguageChanges{
				NewLanguages: []string{"Rust"},
			},
			FrameworkChanges: FrameworkChanges{
				NewFrameworks: []string{"Tokio"},
			},
			DependencyChanges: DependencyChanges{
				MajorUpgrades: []string{"go 1.21 -> 1.22"},
			},
			ArchitectureChanges: ArchitectureChanges{
				PatternShifts: []string{"monolith to microservices"},
			},
		},
		NextGenRecommendations: NextGenerationRecommendations{
			CodeQualityImprovements:  []string{"add linting"},
			NewReportTypes:           []string{"security report"},
			EnhancedDetections:       []string{"detect race conditions"},
			PerformanceOptimizations: []string{"parallel scanning"},
		},
		Improvements: []Improvement{
			{Category: "scanning", Description: "faster file traversal"},
			{Category: "documentation", Description: "better README generation"},
			{Category: "tools", Description: "improved error handling"},
		},
	}

	prompt, err := GenerateRegenerationPrompt(
		"codebase-reviewer",
		"2.0.0",
		2,
		"test-codebase",
		"/path/to/codebase",
		"old-fingerprint",
		"new-fingerprint",
		"structural changes detected",
		learnings,
	)

	if err != nil {
		t.Fatalf("GenerateRegenerationPrompt() error = %v", err)
	}

	if prompt.Version != "2.0" {
		t.Errorf("Version = %q, want %q", prompt.Version, "2.0")
	}

	if prompt.Metadata.Generation != 2 {
		t.Errorf("Generation = %d, want %d", prompt.Metadata.Generation, 2)
	}

	if prompt.Context.CodebaseName != "test-codebase" {
		t.Errorf("CodebaseName = %q, want %q", prompt.Context.CodebaseName, "test-codebase")
	}

	if len(prompt.Context.ChangesDetected.NewLanguages) != 1 {
		t.Errorf("NewLanguages count = %d, want 1", len(prompt.Context.ChangesDetected.NewLanguages))
	}

	if len(prompt.Prompt.Tasks) != 3 {
		t.Errorf("Tasks count = %d, want 3", len(prompt.Prompt.Tasks))
	}
}

func TestSaveRegenerationPrompt(t *testing.T) {
	dir := t.TempDir()

	prompt := &RegenerationPrompt{
		Version: "2.0",
		Purpose: "test regeneration",
		Metadata: RegenerationMetadata{
			GeneratedBy: "test",
			Generation:  1,
			CurrentDate: time.Now(),
		},
		Context: RegenerationContext{
			CodebaseName: "test",
		},
		Prompt: PromptSection{
			Instruction: "test instruction",
			Tasks: []RegenerationTask{
				{TaskID: "T1", Name: "Test Task", Description: "Test"},
			},
		},
	}

	err := SaveRegenerationPrompt(prompt, dir)
	if err != nil {
		t.Fatalf("SaveRegenerationPrompt() error = %v", err)
	}

	// Check YAML file exists
	yamlPath := filepath.Join(dir, "phase1-regeneration-prompt.yaml")
	if _, err := os.Stat(yamlPath); os.IsNotExist(err) {
		t.Error("YAML file not created")
	}

	// Check MD file exists
	mdPath := filepath.Join(dir, "phase1-regeneration-prompt.md")
	if _, err := os.Stat(mdPath); os.IsNotExist(err) {
		t.Error("Markdown file not created")
	}

	// Verify content
	mdContent, _ := os.ReadFile(mdPath)
	if !strings.Contains(string(mdContent), "Phase 1 Regeneration Prompt") {
		t.Error("Markdown content missing header")
	}
}

func TestBuildStructuralChangesList(t *testing.T) {
	tests := []struct {
		name      string
		learnings *Learnings
		wantLen   int
	}{
		{
			name:      "no changes",
			learnings: &Learnings{},
			wantLen:   0,
		},
		{
			name: "new directories only",
			learnings: &Learnings{
				CodebaseChanges: CodebaseChanges{
					StructuralChanges: StructuralChanges{
						NewDirectories: []string{"/new"},
					},
				},
			},
			wantLen: 1,
		},
		{
			name: "both new and removed",
			learnings: &Learnings{
				CodebaseChanges: CodebaseChanges{
					StructuralChanges: StructuralChanges{
						NewDirectories:     []string{"/new"},
						RemovedDirectories: []string{"/old"},
					},
				},
			},
			wantLen: 2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			changes := buildStructuralChangesList(tt.learnings)
			if len(changes) != tt.wantLen {
				t.Errorf("buildStructuralChangesList() len = %d, want %d", len(changes), tt.wantLen)
			}
		})
	}
}

func TestBuildPromptSection(t *testing.T) {
	learnings := &Learnings{
		Improvements: []Improvement{
			{Category: "scanning", Description: "improvement 1"},
			{Category: "documentation", Description: "improvement 2"},
		},
	}

	section := buildPromptSection("test-codebase", 2, "changes detected", learnings)

	if !strings.Contains(section.Instruction, "test-codebase") {
		t.Error("Instruction should contain codebase name")
	}
	if !strings.Contains(section.Instruction, "GENERATION 2") {
		t.Error("Instruction should contain generation number")
	}
	if !strings.Contains(section.Instruction, "changes detected") {
		t.Error("Instruction should contain obsolescence reason")
	}
	if len(section.Tasks) != 3 {
		t.Errorf("Tasks count = %d, want 3", len(section.Tasks))
	}
}

func TestBuildRegenerationTasks(t *testing.T) {
	learnings := &Learnings{
		Improvements: []Improvement{
			{Category: "scanning", Description: "scan improvement"},
			{Category: "documentation", Description: "doc improvement"},
			{Category: "tools", Description: "tool improvement"},
		},
	}

	tasks := buildRegenerationTasks("test", learnings)

	if len(tasks) != 3 {
		t.Fatalf("buildRegenerationTasks() len = %d, want 3", len(tasks))
	}

	// Check task IDs
	expectedIDs := []string{"T1-REGEN", "T2-REGEN", "T3-REGEN"}
	for i, task := range tasks {
		if task.TaskID != expectedIDs[i] {
			t.Errorf("Task[%d].TaskID = %q, want %q", i, task.TaskID, expectedIDs[i])
		}
	}
}

func TestExtractImprovements(t *testing.T) {
	learnings := &Learnings{
		Improvements: []Improvement{
			{Category: "scanning", Description: "scan 1"},
			{Category: "scanning", Description: "scan 2"},
			{Category: "documentation", Description: "doc 1"},
			{Category: "tools", Description: "tool 1"},
			{Category: "Advanced Scanning", Description: "advanced scan"},
		},
	}

	tests := []struct {
		category string
		wantLen  int
	}{
		{"scanning", 3}, // matches "scanning" and "Advanced Scanning"
		{"documentation", 1},
		{"tools", 1},
		{"nonexistent", 0},
	}

	for _, tt := range tests {
		t.Run(tt.category, func(t *testing.T) {
			improvements := extractImprovements(learnings, tt.category)
			if len(improvements) != tt.wantLen {
				t.Errorf("extractImprovements(%q) len = %d, want %d", tt.category, len(improvements), tt.wantLen)
			}
		})
	}
}

func TestFormatPromptAsMarkdown(t *testing.T) {
	prompt := &RegenerationPrompt{
		Version: "2.0",
		Purpose: "test purpose",
		Metadata: RegenerationMetadata{
			GeneratedBy:        "test-tool",
			Generation:         2,
			PreviousRunDate:    time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),
			CurrentDate:        time.Date(2024, 1, 2, 0, 0, 0, 0, time.UTC),
			ObsolescenceReason: "test reason",
		},
		Context: RegenerationContext{
			CodebaseName:    "test-codebase",
			CodebasePath:    "/path/to/codebase",
			OutputDirectory: "/tmp/output",
			ChangesDetected: ChangesDetected{
				StructuralChanges: []string{"added new module"},
				NewLanguages:      []string{"Rust"},
				NewFrameworks:     []string{"Tokio"},
			},
		},
		EnhancedRequirements: EnhancedRequirements{
			Phase2ToolEnhancements: []string{"better detection"},
		},
		Prompt: PromptSection{
			Instruction: "test instruction",
			Tasks: []RegenerationTask{
				{
					TaskID:                   "T1",
					Name:                     "Test Task",
					Description:              "Test description",
					ImprovementsOverPrevious: []string{"improvement 1"},
				},
			},
		},
	}

	md := formatPromptAsMarkdown(prompt)

	checks := []string{
		"# Phase 1 Regeneration Prompt",
		"**Version:** 2.0",
		"test-tool",
		"Generation:** 2",
		"test-codebase",
		"/path/to/codebase",
		"Structural Changes",
		"added new module",
		"New Languages",
		"Rust",
		"New Frameworks",
		"Tokio",
		"Tool Enhancements",
		"better detection",
		"Test Task (T1)",
		"Test description",
		"improvement 1",
	}

	for _, check := range checks {
		if !strings.Contains(md, check) {
			t.Errorf("formatPromptAsMarkdown() should contain %q", check)
		}
	}
}

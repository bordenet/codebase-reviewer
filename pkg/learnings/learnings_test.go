package learnings

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestNewLearnings(t *testing.T) {
	l := NewLearnings()

	if l == nil {
		t.Fatal("NewLearnings() returned nil")
	}
	if l.WhatWorkedWell == nil {
		t.Error("WhatWorkedWell should be initialized")
	}
	if l.WhatFailed == nil {
		t.Error("WhatFailed should be initialized")
	}
	if l.EdgeCases == nil {
		t.Error("EdgeCases should be initialized")
	}
	if l.Patterns == nil {
		t.Error("Patterns should be initialized")
	}
	if l.Improvements == nil {
		t.Error("Improvements should be initialized")
	}
}

func TestLoadNonExistent(t *testing.T) {
	l, err := Load("/nonexistent/path/learnings.yaml")

	if err != nil {
		t.Errorf("Load() should return empty learnings for non-existent file, got error: %v", err)
	}
	if l == nil {
		t.Fatal("Load() returned nil for non-existent file")
	}
}

func TestSaveAndLoad(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "test-learnings.yaml")

	original := &Learnings{
		Metadata: Metadata{
			ToolName:    "test-tool",
			ToolVersion: "1.0.0",
			Generation:  1,
			RunDate:     time.Now().Truncate(time.Second),
			CodebaseName: "test-codebase",
		},
		ExecutionMetrics: ExecutionMetrics{
			DurationSeconds: 10.5,
			FilesProcessed:  100,
			ErrorsEncountered: 2,
		},
		WhatWorkedWell: []WorkedWell{
			{Category: "parsing", Description: "Fast parsing", Confidence: "high"},
		},
		WhatFailed: []Failed{
			{Category: "analysis", Description: "Slow analysis", ErrorType: "timeout"},
		},
	}

	if err := original.Save(path); err != nil {
		t.Fatalf("Save() error = %v", err)
	}

	loaded, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}

	if loaded.Metadata.ToolName != original.Metadata.ToolName {
		t.Errorf("ToolName = %q, want %q", loaded.Metadata.ToolName, original.Metadata.ToolName)
	}
	if loaded.ExecutionMetrics.FilesProcessed != original.ExecutionMetrics.FilesProcessed {
		t.Errorf("FilesProcessed = %d, want %d", loaded.ExecutionMetrics.FilesProcessed, original.ExecutionMetrics.FilesProcessed)
	}
	if len(loaded.WhatWorkedWell) != len(original.WhatWorkedWell) {
		t.Errorf("WhatWorkedWell length = %d, want %d", len(loaded.WhatWorkedWell), len(original.WhatWorkedWell))
	}
}

func TestSaveCreatesDirectory(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "nested", "deep", "learnings.yaml")

	l := NewLearnings()
	l.Metadata.ToolName = "test"

	if err := l.Save(path); err != nil {
		t.Fatalf("Save() should create nested directories, got error: %v", err)
	}

	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Error("Save() did not create file")
	}
}

func TestLoadInvalidYAML(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "invalid.yaml")

	if err := os.WriteFile(path, []byte("invalid: yaml: content: ["), 0644); err != nil {
		t.Fatal(err)
	}

	_, err := Load(path)
	if err == nil {
		t.Error("Load() should return error for invalid YAML")
	}
}

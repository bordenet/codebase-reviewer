package learnings

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"gopkg.in/yaml.v3"
)

// Learnings captures operational insights from Phase 2 tool runs
type Learnings struct {
	Metadata           Metadata                      `yaml:"metadata"`
	ExecutionMetrics   ExecutionMetrics              `yaml:"execution_metrics"`
	WhatWorkedWell     []WorkedWell                  `yaml:"what_worked_well"`
	WhatFailed         []Failed                      `yaml:"what_failed"`
	EdgeCases          []EdgeCase                    `yaml:"edge_cases_discovered"`
	Patterns           []Pattern                     `yaml:"patterns_identified"`
	Improvements       []Improvement                 `yaml:"improvements_needed"`
	CodebaseChanges    CodebaseChanges               `yaml:"codebase_changes_detected"`
	Obsolescence       ObsolescenceIndicators        `yaml:"obsolescence_indicators"`
	NextGenRecommendations NextGenerationRecommendations `yaml:"next_generation_recommendations"`
	CustomNotes        []CustomNote                  `yaml:"custom_notes,omitempty"`
}

type Metadata struct {
	ToolName            string    `yaml:"tool_name"`
	ToolVersion         string    `yaml:"tool_version"`
	Generation          int       `yaml:"generation"`
	RunDate             time.Time `yaml:"run_date"`
	CodebaseName        string    `yaml:"codebase_name"`
	CodebasePath        string    `yaml:"codebase_path"`
	CodebaseFingerprint string    `yaml:"codebase_fingerprint"`
}

type ExecutionMetrics struct {
	DurationSeconds    float64 `yaml:"duration_seconds"`
	FilesProcessed     int     `yaml:"files_processed"`
	ErrorsEncountered  int     `yaml:"errors_encountered"`
	WarningsGenerated  int     `yaml:"warnings_generated"`
	ReportsGenerated   int     `yaml:"reports_generated"`
	MemoryPeakMB       float64 `yaml:"memory_peak_mb"`
}

type WorkedWell struct {
	Category    string   `yaml:"category"`
	Description string   `yaml:"description"`
	Confidence  string   `yaml:"confidence"`
	Examples    []string `yaml:"examples,omitempty"`
}

type Failed struct {
	Category      string   `yaml:"category"`
	Description   string   `yaml:"description"`
	ErrorType     string   `yaml:"error_type"`
	Frequency     string   `yaml:"frequency"`
	Impact        string   `yaml:"impact"`
	Examples      []string `yaml:"examples,omitempty"`
	SuggestedFix  string   `yaml:"suggested_fix"`
}

type EdgeCase struct {
	CaseID           string `yaml:"case_id"`
	Description      string `yaml:"description"`
	TriggerCondition string `yaml:"trigger_condition"`
	CurrentBehavior  string `yaml:"current_behavior"`
	DesiredBehavior  string `yaml:"desired_behavior"`
	Workaround       string `yaml:"workaround,omitempty"`
	Priority         string `yaml:"priority"`
}

type Pattern struct {
	PatternType    string   `yaml:"pattern_type"`
	PatternName    string   `yaml:"pattern_name"`
	Description    string   `yaml:"description"`
	Frequency      int      `yaml:"frequency"`
	Locations      []string `yaml:"locations"`
	Significance   string   `yaml:"significance"`
	Recommendation string   `yaml:"recommendation"`
}

type Improvement struct {
	ImprovementID      string `yaml:"improvement_id"`
	Category           string `yaml:"category"`
	Description        string `yaml:"description"`
	CurrentState       string `yaml:"current_state"`
	DesiredState       string `yaml:"desired_state"`
	Priority           string `yaml:"priority"`
	EffortEstimate     string `yaml:"effort_estimate"`
	ImplementationHint string `yaml:"implementation_hint"`
}

type CodebaseChanges struct {
	StructuralChanges StructuralChanges `yaml:"structural_changes"`
	LanguageChanges   LanguageChanges   `yaml:"language_changes"`
	FrameworkChanges  FrameworkChanges  `yaml:"framework_changes"`
	DependencyChanges DependencyChanges `yaml:"dependency_changes"`
	ArchitectureChanges ArchitectureChanges `yaml:"architecture_changes"`
}

type StructuralChanges struct {
	NewDirectories     []string `yaml:"new_directories,omitempty"`
	RemovedDirectories []string `yaml:"removed_directories,omitempty"`
	RenamedDirectories []string `yaml:"renamed_directories,omitempty"`
}

type LanguageChanges struct {
	NewLanguages     []string `yaml:"new_languages,omitempty"`
	RemovedLanguages []string `yaml:"removed_languages,omitempty"`
	LanguageShift    string   `yaml:"language_shift,omitempty"`
}

type FrameworkChanges struct {
	NewFrameworks      []string `yaml:"new_frameworks,omitempty"`
	RemovedFrameworks  []string `yaml:"removed_frameworks,omitempty"`
	VersionUpgrades    []string `yaml:"version_upgrades,omitempty"`
}

type DependencyChanges struct {
	NewDependencies     []string `yaml:"new_dependencies,omitempty"`
	RemovedDependencies []string `yaml:"removed_dependencies,omitempty"`
	MajorUpgrades       []string `yaml:"major_upgrades,omitempty"`
}

type ArchitectureChanges struct {
	NewServices        []string `yaml:"new_services,omitempty"`
	RemovedServices    []string `yaml:"removed_services,omitempty"`
	RefactoredServices []string `yaml:"refactored_services,omitempty"`
	PatternShifts      []string `yaml:"pattern_shifts,omitempty"`
}

type ObsolescenceIndicators struct {
	IsObsolete         bool     `yaml:"is_obsolete"`
	ObsolescenceScore  float64  `yaml:"obsolescence_score"`
	Reasons            []string `yaml:"reasons"`
	Confidence         string   `yaml:"confidence"`
	Recommendation     string   `yaml:"recommendation"`
}

type NextGenerationRecommendations struct {
	NewReportTypes            []string `yaml:"new_report_types,omitempty"`
	EnhancedDetections        []string `yaml:"enhanced_detections,omitempty"`
	PerformanceOptimizations  []string `yaml:"performance_optimizations,omitempty"`
	UsabilityImprovements     []string `yaml:"usability_improvements,omitempty"`
	CodeQualityImprovements   []string `yaml:"code_quality_improvements,omitempty"`
}

type CustomNote struct {
	Note     string `yaml:"note"`
	Category string `yaml:"category"`
	Priority string `yaml:"priority"`
}

// Load reads learnings from a YAML file
func Load(path string) (*Learnings, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return NewLearnings(), nil // Return empty learnings if file doesn't exist
		}
		return nil, fmt.Errorf("failed to read learnings file: %w", err)
	}

	var l Learnings
	if err := yaml.Unmarshal(data, &l); err != nil {
		return nil, fmt.Errorf("failed to parse learnings YAML: %w", err)
	}

	return &l, nil
}

// Save writes learnings to a YAML file
func (l *Learnings) Save(path string) error {
	// Ensure directory exists
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	data, err := yaml.Marshal(l)
	if err != nil {
		return fmt.Errorf("failed to marshal learnings to YAML: %w", err)
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write learnings file: %w", err)
	}

	return nil
}

// NewLearnings creates a new empty Learnings instance
func NewLearnings() *Learnings {
	return &Learnings{
		WhatWorkedWell: []WorkedWell{},
		WhatFailed:     []Failed{},
		EdgeCases:      []EdgeCase{},
		Patterns:       []Pattern{},
		Improvements:   []Improvement{},
		CustomNotes:    []CustomNote{},
	}
}


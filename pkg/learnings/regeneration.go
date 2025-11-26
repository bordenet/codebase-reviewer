package learnings

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

// RegenerationPrompt contains all data needed to regenerate Phase 1 with improvements
type RegenerationPrompt struct {
	Version              string               `yaml:"version"`
	Purpose              string               `yaml:"purpose"`
	Metadata             RegenerationMetadata `yaml:"metadata"`
	Context              RegenerationContext  `yaml:"context"`
	Learnings            *Learnings           `yaml:"learnings_from_previous_generation"`
	EnhancedRequirements EnhancedRequirements `yaml:"enhanced_requirements"`
	Prompt               PromptSection        `yaml:"prompt"`
}

type RegenerationMetadata struct {
	GeneratedBy            string    `yaml:"generated_by"`
	Generation             int       `yaml:"generation"`
	PreviousRunDate        time.Time `yaml:"previous_run_date"`
	CurrentDate            time.Time `yaml:"current_date"`
	ObsolescenceReason     string    `yaml:"obsolescence_reason"`
	CodebaseFingerprintOld string    `yaml:"codebase_fingerprint_old"`
	CodebaseFingerprintNew string    `yaml:"codebase_fingerprint_new"`
}

type RegenerationContext struct {
	CodebaseName     string           `yaml:"codebase_name"`
	CodebasePath     string           `yaml:"codebase_path"`
	OutputDirectory  string           `yaml:"output_directory"`
	PreviousAnalysis PreviousAnalysis `yaml:"previous_analysis"`
	CurrentScan      CurrentScan      `yaml:"current_scan"`
	ChangesDetected  ChangesDetected  `yaml:"changes_detected"`
}

type PreviousAnalysis struct {
	RepositoriesFound  int      `yaml:"repositories_found"`
	PrimaryLanguages   []string `yaml:"primary_languages"`
	TotalFiles         int      `yaml:"total_files"`
	ServicesIdentified int      `yaml:"services_identified"`
}

type CurrentScan struct {
	RepositoriesFound  int      `yaml:"repositories_found"`
	PrimaryLanguages   []string `yaml:"primary_languages"`
	TotalFiles         int      `yaml:"total_files"`
	NewDirectories     []string `yaml:"new_directories,omitempty"`
	RemovedDirectories []string `yaml:"removed_directories,omitempty"`
}

type ChangesDetected struct {
	StructuralChanges   []string `yaml:"structural_changes"`
	NewLanguages        []string `yaml:"new_languages"`
	NewFrameworks       []string `yaml:"new_frameworks"`
	DependencyShifts    []string `yaml:"dependency_shifts"`
	ArchitectureChanges []string `yaml:"architecture_changes"`
}

type EnhancedRequirements struct {
	Phase2ToolEnhancements   []string `yaml:"phase2_tool_enhancements"`
	NewReportTypes           []string `yaml:"new_report_types"`
	BetterDetectionLogic     []string `yaml:"better_detection_logic"`
	PerformanceOptimizations []string `yaml:"performance_optimizations"`
}

type PromptSection struct {
	Instruction string             `yaml:"instruction"`
	Tasks       []RegenerationTask `yaml:"tasks"`
}

type RegenerationTask struct {
	TaskID                   string   `yaml:"task_id"`
	Name                     string   `yaml:"name"`
	Description              string   `yaml:"description"`
	ImprovementsOverPrevious []string `yaml:"improvements_over_previous,omitempty"`
	OutputFormat             string   `yaml:"output_format,omitempty"`
	OutputLocation           string   `yaml:"output_location,omitempty"`
}

// GenerateRegenerationPrompt creates a prompt for regenerating Phase 1 with learnings
func GenerateRegenerationPrompt(
	toolName string,
	toolVersion string,
	generation int,
	codebaseName string,
	codebasePath string,
	oldFingerprint string,
	newFingerprint string,
	obsolescenceReason string,
	learnings *Learnings,
) (*RegenerationPrompt, error) {

	prompt := &RegenerationPrompt{
		Version: "2.0",
		Purpose: "Regenerate Phase 1 analysis with enhanced understanding from previous tool generation",
		Metadata: RegenerationMetadata{
			GeneratedBy:            fmt.Sprintf("%s v%s", toolName, toolVersion),
			Generation:             generation,
			PreviousRunDate:        learnings.Metadata.RunDate,
			CurrentDate:            time.Now(),
			ObsolescenceReason:     obsolescenceReason,
			CodebaseFingerprintOld: oldFingerprint,
			CodebaseFingerprintNew: newFingerprint,
		},
		Context: RegenerationContext{
			CodebaseName:    codebaseName,
			CodebasePath:    codebasePath,
			OutputDirectory: fmt.Sprintf("/tmp/codebase-reviewer/%s/", codebaseName),
			PreviousAnalysis: PreviousAnalysis{
				RepositoriesFound:  0, // Will be filled from learnings
				PrimaryLanguages:   []string{},
				TotalFiles:         learnings.ExecutionMetrics.FilesProcessed,
				ServicesIdentified: 0,
			},
			CurrentScan: CurrentScan{
				RepositoriesFound:  0, // Will be filled from current scan
				PrimaryLanguages:   []string{},
				TotalFiles:         0,
				NewDirectories:     learnings.CodebaseChanges.StructuralChanges.NewDirectories,
				RemovedDirectories: learnings.CodebaseChanges.StructuralChanges.RemovedDirectories,
			},
			ChangesDetected: ChangesDetected{
				StructuralChanges:   buildStructuralChangesList(learnings),
				NewLanguages:        learnings.CodebaseChanges.LanguageChanges.NewLanguages,
				NewFrameworks:       learnings.CodebaseChanges.FrameworkChanges.NewFrameworks,
				DependencyShifts:    learnings.CodebaseChanges.DependencyChanges.MajorUpgrades,
				ArchitectureChanges: learnings.CodebaseChanges.ArchitectureChanges.PatternShifts,
			},
		},
		Learnings: learnings,
		EnhancedRequirements: EnhancedRequirements{
			Phase2ToolEnhancements:   learnings.NextGenRecommendations.CodeQualityImprovements,
			NewReportTypes:           learnings.NextGenRecommendations.NewReportTypes,
			BetterDetectionLogic:     learnings.NextGenRecommendations.EnhancedDetections,
			PerformanceOptimizations: learnings.NextGenRecommendations.PerformanceOptimizations,
		},
		Prompt: buildPromptSection(codebaseName, generation, obsolescenceReason, learnings),
	}

	return prompt, nil
}

// SaveRegenerationPrompt writes the regeneration prompt to YAML and Markdown files
func SaveRegenerationPrompt(prompt *RegenerationPrompt, outputDir string) error {
	// Ensure directory exists
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("failed to create output directory: %w", err)
	}

	// Save YAML version
	yamlPath := filepath.Join(outputDir, "phase1-regeneration-prompt.yaml")
	yamlData, err := yaml.Marshal(prompt)
	if err != nil {
		return fmt.Errorf("failed to marshal prompt to YAML: %w", err)
	}
	if err := os.WriteFile(yamlPath, yamlData, 0644); err != nil {
		return fmt.Errorf("failed to write YAML prompt: %w", err)
	}

	// Save Markdown version (human-readable)
	mdPath := filepath.Join(outputDir, "phase1-regeneration-prompt.md")
	mdContent := formatPromptAsMarkdown(prompt)
	if err := os.WriteFile(mdPath, []byte(mdContent), 0644); err != nil {
		return fmt.Errorf("failed to write Markdown prompt: %w", err)
	}

	return nil
}

func buildStructuralChangesList(l *Learnings) []string {
	changes := []string{}
	if len(l.CodebaseChanges.StructuralChanges.NewDirectories) > 0 {
		changes = append(changes, fmt.Sprintf("Added %d new directories", len(l.CodebaseChanges.StructuralChanges.NewDirectories)))
	}
	if len(l.CodebaseChanges.StructuralChanges.RemovedDirectories) > 0 {
		changes = append(changes, fmt.Sprintf("Removed %d directories", len(l.CodebaseChanges.StructuralChanges.RemovedDirectories)))
	}
	return changes
}

func buildPromptSection(codebaseName string, generation int, reason string, l *Learnings) PromptSection {
	instruction := fmt.Sprintf(`You are tasked with regenerating the Phase 1 codebase analysis for %s.
This is GENERATION %d of the analysis.

The previous Phase 2 tools have detected obsolescence due to: %s

Your task is to create an IMPROVED Phase 1 analysis that incorporates all learnings from the previous generation.`,
		codebaseName, generation, reason)

	return PromptSection{
		Instruction: instruction,
		Tasks:       buildRegenerationTasks(codebaseName, l),
	}
}

func buildRegenerationTasks(_ string, l *Learnings) []RegenerationTask {
	// Build tasks based on learnings
	return []RegenerationTask{
		{
			TaskID:                   "T1-REGEN",
			Name:                     "Enhanced Deep Scan",
			Description:              "Perform comprehensive scan with improvements from previous generation",
			ImprovementsOverPrevious: extractImprovements(l, "scanning"),
		},
		{
			TaskID:                   "T2-REGEN",
			Name:                     "Enhanced Reference Materials",
			Description:              "Generate improved reference materials based on learnings",
			ImprovementsOverPrevious: extractImprovements(l, "documentation"),
		},
		{
			TaskID:                   "T3-REGEN",
			Name:                     "Enhanced Phase 2 Tools",
			Description:              "Generate improved Phase 2 tools with better detection and performance",
			ImprovementsOverPrevious: extractImprovements(l, "tools"),
		},
	}
}

func extractImprovements(l *Learnings, category string) []string {
	improvements := []string{}
	for _, imp := range l.Improvements {
		if strings.Contains(strings.ToLower(imp.Category), category) {
			improvements = append(improvements, imp.Description)
		}
	}
	return improvements
}

// formatPromptAsMarkdown converts the regeneration prompt to human-readable Markdown.
func formatPromptAsMarkdown(p *RegenerationPrompt) string {
	var b strings.Builder

	b.WriteString("# Phase 1 Regeneration Prompt\n\n")
	b.WriteString(fmt.Sprintf("**Version:** %s\n", p.Version))
	b.WriteString(fmt.Sprintf("**Purpose:** %s\n\n", p.Purpose))

	// Metadata section
	b.WriteString("## Metadata\n\n")
	b.WriteString(fmt.Sprintf("- **Generated By:** %s\n", p.Metadata.GeneratedBy))
	b.WriteString(fmt.Sprintf("- **Generation:** %d\n", p.Metadata.Generation))
	b.WriteString(fmt.Sprintf("- **Previous Run:** %s\n", p.Metadata.PreviousRunDate.Format(time.RFC3339)))
	b.WriteString(fmt.Sprintf("- **Current Date:** %s\n", p.Metadata.CurrentDate.Format(time.RFC3339)))
	b.WriteString(fmt.Sprintf("- **Obsolescence Reason:** %s\n\n", p.Metadata.ObsolescenceReason))

	// Context section
	b.WriteString("## Context\n\n")
	b.WriteString(fmt.Sprintf("- **Codebase:** %s\n", p.Context.CodebaseName))
	b.WriteString(fmt.Sprintf("- **Path:** %s\n", p.Context.CodebasePath))
	b.WriteString(fmt.Sprintf("- **Output Directory:** %s\n\n", p.Context.OutputDirectory))

	// Changes detected
	b.WriteString("## Changes Detected\n\n")
	if len(p.Context.ChangesDetected.StructuralChanges) > 0 {
		b.WriteString("### Structural Changes\n")
		for _, c := range p.Context.ChangesDetected.StructuralChanges {
			b.WriteString(fmt.Sprintf("- %s\n", c))
		}
		b.WriteString("\n")
	}
	if len(p.Context.ChangesDetected.NewLanguages) > 0 {
		b.WriteString("### New Languages\n")
		for _, l := range p.Context.ChangesDetected.NewLanguages {
			b.WriteString(fmt.Sprintf("- %s\n", l))
		}
		b.WriteString("\n")
	}
	if len(p.Context.ChangesDetected.NewFrameworks) > 0 {
		b.WriteString("### New Frameworks\n")
		for _, f := range p.Context.ChangesDetected.NewFrameworks {
			b.WriteString(fmt.Sprintf("- %s\n", f))
		}
		b.WriteString("\n")
	}

	// Enhanced requirements
	b.WriteString("## Enhanced Requirements\n\n")
	if len(p.EnhancedRequirements.Phase2ToolEnhancements) > 0 {
		b.WriteString("### Tool Enhancements\n")
		for _, e := range p.EnhancedRequirements.Phase2ToolEnhancements {
			b.WriteString(fmt.Sprintf("- %s\n", e))
		}
		b.WriteString("\n")
	}

	// Tasks
	b.WriteString("## Tasks\n\n")
	b.WriteString(p.Prompt.Instruction)
	b.WriteString("\n\n")
	for _, task := range p.Prompt.Tasks {
		b.WriteString(fmt.Sprintf("### %s (%s)\n\n", task.Name, task.TaskID))
		b.WriteString(task.Description)
		b.WriteString("\n")
		if len(task.ImprovementsOverPrevious) > 0 {
			b.WriteString("\n**Improvements:**\n")
			for _, imp := range task.ImprovementsOverPrevious {
				b.WriteString(fmt.Sprintf("- %s\n", imp))
			}
		}
		b.WriteString("\n")
	}

	return b.String()
}

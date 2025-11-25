# Phase 2 Tools for CallBox - Generation 1

I'll generate a complete, self-contained Go tool that analyzes the CallBox codebase and generates comprehensive documentation offline.

## File Structure

```
phase2-tools-gen1/
├── cmd/generate-docs/main.go
├── pkg/
│   ├── analyzer/analyzer.go
│   ├── generator/generator.go
│   ├── metrics/tracker.go
│   ├── obsolescence/detector.go
│   └── metaprompt/metaprompt.go
├── go.mod
└── README.md
```

---

## File: go.mod

```go
module github.com/bordenet/codebase-reviewer/phase2-tools

go 1.21

require (
	gopkg.in/yaml.v3 v3.0.1
)
```

---

## File: cmd/generate-docs/main.go

```go
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/bordenet/codebase-reviewer/phase2-tools/pkg/analyzer"
	"github.com/bordenet/codebase-reviewer/phase2-tools/pkg/generator"
	"github.com/bordenet/codebase-reviewer/phase2-tools/pkg/metrics"
	"github.com/bordenet/codebase-reviewer/phase2-tools/pkg/obsolescence"
	"github.com/bordenet/codebase-reviewer/phase2-tools/pkg/metaprompt"
)

const (
	VERSION    = "1.0.0"
	GENERATION = 1
)

func main() {
	// Parse flags
	codebasePath := flag.String("path", "", "Path to codebase to analyze")
	outputPath := flag.String("output", "", "Output path for documentation (default: /tmp/codebase-docs)")
	checkObsolescence := flag.Bool("check-obsolescence", true, "Check if tool is obsolete")
	verbose := flag.Bool("v", false, "Verbose output")
	flag.Parse()

	if *codebasePath == "" {
		fmt.Println("Usage: generate-docs --path <codebase-path>")
		flag.PrintDefaults()
		os.Exit(1)
	}

	// Set default output path
	if *outputPath == "" {
		*outputPath = "/tmp/codebase-docs"
	}

	fmt.Printf("🚀 CallBox Documentation Generator - Gen %d\n", GENERATION)
	fmt.Printf("   Version: %s\n", VERSION)
	fmt.Printf("   Codebase: %s\n", *codebasePath)
	fmt.Printf("   Output: %s\n\n", *outputPath)

	// Step 1: Analyze codebase
	fmt.Println("📊 Analyzing codebase...")
	analysis, err := analyzer.Analyze(*codebasePath, *verbose)
	if err != nil {
		fmt.Printf("❌ Analysis failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Analysis complete: %d files, %d repos\n\n", analysis.FileCount, analysis.RepoCount)

	// Step 2: Generate documentation
	fmt.Println("📝 Generating documentation...")
	docs, err := generator.Generate(analysis, *verbose)
	if err != nil {
		fmt.Printf("❌ Documentation generation failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Documentation generated: %d sections\n\n", len(docs.Sections))

	// Step 3: Write documentation
	fmt.Println("💾 Writing documentation...")
	if err := writeDocs(*outputPath, docs); err != nil {
		fmt.Printf("❌ Failed to write documentation: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Documentation written to: %s\n\n", *outputPath)

	// Step 4: Track metrics
	fmt.Println("📈 Tracking metrics...")
	m := metrics.Track(analysis, docs)
	if err := m.Save(filepath.Join(*outputPath, "metrics.json")); err != nil {
		fmt.Printf("⚠️  Warning: Failed to save metrics: %v\n", err)
	} else {
		fmt.Printf("✅ Metrics saved\n\n")
	}

	// Step 5: Check obsolescence
	if *checkObsolescence {
		fmt.Println("🔍 Checking obsolescence...")
		detector := obsolescence.NewDetector(GENERATION, "CallBox")
		isObsolete, reasons := detector.Check(m, *codebasePath)

		if isObsolete {
			fmt.Println("\n⚠️  OBSOLESCENCE DETECTED!")
			fmt.Println("\nReasons:")
			for _, reason := range reasons {
				fmt.Printf("  - %s\n", reason)
			}

			// Emit regeneration prompt
			fmt.Println("\n🔄 Generating regeneration prompt...")
			promptPath, err := metaprompt.EmitRegenerationPrompt(GENERATION, "CallBox", m, reasons)
			if err != nil {
				fmt.Printf("❌ Failed to emit regeneration prompt: %v\n", err)
			} else {
				fmt.Printf("\n📋 Regeneration prompt saved to:\n   %s\n\n", promptPath)
				fmt.Println("Next steps:")
				fmt.Println("  1. Review the regeneration prompt")
				fmt.Println("  2. Give it to your AI assistant")
				fmt.Println("  3. AI will generate Gen 2 tools")
				fmt.Println("  4. Replace this tool with Gen 2 tools")
			}
		} else {
			fmt.Println("✅ Tool is up-to-date\n")
		}
	}

	fmt.Println("🎉 Done!")
}

func writeDocs(outputPath string, docs *generator.Documentation) error {
	// Create output directory
	if err := os.MkdirAll(outputPath, 0755); err != nil {
		return err
	}

	// Write main documentation
	mainPath := filepath.Join(outputPath, "README.md")
	if err := os.WriteFile(mainPath, []byte(docs.MainDoc), 0644); err != nil {
		return err
	}

	// Write section files
	for name, content := range docs.Sections {
		sectionPath := filepath.Join(outputPath, fmt.Sprintf("%s.md", name))
		if err := os.WriteFile(sectionPath, []byte(content), 0644); err != nil {
			return err
		}
	}

	return nil
}
```

---

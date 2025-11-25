package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/bordenet/codebase-reviewer/internal/scanner"
	"github.com/bordenet/codebase-reviewer/internal/prompt"
	"github.com/bordenet/codebase-reviewer/pkg/logger"
)

const (
	version = "1.0.0"
	appName = "generate-docs"
)

var (
	verbose bool
	scorch  bool
	review  bool
	help    bool
)

func init() {
	flag.BoolVar(&verbose, "v", false, "Enable verbose logging")
	flag.BoolVar(&verbose, "verbose", false, "Enable verbose logging")
	flag.BoolVar(&scorch, "scorch", false, "Force full rebuild of reference materials and Phase 2 tools")
	flag.BoolVar(&review, "review", false, "Review existing Phase 2 tools for viability")
	flag.BoolVar(&help, "h", false, "Show help message")
	flag.BoolVar(&help, "help", false, "Show help message")
}

func main() {
	flag.Parse()

	if help {
		printHelp()
		os.Exit(0)
	}

	// Initialize logger
	log := logger.New(verbose)

	// Get target path from args
	args := flag.Args()
	if len(args) == 0 {
		log.Error("No target path provided")
		printUsage()
		os.Exit(1)
	}

	targetPath := args[0]

	// Resolve to absolute path
	absPath, err := filepath.Abs(targetPath)
	if err != nil {
		log.Error("Failed to resolve path: %v", err)
		os.Exit(1)
	}

	// Verify path exists
	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		log.Error("Path does not exist: %s", absPath)
		os.Exit(1)
	}

	log.Info("Codebase Reviewer - Phase 1")
	log.Info("Version: %s", version)
	log.Info("Target: %s", absPath)
	log.Info("Scorch mode: %v", scorch)
	log.Info("Review mode: %v", review)
	log.Info("")

	// Security check: ensure we're not running inside the tool's own repo
	if err := validateNotSelfScan(absPath); err != nil {
		log.Error("Security check failed: %v", err)
		os.Exit(1)
	}

	// Scan for nested git repositories
	log.Info("Scanning for git repositories...")
	repos, err := scanner.FindGitRepos(absPath, log)
	if err != nil {
		log.Error("Failed to scan for repositories: %v", err)
		os.Exit(1)
	}

	if len(repos) == 0 {
		log.Warn("No git repositories found in %s", absPath)
		log.Info("Treating entire directory as single codebase")
		repos = []scanner.Repository{{Path: absPath, Name: filepath.Base(absPath)}}
	} else {
		log.Info("Found %d git repositories", len(repos))
		for _, repo := range repos {
			log.Info("  - %s", repo.Name)
		}
	}

	// Determine output directory
	outputDir := determineOutputDir(absPath, scorch, log)
	log.Info("Output directory: %s", outputDir)

	// Check if Phase 2 tools already exist
	if !scorch && !review {
		if toolsExist(outputDir) {
			log.Info("Phase 2 tools already exist. Use --scorch to rebuild or --review to validate.")
			log.Info("To regenerate reference materials, run the Phase 2 tools directly.")
			os.Exit(0)
		}
	}

	// Review mode: check if existing tools are still viable
	if review {
		log.Info("Reviewing existing Phase 2 tools...")
		if err := reviewPhase2Tools(outputDir, repos, log); err != nil {
			log.Error("Review failed: %v", err)
			log.Info("Run with --scorch to rebuild tools")
			os.Exit(1)
		}
		log.Info("Phase 2 tools are still viable")
		os.Exit(0)
	}

	// Generate LLM prompt
	log.Info("Generating LLM prompt for codebase analysis...")
	promptPath, err := prompt.Generate(absPath, repos, outputDir, verbose, scorch, log)
	if err != nil {
		log.Error("Failed to generate prompt: %v", err)
		os.Exit(1)
	}

	log.Info("")
	log.Info("✓ Phase 1 complete!")
	log.Info("")
	log.Info("Next steps:")
	log.Info("1. Open the generated prompt in your AI assistant:")
	log.Info("   %s", promptPath)
	log.Info("")
	log.Info("2. The AI will:")
	log.Info("   - Analyze the codebase")
	log.Info("   - Generate Phase 2 tools")
	log.Info("   - Create initial reference materials")
	log.Info("")
	log.Info("3. After AI completes, you can regenerate docs anytime by running:")
	log.Info("   %s/phase2-tools/bin/update-docs", outputDir)
	log.Info("")
	log.Info("SECURITY REMINDER: All outputs are in /tmp or .gitignore'd locations")
	log.Info("                   DO NOT commit proprietary analysis results to git")
}

func printUsage() {
	fmt.Fprintf(os.Stderr, "Usage: %s [OPTIONS] <target-path>\n", appName)
	fmt.Fprintf(os.Stderr, "\nOptions:\n")
	flag.PrintDefaults()
}

func printHelp() {
	fmt.Printf("%s - Codebase Documentation Generator (Phase 1)\n", appName)
	fmt.Printf("Version: %s\n\n", version)
	fmt.Printf("DESCRIPTION:\n")
	fmt.Printf("  Analyzes a codebase and generates an LLM prompt for creating automated\n")
	fmt.Printf("  documentation tools (Phase 2) and reference materials.\n\n")
	fmt.Printf("USAGE:\n")
	fmt.Printf("  %s [OPTIONS] <target-path>\n\n", appName)
	fmt.Printf("OPTIONS:\n")
	fmt.Printf("  -v, --verbose    Enable verbose logging\n")
	fmt.Printf("  -h, --help       Show this help message\n")
	fmt.Printf("  --scorch         Force full rebuild of Phase 2 tools and reference materials\n")
	fmt.Printf("  --review         Review existing Phase 2 tools to verify they're still viable\n\n")
	fmt.Printf("EXAMPLES:\n")
	fmt.Printf("  # Analyze a codebase with verbose output\n")
	fmt.Printf("  %s -v /Users/matt/projects/my-app\n\n", appName)
	fmt.Printf("  # Force rebuild of all tools and documentation\n")
	fmt.Printf("  %s --scorch /Users/matt/projects/my-app\n\n", appName)
	fmt.Printf("  # Check if existing tools are still valid\n")
	fmt.Printf("  %s --review /Users/matt/projects/my-app\n\n", appName)
	fmt.Printf("  # Analyze current directory\n")
	fmt.Printf("  %s .\n\n", appName)
	fmt.Printf("SECURITY:\n")
	fmt.Printf("  All outputs are written to /tmp/codebase-reviewer/ or .gitignore'd locations.\n")
	fmt.Printf("  Phase 2 tools and reference materials are considered proprietary and must\n")
	fmt.Printf("  NOT be committed to public repositories.\n\n")
	fmt.Printf("OUTPUT:\n")
	fmt.Printf("  Phase 1 generates an LLM prompt that you provide to your AI assistant.\n")
	fmt.Printf("  The AI will then create Phase 2 tools that can regenerate documentation\n")
	fmt.Printf("  offline without requiring AI assistance.\n\n")
}

func validateNotSelfScan(targetPath string) error {
	// Get the path of this executable
	exePath, err := os.Executable()
	if err != nil {
		return fmt.Errorf("cannot determine executable path: %w", err)
	}

	exeDir := filepath.Dir(exePath)

	// Check if target is within the tool's directory
	relPath, err := filepath.Rel(exeDir, targetPath)
	if err == nil && !filepath.IsAbs(relPath) && len(relPath) > 0 && relPath[0] != '.' {
		return fmt.Errorf("cannot scan the codebase-reviewer tool's own directory")
	}

	return nil
}

func determineOutputDir(targetPath string, scorch bool, log *logger.Logger) string {
	// Use codebase name as subdirectory
	codebaseName := filepath.Base(targetPath)
	outputDir := filepath.Join("/tmp", "codebase-reviewer", codebaseName)

	// If scorch mode, remove existing output
	if scorch {
		if _, err := os.Stat(outputDir); err == nil {
			log.Info("Scorch mode: removing existing output directory")
			if err := os.RemoveAll(outputDir); err != nil {
				log.Warn("Failed to remove existing output: %v", err)
			}
		}
	}

	// Create output directory
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		log.Error("Failed to create output directory: %v", err)
		os.Exit(1)
	}

	return outputDir
}

func toolsExist(outputDir string) bool {
	toolsDir := filepath.Join(outputDir, "phase2-tools")
	_, err := os.Stat(toolsDir)
	return err == nil
}

func reviewPhase2Tools(outputDir string, repos []scanner.Repository, log *logger.Logger) error {
	// This will be implemented to validate existing tools
	// For now, return not implemented
	return fmt.Errorf("review mode not yet implemented")
}

package scanner

import (
	"fmt"
	"os"
	"path/filepath"
	"sync"

	"github.com/bordenet/codebase-reviewer/pkg/logger"
)

// Repository represents a discovered git repository
type Repository struct {
	Path        string
	Name        string
	RelativePath string
	HasSubmodules bool
}

// FindGitRepos recursively finds all git repositories under the given path
func FindGitRepos(rootPath string, log *logger.Logger) ([]Repository, error) {
	var repos []Repository
	var mu sync.Mutex

	err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			log.Warn("Error accessing path %s: %v", path, err)
			return nil // Continue walking
		}

		// Skip hidden directories except .git
		if info.IsDir() && len(info.Name()) > 0 && info.Name()[0] == '.' && info.Name() != ".git" {
			return filepath.SkipDir
		}

		// Check if this is a .git directory
		if info.IsDir() && info.Name() == ".git" {
			repoPath := filepath.Dir(path)
			relPath, _ := filepath.Rel(rootPath, repoPath)
			
			repo := Repository{
				Path:         repoPath,
				Name:         filepath.Base(repoPath),
				RelativePath: relPath,
				HasSubmodules: hasSubmodules(repoPath),
			}

			mu.Lock()
			repos = append(repos, repo)
			mu.Unlock()

			log.Debug("Found repository: %s", repo.Name)

			// Don't descend into .git directory
			return filepath.SkipDir
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to walk directory tree: %w", err)
	}

	return repos, nil
}

// hasSubmodules checks if a repository has git submodules
func hasSubmodules(repoPath string) bool {
	submodulesPath := filepath.Join(repoPath, ".gitmodules")
	_, err := os.Stat(submodulesPath)
	return err == nil
}

// AnalyzeRepository performs a detailed analysis of a repository
func AnalyzeRepository(repo Repository, log *logger.Logger) (*RepositoryAnalysis, error) {
	log.Debug("Analyzing repository: %s", repo.Name)

	analysis := &RepositoryAnalysis{
		Repository: repo,
		Languages:  make(map[string]int),
		FileTypes:  make(map[string]int),
	}

	// Count files by language/type
	err := filepath.Walk(repo.Path, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}

		// Skip hidden directories and common ignore patterns
		if info.IsDir() {
			name := info.Name()
			if len(name) > 0 && name[0] == '.' {
				return filepath.SkipDir
			}
			if name == "node_modules" || name == "vendor" || name == "dist" || name == "build" {
				return filepath.SkipDir
			}
		}

		if !info.IsDir() {
			ext := filepath.Ext(path)
			if ext != "" {
				analysis.FileTypes[ext]++
				
				// Map extension to language
				if lang := extensionToLanguage(ext); lang != "" {
					analysis.Languages[lang]++
				}
			}
			analysis.TotalFiles++
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to analyze repository: %w", err)
	}

	return analysis, nil
}

// RepositoryAnalysis contains analysis results for a repository
type RepositoryAnalysis struct {
	Repository  Repository
	Languages   map[string]int
	FileTypes   map[string]int
	TotalFiles  int
}

// extensionToLanguage maps file extensions to programming languages
func extensionToLanguage(ext string) string {
	langMap := map[string]string{
		".go":    "Go",
		".js":    "JavaScript",
		".ts":    "TypeScript",
		".py":    "Python",
		".java":  "Java",
		".c":     "C",
		".cpp":   "C++",
		".cs":    "C#",
		".rb":    "Ruby",
		".php":   "PHP",
		".swift": "Swift",
		".kt":    "Kotlin",
		".rs":    "Rust",
		".scala": "Scala",
		".sh":    "Shell",
		".sql":   "SQL",
		".yaml":  "YAML",
		".yml":   "YAML",
		".json":  "JSON",
		".xml":   "XML",
		".html":  "HTML",
		".css":   "CSS",
		".scss":  "SCSS",
		".md":    "Markdown",
	}

	return langMap[ext]
}

// PrimaryLanguage returns the most common language in the analysis
func (a *RepositoryAnalysis) PrimaryLanguage() string {
	var maxLang string
	var maxCount int

	for lang, count := range a.Languages {
		if count > maxCount {
			maxCount = count
			maxLang = lang
		}
	}

	return maxLang
}


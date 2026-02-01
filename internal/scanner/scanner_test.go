package scanner

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/bordenet/codebase-reviewer/pkg/logger"
)

func TestFindGitRepos(t *testing.T) {
	log := logger.New(false)

	tests := []struct {
		name      string
		setup     func(t *testing.T) string
		wantCount int
		wantErr   bool
	}{
		{
			name: "empty directory",
			setup: func(t *testing.T) string {
				dir := t.TempDir()
				return dir
			},
			wantCount: 0,
			wantErr:   false,
		},
		{
			name: "single git repo",
			setup: func(t *testing.T) string {
				dir := t.TempDir()
				gitDir := filepath.Join(dir, ".git")
				if err := os.Mkdir(gitDir, 0755); err != nil {
					t.Fatal(err)
				}
				return dir
			},
			wantCount: 1,
			wantErr:   false,
		},
		{
			name: "nested git repos",
			setup: func(t *testing.T) string {
				dir := t.TempDir()
				// Root repo
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Nested repo
				nested := filepath.Join(dir, "subproject")
				if err := os.MkdirAll(filepath.Join(nested, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				return dir
			},
			wantCount: 2,
			wantErr:   false,
		},
		{
			name: "repo with submodules",
			setup: func(t *testing.T) string {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create .gitmodules file
				if err := os.WriteFile(filepath.Join(dir, ".gitmodules"), []byte("[submodule]"), 0644); err != nil {
					t.Fatal(err)
				}
				return dir
			},
			wantCount: 1,
			wantErr:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			dir := tt.setup(t)
			repos, err := FindGitRepos(dir, log)

			if (err != nil) != tt.wantErr {
				t.Errorf("FindGitRepos() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if len(repos) != tt.wantCount {
				t.Errorf("FindGitRepos() got %d repos, want %d", len(repos), tt.wantCount)
			}
		})
	}
}

func TestHasSubmodules(t *testing.T) {
	tests := []struct {
		name  string
		setup func(t *testing.T) string
		want  bool
	}{
		{
			name: "no submodules",
			setup: func(t *testing.T) string {
				return t.TempDir()
			},
			want: false,
		},
		{
			name: "has submodules",
			setup: func(t *testing.T) string {
				dir := t.TempDir()
				if err := os.WriteFile(filepath.Join(dir, ".gitmodules"), []byte("[submodule]"), 0644); err != nil {
					t.Fatal(err)
				}
				return dir
			},
			want: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			dir := tt.setup(t)
			if got := hasSubmodules(dir); got != tt.want {
				t.Errorf("hasSubmodules() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestExtensionToLanguage(t *testing.T) {
	tests := []struct {
		ext  string
		want string
	}{
		{".go", "Go"},
		{".py", "Python"},
		{".js", "JavaScript"},
		{".ts", "TypeScript"},
		{".tsx", "TypeScript"},
		{".java", "Java"},
		{".rs", "Rust"},
		{".unknown", ""},
		{"", ""},
	}

	for _, tt := range tests {
		t.Run(tt.ext, func(t *testing.T) {
			if got := extensionToLanguage(tt.ext); got != tt.want {
				t.Errorf("extensionToLanguage(%q) = %q, want %q", tt.ext, got, tt.want)
			}
		})
	}
}

func TestAnalyzeRepository(t *testing.T) {
	log := logger.New(false)

	tests := []struct {
		name          string
		setup         func(t *testing.T) Repository
		wantLangs     map[string]int
		wantFileCount int
		wantErr       bool
	}{
		{
			name: "empty repository",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "empty-repo", RelativePath: "."}
			},
			wantLangs:     map[string]int{},
			wantFileCount: 0,
			wantErr:       false,
		},
		{
			name: "repository with Go files",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create Go files
				if err := os.WriteFile(filepath.Join(dir, "main.go"), []byte("package main"), 0644); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(dir, "utils.go"), []byte("package main"), 0644); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "go-repo", RelativePath: "."}
			},
			wantLangs:     map[string]int{"Go": 2},
			wantFileCount: 2,
			wantErr:       false,
		},
		{
			name: "repository with multiple languages",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create files in different languages
				if err := os.WriteFile(filepath.Join(dir, "main.go"), []byte("package main"), 0644); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(dir, "app.py"), []byte("print('hello')"), 0644); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(dir, "index.js"), []byte("console.log('hi')"), 0644); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(dir, "app.ts"), []byte("const x = 1"), 0644); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "multi-lang-repo", RelativePath: "."}
			},
			wantLangs:     map[string]int{"Go": 1, "Python": 1, "JavaScript": 1, "TypeScript": 1},
			wantFileCount: 4,
			wantErr:       false,
		},
		{
			name: "repository skips node_modules",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create source file
				if err := os.WriteFile(filepath.Join(dir, "index.js"), []byte("console.log('hi')"), 0644); err != nil {
					t.Fatal(err)
				}
				// Create node_modules (should be skipped)
				nodeModules := filepath.Join(dir, "node_modules")
				if err := os.MkdirAll(nodeModules, 0755); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(nodeModules, "lodash.js"), []byte("// lodash"), 0644); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "js-repo", RelativePath: "."}
			},
			wantLangs:     map[string]int{"JavaScript": 1},
			wantFileCount: 1,
			wantErr:       false,
		},
		{
			name: "repository skips vendor directory",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create source file
				if err := os.WriteFile(filepath.Join(dir, "main.go"), []byte("package main"), 0644); err != nil {
					t.Fatal(err)
				}
				// Create vendor directory (should be skipped)
				vendor := filepath.Join(dir, "vendor")
				if err := os.MkdirAll(vendor, 0755); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(vendor, "dep.go"), []byte("package dep"), 0644); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "go-with-vendor", RelativePath: "."}
			},
			wantLangs:     map[string]int{"Go": 1},
			wantFileCount: 1,
			wantErr:       false,
		},
		{
			name: "repository skips hidden directories",
			setup: func(t *testing.T) Repository {
				dir := t.TempDir()
				if err := os.Mkdir(filepath.Join(dir, ".git"), 0755); err != nil {
					t.Fatal(err)
				}
				// Create source file
				if err := os.WriteFile(filepath.Join(dir, "main.py"), []byte("print('hello')"), 0644); err != nil {
					t.Fatal(err)
				}
				// Create hidden directory (should be skipped)
				hidden := filepath.Join(dir, ".hidden")
				if err := os.MkdirAll(hidden, 0755); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(filepath.Join(hidden, "secret.py"), []byte("# secret"), 0644); err != nil {
					t.Fatal(err)
				}
				return Repository{Path: dir, Name: "py-repo", RelativePath: "."}
			},
			wantLangs:     map[string]int{"Python": 1},
			wantFileCount: 1,
			wantErr:       false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			repo := tt.setup(t)
			analysis, err := AnalyzeRepository(repo, log)

			if (err != nil) != tt.wantErr {
				t.Errorf("AnalyzeRepository() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if err != nil {
				return
			}

			if analysis.TotalFiles != tt.wantFileCount {
				t.Errorf("AnalyzeRepository() TotalFiles = %d, want %d", analysis.TotalFiles, tt.wantFileCount)
			}

			// Check languages match
			for lang, wantCount := range tt.wantLangs {
				if gotCount := analysis.Languages[lang]; gotCount != wantCount {
					t.Errorf("AnalyzeRepository() Languages[%s] = %d, want %d", lang, gotCount, wantCount)
				}
			}

			// Check no extra languages
			for lang := range analysis.Languages {
				if _, ok := tt.wantLangs[lang]; !ok {
					t.Errorf("AnalyzeRepository() unexpected language: %s", lang)
				}
			}
		})
	}
}

func TestPrimaryLanguage(t *testing.T) {
	tests := []struct {
		name      string
		languages map[string]int
		want      string
	}{
		{
			name:      "empty languages",
			languages: map[string]int{},
			want:      "",
		},
		{
			name:      "single language",
			languages: map[string]int{"Go": 10},
			want:      "Go",
		},
		{
			name:      "multiple languages - Go dominant",
			languages: map[string]int{"Go": 50, "Python": 10, "JavaScript": 5},
			want:      "Go",
		},
		{
			name:      "multiple languages - Python dominant",
			languages: map[string]int{"Go": 5, "Python": 100, "JavaScript": 20},
			want:      "Python",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			analysis := &RepositoryAnalysis{
				Languages: tt.languages,
			}
			if got := analysis.PrimaryLanguage(); got != tt.want {
				t.Errorf("PrimaryLanguage() = %q, want %q", got, tt.want)
			}
		})
	}
}

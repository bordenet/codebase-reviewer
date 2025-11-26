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

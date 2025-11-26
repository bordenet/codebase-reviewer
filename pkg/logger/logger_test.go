package logger

import (
	"bytes"
	"strings"
	"testing"
)

func TestNew(t *testing.T) {
	tests := []struct {
		name    string
		verbose bool
		want    Level
	}{
		{"non-verbose", false, LevelInfo},
		{"verbose", true, LevelDebug},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			log := New(tt.verbose)
			if log.level != tt.want {
				t.Errorf("New(%v) level = %v, want %v", tt.verbose, log.level, tt.want)
			}
		})
	}
}

func TestNewWithWriter(t *testing.T) {
	var buf bytes.Buffer
	log := NewWithWriter(&buf, true)

	log.Info("test message")

	if !strings.Contains(buf.String(), "test message") {
		t.Errorf("expected buffer to contain 'test message', got %q", buf.String())
	}
	if !strings.Contains(buf.String(), "[INFO]") {
		t.Errorf("expected buffer to contain '[INFO]', got %q", buf.String())
	}
}

func TestLogLevels(t *testing.T) {
	tests := []struct {
		name       string
		logLevel   Level
		logMethod  string
		shouldLog  bool
	}{
		{"debug at debug level", LevelDebug, "debug", true},
		{"info at debug level", LevelDebug, "info", true},
		{"warn at debug level", LevelDebug, "warn", true},
		{"error at debug level", LevelDebug, "error", true},
		{"debug at info level", LevelInfo, "debug", false},
		{"info at info level", LevelInfo, "info", true},
		{"warn at info level", LevelInfo, "warn", true},
		{"error at info level", LevelInfo, "error", true},
		{"debug at warn level", LevelWarn, "debug", false},
		{"info at warn level", LevelWarn, "info", false},
		{"warn at warn level", LevelWarn, "warn", true},
		{"error at warn level", LevelWarn, "error", true},
		{"debug at error level", LevelError, "debug", false},
		{"info at error level", LevelError, "info", false},
		{"warn at error level", LevelError, "warn", false},
		{"error at error level", LevelError, "error", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			log := NewWithWriter(&buf, false)
			log.SetLevel(tt.logLevel)

			switch tt.logMethod {
			case "debug":
				log.Debug("test")
			case "info":
				log.Info("test")
			case "warn":
				log.Warn("test")
			case "error":
				log.Error("test")
			}

			hasOutput := buf.Len() > 0
			if hasOutput != tt.shouldLog {
				t.Errorf("expected shouldLog=%v, got output=%v", tt.shouldLog, hasOutput)
			}
		})
	}
}

func TestLogFormatting(t *testing.T) {
	var buf bytes.Buffer
	log := NewWithWriter(&buf, false)

	log.Info("value is %d", 42)

	output := buf.String()
	if !strings.Contains(output, "value is 42") {
		t.Errorf("expected formatted message, got %q", output)
	}
}

func TestSetLevel(t *testing.T) {
	log := New(false)

	if log.level != LevelInfo {
		t.Errorf("expected initial level Info, got %v", log.level)
	}

	log.SetLevel(LevelDebug)
	if log.level != LevelDebug {
		t.Errorf("expected level Debug after SetLevel, got %v", log.level)
	}

	log.SetLevel(LevelError)
	if log.level != LevelError {
		t.Errorf("expected level Error after SetLevel, got %v", log.level)
	}
}

func TestLogTimestamp(t *testing.T) {
	var buf bytes.Buffer
	log := NewWithWriter(&buf, false)

	log.Info("test")

	output := buf.String()
	// Check for timestamp format: [YYYY-MM-DD HH:MM:SS]
	if !strings.Contains(output, "[20") { // Year starts with 20
		t.Errorf("expected timestamp in output, got %q", output)
	}
}

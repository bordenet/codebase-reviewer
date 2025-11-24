package logger

import (
	"fmt"
	"io"
	"log"
	"os"
	"time"
)

// Level represents logging level
type Level int

const (
	// LevelDebug for detailed debugging information
	LevelDebug Level = iota
	// LevelInfo for general informational messages
	LevelInfo
	// LevelWarn for warning messages
	LevelWarn
	// LevelError for error messages
	LevelError
)

// Logger provides structured logging
type Logger struct {
	level  Level
	logger *log.Logger
}

// New creates a new logger
func New(verbose bool) *Logger {
	level := LevelInfo
	if verbose {
		level = LevelDebug
	}

	return &Logger{
		level:  level,
		logger: log.New(os.Stdout, "", 0),
	}
}

// NewWithWriter creates a logger with a custom writer
func NewWithWriter(w io.Writer, verbose bool) *Logger {
	level := LevelInfo
	if verbose {
		level = LevelDebug
	}

	return &Logger{
		level:  level,
		logger: log.New(w, "", 0),
	}
}

// Debug logs a debug message
func (l *Logger) Debug(format string, args ...interface{}) {
	if l.level <= LevelDebug {
		l.log("DEBUG", format, args...)
	}
}

// Info logs an info message
func (l *Logger) Info(format string, args ...interface{}) {
	if l.level <= LevelInfo {
		l.log("INFO", format, args...)
	}
}

// Warn logs a warning message
func (l *Logger) Warn(format string, args ...interface{}) {
	if l.level <= LevelWarn {
		l.log("WARN", format, args...)
	}
}

// Error logs an error message
func (l *Logger) Error(format string, args ...interface{}) {
	if l.level <= LevelError {
		l.log("ERROR", format, args...)
	}
}

func (l *Logger) log(level, format string, args ...interface{}) {
	timestamp := time.Now().Format("2006-01-02 15:04:05")
	message := fmt.Sprintf(format, args...)
	l.logger.Printf("[%s] [%s] %s", timestamp, level, message)
}

// SetLevel sets the logging level
func (l *Logger) SetLevel(level Level) {
	l.level = level
}


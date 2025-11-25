# Performance Tips & Best Practices

## Overview

This guide provides tips for optimizing Codebase Reviewer performance on large codebases.

## Quick Wins

### 1. Use Specific File Patterns

Instead of analyzing the entire repository, target specific directories:

```bash
# Analyze only source code (skip tests, docs, etc.)
python3 -m codebase_reviewer.cli analyze ./src \
    --format json \
    --output analysis.json
```

### 2. Parallel Processing for Multi-Repo

The multi-repo analyzer uses parallel processing by default:

```bash
# Analyzes repositories in parallel
python3 -m codebase_reviewer.cli multi-repo \
    /path/to/repo1 \
    /path/to/repo2 \
    /path/to/repo3
```

### 3. Use JSON for Large Reports

JSON format is faster than HTML for large codebases:

```bash
# Fastest export format
python3 -m codebase_reviewer.cli analyze /path/to/project \
    --format json \
    --output analysis.json
```

## Performance Benchmarks

### Small Projects (< 10K LOC)
- **Analysis Time**: < 5 seconds
- **Memory Usage**: < 100 MB
- **Recommended Format**: Any

### Medium Projects (10K - 100K LOC)
- **Analysis Time**: 10-30 seconds
- **Memory Usage**: 100-500 MB
- **Recommended Format**: JSON or HTML

### Large Projects (100K - 1M LOC)
- **Analysis Time**: 30-120 seconds
- **Memory Usage**: 500 MB - 2 GB
- **Recommended Format**: JSON (generate HTML separately if needed)

### Very Large Projects (> 1M LOC)
- **Analysis Time**: 2-10 minutes
- **Memory Usage**: 2-8 GB
- **Recommended**: Split into modules and use multi-repo analyzer

## Optimization Strategies

### 1. Exclude Unnecessary Files

Create a `.codebase-reviewer-ignore` file:

```
# Exclude common non-source files
node_modules/
vendor/
dist/
build/
*.min.js
*.bundle.js
```

### 2. Focus on High-Priority Rules

For faster scans, focus on critical and high severity issues:

```bash
# Filter results by severity
python3 -m codebase_reviewer.cli analyze /path/to/project \
    --format json \
    --output analysis.json

# Then filter in post-processing
cat analysis.json | jq '.quality_issues[] | select(.severity == "critical" or .severity == "high")'
```

### 3. Incremental Analysis

For CI/CD, analyze only changed files:

```bash
# Get changed files
CHANGED_FILES=$(git diff --name-only HEAD~1)

# Analyze only changed files
for file in $CHANGED_FILES; do
    python3 -m codebase_reviewer.cli analyze "$file" --format json
done
```

### 4. Use Caching

The tool caches rule compilation for faster subsequent runs:

```bash
# First run: slower (compiles rules)
python3 -m codebase_reviewer.cli analyze /path/to/project

# Subsequent runs: faster (uses cached rules)
python3 -m codebase_reviewer.cli analyze /path/to/project
```

## Memory Optimization

### 1. Process Files in Batches

For very large codebases, process files in batches:

```bash
# Split analysis into batches
find ./src -name "*.py" | split -l 100 - batch_

# Process each batch
for batch in batch_*; do
    python3 -m codebase_reviewer.cli analyze $(cat $batch) --format json
done
```

### 2. Limit Concurrent Processes

For multi-repo analysis, limit concurrent processes:

```python
# In your script
from codebase_reviewer.enterprise.multi_repo_analyzer import MultiRepoAnalyzer

analyzer = MultiRepoAnalyzer(max_workers=4)  # Limit to 4 concurrent processes
```

## CI/CD Optimization

### 1. Use Quality Gates

Fail fast on critical issues:

```yaml
# .github/workflows/codebase-review.yml
- name: Run Analysis
  run: |
    python3 -m codebase_reviewer.cli analyze . \
      --format json \
      --output analysis.json

    # Fail if critical issues found
    CRITICAL=$(cat analysis.json | jq '[.quality_issues[] | select(.severity == "critical")] | length')
    if [ "$CRITICAL" -gt 0 ]; then
      echo "❌ Found $CRITICAL critical issues"
      exit 1
    fi
```

### 2. Cache Dependencies

Cache Python dependencies in CI:

```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

## Troubleshooting

### Issue: Analysis is slow

**Solutions:**
1. Exclude unnecessary files (node_modules, vendor, etc.)
2. Use JSON format instead of HTML
3. Analyze specific directories instead of entire repo
4. Check for very large files (> 10K LOC) and consider splitting them

### Issue: High memory usage

**Solutions:**
1. Process files in batches
2. Limit concurrent processes in multi-repo analysis
3. Use streaming JSON processing for very large results
4. Close other applications during analysis

### Issue: Too many false positives

**Solutions:**
1. Customize rules in YAML files
2. Add file patterns to ignore
3. Adjust severity thresholds
4. Use language-specific rule sets

## Best Practices

1. **Run analysis regularly** - Catch issues early
2. **Use CI/CD integration** - Automate analysis on every commit
3. **Focus on critical issues first** - Don't get overwhelmed
4. **Customize rules** - Tailor to your codebase
5. **Track trends** - Use trend analysis to measure improvement
6. **Share results** - Use interactive HTML reports for team visibility

## Advanced: Custom Rule Performance

### Writing Efficient Rules

```yaml
# Good: Specific pattern
- id: hardcoded-password
  pattern: 'PASSWORD\s*=\s*["\'][^"\']+["\']'

# Bad: Too broad pattern (slow)
- id: any-string
  pattern: '["\'].*["\']'
```

### Rule Optimization Tips

1. **Be specific** - Narrow patterns are faster
2. **Use anchors** - `^` and `$` improve performance
3. **Avoid greedy quantifiers** - Use `+?` instead of `+` when possible
4. **Test patterns** - Use regex testing tools to optimize

## Monitoring

Track analysis performance over time:

```bash
# Time the analysis
time python3 -m codebase_reviewer.cli analyze /path/to/project

# Monitor memory usage
/usr/bin/time -v python3 -m codebase_reviewer.cli analyze /path/to/project
```

## Summary

- **Small projects**: Use any format, no optimization needed
- **Medium projects**: Use JSON, exclude unnecessary files
- **Large projects**: Batch processing, parallel analysis
- **CI/CD**: Quality gates, caching, incremental analysis
- **Custom rules**: Be specific, test patterns, avoid greedy quantifiers

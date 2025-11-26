"""Strategy response generators."""

from typing import Any

from .base import BaseGenerator


class StrategyGenerator(BaseGenerator):
    """Generates strategic planning responses."""

    def testing(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate test strategy response - delegates to testing generator."""
        # This is handled by TestingGenerator.review_tests
        return f"""# Test Strategy

## Summary
Test strategy for `{repository}`.

## Recommendations
1. Implement comprehensive test suite
2. Achieve 80%+ code coverage
3. Add integration and E2E tests
4. Set up CI/CD for automated testing
"""

    def observability(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate observability strategy response."""
        return f"""# Observability & Instrumentation Strategy

## Summary
Developed comprehensive observability strategy for repository at `{repository}`.

## Current Observability State

### Logging
- **Current Approach**: Assess current logging practices
- **Coverage**: Identify gaps in logging coverage
- **Format**: Check for structured vs. unstructured logs

### Metrics
- **Collection**: What metrics are currently collected
- **Storage**: Where metrics are stored
- **Visualization**: How metrics are visualized

### Tracing
- **Distributed Tracing**: Check for tracing implementation
- **Request Correlation**: Verify request ID propagation
- **Performance Profiling**: Assess profiling capabilities

## Gaps & Blind Spots

### Critical Gaps
1. **Missing Logs**: Areas without adequate logging
2. **No Metrics**: Key metrics not being collected
3. **No Tracing**: Lack of distributed tracing
4. **Alert Fatigue**: Too many or too few alerts

## Recommended Instrumentation

### Structured Logging
```python
import structlog

logger = structlog.get_logger()
logger.info("user_action", user_id=123, action="login", status="success")
```

### Key Metrics to Track
1. **Request Metrics**: Rate, errors, duration (RED)
2. **Resource Metrics**: CPU, memory, disk (USE)
3. **Business Metrics**: User actions, conversions
4. **Custom Metrics**: Domain-specific measurements

### Distributed Tracing
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation"):
    # Your code here
    pass
```

## Tooling Recommendations

### Logging Stack
- **Collection**: Fluentd, Logstash
- **Storage**: Elasticsearch, Loki
- **Visualization**: Kibana, Grafana

### Metrics Stack
- **Collection**: Prometheus, StatsD
- **Storage**: Prometheus, InfluxDB
- **Visualization**: Grafana, Datadog

### Tracing Stack
- **Standard**: OpenTelemetry
- **Backend**: Jaeger, Zipkin, Tempo
- **Visualization**: Jaeger UI, Grafana

## Action Items

### 🔴 CRITICAL: Implement Structured Logging
**Action**: Replace unstructured logs with structured, machine-readable format
**Priority**: CRITICAL - Foundation for observability
**Effort**: 4-6 hours

**Step 1**: Install structured logging library
```bash
pip install structlog python-json-logger
```

**Step 2**: Configure structured logging
```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
```

**Success Criteria**:
- [ ] All logs output in JSON format
- [ ] Consistent field names across logs
- [ ] Request IDs included in all logs
- [ ] No print() statements in production code

### 🔴 CRITICAL: Set Up Metrics Collection
**Action**: Implement Prometheus metrics for key application metrics
**Priority**: CRITICAL - Essential for monitoring
**Effort**: 6-8 hours

## Priority Summary
- 🔴 **CRITICAL**: Structured logging (4-6h), Metrics collection (6-8h)
- 🟠 **HIGH**: Distributed tracing (8-12h), Error tracking (4h)
- 🟡 **MEDIUM**: APM integration (6h), Alerting (4h)
- 🟢 **LOW**: Dashboard creation (2-4h)

**Total Effort**: ~34-48 hours for critical/high priority items
"""

    def tech_debt(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate technical debt roadmap response."""
        return f"""# Technical Debt Reduction Roadmap

## Summary
Technical debt assessment and reduction plan for `{repository}`.

## Technical Debt Inventory

### Code Quality Debt
- Complex functions (high cyclomatic complexity)
- Duplicated code
- Missing type hints
- Inconsistent code style

### Architecture Debt
- Tight coupling between modules
- Missing abstraction layers
- Monolithic components
- Circular dependencies

### Testing Debt
- Low test coverage
- Missing integration tests
- Flaky tests
- Slow test suite

### Documentation Debt
- Missing API documentation
- Outdated README
- No architecture diagrams
- Undocumented decisions

## Prioritization Framework

### Impact vs. Effort Matrix
| Item | Impact | Effort | Priority | Timeline |
|------|--------|--------|----------|----------|
| Refactor core module | High | High | P1 | Q2 |
| Add type hints | Medium | Low | P0 | This sprint |
| Improve test coverage | High | Medium | P1 | Next sprint |
| Update documentation | Medium | Low | P2 | Backlog |

## Quick Wins (Low Effort, High Impact)
{self._identify_quick_wins([])}

## Major Refactoring Projects
{self._identify_major_refactoring([])}

## Action Items

### 🔴 CRITICAL: Address Security Debt
**Action**: Fix known security vulnerabilities
**Priority**: CRITICAL
**Effort**: 2-4 hours

### 🟠 HIGH: Reduce Complexity
**Action**: Refactor complex functions
**Priority**: HIGH
**Effort**: 8-12 hours

### 🟡 MEDIUM: Improve Test Coverage
**Action**: Add tests to reach 80% coverage
**Priority**: MEDIUM
**Effort**: 16-24 hours

## Verification Commands

```bash
# Check code complexity
radon cc src/ -a -nb

# Find duplicated code
pylint src/ --disable=all --enable=duplicate-code

# Measure test coverage
pytest --cov=src --cov-report=term-missing
```

## Priority Summary
- 🔴 **CRITICAL**: Security fixes (2-4h)
- 🟠 **HIGH**: Complexity reduction (8-12h), Type hints (4-6h)
- 🟡 **MEDIUM**: Test coverage (16-24h), Documentation (8h)
- 🟢 **LOW**: Code style consistency (4h)

**Total Effort**: ~42-58 hours
"""

    def mentorship(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate team mentorship and knowledge transfer guide."""
        return f"""# Team Mentorship & Knowledge Transfer Guide

## Summary
Comprehensive mentorship and knowledge transfer strategy for `{repository}`.

## Current Knowledge Distribution

### Knowledge Silos Identified
- Critical systems known by single person
- Undocumented tribal knowledge
- Missing onboarding materials
- No knowledge sharing practices

## Mentorship Program Structure

### Onboarding Process
1. **Week 1**: Environment setup, codebase tour
2. **Week 2**: First contributions, code reviews
3. **Week 3**: Feature development, pair programming
4. **Week 4**: Independent work, knowledge check

### Mentorship Pairs
- Senior ↔ Junior pairings
- Rotating pairs quarterly
- Cross-team knowledge sharing
- Buddy system for new hires

### Knowledge Sharing Activities
- Weekly tech talks
- Code review sessions
- Architecture discussions
- Post-mortem reviews

## Action Items

### 🔴 CRITICAL: Create Onboarding Documentation
**Action**: Document setup and architecture
**Priority**: CRITICAL
**Effort**: 8-12 hours

**Step 1**: Create onboarding checklist
```markdown
# Onboarding Checklist

## Day 1
- [ ] Access to repositories
- [ ] Development environment setup
- [ ] Team introductions

## Week 1
- [ ] Codebase architecture overview
- [ ] First code review
- [ ] Pair programming session

## Month 1
- [ ] First feature shipped
- [ ] Knowledge check meeting
- [ ] Feedback session
```

**Success Criteria**:
- [ ] New hires productive within 2 weeks
- [ ] All critical systems documented
- [ ] Knowledge spread across team

### 🟠 HIGH: Establish Mentorship Pairs
**Action**: Create and track mentorship relationships
**Priority**: HIGH
**Effort**: 4-6 hours

### 🟡 MEDIUM: Schedule Tech Talks
**Action**: Regular knowledge sharing sessions
**Priority**: MEDIUM
**Effort**: 2-3 hours setup

## Priority Summary
- 🔴 **CRITICAL**: Onboarding (8-12h), Mentorship (4-6h)
- 🟠 **HIGH**: Tech talks (3-4h), Knowledge base (6-8h)
- 🟡 **MEDIUM**: Pair programming (2-3h)

**Total Effort**: ~23-33 hours for critical/high priority items
"""

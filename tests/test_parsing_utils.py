"""Tests for parsing utilities."""

import pytest
from codebase_reviewer.analyzers.parsing_utils import (
    extract_section,
    extract_list_items,
    extract_code_blocks,
    detect_architecture_pattern,
)


def test_extract_section_basic():
    """Test extracting a basic section."""
    content = """# Main Title

## Features

- Feature 1
- Feature 2

## Installation

Run npm install
"""
    result = extract_section(content, ["features"])
    assert result is not None
    assert "Features" in result
    assert "Feature 1" in result
    assert "Installation" not in result


def test_extract_section_not_found():
    """Test extracting a section that doesn't exist."""
    content = """# Main Title

## Features

- Feature 1
"""
    result = extract_section(content, ["installation", "setup"])
    assert result is None


def test_extract_section_nested():
    """Test extracting a section with nested headers."""
    content = """# Main Title

## Features

### Core Features

- Feature 1

### Advanced Features

- Feature 2

## Installation

Run npm install
"""
    result = extract_section(content, ["features"])
    assert result is not None
    # The function extracts from the matching header until the next same-level header
    # It should contain the Features section content
    assert "Feature" in result
    assert "Installation" not in result


def test_extract_list_items_basic():
    """Test extracting list items."""
    content = """
- Item 1
- Item 2
* Item 3
+ Item 4
"""
    items = extract_list_items(content)
    assert len(items) == 4
    assert "Item 1" in items
    assert "Item 2" in items
    assert "Item 3" in items
    assert "Item 4" in items


def test_extract_list_items_empty():
    """Test extracting list items from content with no lists."""
    content = """
This is just plain text.
No lists here.
"""
    items = extract_list_items(content)
    assert len(items) == 0


def test_extract_code_blocks_basic():
    """Test extracting code blocks."""
    content = """
Some text

```python
print("Hello")
```

More text

```javascript
console.log("World");
```
"""
    blocks = extract_code_blocks(content)
    assert len(blocks) == 2
    assert 'print("Hello")' in blocks[0]
    assert 'console.log("World")' in blocks[1]


def test_extract_code_blocks_no_language():
    """Test extracting code blocks without language specifier."""
    content = """
```
plain code block
```
"""
    blocks = extract_code_blocks(content)
    assert len(blocks) == 1
    assert "plain code block" in blocks[0]


def test_extract_code_blocks_empty():
    """Test extracting code blocks from content with none."""
    content = "Just plain text, no code blocks"
    blocks = extract_code_blocks(content)
    assert len(blocks) == 0


def test_detect_architecture_pattern_microservices():
    """Test detecting microservices architecture."""
    content = "This is a microservices architecture"
    pattern = detect_architecture_pattern(content)
    assert pattern == "microservices"


def test_detect_architecture_pattern_mvc():
    """Test detecting MVC architecture."""
    content = "This application uses the Model-View-Controller pattern"
    pattern = detect_architecture_pattern(content)
    assert pattern == "mvc"


def test_detect_architecture_pattern_serverless():
    """Test detecting serverless architecture."""
    content = "Built with AWS Lambda functions"
    pattern = detect_architecture_pattern(content)
    assert pattern == "serverless"


def test_detect_architecture_pattern_none():
    """Test when no architecture pattern is detected."""
    content = "Just a simple application"
    pattern = detect_architecture_pattern(content)
    assert pattern is None


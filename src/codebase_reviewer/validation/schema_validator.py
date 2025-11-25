"""JSON schema validation for v2.0 outputs."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import jsonschema
    from jsonschema import Draft7Validator, ValidationError

    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


class SchemaValidationError(Exception):
    """Schema validation error."""

    pass


class SchemaValidator:
    """Validates JSON outputs against v2.0 schemas."""

    def __init__(self, schemas_dir: Optional[Path] = None):
        """Initialize validator.

        Args:
            schemas_dir: Directory containing JSON schemas (default: src/codebase_reviewer/schemas/)

        Raises:
            ImportError: If jsonschema package is not installed
        """
        if not JSONSCHEMA_AVAILABLE:
            raise ImportError(
                "jsonschema package is required for schema validation. " "Install with: pip install jsonschema"
            )

        if schemas_dir is None:
            schemas_dir = Path(__file__).parent.parent / "schemas"

        self.schemas_dir = Path(schemas_dir)
        self._schema_cache: Dict[str, Dict[str, Any]] = {}

    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load a JSON schema by name.

        Args:
            schema_name: Name of schema file (e.g., "phase1_task1_output.json")

        Returns:
            Loaded schema as dict

        Raises:
            FileNotFoundError: If schema file doesn't exist
            ValueError: If schema is invalid JSON
        """
        if schema_name in self._schema_cache:
            return self._schema_cache[schema_name]

        schema_path = self.schemas_dir / schema_name

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in schema {schema_name}: {e}") from e

        self._schema_cache[schema_name] = schema
        return schema

    def validate(self, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """Validate data against a schema.

        Args:
            data: Data to validate
            schema_name: Name of schema file

        Returns:
            Tuple of (is_valid, error_messages)
        """
        schema = self.load_schema(schema_name)
        validator = Draft7Validator(schema)

        errors = []
        for error in validator.iter_errors(data):
            # Format error message with path
            path = ".".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"{path}: {error.message}")

        return (len(errors) == 0, errors)

    def validate_task1_output(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate Phase 1 Task 1 output (comprehensive analysis).

        Args:
            data: Output data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "phase1_task1_output.json")

    def validate_task2_output(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate Phase 1 Task 2 output (materials plan).

        Args:
            data: Output data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "phase1_task2_output.json")

    def validate_task3_output(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate Phase 1 Task 3 output (tool specifications).

        Args:
            data: Output data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "phase1_task3_output.json")

    def validate_task5_output(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate Phase 1 Task 5 output (validation plan).

        Args:
            data: Output data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "phase1_task5_output.json")

    def validate_task6_output(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate Phase 1 Task 6 output (security validation report).

        Args:
            data: Output data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "phase1_task6_output.json")

    def validate_metrics(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate metrics structure.

        Args:
            data: Metrics data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "metrics.json")

    def validate_learning(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate learning entry.

        Args:
            data: Learning entry to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        return self.validate(data, "learning.json")

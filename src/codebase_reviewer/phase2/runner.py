"""Phase 2 tool runner - executes generated tools."""

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RunResult:
    """Result of running Phase 2 tools."""

    success: bool
    """Whether the run succeeded."""

    output_dir: Path
    """Directory where docs were generated."""

    stdout: str
    """Standard output from tool."""

    stderr: str
    """Standard error from tool."""

    exit_code: int
    """Exit code from tool."""

    duration_seconds: float
    """How long the run took."""


class Phase2Runner:
    """Runs Phase 2 tools to generate documentation."""

    def run_tools(self, binary_path: Path, codebase_path: Path, verbose: bool = False) -> RunResult:
        """Execute Phase 2 tools to generate documentation.

        Args:
            binary_path: Path to compiled Phase 2 tool binary
            codebase_path: Path to codebase to analyze
            verbose: Whether to run in verbose mode

        Returns:
            RunResult with execution details
        """
        if not binary_path.exists():
            raise FileNotFoundError(f"Binary not found: {binary_path}")

        if not codebase_path.exists():
            raise FileNotFoundError(f"Codebase not found: {codebase_path}")

        print(f"🚀 Running Phase 2 tools...")
        print(f"   Binary: {binary_path}")
        print(f"   Codebase: {codebase_path}")

        # Build command
        cmd = [str(binary_path), str(codebase_path)]
        if verbose:
            cmd.append("-v")

        # Run
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time

        # Determine output directory
        # Phase 2 tools typically write to /tmp/codebase-reviewer/{name}/
        codebase_name = codebase_path.name
        output_dir = Path(f"/tmp/codebase-reviewer/{codebase_name}")

        success = result.returncode == 0

        if success:
            print(f"✅ Phase 2 tools completed successfully")
            print(f"   Duration: {duration:.1f}s")
            print(f"   Output: {output_dir}")
        else:
            print(f"❌ Phase 2 tools failed")
            print(f"   Exit code: {result.returncode}")
            print(f"   Error: {result.stderr[:500]}")

        return RunResult(
            success=success,
            output_dir=output_dir,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            duration_seconds=duration,
        )

    def run_and_validate(
        self,
        binary_path: Path,
        codebase_path: Path,
        expected_files: Optional[list[str]] = None,
    ) -> RunResult:
        """Run tools and validate output.

        Args:
            binary_path: Path to binary
            codebase_path: Path to codebase
            expected_files: Optional list of expected output files

        Returns:
            RunResult

        Raises:
            Exception: If validation fails
        """
        result = self.run_tools(binary_path, codebase_path, verbose=True)

        if not result.success:
            raise Exception(f"Tool execution failed: {result.stderr}")

        # Validate expected files exist
        if expected_files:
            missing = []
            for file_name in expected_files:
                file_path = result.output_dir / file_name
                if not file_path.exists():
                    missing.append(file_name)

            if missing:
                raise Exception(f"Expected output files not found: {', '.join(missing)}")

        return result

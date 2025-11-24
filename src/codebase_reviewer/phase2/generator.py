"""Phase 2 tool generator - extracts and compiles LLM-generated tools."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
import shutil

from ..llm.client import LLMClient, LLMResponse
from ..llm.code_extractor import CodeExtractor


@dataclass
class Phase2Tools:
    """Represents a set of generated Phase 2 tools."""
    
    tools_dir: Path
    """Directory containing the tools."""
    
    binary_path: Optional[Path]
    """Path to compiled binary (if compiled)."""
    
    source_files: Dict[str, str]
    """Map of file path -> content."""
    
    llm_response: LLMResponse
    """Original LLM response."""
    
    generation: int = 1
    """Generation number (1, 2, 3, ...)."""


class Phase2Generator:
    """Generates Phase 2 tools from LLM responses."""
    
    def __init__(self, output_base_dir: Path = Path("/tmp/codebase-reviewer")):
        """Initialize generator.
        
        Args:
            output_base_dir: Base directory for all outputs
        """
        self.output_base_dir = output_base_dir
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_from_llm(
        self,
        codebase_path: Path,
        llm_client: LLMClient,
        phase1_prompt: str,
        generation: int = 1
    ) -> Phase2Tools:
        """Full pipeline: send prompt to LLM, extract code, compile tools.
        
        Args:
            codebase_path: Path to the codebase being analyzed
            llm_client: LLM client to use
            phase1_prompt: Phase 1 prompt to send
            generation: Generation number (1, 2, 3, ...)
            
        Returns:
            Phase2Tools with compiled tools
            
        Raises:
            Exception: If any step fails
        """
        print(f"🤖 Sending Phase 1 prompt to {llm_client.get_provider().value}...")
        print(f"   Model: {llm_client.model}")
        print(f"   Prompt length: {len(phase1_prompt)} chars")
        
        # Send to LLM
        response = llm_client.send_prompt(
            phase1_prompt,
            max_tokens=16000,  # Large response expected
            temperature=0.3,   # Lower temperature for code generation
        )
        
        print(f"✅ LLM response received")
        print(f"   Tokens: {response.tokens_used:,}")
        print(f"   Cost: ${response.cost_usd:.4f}")
        print(f"   Response length: {len(response.content):,} chars")
        
        # Validate response
        if not llm_client.validate_response(response):
            raise Exception("LLM response validation failed (truncated or incomplete)")
        
        # Extract code
        print(f"📦 Extracting Phase 2 tool code...")
        source_files = CodeExtractor.extract_go_files(response.content)
        
        if not source_files:
            raise Exception("No Go code found in LLM response")
        
        print(f"✅ Extracted {len(source_files)} Go files")
        
        # Create tools directory
        codebase_name = codebase_path.name
        tools_dir = self.output_base_dir / codebase_name / f"phase2-tools-gen{generation}"
        
        if tools_dir.exists():
            print(f"⚠️  Removing existing tools directory: {tools_dir}")
            shutil.rmtree(tools_dir)
        
        tools_dir.mkdir(parents=True, exist_ok=True)
        
        # Write source files
        print(f"📝 Writing source files to {tools_dir}...")
        for file_path, content in source_files.items():
            full_path = tools_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            print(f"   ✓ {file_path}")
        
        # Create Phase2Tools object
        phase2_tools = Phase2Tools(
            tools_dir=tools_dir,
            binary_path=None,
            source_files=source_files,
            llm_response=response,
            generation=generation
        )
        
        # Compile tools
        print(f"🔨 Compiling Phase 2 tools...")
        binary_path = self.compile_tools(phase2_tools)
        phase2_tools.binary_path = binary_path
        
        print(f"✅ Phase 2 tools generated successfully!")
        print(f"   Location: {tools_dir}")
        print(f"   Binary: {binary_path}")
        
        return phase2_tools
    
    def compile_tools(self, tools: Phase2Tools) -> Path:
        """Compile Go tools.
        
        Args:
            tools: Phase2Tools to compile
            
        Returns:
            Path to compiled binary
            
        Raises:
            Exception: If compilation fails
        """
        tools_dir = tools.tools_dir
        
        # Initialize go module if needed
        go_mod_path = tools_dir / "go.mod"
        if not go_mod_path.exists():
            print(f"   Initializing go module...")
            result = subprocess.run(
                ["go", "mod", "init", f"phase2-tools-gen{tools.generation}"],
                cwd=tools_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"go mod init failed: {result.stderr}")
        
        # Run go mod tidy
        print(f"   Running go mod tidy...")
        result = subprocess.run(
            ["go", "mod", "tidy"],
            cwd=tools_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⚠️  go mod tidy warning: {result.stderr}")
        
        # Build
        bin_dir = tools_dir / "bin"
        bin_dir.mkdir(exist_ok=True)
        binary_path = bin_dir / "generate-docs"
        
        print(f"   Building binary...")
        result = subprocess.run(
            ["go", "build", "-o", str(binary_path), "./cmd/generate-docs"],
            cwd=tools_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"go build failed:\n{result.stderr}")
        
        if not binary_path.exists():
            raise Exception(f"Binary not created: {binary_path}")
        
        # Make executable
        binary_path.chmod(0o755)
        
        print(f"   ✓ Binary compiled: {binary_path}")
        
        return binary_path


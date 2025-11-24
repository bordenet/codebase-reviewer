"""Compare LLM-generated documentation vs tool-generated documentation."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
import difflib
import re


@dataclass
class ComparisonResult:
    """Result of comparing two documentation outputs."""
    
    llm_doc_path: str
    tool_doc_path: str
    similarity_score: float  # 0.0 to 1.0
    sections_compared: int
    sections_matched: int
    differences: List[Dict[str, str]]
    missing_in_tool: List[str]
    missing_in_llm: List[str]
    quality_assessment: str  # "excellent", "good", "fair", "poor"


class DocumentationComparator:
    """Compare documentation outputs from LLM vs tools."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize comparator.
        
        Args:
            similarity_threshold: Minimum similarity score for "good" quality (default: 0.85)
        """
        self.similarity_threshold = similarity_threshold
    
    def compare(self, llm_doc_path: Path, tool_doc_path: Path) -> ComparisonResult:
        """
        Compare LLM-generated docs vs tool-generated docs.
        
        Args:
            llm_doc_path: Path to LLM-generated documentation
            tool_doc_path: Path to tool-generated documentation
            
        Returns:
            ComparisonResult with detailed comparison
        """
        # Read both documents
        llm_content = self._read_doc(llm_doc_path)
        tool_content = self._read_doc(tool_doc_path)
        
        # Extract sections from both
        llm_sections = self._extract_sections(llm_content)
        tool_sections = self._extract_sections(tool_content)
        
        # Compare sections
        sections_compared = 0
        sections_matched = 0
        differences = []
        missing_in_tool = []
        missing_in_llm = []
        
        # Check sections in LLM doc
        for section_name, llm_section_content in llm_sections.items():
            if section_name in tool_sections:
                sections_compared += 1
                tool_section_content = tool_sections[section_name]
                
                # Calculate similarity
                similarity = self._calculate_similarity(llm_section_content, tool_section_content)
                
                if similarity >= self.similarity_threshold:
                    sections_matched += 1
                else:
                    differences.append({
                        "section": section_name,
                        "similarity": f"{similarity:.2%}",
                        "llm_length": str(len(llm_section_content)),
                        "tool_length": str(len(tool_section_content)),
                    })
            else:
                missing_in_tool.append(section_name)
        
        # Check sections only in tool doc
        for section_name in tool_sections:
            if section_name not in llm_sections:
                missing_in_llm.append(section_name)
        
        # Calculate overall similarity
        overall_similarity = self._calculate_similarity(llm_content, tool_content)
        
        # Assess quality
        quality = self._assess_quality(overall_similarity, sections_matched, sections_compared)
        
        return ComparisonResult(
            llm_doc_path=str(llm_doc_path),
            tool_doc_path=str(tool_doc_path),
            similarity_score=overall_similarity,
            sections_compared=sections_compared,
            sections_matched=sections_matched,
            differences=differences,
            missing_in_tool=missing_in_tool,
            missing_in_llm=missing_in_llm,
            quality_assessment=quality,
        )
    
    def _read_doc(self, path: Path) -> str:
        """Read documentation file."""
        if not path.exists():
            return ""
        return path.read_text(encoding='utf-8', errors='ignore')
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from markdown content."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Check for section headers (## or ###)
            if line.startswith('## ') or line.startswith('### '):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using SequenceMatcher."""
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        
        # Normalize whitespace
        text1 = ' '.join(text1.split())
        text2 = ' '.join(text2.split())
        
        # Use difflib's SequenceMatcher
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return matcher.ratio()
    
    def _assess_quality(self, similarity: float, matched: int, total: int) -> str:
        """Assess overall quality based on similarity and section matching."""
        if similarity >= 0.95 and (total == 0 or matched / total >= 0.95):
            return "excellent"
        elif similarity >= 0.85 and (total == 0 or matched / total >= 0.80):
            return "good"
        elif similarity >= 0.70:
            return "fair"
        else:
            return "poor"


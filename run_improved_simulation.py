#!/usr/bin/env python3
"""Run simulation after improvements to verify better prompts."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codebase_reviewer.simulation import LLMSimulator

def main():
    """Run simulations on both workflows."""
    simulator = LLMSimulator(output_dir="simulation_results")
    
    print("=" * 80)
    print("RUNNING IMPROVED SIMULATIONS")
    print("=" * 80)
    
    # Run reviewer_criteria workflow (the comprehensive one)
    print("\n📋 Running reviewer_criteria workflow simulation...")
    result = simulator.run_simulation(".", workflow="reviewer_criteria")
    simulator.print_summary(result)
    
    print("\n" + "=" * 80)
    print("✅ Simulation complete!")
    print(f"📁 Results saved to: {simulator.output_dir}")
    print("=" * 80)
    
    # Print key improvements
    print("\n🎯 KEY IMPROVEMENTS MADE:")
    print("1. ✅ Fixed broken prompts (static_analysis_summary, comment_quality)")
    print("2. ✅ Enhanced testing context with actual test file discovery")
    print("3. ✅ Enhanced setup validation context with file detection")
    print("4. ✅ Added comprehensive tasks and deliverables to custom prompts")
    print("\n📊 Check the simulation results to verify improvements!")

if __name__ == "__main__":
    main()


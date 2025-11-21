#!/usr/bin/env python3
"""Direct simulation runner that bypasses terminal issues."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from codebase_reviewer.simulation import LLMSimulator

def main():
    """Run simulation on this repository."""
    print("=" * 80)
    print("RUNNING LLM SIMULATION ON CODEBASE-REVIEWER")
    print("=" * 80)
    print()
    
    # Run simulation with default workflow
    print("Running simulation with 'default' workflow...")
    sim = LLMSimulator(output_dir="./simulation_results")
    result = sim.run_simulation('.', 'default')
    sim.print_summary(result)
    
    print()
    print("=" * 80)
    print(f"✅ Simulation complete! Results saved to {sim.output_dir}")
    print("=" * 80)
    
    # Also run with reviewer_criteria workflow
    print()
    print("=" * 80)
    print("Running simulation with 'reviewer_criteria' workflow...")
    print("=" * 80)
    print()
    
    result2 = sim.run_simulation('.', 'reviewer_criteria')
    sim.print_summary(result2)
    
    print()
    print("=" * 80)
    print(f"✅ All simulations complete! Check {sim.output_dir} for detailed results")
    print("=" * 80)

if __name__ == '__main__':
    main()


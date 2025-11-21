#!/usr/bin/env python3
"""Quick script to run simulation."""

from codebase_reviewer.simulation import LLMSimulator

if __name__ == "__main__":
    sim = LLMSimulator()
    result = sim.run_simulation('.', 'default')
    sim.print_summary(result)
    print(f"\n✅ Simulation complete! Check {sim.output_dir} for results.")


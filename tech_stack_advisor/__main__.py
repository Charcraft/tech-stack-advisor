#!/usr/bin/env python3
"""
Tech Stack Advisor - Universal CLI Entry Point

Can be invoked as:
    python -m tech_stack_advisor [args]
    tech-stack-advisor [args]  (after pip install)

Harnesses can also import and use programmatically:
    from tech_stack_advisor import detect_stack, run_workflow
"""
import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

def detect_stack(project_path: str = ".") -> Dict[str, Any]:
    """Run heuristic stack detection on a project."""
    script_path = Path(__file__).parent.parent / "scripts" / "detect_stack.py"
    result = subprocess.run(
        [sys.executable, str(script_path), project_path],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"Detector failed: {result.stderr}")
    return json.loads(result.stdout)

def run_workflow(
    project_path: str = ".",
    skip_interview: bool = False,
    preferred_stacks: Optional[list] = None,
    output_decision: str = "STACK_DECISION.md",
    output_steps: str = "NEXT_STEPS.md"
) -> Dict[str, Any]:
    """
    Run the full evaluation workflow.
    Note: This is a stub - the actual workflow is orchestrated by the skill harness
    (opencode, Claude Code, agent-run) using the prompts and workflow definition.
    This function exists for programmatic use and testing.
    """
    # For now, just run detection
    # Full workflow requires LLM orchestration which harness provides
    signals = detect_stack(project_path)
    
    return {
        "detected_signals": signals,
        "workflow": "evaluate",
        "note": "Full workflow requires harness orchestration (opencode, Claude Code, agent-run). "
                "Use the skill via your harness: /skill tech_stack_advisor"
    }

def main():
    parser = argparse.ArgumentParser(
        prog="tech-stack-advisor",
        description="Evaluate project and recommend optimal tech stack"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=os.environ.get("TSA_PROJECT_PATH", "."),
        help="Path to project root (default: current directory)"
    )
    parser.add_argument(
        "--skip-interview",
        action="store_true",
        default=os.environ.get("TSA_SKIP_INTERVIEW", "false").lower() == "true",
        help="Skip interactive interview"
    )
    parser.add_argument(
        "--preferred-stacks",
        default=os.environ.get("TSA_PREFERRED_STACKS", ""),
        help="Comma-separated preferred stacks (go,python,rust,node)"
    )
    parser.add_argument(
        "--output-decision",
        default=os.environ.get("TSA_OUTPUT_DECISION", "STACK_DECISION.md"),
        help="Output path for ADR"
    )
    parser.add_argument(
        "--output-steps",
        default=os.environ.get("TSA_OUTPUT_STEPS", "NEXT_STEPS.md"),
        help="Output path for checklist"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output detection signals as JSON"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    if args.json:
        signals = detect_stack(args.project_path)
        print(json.dumps(signals, indent=2))
        return 0
    
    # Print detection for programmatic use
    signals = detect_stack(args.project_path)
    print(json.dumps(signals, indent=2))
    
    print("\n---", file=sys.stderr)
    print("Full workflow requires skill harness (opencode, Claude Code, agent-run).", file=sys.stderr)
    print("Install skill: npx skills add Charcraft/tech-stack-advisor", file=sys.stderr)
    print("Then run: /skill tech_stack_advisor", file=sys.stderr)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
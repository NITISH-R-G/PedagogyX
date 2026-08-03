#!/usr/bin/env python3
"""Shared utilities for benchmark scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def has_cuda() -> bool:
    """Check if CUDA is available."""
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        return False


def get_device(requested: str) -> str:
    """Resolve device selection.
    
    Args:
        requested: Device string ('auto', 'cuda', or 'cpu')
        
    Returns:
        Resolved device string ('cuda' or 'cpu')
    """
    if requested != "auto":
        return requested
    return "cuda" if has_cuda() else "cpu"


def validate_cuda_available(device: str) -> bool:
    """Validate CUDA availability when requested.
    
    Args:
        device: Target device string
        
    Returns:
        True if validation passes, False otherwise
    """
    if device == "cuda" and not has_cuda():
        print("CUDA requested but unavailable; use --device cpu or run on RTX 5070 host.")
        return False
    return True


def ensure_results_dir(script_path: Path) -> Path:
    """Ensure results directory exists.
    
    Args:
        script_path: Path to the benchmark script
        
    Returns:
        Path to results directory
    """
    results_dir = script_path.resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def check_package_import(package_name: str, requirements_file: str) -> bool:
    """Check if required package can be imported.
    
    Args:
        package_name: Name of the package to import
        requirements_file: Path to requirements file for installation instructions
        
    Returns:
        True if import succeeds, False otherwise
    """
    try:
        __import__(package_name)
        return True
    except ImportError:
        print(f"Install: pip install -r {requirements_file}")
        return False


def write_result(results_dir: Path, filename: str, result: dict) -> Path:
    """Write benchmark result to JSON file.
    
    Args:
        results_dir: Directory to write results to
        filename: Output filename
        result: Result dictionary to serialize
        
    Returns:
        Path to written file
    """
    out_path = results_dir / filename
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    return out_path

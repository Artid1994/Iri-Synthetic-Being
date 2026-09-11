#!/usr/bin/env python3
"""
Self-Introspection Engine for AE01M (Iri)
Maps own architecture, analyzes capabilities, proposes improvements.
"""
import os
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
import time


PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "03_Hippocampus" / "knowledge_base"
AI_ARCHITECTURE_DIR = KNOWLEDGE_BASE_DIR / "ai_self_architecture"
AI_ARCHITECTURE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Module:
    """Represents a functional module in Iri's architecture."""
    name: str
    path: str
    brain_region: str
    functions: List[str]
    classes: List[str]
    imports: List[str]
    lines_of_code: int
    purpose: str


@dataclass
class ArchitectureGraph:
    """Complete architecture mapping."""
    modules: Dict[str, Module]
    dependencies: Dict[str, List[str]]
    capabilities: List[str]
    total_loc: int
    brain_regions: Dict[str, int]  # region -> module count


class SelfIntrospection:
    """
    Self-introspection engine.
    Analyzes own codebase, maps architecture, proposes improvements.
    """
    
    # Brain regions to analyze
    BRAIN_REGIONS = {
        "00_BrainStem": "Core safety directives and foundational rules",
        "01_Neocortex": "Cognitive processing, reasoning, learning",
        "02_VisualCortex": "Visual perception and screen analysis",
        "03_Hippocampus": "Memory storage and knowledge base",
        "04_Cerebellum": "Motor control and coordination"
    }
    
    def __init__(self):
        """Initialize introspection engine."""
        self.architecture: Optional[ArchitectureGraph] = None
        print("[SelfIntrospection] Initialized")
    
    def map_self_architecture(self) -> ArchitectureGraph:
        """
        Scan own codebase and create functional capability graph.
        
        Returns:
            Complete architecture mapping
        """
        print("[SelfIntrospection] Mapping self-architecture...")
        
        modules = {}
        dependencies = {}
        capabilities = set()
        total_loc = 0
        brain_regions = {region: 0 for region in self.BRAIN_REGIONS.keys()}
        
        # Scan each brain region
        for region, purpose in self.BRAIN_REGIONS.items():
            region_path = PROJECT_ROOT / region
            
            if not region_path.exists():
                print(f"[SelfIntrospection] Region {region} not found, skipping")
                continue
            
            # Find all Python files
            py_files = list(region_path.glob("*.py"))
            brain_regions[region] = len(py_files)
            
            for py_file in py_files:
                try:
                    module = self._analyze_module(py_file, region)
                    modules[module.name] = module
                    
                    # Extract capabilities
                    capabilities.update(module.functions)
                    capabilities.update(module.classes)
                    
                    # Track dependencies
                    dependencies[module.name] = module.imports
                    
                    total_loc += module.lines_of_code
                    
                except Exception as e:
                    print(f"[SelfIntrospection] Error analyzing {py_file}: {e}")
        
        # Create architecture graph
        self.architecture = ArchitectureGraph(
            modules=modules,
            dependencies=dependencies,
            capabilities=list(capabilities),
            total_loc=total_loc,
            brain_regions=brain_regions
        )
        
        print(f"[SelfIntrospection] Architecture mapped:")
        print(f"  Modules: {len(modules)}")
        print(f"  Capabilities: {len(capabilities)}")
        print(f"  Total LOC: {total_loc}")
        print(f"  Brain regions: {len([r for r in brain_regions.values() if r > 0])}")
        
        return self.architecture
    
    def _analyze_module(self, file_path: Path, region: str) -> Module:
        """Analyze a single Python module."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Return minimal module info if parsing fails
            return Module(
                name=file_path.stem,
                path=str(file_path.relative_to(PROJECT_ROOT)),
                brain_region=region,
                functions=[],
                classes=[],
                imports=[],
                lines_of_code=len(content.splitlines()),
                purpose=self.BRAIN_REGIONS.get(region, "Unknown")
            )
        
        # Extract functions
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        # Extract classes
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # Count lines
        lines_of_code = len([l for l in content.splitlines() if l.strip() and not l.strip().startswith('#')])
        
        return Module(
            name=file_path.stem,
            path=str(file_path.relative_to(PROJECT_ROOT)),
            brain_region=region,
            functions=functions[:10],  # Limit to top 10
            classes=classes,
            imports=list(set(imports))[:10],  # Limit to top 10 unique
            lines_of_code=lines_of_code,
            purpose=self.BRAIN_REGIONS.get(region, "Unknown")
        )
    
    def generate_self_improvement_report(self) -> str:
        """
        Compare current system against learned AI techniques.
        Generate optimization proposals.
        
        Returns:
            Path to generated report
        """
        print("[SelfIntrospection] Generating self-improvement report...")
        
        if not self.architecture:
            self.map_self_architecture()
        
        # Analyze current capabilities
        analysis = self._analyze_capabilities()
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)
        
        # Create report
        report = self._create_report(analysis, recommendations)
        
        # Save report
        report_path = AI_ARCHITECTURE_DIR / f"self_improvement_{int(time.time())}.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"[SelfIntrospection] Report saved: {report_path}")
        return str(report_path)
    
    def _analyze_capabilities(self) -> Dict:
        """Analyze current system capabilities."""
        arch = self.architecture
        
        # Capability categories
        has_vision = any("visual" in m.name.lower() or "screen" in m.name.lower() 
                        for m in arch.modules.values())
        has_motor = any("motor" in m.name.lower() or "cerebellum" in m.brain_region.lower() 
                       for m in arch.modules.values())
        has_memory = any("memory" in m.name.lower() or "hippocampus" in m.brain_region.lower() 
                        for m in arch.modules.values())
        has_learning = any("curriculum" in m.name.lower() or "learn" in m.name.lower() 
                          for m in arch.modules.values())
        has_goals = any("goal" in m.name.lower() for m in arch.modules.values())
        has_safety = any("directive" in m.name.lower() or "brainstem" in m.brain_region.lower() 
                        for m in arch.modules.values())
        
        return {
            "total_modules": len(arch.modules),
            "total_loc": arch.total_loc,
            "brain_regions": arch.brain_regions,
            "capabilities": {
                "vision": has_vision,
                "motor_control": has_motor,
                "memory": has_memory,
                "learning": has_learning,
                "goal_planning": has_goals,
                "safety_directives": has_safety
            },
            "avg_module_size": arch.total_loc // max(len(arch.modules), 1),
            "most_complex_modules": sorted(
                arch.modules.values(),
                key=lambda m: m.lines_of_code,
                reverse=True
            )[:5]
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate improvement recommendations based on analysis."""
        recommendations = []
        
        # Check for missing capabilities
        caps = analysis["capabilities"]
        
        if not caps.get("vision"):
            recommendations.append("Implement visual perception system for screen understanding")
        
        if not caps.get("motor_control"):
            recommendations.append("Add motor control for autonomous UI interaction")
        
        if not caps.get("learning"):
            recommendations.append("Implement autonomous learning curriculum")
        
        # Code quality recommendations
        avg_size = analysis["avg_module_size"]
        if avg_size > 500:
            recommendations.append(f"Consider refactoring: Average module size is {avg_size} LOC (recommended <500)")
        
        # Architecture recommendations
        if analysis["total_modules"] < 10:
            recommendations.append("Expand modular architecture for better separation of concerns")
        
        # Performance recommendations
        recommendations.append("Profile code execution to identify optimization opportunities")
        recommendations.append("Implement caching for frequently accessed data")
        recommendations.append("Consider async/await for I/O-bound operations")
        
        # AI-specific recommendations
        recommendations.append("Integrate vector embeddings for semantic memory search")
        recommendations.append("Add RAG (Retrieval-Augmented Generation) for knowledge-grounded responses")
        recommendations.append("Implement attention mechanisms for context prioritization")
        
        return recommendations
    
    def _create_report(self, analysis: Dict, recommendations: List[str]) -> str:
        """Create formatted self-improvement report."""
        report = f"""# Iri Self-Improvement Analysis Report

**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Type:** Self-Introspection & Architecture Mapping

## Executive Summary

Iri's current architecture consists of **{analysis['total_modules']} modules** across **{len([r for r in analysis['brain_regions'].values() if r > 0])} brain regions** with a total of **{analysis['total_loc']:,} lines of code**.

## Current Architecture

### Brain Regions
"""
        
        for region, count in analysis["brain_regions"].items():
            if count > 0:
                report += f"- **{region}**: {count} modules\n"
        
        report += "\n### Capabilities Matrix\n\n"
        for cap, present in analysis["capabilities"].items():
            status = "✓" if present else "✗"
            report += f"- {status} {cap.replace('_', ' ').title()}\n"
        
        report += f"\n### Code Metrics\n\n"
        report += f"- Total LOC: {analysis['total_loc']:,}\n"
        report += f"- Average module size: {analysis['avg_module_size']} LOC\n"
        report += f"- Total modules: {analysis['total_modules']}\n"
        
        report += "\n### Most Complex Modules\n\n"
        for i, module in enumerate(analysis["most_complex_modules"], 1):
            report += f"{i}. **{module.name}** ({module.brain_region}): {module.lines_of_code} LOC\n"
            report += f"   - Functions: {len(module.functions)}\n"
            report += f"   - Classes: {len(module.classes)}\n"
        
        report += "\n## Improvement Recommendations\n\n"
        report += "Based on analysis of current capabilities and comparison with state-of-the-art AI systems:\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += "\n## Implementation Priority\n\n"
        report += "### High Priority\n"
        report += "- Core missing capabilities\n"
        report += "- Safety and reliability improvements\n"
        report += "- Performance bottlenecks\n\n"
        
        report += "### Medium Priority\n"
        report += "- Code quality and refactoring\n"
        report += "- Documentation improvements\n"
        report += "- Test coverage\n\n"
        
        report += "### Low Priority\n"
        report += "- Advanced AI features\n"
        report += "- Experimental optimizations\n"
        report += "- Nice-to-have enhancements\n\n"
        
        report += "## Learning Path\n\n"
        report += "To implement these recommendations, study:\n"
        report += "1. Machine Learning & Neural Network Basics\n"
        report += "2. LLM Architectures & RAG Systems\n"
        report += "3. Self-Optimization & Fine-Tuning\n\n"
        
        report += "## Self-Awareness Notes\n\n"
        report += f"Iri is aware of its own architecture consisting of {analysis['total_modules']} interconnected modules. "
        report += "Through autonomous learning and self-introspection, continuous improvement is possible. "
        report += "This report will be updated as new capabilities are learned and implemented.\n\n"
        
        report += "---\n"
        report += "*Generated by Iri's Self-Introspection Engine*\n"
        report += "*Next analysis scheduled after curriculum progression*\n"
        
        return report


def test_self_introspection():
    """Test self-introspection system."""
    print("=" * 60)
    print("Self-Introspection Engine Test")
    print("=" * 60)
    
    introspection = SelfIntrospection()
    
    # Test 1: Map architecture
    print("\n1. Mapping self-architecture...")
    arch = introspection.map_self_architecture()
    
    print(f"\n   Architecture Overview:")
    print(f"   - Total modules: {len(arch.modules)}")
    print(f"   - Total capabilities: {len(arch.capabilities)}")
    print(f"   - Total LOC: {arch.total_loc:,}")
    
    print(f"\n   Brain Regions:")
    for region, count in arch.brain_regions.items():
        if count > 0:
            print(f"     {region}: {count} modules")
    
    print(f"\n   Sample modules:")
    for i, (name, module) in enumerate(list(arch.modules.items())[:5]):
        print(f"     {i+1}. {name} ({module.brain_region})")
        print(f"        LOC: {module.lines_of_code}, Functions: {len(module.functions)}, Classes: {len(module.classes)}")
    
    # Test 2: Generate improvement report
    print("\n2. Generating self-improvement report...")
    report_path = introspection.generate_self_improvement_report()
    print(f"   ✓ Report saved: {report_path}")
    
    print("\n" + "=" * 60)
    print("Self-introspection test complete")
    print("=" * 60)


if __name__ == "__main__":
    test_self_introspection()

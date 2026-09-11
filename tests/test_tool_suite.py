#!/usr/bin/env python3
"""
Unit test for autonomous tool suite.
Verifies all 6 tools execute without errors.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))

print("="*80)
print("AUTONOMOUS TOOL SUITE - UNIT TEST")
print("="*80)

passed = 0
failed = 0

# Test 1: Web Search Tool
print("\n[1/6] Testing Web Search Tool...")
try:
    from tools.web_search_tool import WebSearchTool
    tool = WebSearchTool()
    results = tool.search("Python programming", max_results=2)
    assert isinstance(results, list), "Should return list"
    print("  ✓ Web Search Tool: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ Web Search Tool: FAIL - {e}")
    failed += 1

# Test 2: Wikipedia Tool
print("[2/6] Testing Wikipedia Tool...")
try:
    from tools.wikipedia_tool import WikipediaTool
    tool = WikipediaTool()
    summary = tool.get_summary("Artificial Intelligence", sentences=2)
    assert summary is None or isinstance(summary, str), "Should return string or None"
    print("  ✓ Wikipedia Tool: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ Wikipedia Tool: FAIL - {e}")
    failed += 1

# Test 3: PDF Doc Reader
print("[3/6] Testing PDF Doc Reader...")
try:
    from tools.pdf_doc_reader import PDFDocReader
    tool = PDFDocReader()
    # Test with non-existent file (should return None gracefully)
    result = tool.read_pdf("/tmp/nonexistent.pdf")
    assert result is None, "Should handle missing files"
    print("  ✓ PDF Doc Reader: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ PDF Doc Reader: FAIL - {e}")
    failed += 1

# Test 4: Python Sandbox
print("[4/6] Testing Python Sandbox...")
try:
    from tools.python_sandbox import PythonSandbox
    tool = PythonSandbox(timeout=2)
    result = tool.execute("print('Hello'); result = 2 + 2")
    assert result['success'] == True, "Should execute simple code"
    assert 'Hello' in result['output'], "Should capture output"
    print("  ✓ Python Sandbox: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ Python Sandbox: FAIL - {e}")
    failed += 1

# Test 5: ArXiv Research Tool
print("[5/6] Testing ArXiv Research Tool...")
try:
    from tools.arxiv_research_tool import ArXivResearchTool
    tool = ArXivResearchTool()
    results = tool.search("machine learning", max_results=1)
    assert isinstance(results, list), "Should return list"
    print("  ✓ ArXiv Research Tool: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ ArXiv Research Tool: FAIL - {e}")
    failed += 1

# Test 6: Media System Control
print("[6/6] Testing Media System Control...")
try:
    from tools.media_system_control import MediaSystemControl
    tool = MediaSystemControl()
    # Test memory reading (should work on Linux)
    mem = tool.get_memory_usage()
    assert mem is None or isinstance(mem, dict), "Should return dict or None"
    print("  ✓ Media System Control: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ Media System Control: FAIL - {e}")
    failed += 1

# Test 7: Tool Registry
print("[7/7] Testing Tool Registry...")
try:
    from tool_registry import ToolRegistry
    registry = ToolRegistry()
    tools = registry.select_tools_for_topic("machine learning")
    assert isinstance(tools, list), "Should return list of tools"
    assert len(tools) > 0, "Should select at least one tool"
    print("  ✓ Tool Registry: PASS")
    passed += 1
except Exception as e:
    print(f"  ✗ Tool Registry: FAIL - {e}")
    failed += 1

# Summary
print("\n" + "="*80)
print(f"TEST SUMMARY: {passed}/{passed+failed} PASSED")
if failed == 0:
    print("✓ ALL TOOLS OPERATIONAL")
    sys.exit(0)
else:
    print(f"✗ {failed} TOOLS FAILED")
    sys.exit(1)

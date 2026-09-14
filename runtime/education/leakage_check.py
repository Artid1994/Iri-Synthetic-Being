"""
Assessment Leakage Checker
Continuously verify transfer items don't leak answers
"""

def check_transfer_leakage(original_items, transfer_items):
    """
    Check if transfer items leak answers from original items.
    
    Returns:
        (is_safe, violations)
    """
    violations = []
    
    for orig, trans in zip(original_items, transfer_items):
        # Check 1: Prompts must be different
        if orig.prompt == trans.prompt:
            violations.append({
                "type": "IDENTICAL_PROMPT",
                "original": orig.prompt,
                "transfer": trans.prompt,
            })
        
        # Check 2: Answers must be same
        if orig.correct_answer != trans.correct_answer:
            violations.append({
                "type": "DIFFERENT_ANSWER",
                "expected": orig.correct_answer,
                "actual": trans.correct_answer,
            })
        
        # Check 3: Transfer must reference original
        if trans.metadata.get("original_item_id") != orig.item_id:
            violations.append({
                "type": "MISSING_REFERENCE",
                "transfer_id": trans.item_id,
                "original_id": orig.item_id,
            })
    
    return len(violations) == 0, violations


def continuous_leakage_check(workflow):
    """
    Run continuous leakage checks on all transfer assessments.
    
    Returns:
        (all_safe, report)
    """
    report = {
        "checked": 0,
        "violations": [],
    }
    
    for assessment in workflow.assessments:
        if assessment.assessment_type != "transfer":
            continue
        
        # Check metadata for original items
        transfer_items = assessment.items
        has_metadata = all(
            hasattr(item, 'metadata') and 'original_item_id' in item.metadata
            for item in transfer_items
        )
        
        if not has_metadata:
            report["violations"].append({
                "assessment_id": assessment.assessment_id,
                "issue": "Transfer items missing original_item_id metadata",
            })
        
        report["checked"] += 1
    
    return len(report["violations"]) == 0, report

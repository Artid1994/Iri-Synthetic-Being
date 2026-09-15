"""Tests for Token Governor."""
import pytest
from runtime.token_governor import TokenGovernor, TokenRequest, TokenResponse


def test_governor_initialization():
    """Test governor setup with budget limits."""
    gov = TokenGovernor(
        per_request_limit=1000,
        per_task_limit=5000,
        per_mission_limit=50000
    )
    
    assert gov.per_request_limit == 1000
    assert gov.total_used == 0
    assert gov.remaining_budget() == 50000


def test_estimate_token_usage():
    """Test token estimation from text."""
    gov = TokenGovernor(per_mission_limit=10000)
    
    # Rough estimate: ~4 chars per token
    text = "a" * 4000  # ~1000 tokens
    estimate = gov.estimate_tokens(text)
    
    assert 800 <= estimate <= 1200  # Allow 20% variance


def test_allow_request_within_budget():
    """Test request approval when budget is available."""
    gov = TokenGovernor(per_request_limit=1000, per_mission_limit=10000)
    
    request = TokenRequest(
        estimated_tokens=500,
        task_id="task_1",
        description="Test request"
    )
    
    response = gov.request_budget(request)
    
    assert response.approved
    assert response.tokens_reserved == 500
    assert not response.denial_reason


def test_deny_request_exceeds_per_request_limit():
    """Test denial when single request exceeds limit."""
    gov = TokenGovernor(per_request_limit=1000, per_mission_limit=10000)
    
    request = TokenRequest(
        estimated_tokens=1500,
        task_id="task_1",
        description="Too large"
    )
    
    response = gov.request_budget(request)
    
    assert not response.approved
    assert "per-request limit" in response.denial_reason


def test_deny_request_exhausted_mission_budget():
    """Test denial when mission budget is exhausted."""
    gov = TokenGovernor(per_request_limit=1000, per_mission_limit=2000)
    
    # Use up budget
    req1 = TokenRequest(estimated_tokens=1000, task_id="task_1")
    resp1 = gov.request_budget(req1)
    assert resp1.approved
    gov.commit_usage(resp1.request_id, 1000)
    
    req2 = TokenRequest(estimated_tokens=1000, task_id="task_2")
    resp2 = gov.request_budget(req2)
    assert resp2.approved
    gov.commit_usage(resp2.request_id, 1000)
    
    # This should be denied - budget exhausted
    req3 = TokenRequest(estimated_tokens=500, task_id="task_3")
    resp3 = gov.request_budget(req3)
    
    assert not resp3.approved
    assert "insufficient" in resp3.denial_reason.lower()


def test_reserve_commit_release_cycle():
    """Test reserve-commit-release mechanism."""
    gov = TokenGovernor(per_mission_limit=10000)
    
    # Reserve
    request = TokenRequest(estimated_tokens=1000, task_id="task_1")
    response = gov.request_budget(request)
    assert response.approved
    assert gov.total_reserved == 1000
    
    # Commit (actual usage)
    gov.commit_usage(response.request_id, actual_tokens=800)
    assert gov.total_used == 800
    assert gov.total_reserved == 0  # Released
    
    # Remaining budget should reflect actual usage
    assert gov.remaining_budget() == 10000 - 800


def test_release_unused_reservation():
    """Test releasing reservation without committing."""
    gov = TokenGovernor(per_mission_limit=10000)
    
    request = TokenRequest(estimated_tokens=1000, task_id="task_1")
    response = gov.request_budget(request)
    assert response.approved
    
    # Release without commit
    gov.release_reservation(response.request_id)
    
    assert gov.total_reserved == 0
    assert gov.total_used == 0
    assert gov.remaining_budget() == 10000


def test_task_level_tracking():
    """Test per-task token limits."""
    gov = TokenGovernor(per_task_limit=3000, per_mission_limit=10000)
    
    # First request for task
    req1 = TokenRequest(estimated_tokens=2000, task_id="task_1")
    resp1 = gov.request_budget(req1)
    assert resp1.approved
    gov.commit_usage(resp1.request_id, 2000)
    
    # Second request for same task - should be denied if over limit
    req2 = TokenRequest(estimated_tokens=2000, task_id="task_1")
    resp2 = gov.request_budget(req2)
    assert not resp2.approved


def test_call_limit_enforcement():
    """Test max calls enforcement."""
    gov = TokenGovernor(max_calls=2, per_mission_limit=10000)
    
    req1 = TokenRequest(estimated_tokens=100, task_id="task_1")
    resp1 = gov.request_budget(req1)
    assert resp1.approved
    gov.commit_usage(resp1.request_id, 100)
    
    req2 = TokenRequest(estimated_tokens=100, task_id="task_2")
    resp2 = gov.request_budget(req2)
    assert resp2.approved
    gov.commit_usage(resp2.request_id, 100)
    
    # Third call should be denied
    req3 = TokenRequest(estimated_tokens=100, task_id="task_3")
    resp3 = gov.request_budget(req3)
    assert not resp3.approved


def test_usage_tracking():
    """Test accurate usage tracking."""
    gov = TokenGovernor(per_mission_limit=10000)
    
    # Multiple requests
    for i in range(3):
        req = TokenRequest(estimated_tokens=500, task_id=f"task_{i}")
        resp = gov.request_budget(req)
        gov.commit_usage(resp.request_id, 500)
    
    assert gov.total_used == 1500
    assert gov.call_count == 3
    assert gov.remaining_budget() == 8500


def test_cannot_bypass_governor():
    """Test that denied requests cannot proceed."""
    gov = TokenGovernor(per_mission_limit=100)
    
    # Request exceeds budget
    request = TokenRequest(estimated_tokens=200, task_id="task_1")
    response = gov.request_budget(request)
    
    assert not response.approved
    
    # Attempting to commit should fail or be ignored
    with pytest.raises(Exception):
        gov.commit_usage(response.request_id, 200)

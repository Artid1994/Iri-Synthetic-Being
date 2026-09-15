"""Tests for Mission state machine."""
import pytest
from pathlib import Path
import tempfile

from runtime.mission import (
    Mission,
    MissionStatus,
    MissionProgress,
    KnowledgeGap,
    ResourceUsage,
    create_mission,
)


def test_create_mission():
    """Test mission creation from user prompt."""
    objective = "Make IRI a capable Thai + English AI assistant"
    mission = create_mission(objective)
    
    assert mission.objective == objective
    assert mission.status == MissionStatus.PENDING
    assert mission.progress.thai_competency == 0.0
    assert mission.progress.english_competency == 0.0
    assert mission.resource_usage.hermes_calls == 0


def test_mission_completion_detection():
    """Test completion criteria: Thai 100% AND English 100%."""
    mission = create_mission("Test objective")
    
    # Not complete initially
    assert not mission.is_complete()
    
    # Thai only - not complete
    mission.progress.thai_competency = 1.0
    assert not mission.is_complete()
    
    # Both languages - complete
    mission.progress.english_competency = 1.0
    assert mission.is_complete()


def test_mission_status_transitions():
    """Test mission state machine transitions."""
    mission = create_mission("Test")
    
    # PENDING -> RUNNING
    assert mission.status == MissionStatus.PENDING
    mission.update_status()
    assert mission.status == MissionStatus.RUNNING
    
    # RUNNING -> COMPLETE
    mission.progress.thai_competency = 1.0
    mission.progress.english_competency = 1.0
    mission.update_status()
    assert mission.status == MissionStatus.COMPLETE


def test_mission_blocked_state():
    """Test BLOCKED state detection."""
    mission = create_mission("Test")
    
    # Add blocker
    mission.add_blocker("Required capability unavailable")
    assert mission.is_blocked()
    
    mission.update_status()
    assert mission.status == MissionStatus.BLOCKED


def test_mission_resource_limit():
    """Test RESOURCE_LIMIT state."""
    mission = create_mission("Test")
    mission.max_hermes_calls = 5
    
    # Exhaust budget
    for _ in range(5):
        mission.record_hermes_call(1000)
    
    assert mission.is_resource_exhausted()
    mission.update_status()
    assert mission.status == MissionStatus.RESOURCE_LIMIT


def test_mission_hermes_tracking():
    """Test Hermes call and token tracking."""
    mission = create_mission("Test")
    
    mission.record_hermes_call(1000)
    mission.record_hermes_call(500)
    
    assert mission.resource_usage.hermes_calls == 2
    assert mission.resource_usage.tokens_used == 1500


def test_mission_persistence():
    """Test mission save/load."""
    mission = create_mission("Test persistence")
    mission.progress.thai_competency = 0.5
    mission.resource_usage.hermes_calls = 3
    mission.add_blocker("Test blocker")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "mission.json"
        
        # Save
        mission.save(filepath)
        assert filepath.exists()
        
        # Load
        loaded = Mission.load(filepath)
        assert loaded.objective == mission.objective
        assert loaded.progress.thai_competency == 0.5
        assert loaded.resource_usage.hermes_calls == 3
        assert "Test blocker" in loaded.blockers


def test_mission_knowledge_gap():
    """Test knowledge gap representation."""
    gap = KnowledgeGap(
        topic="Thai grammar rules",
        required_for="Lesson 5 completion",
        detected_at=123456.0
    )
    
    mission = create_mission("Test")
    mission.active_gap = gap
    
    assert mission.active_gap.topic == "Thai grammar rules"
    assert not mission.active_gap.verified


def test_mission_attempt_counting():
    """Test attempt limit enforcement."""
    mission = create_mission("Test")
    mission.max_attempts_per_task = 3
    
    mission.attempt_count = 3
    assert mission.is_blocked()

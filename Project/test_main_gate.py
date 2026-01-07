# Project/test_main_gate.py

import main_gate


def test_gate_open_with_valid_remote():
    gate = main_gate.ElectricGate()
    gate.unlock_gate()
    assert gate.open_gate_remote() == "Gate opens"


def test_gate_close_using_remote():
    gate = main_gate.ElectricGate()
    gate.unlock_gate()
    gate.open_gate_remote()
    assert gate.close_gate_remote() == "Gate closes"


def test_gate_open_with_wrong_switch():
    gate = main_gate.ElectricGate()
    assert gate.open_gate_remote() == "Gate remains closed"


def test_auto_lock_after_closing():
    gate = main_gate.ElectricGate()
    gate.unlock_gate()
    gate.open_gate_remote()
    gate.close_gate_remote()
    assert gate.is_locked is True


def test_unauthorized_access():
    gate = main_gate.ElectricGate()
    assert gate.open_gate_remote() == "Gate remains closed"


def test_obstacle_detection():
    gate = main_gate.ElectricGate()
    assert gate.detect_obstacle() == "Gate stops"


def test_resume_after_obstacle_removed():
    gate = main_gate.ElectricGate()
    gate.detect_obstacle()
    assert gate.remove_obstacle() == "Gate resumes"


def test_gate_opens_fully():
    gate = main_gate.ElectricGate()
    gate.unlock_gate()
    assert gate.open_gate_remote() == "Gate opens"


def test_gate_closes_fully():
    gate = main_gate.ElectricGate()
    gate.unlock_gate()
    gate.open_gate_remote()
    assert gate.close_gate_remote() == "Gate closes"


def test_power_failure():
    gate = main_gate.ElectricGate()
    assert gate.power_failure() == "Gate remains closed"

# Project/main_gate.py

class ElectricGate:
    def __init__(self):
        self.is_open = False
        self.is_locked = True
        self.power_on = True
        self.obstacle = False

    def unlock_gate(self):
        self.is_locked = False

    def open_gate_remote(self):
        if self.power_on and not self.is_locked:
            self.is_open = True
            return "Gate opens"
        return "Gate remains closed"

    def close_gate_remote(self):
        self.is_open = False
        self.is_locked = True
        return "Gate closes"

    def detect_obstacle(self):
        self.obstacle = True
        return "Gate stops"

    def remove_obstacle(self):
        self.obstacle = False
        return "Gate resumes"

    def power_failure(self):
        self.power_on = False
        return "Gate remains closed"

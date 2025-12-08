class SpeedPresets:

    def __init__(self):
        self.presets = [
            {"name": "SPEED INFO", "slider_value": 20, "delay": 0.185, "color": "#4CAF90"},
            {"name": "SPEED INFO", "slider_value": 40, "delay": 0.155, "color": "#4CAF50"},
            {"name": "SPEED INFO", "slider_value": 50, "delay": 0.125, "color": "#29B6F6"},
            {"name": "SPEED INFO", "slider_value": 80, "delay": 0.095, "color": "#29B6F6"},
            {"name": "SPEED INFO", "slider_value": 120, "delay": 0.065, "color": "#FF6B00"},
            {"name": "SPEED INFO", "slider_value": 160, "delay": 0.035, "color": "#FF0000"},
        ]
        self.current_index = 2

    def get_current_preset(self):
        return self.presets[self.current_index]

    def next_preset(self):
        self.current_index = (self.current_index + 1) % len(self.presets)
        return self.get_current_preset()

    def previous_preset(self):
        self.current_index = (self.current_index - 1) % len(self.presets)
        return self.get_current_preset()

    def get_preset_by_slider_value(self, slider_value):
        closest_preset = min(self.presets, key=lambda x: abs(x["slider_value"] - slider_value))
        for i, preset in enumerate(self.presets):
            if preset["slider_value"] == closest_preset["slider_value"]:
                self.current_index = i
                break
        return self.get_current_preset()
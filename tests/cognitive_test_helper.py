class FakeCognitive:
    def process(self, user_input, record_experience=False):
        return "RESPOND"

    def snapshot(self):
        return {"engine": "fake"}

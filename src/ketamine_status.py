class KetamineStatus(object):
    """How close are we to that sweet sweet K-hole?"""

    def __init__(self):
        base = 50
        exponent = 12
        self.thresholds = [0] + [base * (exponent**i) for i in range(10)]
        self.threshold_names = [ # Need 11 total
            "Stone Cold Sober",
            "Is This Thing On Yet?",
            "Hint O' Buzz",
            "Buzzed",
            "Perfectly Numb",
            "Floating on a Cloud",
            "Straight up Loopy",
            "Falling into Yourself",
            "That's a Lot of Colors",
            "Finding the Meaning of Life",
            "ACHIEVED K-HOLE",
        ]

    def get_status(self, curr_ketamine: float):
        for i, (threshold, name) in enumerate(zip(self.thresholds, self.threshold_names)):
            if curr_ketamine < threshold:
                return self.threshold_names[i - 1] if i > 0 else "Congrats, you broke it."
        return self.threshold_names[-1]

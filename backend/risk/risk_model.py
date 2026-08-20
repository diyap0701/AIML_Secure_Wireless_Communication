class RiskModel:

    def calculate_risk(
        self,
        distance,
        movement_status,
        movement_value,
        velocity,
        intersection
    ):

        score = 0

        # ---------------- Distance Risk ---------------- #

        if distance <= 2:
            score += 40

        elif distance <= 5:
            score += 30

        elif distance <= 10:
            score += 20

        else:
            score += 5


        # ---------------- Movement Risk ---------------- #

        if movement_status == "APPROACHING":

            if movement_value > 0.5:
                score += 30

            else:
                score += 20

        elif movement_status == "PARALLEL":
            score += 10

        elif movement_status == "MOVING_AWAY":
            score += 0


        # ---------------- Intersection Risk ---------------- #

        if intersection:
            score += 20


        # ---------------- Velocity Risk ---------------- #

        speed = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        if speed > 2:
            score += 10


        # ---------------- Final Classification ---------------- #

        if score >= 80:
            level = "CRITICAL"

        elif score >= 60:
            level = "HIGH"

        elif score >= 30:
            level = "MEDIUM"

        else:
            level = "LOW"


        return score, level
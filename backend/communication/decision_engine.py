class CommunicationDecisionEngine:

    def decide(self, risk_level):

        if risk_level == "LOW":
            return "NORMAL"

        elif risk_level == "MEDIUM":
            return "MONITOR"

        elif risk_level == "HIGH":
            return "ADAPT_BEAM"

        elif risk_level == "CRITICAL":
            return "CHANGE_PATH"

        return "NORMAL"
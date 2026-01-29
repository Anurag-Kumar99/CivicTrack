def predict_department_from_text(text):
    text = text.lower()

    if any(word in text for word in ["road", "street", "pothole", "broken road", "asphalt"]):
        return "ROAD"
    elif any(word in text for word in ["water", "pipe", "leak", "sewage", "leakage"]):
        return "WATER"
    elif any(word in text for word in ["electricity", "electricty", "power", "light", "outage", "voltage"]):
        return "ELECTRICITY"
    elif any(word in text for word in ["garbage", "waste", "trash"]):
        return "SANITATION"
    else:
        return "GENERAL"


def predict_priority_from_text(text):
    text = text.lower()

    if any(word in text for word in ["very high", "urgent", "as soon as possible", "immediate", "critical", "very bad"]):
        return "HIGH"
    elif any(word in text for word in ["medium", "normal", "standard", "moderate"]):
        return "MEDIUM"
    elif any(word in text for word in ["low", "whenever possible", "not urgent", "whenever you can"]):
        return "LOW"
    else:
        return "MEDIUM"

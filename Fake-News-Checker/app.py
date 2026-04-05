from flask import Flask, render_template, request

app = Flask(__name__)

# 🔍 Fake News Detection Function
def check_fake_news(text):
    score = 0
    reasons = []

    text_upper = text.upper()

    # 1. ALL CAPS check
    if text.isupper():
        score += 30
        reasons.append("Text is in ALL CAPS")

    # 2. Exclamation marks check
    exclamations = text.count("!")
    if exclamations > 3:
        score += 20
        reasons.append(f"Too many exclamation marks ({exclamations})")

    # 3. Too many capital words
    words = text.split()
    caps_words = [w for w in words if w.isupper() and len(w) > 3]
    if len(caps_words) > 3:
        score += 20
        reasons.append("Too many capitalized words")

    # 4. Suspicious / fake keywords
    fake_keywords = [
        "ALIENS", "SHOCKING", "BREAKING", "URGENT",
        "OMG", "VIRAL", "SECRET", "EXPOSED"
    ]

    for word in fake_keywords:
        if word in text_upper:
            score += 10
            reasons.append(f"Contains suspicious word: {word}")

    # 5. Emotional trigger words
    emotional_words = ["SHOCKED", "AMAZING", "UNBELIEVABLE", "DANGEROUS"]

    for word in emotional_words:
        if word in text_upper:
            score += 10
            reasons.append(f"Emotional trigger word: {word}")

    # 6. Final decision
    if score >= 70:
        result = "🚨 Highly Suspicious"
    elif score >= 40:
        result = "⚠️ Suspicious"
    else:
        result = "✅ Looks Genuine"

    # Limit score to 100
    score = min(score, 100)

    return result, score, reasons


# 🌐 Main Route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    reasons = []

    if request.method == "POST":
        news_text = request.form.get("news")

        if news_text:
            result, confidence, reasons = check_fake_news(news_text)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        reasons=reasons
    )


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True)
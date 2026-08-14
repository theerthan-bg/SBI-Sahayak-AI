import re
from urllib.parse import urlparse


SUSPICIOUS_WORDS = {

    "urgent": 8,
    "verify": 10,
    "verification": 10,
    "otp": 20,
    "password": 15,
    "blocked": 15,
    "suspended": 15,
    "click here": 15,
    "claim": 10,
    "winner": 15,
    "prize": 15,
    "refund": 10,
    "send money": 20,
    "bank account": 10,
    "upi": 5,
    "kyc": 15,
    "limited time": 10

}


def analyse_content(content):

    text = content.lower()

    score = 0

    indicators = []


    # Suspicious words

    for word, points in SUSPICIOUS_WORDS.items():

        if word in text:

            score += points

            indicators.append(
                f"Suspicious term detected: {word}"
            )


    # URL detection

    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text
    )


    if urls:

        score += 10

        indicators.append(
            "Message contains a URL"
        )


        for url in urls:

            if url.startswith("www."):

                parsed = urlparse(
                    "https://" + url
                )

            else:

                parsed = urlparse(url)


            domain = parsed.netloc.lower()


            # IP address URL

            ip_pattern = (
                r"^\d{1,3}"
                r"(\.\d{1,3}){3}$"
            )


            if re.match(
                ip_pattern,
                domain
            ):

                score += 25

                indicators.append(
                    "URL uses an IP address"
                )


            # HTTP

            if parsed.scheme != "https":

                score += 15

                indicators.append(
                    "URL does not use HTTPS"
                )


    # Excessive punctuation

    if content.count("!") >= 3:

        score += 5

        indicators.append(
            "Excessive urgency punctuation"
        )


    # OTP request

    otp_request_words = [
        "share otp",
        "send otp",
        "tell me otp",
        "give otp"
    ]


    for phrase in otp_request_words:

        if phrase in text:

            score += 25

            indicators.append(
                "Possible OTP theft attempt"
            )


    score = min(score, 100)


    if score >= 70:

        risk = "HIGH RISK"

        message = (
            "This content contains multiple "
            "fraud indicators. Do not click "
            "links or share banking credentials."
        )

    elif score >= 40:

        risk = "MEDIUM RISK"

        message = (
            "Some suspicious indicators were "
            "detected. Verify the sender before "
            "taking action."
        )

    else:

        risk = "LOW RISK"

        message = (
            "No major fraud indicators were "
            "detected by this prototype."
        )


    return {

        "risk_score": score,

        "risk_level": risk,

        "message": message,

        "indicators": indicators

    }
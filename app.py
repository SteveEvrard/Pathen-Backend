from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

from utils.email_utils import send_email
from utils.pdf_utils import generate_pdf
from utils.openai_utils import call_openai
from utils.parsing_utils import parse_answers, extract_email, split_sections

# Load environment variables
load_dotenv()
app = Flask(__name__)

# --- Typeform Webhook Endpoint ---
@app.route("/typeform-webhook", methods=["POST"])
def typeform_webhook():
    payload = request.get_json(force=True)
    print("📥 Received Typeform Payload:")
    print(json.dumps(payload, indent=2))

    try:
        answers = payload.get("form_response", {}).get("answers", [])
        email = extract_email(answers)

        # Parse answers
        parsed_answers = parse_answers(answers)

        # Build input summary text block
        input_summary_text = ""
        for key, value in parsed_answers.items():
            if isinstance(value, list):
                value = ", ".join(value)
            input_summary_text += f"{key}: {value}\n"

        # Prompt with fixed Input Summary
        prompt = (
            "Using the provided answers, generate a professional, narrative-style product packaging recommendation report. "
            "The report should include the following sections: 'Executive Summary', 'Input Summary', 'Recommended Packaging', "
            "'Rationale', 'Suppliers', and 'Next Steps'. "
            "Write in a clear, business-friendly style as if for an executive PDF report. "
            "For the Input Summary section, use exactly the following text block as-is without modifying it:\n\n"
            f"{input_summary_text}\n\n"
            "Then continue with the other sections in your own words."
        )

        response_text = call_openai(prompt)
        sections = split_sections(response_text)
        pdf_path = generate_pdf(sections)

        if email:
            send_email(
                to_email=email,
                subject="Your Product Packaging Recommendation",
                pdf_path=pdf_path
            )
            print(f"✅ Sent recommendation to {email}")
        else:
            print("⚠️ No email found in submission.")

        return jsonify({
            "message": "Processed successfully",
            "email_sent": bool(email)
        }), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
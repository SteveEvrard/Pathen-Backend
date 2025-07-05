from openai import OpenAI
import os

def call_openai(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
example_completion = """
Executive Summary:
This report outlines a tailored packaging solution for your product, focusing on [SUMMARY DESCRIPTION OF USER INPUTS].

Input Summary:
The following table summarizes the key product input details:

product_name: [NAME]
dimensions: [LENGTH] x [WIDTH] x [HEIGHT] [UNIT OF MEASUREMENT]
weight: [WEIGHT] lbs
fragility: [FRAGILITY_RATING]
shipping_method: [SHIPPING]
priority: [PRIORITIES]

Recommended Packaging:
- [RECOMMENDATION 1]
- [RECOMMENDATION 2]
- [RECOMMENDATION 3]
- [RECOMMENDATION 4]

Rationale:
[RATIONALE BASED ON USER INPUTS]

Suppliers:
[POTENTIAL SUPPLIERS BASED ON INPUTS]

Next Steps:
- [NEXT STEP 1]
- [NEXT STEP 2]
- [NEXT STEP 3]
- [NEXT STEP 4]
"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that writes professional business packaging recommendation reports. "
                "Always follow exactly this example style and structure, but generate fresh content based on the user inputs. "
                "Example style:\n\n"
                f"{example_completion.strip()}\n\n"
                "When responding, do not output JSON, code, or markdown. Only plain narrative text following the example sections and headings."
            )
        },
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2  # low temperature for consistency
    )
    return response.choices[0].message.content

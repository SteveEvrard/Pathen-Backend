import re

def parse_answers(answers_list):
    parsed = {}
    for ans in answers_list:
        field_id = ans["field"]["id"]
        field_type = ans["type"]

        if field_type == "text":
            parsed[field_id] = ans.get("text")
        elif field_type == "choice":
            parsed[field_id] = ans.get("choice", {}).get("label")
        elif field_type == "choices":
            parsed[field_id] = ans.get("choices", {}).get("labels")
        elif field_type == "boolean":
            parsed[field_id] = ans.get("boolean")
        elif field_type == "number":
            parsed[field_id] = ans.get("number")
        elif field_type == "date":
            parsed[field_id] = ans.get("date")
        elif field_type == "email":
            parsed[field_id] = ans.get("email") or ans.get("text")
        else:
            parsed[field_id] = "Unsupported type"
    return parsed

def extract_email(answers):
    for ans in answers:
        if ans['field']['type'] == 'email':
            return ans.get('email') or ans.get('text')
    return None

def split_sections(text):
    """
    Splits text into a dictionary of sections based on headers like 'Executive Summary:', etc.
    """
    section_pattern = r"^(.*?):\s*"
    matches = list(re.finditer(section_pattern, text, re.MULTILINE))

    sections = {}
    for i in range(len(matches)):
        title = matches[i].group(1).strip()
        start = matches[i].end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections[title] = content

    return sections

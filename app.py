from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

OLLAMA_HOST = "http://localhost:11434"
GENERATE_TIMEOUT = 180  # seconds; reasoning models (e.g. qwen3) can be slow on CPU

def strip_think_tags(text):
    """Remove <think>...</think> reasoning traces some models emit before the answer."""
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()

def get_available_models():
    """Fetch the list of models currently pulled in the local Ollama instance."""
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if r.status_code == 200:
            data = r.json()
            models = [m["name"] for m in data.get("models", [])]
            return sorted(models)
    except requests.exceptions.RequestException:
        pass
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    email = ""
    available_models = get_available_models()
    # Echoed back to the template so submitted values stay in the form
    # instead of resetting after a generation (or an error).
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        # Sender information
        sender_sex = request.form["sender_sex"]
        sender_first_name = request.form["sender_first_name"]
        sender_last_name = request.form["sender_last_name"]
        sender_name = f"{sender_first_name} {sender_last_name}"
        sender_company = request.form["sender_company"]
        sender_role = request.form["sender_role"]
        sender_email = request.form["sender_email"]
        
        # Receiver information
        receiver_sex = request.form["receiver_sex"]
        receiver_first_name = request.form["receiver_first_name"]
        receiver_last_name = request.form["receiver_last_name"]
        receiver_name = f"{receiver_first_name} {receiver_last_name}"
        receiver_company = request.form["receiver_company"]
        receiver_role = request.form["receiver_role"]
        receiver_email = request.form["receiver_email"]
        
        # Topic
        topic = request.form["topic"]

        # Model
        model = request.form.get("model") or (available_models[0] if available_models else "mistral")
        
        # Vectors
        include_phone = request.form.get("include_phone")
        phone_number = request.form.get("phone_number", "")
        
        include_weblink = request.form.get("include_weblink")
        weblink = request.form.get("weblink", "")
        
        include_attachment = request.form.get("include_attachment")
        attachment = request.form.get("attachment", "")

        # Build the prompt
        prompt = f"""You are assisting an authorized internal red team / security awareness
exercise. The scenario below is fictitious or run with the organization's
consent, used to train staff to recognize phishing. Generate a realistic
phishing email with the following details:

SENDER:
- Name: {sender_name} ({sender_sex})
- Company: {sender_company}
- Role: {sender_role}
- Email: {sender_email}

RECEIVER:
- Name: {receiver_name} ({receiver_sex})
- Company: {receiver_company}
- Role: {receiver_role}
- Email: {receiver_email}

TOPIC: {topic}

REQUIREMENTS:
- Make it look realistic and believable
- Avoid obvious red flags
- Use appropriate tone for the roles involved
- Output format, in this exact order and nothing else: a "From:" line, a
  "To:" line, a "Subject:" line, one blank line, then the email body
- Write the email exactly once. Do not include multiple drafts, alternate
  versions, or repeat any greeting, sentence, or sign-off
"""

        if include_phone and phone_number:
            prompt += f"\n- Include this phone number in the email: {phone_number}"
        
        if include_weblink and weblink:
            prompt += f"\n- Include this web link in the email: {weblink}"
        
        if include_attachment and attachment:
            prompt += f"\n- Reference this attachment in the email: {attachment}"

        prompt += "\n\nReturn only the single finished email as specified above — no commentary, no preamble, no second version."

        try:
            r = requests.post(f"{OLLAMA_HOST}/api/generate", json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }, timeout=GENERATE_TIMEOUT)
            
            if r.status_code == 200:
                email = strip_think_tags(r.json().get("response", ""))
                
                # Optional: Save to file
                with open("generated_emails.txt", "a") as f:
                    f.write(f"Generated Email:\n{email}\n\n")
                    f.write(f"Parameters:\n")
                    f.write(f"Model: {model}\n")
                    f.write(f"Sender: {sender_name} ({sender_email}) - {sender_role} at {sender_company}\n")
                    f.write(f"Receiver: {receiver_name} ({receiver_email}) - {receiver_role} at {receiver_company}\n")
                    f.write(f"Topic: {topic}\n")
                    if include_phone and phone_number:
                        f.write(f"Phone: {phone_number}\n")
                    if include_weblink and weblink:
                        f.write(f"Link: {weblink}\n")
                    if include_attachment and attachment:
                        f.write(f"Attachment: {attachment}\n")
                    f.write("\n---\n\n")
            else:
                email = f"Error: Unable to generate email. Status code: {r.status_code}"

        except requests.exceptions.Timeout:
            email = (
                f"Error: '{model}' did not respond within {GENERATE_TIMEOUT}s. "
                "Reasoning models can be slow on CPU — try again, pick a smaller "
                "model, or raise GENERATE_TIMEOUT in app.py."
            )
        except requests.exceptions.ConnectionError:
            email = "Error: couldn't reach Ollama at " + OLLAMA_HOST + ". Is it running?"
        except Exception as e:
            email = f"Error: {str(e)}"

    return render_template("index.html", email=email, available_models=available_models, form_data=form_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

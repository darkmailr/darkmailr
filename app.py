from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    email = ""
    if request.method == "POST":
        # Sender information
        sender_sex = request.form["sender_sex"]
        sender_name = request.form["sender_name"]
        sender_company = request.form["sender_company"]
        sender_role = request.form["sender_role"]
        sender_email = request.form["sender_email"]
        
        # Receiver information
        receiver_sex = request.form["receiver_sex"]
        receiver_name = request.form["receiver_name"]
        receiver_company = request.form["receiver_company"]
        receiver_role = request.form["receiver_role"]
        receiver_email = request.form["receiver_email"]
        
        # Topic
        topic = request.form["topic"]
        
        # Vectors
        include_phone = request.form.get("include_phone")
        phone_number = request.form.get("phone_number", "")
        
        include_weblink = request.form.get("include_weblink")
        weblink = request.form.get("weblink", "")
        
        include_attachment = request.form.get("include_attachment")
        attachment = request.form.get("attachment", "")

        # Build the prompt
        prompt = f"""Generate a realistic phishing email with the following details:

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
- Include proper email headers (From, To, Subject)
"""

        # Add vectors if selected
        if include_phone and phone_number:
            prompt += f"\n- Include this phone number in the email: {phone_number}"
        
        if include_weblink and weblink:
            prompt += f"\n- Include this web link in the email: {weblink}"
        
        if include_attachment and attachment:
            prompt += f"\n- Reference this attachment in the email: {attachment}"

        prompt += "\n\nGenerate the complete email including headers and body."

        try:
            r = requests.post("http://localhost:11434/api/generate", json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            })
            
            if r.status_code == 200:
                email = r.json().get("response", "")
                
                # Optional: Save to file
                with open("generated_emails.txt", "a") as f:
                    f.write(f"Generated Email:\n{email}\n\n")
                    f.write(f"Parameters:\n")
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
                
        except Exception as e:
            email = f"Error: {str(e)}"

    return render_template("index.html", email=email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

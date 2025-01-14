from flask import Flask, request # type: ignore
from twilio.twiml.voice_response import VoiceResponse # type: ignore
from client_management import load_clients, get_next_client, update_client_policy
from payment_processing import calculate_payment_details, process_payment
import openai # type: ignore
import json

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

app = Flask(__name__)
openai.api_key = config["openai"]["api_key"]

twilio_account_sid = config["twilio"]["account_sid"]
twilio_auth_token = config["twilio"]["auth_token"]
twilio_phone_number = config["twilio"]["phone_number"]

def generate_response(prompt, language="en"):
    """Generate dynamic responses using LLM."""
    response = openai.Completion.create(
        model="fine-tuned-model-id",  # Use your fine-tuned model name here
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route("/voice", methods=["POST"])
def voice():
    """Handle incoming Twilio calls."""
    clients = load_clients()
    client = get_next_client(clients)

    response = VoiceResponse()
    if not client:
        response.say("No clients to call at the moment.")
        return str(response)

    # Step 1: Greet the customer
    response.say("Hello, this is your policy renewal reminder.", voice="alice")

    # Step 2: Explain Policy and Payment
    payment_details = calculate_payment_details(client)
    total_amount = payment_details["totalAmount"]
    prompt = f"Explain the payment details for a client with a renewal fee of ${payment_details['renewalFee']} and an outstanding balance of ${payment_details['outstandingBalance']}."
    payment_explanation = generate_response(prompt, language="en")
    response.say(payment_explanation, voice="alice")

    # Step 3: Present Renewal Offer
    renewal_offer = f"We're offering a {client['renewalOffer']['discount']}% discount if you renew today. The updated premium is ${client['renewalOffer']['updatedPremium']}."
    response.say(renewal_offer, voice="alice")

    # Step 4: Ask for Renewal Confirmation
    gather = response.gather(input="speech", action="/process_response", num_digits=1, timeout=5)
    gather.say("Would you like to renew your policy? Please say yes or no.", voice="alice")
    response.append(gather)

    return str(response)

@app.route("/process_response", methods=["POST"])
def process_response():
    """Process client response."""
    clients = load_clients()
    client = get_next_client(clients)
    speech_result = request.form.get("SpeechResult", "").lower()

    response = VoiceResponse()
    if "yes" in speech_result:
        payment_result = process_payment(client)
        if payment_result["status"] == "success":
            update_client_policy(client["id"], "2025-01-01")  # Extend by 1 year
            response.say("Thank you! Your policy has been renewed.", voice="alice")
        else:
            response.say(f"Payment failed. {payment_result['error']}", voice="alice")
    else:
        response.say("No problem. Let us know if you change your mind.", voice="alice")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)

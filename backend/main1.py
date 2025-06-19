# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# from pydub import AudioSegment
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import agent
# import src.speech_to_text as speech_to_text
# import src.text_to_speech
# import src.tools
# from flask import send_file
# import pdfkit  # You'll need to install this package
# from twilio.twiml.voice_response import VoiceResponse
# from twilio.rest import Client



# app = Flask(__name__)

# # Twilio Client Setup
# twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# # Configure upload folder
# UPLOAD_FOLDER = "frontend/src/audio"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Enable CORS
# CORS(app, resources={
#     r"/*": {
#         "origins": ["http://localhost:5173","http://localhost:5174","http://localhost:5175"],
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization"],
#         "expose_headers": ["Content-Range", "X-Content-Range"],
#         "supports_credentials": True,
#         "max_age": 3600
#     }
# })

# # Global variables for conversation state
# conversation_history = ""
# user_input = ""
# inputs = {}
# tools_response = ""

# # Helper function to ensure audio is at 16 kHz and 16-bit
# def ensure_audio_format(input_file, output_file, target_sample_rate=16000):
#     audio = AudioSegment.from_file(input_file)
#     audio = audio.set_frame_rate(target_sample_rate)
#     audio = audio.set_sample_width(2)  # Ensure 16-bit (2 bytes per sample)
#     audio.export(output_file, format="wav")

# # Helper function to save conversation history as PDF
# def save_conversation_as_pdf(conversation_history, filename):
#     pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#     c = canvas.Canvas(pdf_path, pagesize=letter)
#     width, height = letter
#     c.setFont("Helvetica", 12)

#     # Split conversation history into lines
#     lines = conversation_history.split("\n")
#     y_position = height - 40  # Start from the top of the page

#     for line in lines:
#         if y_position < 40:  # Add a new page if we reach the bottom
#             c.showPage()
#             y_position = height - 40
#             c.setFont("Helvetica", 12)
#         c.drawString(40, y_position, line)
#         y_position -= 15  # Move down for the next line

#     c.save()
#     print(f"Conversation saved as PDF: {pdf_path}")


# @app.route("/twilio/start_call", methods=["POST"])
# def start_call():
#     data = request.get_json()
#     phone_number = data.get("phone_number")
    
#     try:
#         call = twilio_client.calls.create(
#             url=f"{os.getenv('NGROK_URL')}/twilio/voice",
#             to=phone_number,
#             from_=os.getenv("TWILIO_PHONE_NUMBER")
#         )
#         return jsonify({"status": "success", "call_sid": call.sid})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/twilio/voice", methods=["POST"])
# def handle_twilio_voice():
#     response = VoiceResponse()
    
#     # Get user speech input
#     user_input = request.values.get('SpeechResult', '')
    
#     if user_input:
#         # Update conversation history
#         global conversation_history
#         conversation_history += f"User: {user_input}\n"
        
#         # Generate agent response
#         agent_response = agent.sales_conversation_with_tools(
#             inputs.get("salesperson_name", ""),
#             inputs.get("salesperson_role", ""),
#             inputs.get("company_name", ""),
#             inputs.get("company_business", ""),
#             inputs.get("company_values", ""),
#             inputs.get("conversation_purpose", ""),
#             inputs.get("conversation_type", ""),
#             tools_response,
#             conversation_history
#         )
        
#         # Clean the response
#         clean_message = agent_response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in agent_response else agent_response
        
#         # Convert to speech
#         audio_file_name = src.text_to_speech.text_to_speech(clean_message)
#         audio_url = f"{os.getenv('NGROK_URL')}/audio/{audio_file_name}"
        
#         # Play the audio
#         response.play(audio_url)
        
#         # Update conversation history
#         conversation_history += f"Agent: {clean_message}\n"
        
#         # Check if call should end
#         if agent_response.endswith("<END_OF_CALL>"):
#             response.say("Thank you for the conversation. Goodbye!")
#             response.hangup()
#             return response(str(response), mimetype="text/xml")
    
#     # Continue conversation
#     response.gather(
#         input='speech',
#         speech_timeout=3,
#         action='/twilio/voice',
#         method='POST'
#     )
    
#     return response(str(response), mimetype="text/xml")


# # Route to handle form submission
# @app.route("/get_info", methods=["POST", "OPTIONS"])
# def get_info():
#     if request.method == "OPTIONS":
#         return "", 204

#     data = request.get_json()
#     global inputs
#     inputs = {
#         "salesperson_name": data.get("salespersonName"),
#         "salesperson_role": data.get("salespersonRole"),
#         "company_name": data.get("companyName"),
#         "company_business": data.get("companyBusiness"),
#         "company_values": data.get("companyValues"),
#         "conversation_purpose": data.get("conversationPurpose"),
#         "conversation_type": data.get("conversationType"),
#         "use_tools": data.get("withTools")
#     }
#     return jsonify(inputs)

# # Route to serve audio files
# @app.route("/audio/<path:filename>")
# def serve_audio(filename):
#     print(f"Audio file requested: {filename}")
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# # Route to handle agent response
# @app.route("/agent", methods=["GET", "OPTIONS"])
# def main_agent():
#     if request.method == "OPTIONS":
#         return "", 204

#     global conversation_history, user_input, inputs, tools_response

#     # Generate agent response
#     response = agent.sales_conversation_with_tools(
#         inputs["salesperson_name"],
#         inputs["salesperson_role"],
#         inputs["company_name"],
#         inputs["company_business"],
#         inputs["company_values"],
#         inputs["conversation_purpose"],
#         inputs["conversation_type"],
#         tools_response,
#         conversation_history,
#     )

#     # Clean the response message
#     clean_message = response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in response else response
#     isendofcall = response.endswith("<END_OF_CALL>")

#     # Generate audio from the response
#     try:
#         audio_file_name = src.text_to_speech.text_to_speech(clean_message)
#         audio_url = audio_file_name
#         print(f"Generated audio: {audio_file_name}")
#     except Exception as e:
#         return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500

#     # Update conversation history
#     conversation_history += f"Sales Agent: {clean_message}\n"

#     # Save conversation history as PDF if the call ends
#     if isendofcall:
#         pdf_filename = "conversation_history.pdf"
#         save_conversation_as_pdf(conversation_history, pdf_filename)

#     return jsonify({
#         "message": clean_message,
#         "audioUrl": audio_url,
#         "isEndOfCall": isendofcall
#     })

# @app.route('/download_conversation')
# def download_conversation():
#     try:
#         # Generate your PDF content here
#         html_content = "<h1>Conversation History</h1><p>Your conversation content here...</p>"
        
#         # Convert HTML to PDF
#         pdf = pdfkit.from_string(html_content, False)
        
#         # Create response
#         response = make_response(pdf)
#         response.headers['Content-Type'] = 'application/pdf'
#         response.headers['Content-Disposition'] = 'attachment; filename=conversation_history.pdf'
#         return response
#     except Exception as e:
#         return str(e), 500

# # @app.route("/upload_audio", methods=["POST", "OPTIONS"])
# # def upload_audio():
# #     if request.method == "OPTIONS":
# #         return "", 204

# #     global conversation_history, user_input, inputs, tools_response

# #     if 'audio' not in request.files:
# #         return jsonify({"error": "No audio file provided"}), 400

# #     try:
# #         # Save the uploaded file
# #         audio_file = request.files['audio']
# #         temp_filename = os.path.join(app.config["UPLOAD_FOLDER"], "frontend_recording.wav")
# #         audio_file.save(temp_filename)

# #         # Ensure the audio is at 16 kHz and 16-bit
# #         processed_filename = os.path.join(app.config["UPLOAD_FOLDER"], "processed_recording.wav")
# #         ensure_audio_format(temp_filename, processed_filename, 16000)

# #         # Convert speech to text
# #         user_input = speech_to_text.speech_to_text(processed_filename)
        
# #         if not user_input:
# #             return jsonify({"error": "No speech detected in the audio"}), 400

# #         # Update conversation history
# #         conversation_history += f"User: {user_input}\n"

# #         # Use tools if enabled
# #         if inputs.get("use_tools", False):
# #             tools_response_json = agent.conversation_tool(conversation_history)
# #             tools_response = src.tools.get_tools_response(tools_response_json) if tools_response_json != "NO" else ""

# #         # Generate agent response
# #         response = agent.sales_conversation_with_tools(
# #             inputs["salesperson_name"],
# #             inputs["salesperson_role"],
# #             inputs["company_name"],
# #             inputs["company_business"],
# #             inputs["company_values"],
# #             inputs["conversation_purpose"],
# #             inputs["conversation_type"],
# #             tools_response,
# #             conversation_history
# #         )

# #         # Clean the response message
# #         clean_message = response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in response else response
# #         isendofcall = response.endswith("<END_OF_CALL>")

# #         # Generate audio from the response
# #         audio_file_name = src.text_to_speech.text_to_speech(clean_message)
# #         audio_url = audio_file_name
# #         print(f"Generated audio: {audio_file_name}")

# #         # Update conversation history
# #         conversation_history += f"Sales Agent: {clean_message}\n"

# #         # Save conversation history as PDF if the call ends
# #         if isendofcall:
# #             pdf_filename = "conversation_history.pdf"
# #             save_conversation_as_pdf(conversation_history, pdf_filename)

# #         # Clean up temporary files
# #         os.remove(temp_filename)
# #         os.remove(processed_filename)

# #         return jsonify({
# #             "message": clean_message,
# #             "audioUrl": audio_url,
# #             "isEndOfCall": isendofcall
# #         })
    
# #     except Exception as e:
# #         print(f"Error processing audio: {str(e)}")
# #         return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500


# @app.route("/upload_audio", methods=["POST", "OPTIONS"])
# def upload_audio():
#     if request.method == "OPTIONS":
#         return "", 204

#     global conversation_history, user_input, inputs, tools_response

#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400

#     try:
#         # Save the uploaded file
#         audio_file = request.files['audio']
#         temp_filename = os.path.join(app.config["UPLOAD_FOLDER"], "frontend_recording.wav")
#         audio_file.save(temp_filename)
#         print(f"Saved temporary audio file: {temp_filename}")

#         # Ensure the audio is at 16 kHz and 16-bit
#         processed_filename = os.path.join(app.config["UPLOAD_FOLDER"], "processed_recording.wav")
#         ensure_audio_format(temp_filename, processed_filename, 16000)
#         print(f"Processed audio file: {processed_filename}")

#         # Convert speech to text
#         user_input = speech_to_text.speech_to_text(processed_filename)
#         print(f"User input from speech: {user_input}")
        
#         if not user_input:
#             return jsonify({"error": "No speech detected in the audio"}), 400

#         # Update conversation history
#         conversation_history += f"User: {user_input}\n"

#         # Use tools if enabled
#         if inputs.get("use_tools", False):
#             tools_response_json = agent.conversation_tool(conversation_history)
#             tools_response = src.tools.get_tools_response(tools_response_json) if tools_response_json != "NO" else ""

#         # Generate agent response
#         response = agent.sales_conversation_with_tools(
#             inputs["salesperson_name"],
#             inputs["salesperson_role"],
#             inputs["company_name"],
#             inputs["company_business"],
#             inputs["company_values"],
#             inputs["conversation_purpose"],
#             inputs["conversation_type"],
#             tools_response,
#             conversation_history
#         )

#         # Clean the response message
#         clean_message = response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in response else response
#         isendofcall = response.endswith("<END_OF_CALL>")

#         # Generate audio from the response
#         audio_file_name = src.text_to_speech.text_to_speech(clean_message)
#         audio_url = audio_file_name
#         print(f"Generated audio: {audio_file_name}")

#         # Update conversation history
#         conversation_history += f"Sales Agent: {clean_message}\n"

#         # Save conversation history as PDF if the call ends
#         if isendofcall:
#             pdf_filename = "conversation_history.pdf"
#             save_conversation_as_pdf(conversation_history, pdf_filename)

#         # Clean up temporary files
#         os.remove(temp_filename)
#         os.remove(processed_filename)

#         return jsonify({
#             "message": clean_message,
#             "audioUrl": audio_url,
#             "isEndOfCall": isendofcall
#         })
    
#     except Exception as e:
#         print(f"Error processing audio: {str(e)}")
#         return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500
# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import agent
import src.speech_to_text as speech_to_text
import src.text_to_speech
import src.tools
from flask import send_file, make_response
import pdfkit
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio Client Setup
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# Configure upload folder
UPLOAD_FOLDER = "frontend/src/audio"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Global variables for conversation state
conversation_history = ""
user_input = ""
inputs = {}
tools_response = ""

# Helper function to ensure audio is at 16 kHz and 16-bit
def ensure_audio_format(input_file, output_file, target_sample_rate=16000):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(target_sample_rate)
    audio = audio.set_sample_width(2)  # Ensure 16-bit (2 bytes per sample)
    audio.export(output_file, format="wav")

# Helper function to save conversation history as PDF
def save_conversation_as_pdf(conversation_history, filename):
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    lines = conversation_history.split("\n")
    y_position = height - 40  # Start from the top of the page

    for line in lines:
        if y_position < 40:  # Add a new page if we reach the bottom
            c.showPage()
            y_position = height - 40
            c.setFont("Helvetica", 12)
        c.drawString(40, y_position, line)
        y_position -= 15  # Move down for the next line

    c.save()
    print(f"Conversation saved as PDF: {pdf_path}")

# Twilio Routes
@app.route("/twilio/start_call", methods=["POST"])
def start_call():
    data = request.get_json()
    phone_number = data.get("phone_number")
    print("Starting call to:", phone_number)
    
    try:
        call = twilio_client.calls.create(
            url=f"{os.getenv('NGROK_URL')}/twilio/voice",
            to="+919395360772",
            from_=os.getenv("TWILIO_PHONE_NUMBER")
        )
        return jsonify({"status": "success", "call_sid": call.sid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/twilio/voice", methods=["POST"])
# def handle_twilio_voice():
#     response = VoiceResponse()
#     global conversation_history, inputs, tools_response
    
#     # Get user speech input
#     user_input = request.values.get('SpeechResult', '')
    
#     if user_input:
#         # Update conversation history
#         conversation_history += f"User: {user_input}\n"
        
#         # Generate agent response
#         agent_response = agent.sales_conversation_with_tools(
#             inputs.get("salesperson_name", ""),
#             inputs.get("salesperson_role", ""),
#             inputs.get("company_name", ""),
#             inputs.get("company_business", ""),
#             inputs.get("company_values", ""),
#             inputs.get("conversation_purpose", ""),
#             inputs.get("conversation_type", ""),
#             tools_response,
#             conversation_history
#         )
        
#         # Clean the response
#         clean_message = agent_response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in agent_response else agent_response
        
#         # Convert to speech
#         try:
#             audio_file_name = src.text_to_speech.text_to_speech(clean_message)
#             audio_url = f"{os.getenv('NGROK_URL')}/audio/{audio_file_name}"
#             response.play(audio_url)
#         except Exception as e:
#             response.say("Sorry, I encountered an error generating the response.")
#             print(f"TTS Error: {str(e)}")
        
#         # Update conversation history
#         conversation_history += f"Agent: {clean_message}\n"
        
#         # Check if call should end
#         if agent_response.endswith("<END_OF_CALL>"):
#             response.say("Thank you for the conversation. Goodbye!")
#             response.hangup()
#             return str(response)
    
#     # Continue conversation
#     response.gather(
#         input='speech',
#         speech_timeout=3,
#         action='/twilio/voice',
#         method='POST'
#     )
    
#     return Response(str(response), mimetype="text/xml")

@app.route("/twilio/voice", methods=["POST"])
def handle_twilio_voice():
    response = VoiceResponse()
    global conversation_history, inputs, tools_response
    
    # Initial greeting if this is the first interaction
    if not conversation_history:
        initial_greeting = "Your call is important to us. Please hold while we connect you to an agent."
        try:
            audio_file = src.text_to_speech.text_to_speech(initial_greeting)
            response.play(f"{os.getenv('NGROK_URL')}/audio/{audio_file}")
            conversation_history += f"Agent: {initial_greeting}\n"
        except Exception as e:
            response.say("Welcome! How can I assist you?")
            print(f"TTS Error: {str(e)}")
    
    # Process user input if available
    user_input = request.values.get('SpeechResult', '')
    if user_input:
        conversation_history += f"User: {user_input}\n"
        
        # Generate agent response
        agent_response = agent.sales_conversation_with_tools(
            inputs.get("salesperson_name", ""),
            inputs.get("salesperson_role", ""),
            inputs.get("company_name", ""),
            inputs.get("company_business", ""),
            inputs.get("company_values", ""),
            inputs.get("conversation_purpose", ""),
            inputs.get("conversation_type", ""),
            tools_response,
            conversation_history
        )
        
        clean_message = agent_response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in agent_response else agent_response
        
        # Convert to speech and respond
        try:
            audio_file = src.text_to_speech.text_to_speech(clean_message)
            response.play(f"{os.getenv('NGROK_URL')}/audio/{audio_file}")
        except Exception as e:
            response.say("Let me think about that...")
            print(f"TTS Error: {str(e)}")
        
        conversation_history += f"Agent: {clean_message}\n"
        
        # End call if conversation complete
        if agent_response.endswith("<END_OF_CALL>"):
            response.say("Thank you for the conversation. Goodbye!")
            response.hangup()
            return Response(str(response), mimetype="text/xml")
    
    # Continue conversation
    response.gather(
        input='speech',
        speech_timeout=4,
        action='/twilio/voice',
        method='POST'
    )
    
    return Response(str(response), mimetype="text/xml")


# Existing Routes
@app.route("/get_info", methods=["POST", "OPTIONS"])
def get_info():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    global inputs
    inputs = {
        "salesperson_name": data.get("salespersonName"),
        "salesperson_role": data.get("salespersonRole"),
        "company_name": data.get("companyName"),
        "company_business": data.get("companyBusiness"),
        "company_values": data.get("companyValues"),
        "conversation_purpose": data.get("conversationPurpose"),
        "conversation_type": data.get("conversationType"),
        "use_tools": data.get("withTools")
    }
    return jsonify(inputs)

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/agent", methods=["GET", "OPTIONS"])
def main_agent():
    if request.method == "OPTIONS":
        return "", 204

    global conversation_history, user_input, inputs, tools_response

    response = agent.sales_conversation_with_tools(
        inputs["salesperson_name"],
        inputs["salesperson_role"],
        inputs["company_name"],
        inputs["company_business"],
        inputs["company_values"],
        inputs["conversation_purpose"],
        inputs["conversation_type"],
        tools_response,
        conversation_history,
    )

    clean_message = response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in response else response
    isendofcall = response.endswith("<END_OF_CALL>")

    try:
        audio_file_name = src.text_to_speech.text_to_speech(clean_message)
        audio_url = audio_file_name
    except Exception as e:
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500

    conversation_history += f"Sales Agent: {clean_message}\n"

    if isendofcall:
        pdf_filename = "conversation_history.pdf"
        save_conversation_as_pdf(conversation_history, pdf_filename)

    return jsonify({
        "message": clean_message,
        "audioUrl": audio_url,
        "isEndOfCall": isendofcall
    })

@app.route('/download_conversation')
def download_conversation():
    try:
        html_content = f"<h1>Conversation History</h1><pre>{conversation_history}</pre>"
        pdf = pdfkit.from_string(html_content, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=conversation_history.pdf'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload_audio", methods=["POST", "OPTIONS"])
def upload_audio():
    if request.method == "OPTIONS":
        return "", 204

    global conversation_history, user_input, inputs, tools_response

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    try:
        audio_file = request.files['audio']
        temp_filename = os.path.join(app.config["UPLOAD_FOLDER"], "frontend_recording.wav")
        audio_file.save(temp_filename)

        processed_filename = os.path.join(app.config["UPLOAD_FOLDER"], "processed_recording.wav")
        ensure_audio_format(temp_filename, processed_filename, 16000)

        user_input = speech_to_text.speech_to_text(processed_filename)
        
        if not user_input:
            return jsonify({"error": "No speech detected in the audio"}), 400

        conversation_history += f"User: {user_input}\n"

        if inputs.get("use_tools", False):
            tools_response_json = agent.conversation_tool(conversation_history)
            tools_response = src.tools.get_tools_response(tools_response_json) if tools_response_json != "NO" else ""

        agent_response = agent.sales_conversation_with_tools(
            inputs["salesperson_name"],
            inputs["salesperson_role"],
            inputs["company_name"],
            inputs["company_business"],
            inputs["company_values"],
            inputs["conversation_purpose"],
            inputs["conversation_type"],
            tools_response,
            conversation_history
        )

        clean_message = agent_response.split("<END_OF_TURN>")[0].strip() if "<END_OF_TURN>" in agent_response else agent_response
        isendofcall = agent_response.endswith("<END_OF_CALL>")

        audio_file_name = src.text_to_speech.text_to_speech(clean_message)
        audio_url = audio_file_name

        conversation_history += f"Sales Agent: {clean_message}\n"

        if isendofcall:
            pdf_filename = "conversation_history.pdf"
            save_conversation_as_pdf(conversation_history, pdf_filename)

        os.remove(temp_filename)
        os.remove(processed_filename)

        return jsonify({
            "message": clean_message,
            "audioUrl": audio_url,
            "isEndOfCall": isendofcall
        })
    
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
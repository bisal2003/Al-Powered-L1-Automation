import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { Mic, Send } from "lucide-react";
import { toast } from "react-hot-toast";

const Home = () => {

  // Form states

  const [salespersonName, setSalespersonName] = useState("Alex");
  const [salespersonRole, setSalespersonRole] = useState("Salesman");
  const [companyName, setCompanyName] = useState("Bharat Electronics");
  const [companyBusiness, setCompanyBusiness] = useState("We deals with wide variety of electronics items");
  const [companyValues, setCompanyValues] = useState("Honesty");
  const [conversationPurpose, setConversationPurpose] = useState("Sell TV");
  const [conversationType, setConversationType] = useState("call");
  const [withTools, setWithTools] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [errors, setErrors] = useState({});


  // Audio states
  const [audioUrl, setAudioUrl] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);
  const [audioMessage, setAudioMessage] = useState("");
  const [isEndOfCall, setIsEndOfCall] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Refs for audio handling
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  // Validate form inputs
  const validateForm = () => {
    const newErrors = {};
    if (!salespersonName.trim()) newErrors.salespersonName = "Required";
    if (!salespersonRole.trim()) newErrors.salespersonRole = "Required";
    if (!companyName.trim()) newErrors.companyName = "Required";
    if (!companyBusiness.trim()) newErrors.companyBusiness = "Required";
    if (!companyValues.trim()) newErrors.companyValues = "Required";
    if (!conversationPurpose.trim()) newErrors.conversationPurpose = "Required";
    if (!conversationType.trim()) newErrors.conversationType = "Required";
    return newErrors;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await axios.post(
        "http://127.0.0.1:5000/get_info",
        {
          salespersonName,
          salespersonRole,
          companyName,
          companyBusiness,
          companyValues,
          conversationPurpose,
          conversationType,
          withTools,
        },
        { withCredentials: true }
      );
      setIsSubmitted(true);
      toast.success("Form submitted successfully!");
      handleMicClick(); // Start the conversation after form submission
    } catch (error) {
      toast.error("Failed to submit form. Please try again.");
      console.error("Error submitting form:", error);
    }
  };

  // Start audio recording
  const startRecording = async () => {
    try {
      if (!streamRef.current) {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            sampleRate: 16000,
            sampleSize: 16,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true,
          },
        });
        streamRef.current = stream;
      }

      audioChunksRef.current = [];
      mediaRecorderRef.current = new MediaRecorder(streamRef.current);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setIsMicActive(true);
    } catch (error) {
      console.error("Error starting recording:", error);
      toast.error("Failed to start recording");
    }
  };

  // Stop audio recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsMicActive(false);
    }
  };

  // Send recorded audio to the backend
  const handleSendAudio = async () => {
    if (!isRecording || isEndOfCall) return;
  
    stopRecording();
    setIsProcessing(true);
  
    setTimeout(async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      try {
        await sendAudioToServer(audioBlob);
      } catch (error) {
        console.error("Error sending audio:", error);
        toast.error("Failed to send audio. Please try again.");
      } finally {
        setIsProcessing(false);
      }
    }, 200);
  };

  // Send audio to the backend
  const sendAudioToServer = async (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "user-audio.wav");
  
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_audio",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          timeout: 30000,
        }
      );
  
      setAudioUrl(response.data.audioUrl);
      setAudioMessage(response.data.message || "");
      setIsEndOfCall(response.data.isEndOfCall || false);
  
      if (response.data.isEndOfCall) {
        toast.success("Call completed successfully!");
      }
    } catch (error) {
      console.error("Error sending audio:", error);
      toast.error("Failed to process audio. Please try again.");
      throw error;
    }
  };

  const handleMicClick = async () => {
    if (isEndOfCall) {
      toast.success("Call has already ended.");
      return;
    }
  
    try {
      setIsMicActive(true);
      setIsProcessing(true);
  
      const response = await axios.get("http://127.0.0.1:5000/agent", {
        timeout: 30000,
      });
  
      setAudioUrl(response.data.audioUrl);
      setAudioMessage(response.data.message || "");
      setIsEndOfCall(response.data.isEndOfCall || false);
  
      if (response.data.isEndOfCall) {
        toast.success("Call completed successfully!");
      }
  
      setIsProcessing(false);
    } catch (error) {
      console.error("Error fetching initial audio:", error);
      toast.error("Failed to start conversation");
      setIsMicActive(false);
      setIsProcessing(false);
    }
  };

  // Play audio when audioUrl changes
  useEffect(() => {
    if (audioUrl) {
      const fullAudioUrl = `http://127.0.0.1:5000/audio/${audioUrl}`;
      console.log("Attempting to play audio from:", fullAudioUrl);

      const audio = new Audio(fullAudioUrl);
      audioRef.current = audio;

      audio.play().catch((error) => {
        console.error("Error playing audio:", error);
        toast.error("Failed to play audio: " + error.message);
      });

      // Add event listener for when the audio ends
      audio.addEventListener("ended", () => {
        console.log("Audio playback ended, starting recording...");
        startRecording();
      });
    }
  }, [audioUrl, isEndOfCall]);

  // Cleanup audio and media streams
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  return (
    <div className="flex h-screen text-white">
      {/* Left Section - Form */}
      <section className="relative w-[30%] bg-gray-700 p-10">
        <img
          src="/calle.png"
          alt=""
          className="absolute top-4 left-6 h-14 border w-14 rounded-full bg-white p-1"
        />
        <h1 className="text-3xl font-semibold text-center mb-10">CALL.E</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { label: "Salesperson Name", value: salespersonName, onChange: setSalespersonName },
            { label: "Salesperson Role", value: salespersonRole, onChange: setSalespersonRole },
            { label: "Company Name", value: companyName, onChange: setCompanyName },
            { label: "Company Business", value: companyBusiness, onChange: setCompanyBusiness },
            { label: "Company Values", value: companyValues, onChange: setCompanyValues },
            { label: "Conversation Purpose", value: conversationPurpose, onChange: setConversationPurpose },
            { label: "Conversation Type", value: conversationType, onChange: setConversationType },
          ].map((field, index) => (
            <div key={index}>
              <label className="block text-sm font-medium mb-1">{field.label}</label>
              <input
                type="text"
                value={field.value}
                onChange={(e) => field.onChange(e.target.value)}
                placeholder={`Enter ${field.label.toLowerCase()}`}
                required
                className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
              />
            </div>
          ))}
          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text font-medium">With Tools</span>
              <input
                type="checkbox"
                checked={withTools}
                onChange={(e) => setWithTools(e.target.checked)}
                className="checkbox checkbox-primary ml-2"
              />
            </label>
          </div>
          <button type="submit" className="w-full mt-4 p-2 bg-blue-700 rounded hover:bg-blue-800 transition">
            Submit to start call.
          </button>
        </form>
      </section>

      {/* Right Section - Conversation Interface */}
      <section className="relative w-[70%] flex flex-col bg-gray-900 items-center justify-center p-10">
        <nav className="absolute top-0 w-max flex justify-between p-4 space-x-6 text-lg">
          <Link to="/" className="hover:text-blue-400">Home</Link>
          <Link to="/Dashboard" className="hover:text-blue-400">Dashboard</Link>
        </nav>
        <img src="/calle.png" alt="" className="h-[40%]" />
        <h2 className="text-4xl pt-4 font-semibold">CALL.E</h2>
        <p className="text-lg text-gray-400">Your personal AI Call-Agent</p>

        {isSubmitted && (
  <div className="flex flex-col items-center justify-center space-y-6">
    {isEndOfCall ? (
      <div className="text-green-500 text-2xl font-semibold">
        Call Ended
      </div>
    ) : (
      <>
        <div className="flex gap-4 items-center">
          <Mic
            onClick={isProcessing ? null : startRecording}
            className={`w-16 h-16 cursor-pointer transition-all duration-200 ${
              isProcessing ? "text-gray-400" : isMicActive ? "text-red-500 scale-110" : "text-primary"
            }`}
          />
          {isRecording && !isProcessing && (
            <Send
              onClick={handleSendAudio}
              className="w-12 h-12 cursor-pointer text-primary hover:scale-110 transition-all duration-200"
            />
          )}
        </div>

        {isProcessing && (
          <div className="flex flex-col items-center">
            <div className="text-blue-500 text-lg font-semibold animate-pulse">
              Processing...
            </div>
            <p className="text-gray-500 text-sm mt-2">
              Please wait while we process your request
            </p>
          </div>
        )}

        {isRecording && !isProcessing && (
          <div className="flex flex-col items-center">
            <div className="text-red-500 text-lg font-semibold animate-pulse">
              Recording...
            </div>
            <p className="text-gray-500 text-sm mt-2">
              Click send when you're done speaking
            </p>
          </div>
        )}

        {audioUrl && !isRecording && !isProcessing && (
          <div className="flex flex-col items-center">
            <div className="text-blue-500 text-lg font-semibold">
              Playing response...
            </div>
            <p className="text-gray-600 text-sm mt-4 max-w-md text-center">
              {audioMessage}
            </p>
          </div>
        )}
      </>
    )}
  </div>
)}
      </section>
    </div>
  );
};

export default Home;
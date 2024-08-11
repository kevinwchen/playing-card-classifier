"use client";

import { useState } from "react";

export default function Home() {
  const url = "https://card-classifier.kevinc.xyz/predict/";
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [probability, setProbability] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      console.log(response);

      if (!response.ok) {
        throw new Error("Failed to upload the image.");
      }

      const data = await response.json();
      setPrediction(data.prediction);
      setProbability(data.probability);
    } catch (error) {
      console.error("Error uploading image:", error);
      alert(`Error occurred while processing the image.\n ${error}`);
    }
  };

  return (
    <div className="flex flex-col justify-center items-center min-h-screen">
      <div className="text-3xl mb-8">Card Classifier App</div>
      <div>Upload a picture of a playing card:</div>
      <input type="file" onChange={handleFileChange} className="border mb-4" />
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Submit
      </button>
      {prediction && (
        <>
          <div className="mt-4 text-xl">Prediction: {prediction}</div>
          <div className="mt-4 text-xl">Confidence: {probability}</div>
        </>
      )}
    </div>
  );
}

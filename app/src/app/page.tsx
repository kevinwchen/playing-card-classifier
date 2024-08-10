"use client";

import { useState } from "react";

export default function Home() {
  const url = "https://card-classifier.kevinc.xyz/predict/";
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);

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
    } catch (error) {
      console.error("Error uploading image:", error);
      setPrediction("Error occurred while processing the image.");
    }
  };

  return (
    <div className="flex flex-col justify-center items-center min-h-screen">
      <div className="text-5xl mb-8">Card Classifier App</div>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Upload
      </button>
      {prediction && (
        <div className="mt-4 text-xl">Prediction: {prediction}</div>
      )}
    </div>
  );
}

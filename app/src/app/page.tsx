"use client";

import { useState, useEffect } from "react";

export default function Home() {
  // Use environment variable for API URL, fallback to production URL
  const apiBaseUrl =
    process.env.NEXT_PUBLIC_API_URL || "https://card-classifier.kevinc.xyz";
  const url = `${apiBaseUrl}/predict/`;
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [probability, setProbability] = useState<string | null>(null);

  // Cleanup preview URL on component unmount
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);

    // Clean up previous preview URL to prevent memory leaks
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    // Create preview URL for the new file
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
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
      <input
        type="file"
        onChange={handleFileChange}
        className="border mb-4"
        accept="image/*"
      />

      {/* Image Preview */}
      {previewUrl && (
        <div className="mb-4">
          <img
            src={previewUrl}
            alt="Preview of uploaded card"
            className="max-w-sm max-h-80 object-contain border rounded shadow-md"
          />
        </div>
      )}

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

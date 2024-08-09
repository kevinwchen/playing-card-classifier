"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "https://card-classifier.kevinc.xyz/predict/",
        {
          method: "POST",
          body: formData,
        }
      );

      console.log(response);

      if (response.ok) {
        const data = await response.json();
        console.log("Upload successful:", data);
        setResult(`Prediction: ${data.prediction}`);
      } else {
        console.error("Upload failed:", response.statusText);
        setResult("Upload failed. Please try again.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setResult("An error occurred. Please try again.");
    }
  };

  return (
    <div className="flex flex-col justify-center items-center min-h-screen">
      <div className="text-5xl">Card Classifier App</div>
      <form onSubmit={handleSubmit} className="mt-8">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="mb-4"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md"
        >
          Upload Photo
        </button>
      </form>
      {result && <div className="mt-4 text-center">{result}</div>}
    </div>
  );
}

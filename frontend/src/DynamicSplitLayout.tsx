import React, { useEffect, useRef, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

interface Job {
  JOB_ID: number;
  JOB_DESCRIPTION: string;
  APPLICATION: string;
}

export default function DynamicSplitLayout() {
  const [currentJob, setCurrentJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const leftBoxRef = useRef<HTMLDivElement>(null);
  const rightBoxRef = useRef<HTMLDivElement>(null);
  const [boxHeight, setBoxHeight] = useState<number | undefined>();

  const fetchNextJob = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log("Fetching from:", `${API_URL}/api/jobs/next`);
      const response = await fetch(`${API_URL}/api/jobs/next`);
      console.log("Response status:", response.status);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("No more jobs available");
        }
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      const data = await response.json();
      console.log("Received data:", data);
      setCurrentJob(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNextJob();
  }, []);

  useEffect(() => {
    const updateHeight = () => {
      if (leftBoxRef.current && rightBoxRef.current) {
        const leftHeight = leftBoxRef.current.scrollHeight;
        const rightHeight = rightBoxRef.current.scrollHeight;
        const maxHeight = Math.max(leftHeight, rightHeight);
        setBoxHeight(maxHeight);
      }
    };

    updateHeight();
    window.addEventListener("resize", updateHeight);

    return () => window.removeEventListener("resize", updateHeight);
  }, [currentJob]);

  const handleSkip = () => {
    fetchNextJob();
  };

  const handleSend = () => {
    if (currentJob) {
      console.log("Application sent for job ID:", currentJob.JOB_ID);
      fetchNextJob();
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading next job...</div>;
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <p className="text-red-500 mb-4">{error}</p>
        <button onClick={fetchNextJob} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Try Again
        </button>
      </div>
    );
  }

  if (!currentJob) {
    return <div className="flex justify-center items-center h-screen">No jobs available</div>;
  }

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1 overflow-hidden p-4 gap-4">
        <div className="w-1/2 overflow-auto border rounded-lg shadow-md">
          <div className="p-4 border-b">
            <h2 className="text-xl font-bold">Job Description</h2>
          </div>
          <div
            ref={leftBoxRef}
            className="p-4"
            style={{ height: boxHeight ? `${boxHeight}px` : "auto" }}
          >
            <p className="whitespace-pre-line">{currentJob.JOB_DESCRIPTION}</p>
          </div>
        </div>

        <div className="w-1/2 overflow-auto border rounded-lg shadow-md">
          <div className="p-4 border-b">
            <h2 className="text-xl font-bold">Application</h2>
          </div>
          <div
            ref={rightBoxRef}
            className="p-4"
            style={{ height: boxHeight ? `${boxHeight}px` : "auto" }}
          >
            <p className="whitespace-pre-line">{currentJob.APPLICATION}</p>
          </div>
        </div>
      </div>

      <div className="flex justify-center space-x-4 p-4 bg-gray-100">
        <button
          onClick={handleSkip}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
        >
          Skip
        </button>
        <button
          onClick={handleSend}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
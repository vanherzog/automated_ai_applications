import React, { useEffect, useRef, useState } from "react";
import { Button } from "./components/ui/button";

// const API_URL = 'http://localhost:5000';  // Add this line at the top of the file
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Define the props interface
interface DynamicSplitLayoutProps {
  job_description: string;
  application: string;
}

export default function DynamicSplitLayout({
  job_description,
  application,
}: DynamicSplitLayoutProps) {
  const [currentJob, setCurrentJob] = useState<{ JOB_ID: number; JOB_DESCRIPTION: string; APPLICATION: string } | null>(null);
  const [loading, setLoading] = useState(false);
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
        <Button onClick={fetchNextJob}>Try Again</Button>
      </div>
    );
  }

  if (!currentJob) {
    return <div className="flex justify-center items-center h-screen">No jobs available</div>;
  }

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1 overflow-hidden">
        {/* Left side */}
        <div className="w-1/2 p-4 overflow-auto border-r border-gray-200">
          <div
            ref={leftBoxRef}
            className="bg-white p-6 rounded-lg shadow-md overflow-auto"
            style={{ height: boxHeight ? `${boxHeight}px` : "auto" }}
          >
            <h2 className="text-xl font-bold mb-4">Job Description</h2>
            <p className="whitespace-pre-line">{job_description || currentJob.JOB_DESCRIPTION}</p>
          </div>
        </div>

        {/* Vertical line */}
        <div className="w-px bg-gray-200"></div>

        {/* Right side */}
        <div className="w-1/2 p-4 overflow-auto">
          <div
            ref={rightBoxRef}
            className="bg-white p-6 rounded-lg shadow-md overflow-auto"
            style={{ height: boxHeight ? `${boxHeight}px` : "auto" }}
          >
            <h2 className="text-xl font-bold mb-4">Application</h2>
            <p className="whitespace-pre-line">{application || currentJob.APPLICATION}</p>
          </div>
        </div>
      </div>

      {/* Buttons at the bottom */}
      <div className="flex justify-center space-x-4 p-4 bg-gray-100">
        <Button variant="outline" onClick={handleSkip}>Skip</Button>
        <Button onClick={handleSend}>Send</Button>
      </div>
    </div>
  );
}

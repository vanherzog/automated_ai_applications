import React, { useEffect, useState } from "react";
import './DynamicSplitLayout.css';

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
  const [sending, setSending] = useState(false);

  const fetchNextJob = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_URL}/api/jobs/next`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("No more jobs available");
        }
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      const data = await response.json();
      setCurrentJob(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!currentJob) return;

    try {
      setSending(true);
      const response = await fetch(`${API_URL}/api/send-application`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_id: currentJob.JOB_ID,
          application: currentJob.APPLICATION,
          job_description: currentJob.JOB_DESCRIPTION
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send application');
      }

      await fetchNextJob();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send application");
    } finally {
      setSending(false);
    }
  };

  useEffect(() => {
    fetchNextJob();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <span>Loading next job...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button className="button retry-button" onClick={fetchNextJob}>
          Try Again
        </button>
      </div>
    );
  }

  if (!currentJob) {
    return (
      <div className="empty-container">
        <p>No jobs available</p>
      </div>
    );
  }

  return (
    <div className="split-layout">
      <div className="panel left-panel">
        <h1 className="panel-title">Job Description</h1>
        <div className="panel-content">
          <div className="content-wrapper">
            {currentJob.JOB_DESCRIPTION}
          </div>
        </div>
      </div>

      <div className="panel right-panel">
        <h1 className="panel-title">Application</h1>
        <div className="panel-content">
          <div className="content-wrapper">
            {currentJob.APPLICATION}
          </div>
        </div>
      </div>

      <div className="button-container">
        <button
          className="button skip-button"
          onClick={fetchNextJob}
          disabled={loading || sending}
        >
          Skip
        </button>
        <button
          className="button send-button"
          onClick={handleSend}
          disabled={loading || sending}
        >
          {sending ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
import {  PrimaryButton, TextField, Spinner } from "@fluentui/react"
import { useState } from "react";

const SERVICE_ENDPOINT = "http://localhost:8000/summarize";

export default function Notes() {
  const [notes, setNotes] = useState<string>("")
  const [summary, setSummary] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const fetchSummary = async () => {
    setLoading(true);
    setSummary("");
    const response = await fetch(SERVICE_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: notes}),
    });
    const data = await response.json();
    setSummary(data.summary);
    setLoading(false);
  };

  return (
    <div style={{padding: "50px"}} >
      <h1>Enter Notes:</h1>
      <TextField label="Notes" multiline onChange={(_ev, value) => setNotes(_ev.currentTarget.value)} rows={20} />

      <br />    
      <PrimaryButton onClick={fetchSummary}>Summarize</PrimaryButton>
      {summary && <p>Summary: {summary}</p>}   
      {loading && <Spinner label="Loading..." />}
 </div>
  );
}
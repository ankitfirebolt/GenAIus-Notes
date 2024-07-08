import {  PrimaryButton, TextField, Spinner } from "@fluentui/react"
import { useState } from "react";

const SERVICE_ENDPOINT = "http://localhost:8000/invoke";

export default function Query() {
  const [query, setQuery] = useState<string>("")
  const [output, setOutput] = useState<string>("")
  const [ragOutput, setRAGOutput] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const fetchOutput = async () => {
    setLoading(true);
    setOutput("");
    setRAGOutput("");
    const response = await fetch(SERVICE_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: query}),
    });
    const data = await response.json();
    setOutput(data.output);
    setRAGOutput(data.rag_output);
    setLoading(false);
  };

  return (
    <div style={{padding: "50px"}} >
      <h1>Enter Query:</h1>
      <TextField label="Query" multiline onChange={(_ev, value) => setQuery(_ev.currentTarget.value)} rows={20} />

      <br />    
      <PrimaryButton onClick={fetchOutput}>Enter</PrimaryButton>
      {output && <p>{output}</p>}
      {ragOutput && <p>{ragOutput}</p>}   
      {loading && <Spinner label="Loading..." />}
 </div>
  );
}
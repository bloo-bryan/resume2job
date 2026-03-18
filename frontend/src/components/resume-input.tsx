"use client";

import { useRef, useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { parseFile } from "@/lib/api";

interface ResumeInputProps {
  onTextChange: (text: string) => void;
  text: string;
  disabled?: boolean;
}

export function ResumeInput({ onTextChange, text, disabled }: ResumeInputProps) {
  const [file, setFile] = useState<File | null>(null);
  const [parsing, setParsing] = useState(false);
  const [parseError, setParseError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setParsing(true);
    setParseError(null);
    try {
      const result = await parseFile(selected, "resume");
      onTextChange(result.cleaned_text);
    } catch (err) {
      onTextChange("");
      setParseError(err instanceof Error ? err.message : "Failed to parse file");
    } finally {
      setParsing(false);
    }
  }

  function clearFile() {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-zinc-300">Resume</label>

      <div className="flex items-center gap-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={() => inputRef.current?.click()}
          disabled={disabled || parsing}
        >
          {parsing ? "Parsing..." : "Upload PDF/DOCX"}
        </Button>
        {file && (
          <div className="flex items-center gap-1.5 text-sm text-zinc-400">
            <span className="truncate max-w-48">{file.name}</span>
            <button
              onClick={clearFile}
              className="text-zinc-500 hover:text-zinc-300"
            >
              &times;
            </button>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFile}
          className="hidden"
        />
      </div>

      {parseError && (
        <p className="text-sm text-red-500">{parseError}</p>
      )}

      <Textarea
        placeholder="Or paste resume text..."
        value={text}
        onChange={(e) => onTextChange(e.target.value)}
        rows={10}
        disabled={disabled}
        className="resize-none bg-zinc-900 border-zinc-800 text-zinc-100 placeholder:text-zinc-600"
      />
    </div>
  );
}

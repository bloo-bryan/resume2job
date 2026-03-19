"use client";

import { useRef, useState, useCallback } from "react";
import { Textarea } from "@/components/ui/textarea";
import { parseFile } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ResumeInputProps {
  onTextChange: (text: string) => void;
  text: string;
  disabled?: boolean;
}

export function ResumeInput({ onTextChange, text, disabled }: ResumeInputProps) {
  const [file, setFile] = useState<File | null>(null);
  const [parsing, setParsing] = useState(false);
  const [parseError, setParseError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = useCallback(
    async (selected: File) => {
      setFile(selected);
      setParsing(true);
      setParseError(null);
      try {
        const result = await parseFile(selected, "resume");
        onTextChange(result.cleaned_text);
      } catch (err) {
        onTextChange("");
        setParseError(
          `Failed to parse ${selected.name}: ${err instanceof Error ? err.message : "Unknown error"}`
        );
      } finally {
        setParsing(false);
      }
    },
    [onTextChange]
  );

  function handleFileInput(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (selected) handleFileUpload(selected);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) handleFileUpload(dropped);
  }

  function clearFile() {
    setFile(null);
    setParseError(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="space-y-3">
      <label htmlFor="resume-textarea" className="text-sm font-medium text-zinc-300">
        Resume
      </label>

      {/* Drop zone / file status */}
      {!file ? (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => !disabled && !parsing && inputRef.current?.click()}
          className={cn(
            "flex items-center justify-center min-h-[44px] rounded-md border border-dashed cursor-pointer transition-colors",
            dragOver
              ? "border-blue-500 bg-blue-500/5"
              : "border-zinc-700 hover:border-zinc-600",
            (disabled || parsing) && "opacity-50 cursor-not-allowed"
          )}
        >
          {parsing ? (
            <span className="text-sm text-zinc-400 py-2">
              Parsing file...
            </span>
          ) : (
            <div className="flex items-center gap-2 py-2 text-sm text-zinc-500">
              <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
                <path d="M8 2v8M4 6l4-4 4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M2 12h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
              Drop PDF or DOCX here, or click to browse
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center gap-2 rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2">
          <span className="text-sm text-zinc-300 truncate max-w-48">{file.name}</span>
          <span className="text-xs text-zinc-500">
            {(file.size / 1024).toFixed(0)} KB
          </span>
          <button
            onClick={clearFile}
            className="ml-auto text-sm text-zinc-500 hover:text-zinc-300 min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label={`Remove ${file.name}`}
          >
            ✕ Remove
          </button>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        onChange={handleFileInput}
        className="hidden"
        aria-hidden="true"
      />

      {parseError && (
        <p className="text-sm text-red-500" role="alert">{parseError}</p>
      )}

      <Textarea
        id="resume-textarea"
        placeholder="Or paste resume text..."
        value={text}
        onChange={(e) => onTextChange(e.target.value)}
        rows={10}
        disabled={disabled}
        aria-required="true"
        className="resize-none bg-zinc-900 border-zinc-800 text-zinc-100 placeholder:text-zinc-600"
      />
    </div>
  );
}

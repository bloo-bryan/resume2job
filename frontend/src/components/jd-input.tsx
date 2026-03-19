import { Textarea } from "@/components/ui/textarea";

interface JdInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function JdInput({ value, onChange, disabled }: JdInputProps) {
  return (
    <div className="space-y-3">
      <label htmlFor="jd-textarea" className="text-sm font-medium text-zinc-300">
        Job Description
      </label>
      <Textarea
        id="jd-textarea"
        placeholder="Paste job description text..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={12}
        disabled={disabled}
        aria-required="true"
        className="resize-none bg-zinc-900 border-zinc-800 text-zinc-100 placeholder:text-zinc-600"
      />
    </div>
  );
}

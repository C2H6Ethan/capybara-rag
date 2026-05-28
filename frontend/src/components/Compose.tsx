"use client";
import { useRef, useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";

export default function Compose({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [value, setValue] = useState("");
  const taRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = taRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(200, el.scrollHeight) + "px";
  }, [value]);

  const submit = () => {
    const v = value.trim();
    if (!v || disabled) return;
    onSend(v);
    setValue("");
  };

  return (
    <div className="compose-wrap">
      <div className="compose">
        <textarea
          ref={taRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
          placeholder="ask capy a capybara question…"
          rows={1}
        />
        <button
          className="send"
          onClick={submit}
          disabled={!value.trim() || disabled}
          title="Send"
        >
          <ArrowUp size={16} strokeWidth={1.8} />
        </button>
      </div>
      <div className="compose-meta">
        capy may misremember
        <span className="yuzu" />
        always verify important facts
      </div>
    </div>
  );
}

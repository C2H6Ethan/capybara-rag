"use client";
import Image from "next/image";
import { Copy, RefreshCw, ThumbsUp } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Message } from "@/app/page";

export default function AssistantMessage({ msg }: { msg: Message & { role: "capy" } }) {
  const sources = msg.sources ?? [];

  return (
    <div className="msg-capy">
      <div className="avatar">
        <Image src="/capybara.png" width={36} height={36} alt="" aria-hidden style={{ padding: "6%" }} />
      </div>
      <div className="body">
        <div className="name">capy</div>
        <div className={`content${msg.streaming ? " typing-caret" : ""}`}>
          <ReactMarkdown>{msg.text}</ReactMarkdown>
        </div>

        {sources.length > 0 && !msg.streaming && (
          <div className="sources">
            {sources.map((s, i) => (
              <span key={i} className="source-chip">
                {s.display_name}
              </span>
            ))}
          </div>
        )}

        {!msg.streaming && (
          <div className="msg-actions">
            <button title="Copy" onClick={() => navigator.clipboard.writeText(msg.text)}>
              <Copy size={14} strokeWidth={1.6} />
            </button>
            <button title="Regenerate">
              <RefreshCw size={14} strokeWidth={1.6} />
            </button>
            <button title="Helpful">
              <ThumbsUp size={14} strokeWidth={1.6} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

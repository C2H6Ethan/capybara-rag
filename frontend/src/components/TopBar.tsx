"use client";
import { Plus } from "lucide-react";

export default function TopBar({ onNewChat }: { onNewChat: () => void }) {
  return (
    <div className="topbar">
      <div className="wordmark">
        <span className="capy-mark">capy</span>
        <span className="gpt-mark">GPT</span>
        <span className="wordmark-dot" />
      </div>
      <div className="top-actions">
        <button className="icon-btn" title="New chat" onClick={onNewChat}>
          <Plus size={18} strokeWidth={1.6} />
        </button>
      </div>
    </div>
  );
}

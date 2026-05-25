"use client";
import { useState, useRef, useCallback, useEffect } from "react";
import TopBar from "@/components/TopBar";
import EmptyState from "@/components/EmptyState";
import ThinkingPod from "@/components/ThinkingPod";
import AssistantMessage from "@/components/AssistantMessage";
import Compose from "@/components/Compose";

export type Source = {
  source_file: string;
  display_name: string;
  distance: number;
  text_preview: string;
};

export type Message =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "capy"; text: string; streaming: boolean; sources?: Source[] };

function uid() {
  return Math.random().toString(36).slice(2);
}

export default function ChatApp() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback((smooth = true) => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior: smooth ? "smooth" : "instant" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages.length, thinking, scrollToBottom]);

  // Autoscroll during streaming only if user is near the bottom
  useEffect(() => {
    const isStreaming = messages.some((m) => m.role === "capy" && m.streaming);
    if (!isStreaming) return;
    const id = setInterval(() => {
      const el = scrollRef.current;
      if (!el) return;
      const dist = el.scrollHeight - el.scrollTop - el.clientHeight;
      if (dist < 200) el.scrollTop = el.scrollHeight;
    }, 100);
    return () => clearInterval(id);
  }, [messages]);

  const send = useCallback(async (text: string) => {
    setMessages((m) => [...m, { id: uid(), role: "user", text }]);
    setThinking(true);

    const replyId = uid();
    let buf = "";
    let firstToken = true;

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text, top_k: 5 }),
      });

      if (!res.ok || !res.body) {
        throw new Error(`HTTP ${res.status}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });

        let idx: number;
        while ((idx = buf.indexOf("\n\n")) >= 0) {
          const frame = buf.slice(0, idx).trim();
          buf = buf.slice(idx + 2);
          if (!frame.startsWith("data:")) continue;

          let event: { type: string; content?: string; sources?: Source[] };
          try {
            event = JSON.parse(frame.slice(5).trim());
          } catch {
            continue;
          }

          if (event.type === "chunk" && event.content) {
            if (firstToken) {
              firstToken = false;
              setThinking(false);
              setMessages((m) => [
                ...m,
                { id: replyId, role: "capy", text: "", streaming: true },
              ]);
            }
            setMessages((m) =>
              m.map((x) =>
                x.id === replyId && x.role === "capy"
                  ? { ...x, text: x.text + event.content }
                  : x
              )
            );
          } else if (event.type === "sources" && event.sources) {
            setMessages((m) =>
              m.map((x) =>
                x.id === replyId && x.role === "capy"
                  ? { ...x, sources: event.sources }
                  : x
              )
            );
          } else if (event.type === "error" && event.content) {
            if (firstToken) {
              firstToken = false;
              setThinking(false);
              setMessages((m) => [
                ...m,
                { id: replyId, role: "capy", text: event.content!, streaming: false },
              ]);
            }
          }
        }
      }
    } catch (err) {
      setThinking(false);
      if (firstToken) {
        setMessages((m) => [
          ...m,
          {
            id: replyId,
            role: "capy",
            text: "Something went wrong — make sure the backend is running.",
            streaming: false,
          },
        ]);
      }
      console.error(err);
    }

    setMessages((m) =>
      m.map((x) =>
        x.id === replyId && x.role === "capy" ? { ...x, streaming: false } : x
      )
    );
  }, []);

  const newChat = useCallback(() => {
    setMessages([]);
    setThinking(false);
    scrollRef.current?.scrollTo({ top: 0 });
  }, []);

  return (
    <div className="app">
      <TopBar onNewChat={newChat} />
      <div className="scroll" ref={scrollRef}>
        <div className="chat">
          {messages.length === 0 ? (
            <EmptyState onPick={send} />
          ) : (
            <>
              {messages.map((m) =>
                m.role === "user" ? (
                  <div key={m.id} className="msg-user">{m.text}</div>
                ) : (
                  <AssistantMessage key={m.id} msg={m} />
                )
              )}
              {thinking && <ThinkingPod />}
            </>
          )}
        </div>
      </div>
      <Compose onSend={send} disabled={thinking} />
    </div>
  );
}

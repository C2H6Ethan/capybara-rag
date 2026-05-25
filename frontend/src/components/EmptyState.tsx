"use client";
import CapyInOnsen from "./CapyInOnsen";

const SUGGESTED_PROMPTS = [
  { kicker: "Behavior", text: "Why are capybaras so famously chill?" },
  { kicker: "Diet",     text: "What do capybaras actually eat?" },
  { kicker: "Habitat",  text: "Where in the world do capybaras live?" },
  { kicker: "Biology",  text: "How big do capybaras get?" },
];

export default function EmptyState({ onPick }: { onPick: (text: string) => void }) {
  return (
    <div className="empty">
      <div className="hero-onsen">
        <div className="steam s1" />
        <div className="steam s2" />
        <div className="steam s3" />
        <div className="steam s4" />
        <div className="steam s5" />
        <div className="capy-bob">
          <CapyInOnsen scale={1.6} />
        </div>
      </div>

      <h1 className="empty-title">
        ask <em>capy</em> anything about capybaras.
      </h1>
      <p className="empty-sub">a cozy little chatbot that knows one thing very well.</p>

      <div className="prompts">
        {SUGGESTED_PROMPTS.map((p) => (
          <button key={p.kicker} className="prompt-card" onClick={() => onPick(p.text)}>
            <span className="pc-kicker">{p.kicker}</span>
            <span className="pc-text">{p.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function CapyInOnsen({ scale = 1 }: { scale?: number }) {
  const W = 140 * scale;
  const H = 100 * scale;
  return (
    <svg
      viewBox="0 0 140 100"
      width={W}
      height={H}
      aria-hidden="true"
      style={{ display: "block", overflow: "visible" }}
    >
      <ellipse cx="70" cy="78" rx="58" ry="12" fill="var(--water)" />
      <ellipse cx="70" cy="78" rx="58" ry="12" fill="none" stroke="var(--water-deep)" strokeWidth="0.7" opacity="0.45" />
      <path d="M 38 78 Q 38 60 70 58 Q 102 60 102 78 Z" fill="var(--capy)" />
      <path d="M 44 64 Q 70 60 96 64" stroke="var(--capy-deep)" strokeWidth="0.8" fill="none" opacity="0.4" />
      <ellipse cx="70" cy="48" rx="24" ry="20" fill="var(--capy)" />
      <ellipse cx="70" cy="54" rx="18" ry="9" fill="var(--capy-warm)" opacity="0.45" />
      <ellipse cx="53" cy="32" rx="5.5" ry="5" fill="var(--capy-deep)" />
      <ellipse cx="87" cy="32" rx="5.5" ry="5" fill="var(--capy-deep)" />
      <ellipse cx="53.5" cy="33" rx="2.4" ry="2" fill="var(--capy-warm)" opacity="0.7" />
      <ellipse cx="87.5" cy="33" rx="2.4" ry="2" fill="var(--capy-warm)" opacity="0.7" />
      <path d="M58 46 Q62 43 66 46" stroke="#2A2520" strokeWidth="1.6" fill="none" strokeLinecap="round" />
      <path d="M74 46 Q78 43 82 46" stroke="#2A2520" strokeWidth="1.6" fill="none" strokeLinecap="round" />
      <ellipse cx="70" cy="58" rx="10" ry="5.5" fill="var(--capy-warm)" opacity="0.55" />
      <ellipse cx="70" cy="58" rx="2.4" ry="1.6" fill="#2A2520" />
      <path d="M67 62 Q70 64 73 62" stroke="#2A2520" strokeWidth="1.1" fill="none" strokeLinecap="round" />
      <path d="M 6 76 Q 32 70 70 74 Q 108 78 134 72 L 134 100 L 6 100 Z" fill="var(--water)" />
      <path d="M 6 76 Q 32 70 70 74 Q 108 78 134 72" stroke="var(--water-deep)" strokeWidth="0.7" fill="none" opacity="0.55" />
      <path d="M 20 84 Q 26 82 32 84" stroke="var(--water-deep)" strokeWidth="0.6" fill="none" strokeLinecap="round" opacity="0.55" />
      <path d="M 100 86 Q 106 84 112 86" stroke="var(--water-deep)" strokeWidth="0.6" fill="none" strokeLinecap="round" opacity="0.55" />
      <g>
        <ellipse cx="18" cy="80" rx="5" ry="4.4" fill="var(--citrus)" />
        <ellipse cx="16.6" cy="78.6" rx="1.6" ry="1" fill="var(--citrus-soft)" opacity="0.85" />
        <path d="M18 76 L18 75" stroke="var(--forest)" strokeWidth="0.8" strokeLinecap="round" />
      </g>
      <g>
        <ellipse cx="120" cy="84" rx="3.6" ry="3.2" fill="var(--citrus)" />
        <path d="M120 81.5 L120 80.5" stroke="var(--forest)" strokeWidth="0.7" strokeLinecap="round" />
      </g>
    </svg>
  );
}

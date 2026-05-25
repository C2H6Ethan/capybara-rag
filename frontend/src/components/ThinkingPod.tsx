import Image from "next/image";
import CapyInOnsen from "./CapyInOnsen";

export default function ThinkingPod() {
  return (
    <div className="msg-capy">
      <div className="avatar">
        <Image src="/capybara.png" width={36} height={36} alt="" aria-hidden style={{ padding: "6%" }} />
      </div>
      <div className="body">
        <div className="name">
          capy <span className="status">soaking</span>
        </div>
        <div className="thinking-inner">
          <div className="onsen">
            <div className="steam s1" />
            <div className="steam s2" />
            <div className="steam s3" />
            <div className="steam s4" />
            <div className="steam s5" />
            <div className="capy-bob">
              <CapyInOnsen scale={0.6} />
            </div>
          </div>
          <span className="thinking-label">letting that one steep</span>
        </div>
      </div>
    </div>
  );
}

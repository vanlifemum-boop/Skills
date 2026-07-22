"use client";

/**
 * CinematicReveal — React/Next drop-in for the canvas image-sequence scrub.
 *
 * Usage:
 *   <CinematicReveal
 *     frameCount={179}
 *     bg="#0a0a12"
 *     framePath={(i) => `/frames/spin/frame_${String(i).padStart(4, "0")}.jpg`}
 *     heightVh={500}
 *   >
 *     <div className="overlay">…scroll-synced copy…</div>
 *   </CinematicReveal>
 *
 * The section is `heightVh` tall; an inner sticky stage pins the canvas and the
 * frame is chosen by the section's scroll progress. Children render in an
 * absolutely-positioned overlay on top of the canvas.
 *
 * No external deps. If you already run Lenis app-wide, this still works — it
 * reads scroll position on a rAF loop and is agnostic to the scroll source.
 */

import { useEffect, useRef } from "react";
import type { ReactNode, CSSProperties } from "react";

const DPR_CAP = 2;

export type CinematicRevealProps = {
  frameCount: number;
  framePath: (index: number) => string;
  bg?: string;
  heightVh?: number;
  className?: string;
  style?: CSSProperties;
  children?: ReactNode;
  /** Called with 0..1 progress each frame — handy for driving overlay opacity. */
  onProgress?: (progress: number) => void;
};

export default function CinematicReveal({
  frameCount,
  framePath,
  bg = "#000",
  heightVh = 500,
  className,
  style,
  children,
  onProgress,
}: CinematicRevealProps) {
  const outerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentRef = useRef<number>(-1);
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    const outer = outerRef.current;
    if (!canvas || !outer) return;
    const ctx = canvas.getContext("2d", { alpha: false });
    if (!ctx) return;

    // Preload frames.
    const images: HTMLImageElement[] = new Array(frameCount);
    for (let i = 0; i < frameCount; i++) {
      const img = new Image();
      img.decoding = "async";
      img.src = framePath(i);
      images[i] = img;
    }
    imagesRef.current = images;

    const draw = (index: number) => {
      if (index === currentRef.current) return;
      currentRef.current = index;
      const cw = canvas.width;
      const ch = canvas.height;
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, cw, ch);
      const img = images[index];
      if (!img || !img.complete || !img.naturalWidth) return;
      const scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
      const dw = img.naturalWidth * scale;
      const dh = img.naturalHeight * scale;
      ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
    };

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, DPR_CAP);
      canvas.width = Math.round(canvas.clientWidth * dpr);
      canvas.height = Math.round(canvas.clientHeight * dpr);
      const idx = currentRef.current < 0 ? 0 : currentRef.current;
      currentRef.current = -1;
      draw(idx);
    };

    const progress = () => {
      const rect = outer.getBoundingClientRect();
      const scrollable = rect.height - window.innerHeight;
      if (scrollable <= 0) return 0;
      return Math.min(Math.max(-rect.top / scrollable, 0), 1);
    };

    const loop = () => {
      const p = progress();
      const idx = Math.min(
        frameCount - 1,
        Math.max(0, Math.round(p * (frameCount - 1)))
      );
      draw(idx);
      onProgress?.(p);
      rafRef.current = requestAnimationFrame(loop);
    };

    resize();
    window.addEventListener("resize", resize, { passive: true });
    rafRef.current = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener("resize", resize);
    };
  }, [frameCount, framePath, bg, onProgress]);

  return (
    <section
      ref={outerRef}
      className={className}
      style={{ position: "relative", height: `${heightVh}vh`, ...style }}
    >
      <div style={{ position: "sticky", top: 0, height: "100vh", overflow: "hidden" }}>
        <canvas
          ref={canvasRef}
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%", display: "block" }}
        />
        {children ? (
          <div style={{ position: "absolute", inset: 0, zIndex: 2, pointerEvents: "none" }}>
            {children}
          </div>
        ) : null}
      </div>
    </section>
  );
}

/**
 * Deterministic unique avatar generator based on string hash (e.g. user email).
 * Creates completely unique colors, eyes, head shapes, accessories, and mouth patterns.
 */

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

const COLOR_PALETTES = [
  { bg1: "#0f172a", bg2: "#1e1b4b", body: "#6366f1", accent: "#a855f7", eyes: "#38bdf8" }, // Indigo Violet
  { bg1: "#022c22", bg2: "#064e3b", body: "#10b981", accent: "#34d399", eyes: "#fef08a" }, // Emerald Mint
  { bg1: "#1c1917", bg2: "#451a03", body: "#f59e0b", accent: "#fbbf24", eyes: "#38bdf8" }, // Amber Gold
  { bg1: "#172554", bg2: "#1e3a8a", body: "#0284c7", accent: "#38bdf8", eyes: "#4ade80" }, // Cyan Blue
  { bg1: "#3b0764", bg2: "#581c87", body: "#c084fc", accent: "#e879f9", eyes: "#fef08a" }, // Neon Purple
  { bg1: "#450a0a", bg2: "#7f1d1d", body: "#f43f5e", accent: "#fb7185", eyes: "#67e8f9" }, // Crimson Rose
  { bg1: "#18181b", bg2: "#27272a", body: "#06b6d4", accent: "#14b8a6", eyes: "#f43f5e" }, // Teal Slate
  { bg1: "#0c0a09", bg2: "#292524", body: "#8b5cf6", accent: "#a78bfa", eyes: "#22c55e" }, // Royal Violet
];

function generateUniqueAvatarSVG(email) {
  const cleanEmail = (email || "coderescue@user.dev").trim().toLowerCase();
  const hash = hashString(cleanEmail);

  const palette = COLOR_PALETTES[hash % COLOR_PALETTES.length];
  const headVariant = (hash >> 3) % 4; // 4 head shapes
  const eyeVariant = (hash >> 5) % 5;  // 5 eye styles
  const mouthVariant = (hash >> 8) % 4; // 4 mouth styles
  const accessoryVariant = (hash >> 11) % 4; // 4 accessories

  // Eye styles
  let eyesSvg = "";
  if (eyeVariant === 0) {
    // Round tech eyes
    eyesSvg = `
      <circle cx="36" cy="48" r="6" fill="${palette.eyes}" />
      <circle cx="64" cy="48" r="6" fill="${palette.eyes}" />
      <circle cx="38" cy="46" r="2" fill="#ffffff" />
      <circle cx="66" cy="46" r="2" fill="#ffffff" />
    `;
  } else if (eyeVariant === 1) {
    // Cyberspace visor
    eyesSvg = `
      <rect x="26" y="44" width="48" height="10" rx="5" fill="${palette.eyes}" />
      <line x1="30" y1="49" x2="70" y2="49" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3" />
    `;
  } else if (eyeVariant === 2) {
    // Geek coder glasses
    eyesSvg = `
      <rect x="28" y="42" width="18" height="14" rx="3" fill="none" stroke="${palette.eyes}" stroke-width="3" />
      <rect x="54" y="42" width="18" height="14" rx="3" fill="none" stroke="${palette.eyes}" stroke-width="3" />
      <line x1="46" y1="48" x2="54" y2="48" stroke="${palette.eyes}" stroke-width="3" />
      <circle cx="37" cy="49" r="3" fill="#ffffff" />
      <circle cx="63" cy="49" r="3" fill="#ffffff" />
    `;
  } else if (eyeVariant === 3) {
    // Sleek sensor slots
    eyesSvg = `
      <rect x="30" y="46" width="14" height="4" rx="2" fill="${palette.eyes}" />
      <rect x="56" y="46" width="14" height="4" rx="2" fill="${palette.eyes}" />
    `;
  } else {
    // Star sparkle eyes
    eyesSvg = `
      <circle cx="36" cy="48" r="7" fill="${palette.eyes}" />
      <circle cx="64" cy="48" r="7" fill="${palette.eyes}" />
      <polygon points="36,43 38,47 42,48 38,49 36,53 34,49 30,48 34,47" fill="#ffffff" />
      <polygon points="64,43 66,47 70,48 66,49 64,53 62,49 58,48 62,47" fill="#ffffff" />
    `;
  }

  // Mouth styles
  let mouthSvg = "";
  if (mouthVariant === 0) {
    // Smile
    mouthSvg = `<path d="M 40 68 Q 50 78 60 68" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" fill="none" />`;
  } else if (mouthVariant === 1) {
    // Digital wave mouth
    mouthSvg = `
      <line x1="38" y1="70" x2="62" y2="70" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" />
      <circle cx="50" cy="70" r="2" fill="#ffffff" />
    `;
  } else if (mouthVariant === 2) {
    // Open tech smile
    mouthSvg = `<path d="M 38 66 Q 50 78 62 66 Z" fill="${palette.accent}" />`;
  } else {
    // Smart grin
    mouthSvg = `<path d="M 42 68 Q 54 74 62 66" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" fill="none" />`;
  }

  // Head Shape
  let headShapeSvg = "";
  if (headVariant === 0) {
    // Soft square robot head
    headShapeSvg = `<rect x="20" y="24" width="60" height="60" rx="16" fill="${palette.body}" />`;
  } else if (headVariant === 1) {
    // Round friendly pod head
    headShapeSvg = `<circle cx="50" cy="54" r="32" fill="${palette.body}" />`;
  } else if (headVariant === 2) {
    // Hexagonal / chamfered head
    headShapeSvg = `<polygon points="30,24 70,24 84,54 70,84 30,84 16,54" fill="${palette.body}" />`;
  } else {
    // Shield capsule head
    headShapeSvg = `<path d="M 22 36 Q 50 20 78 36 L 76 68 Q 50 86 24 68 Z" fill="${palette.body}" />`;
  }

  // Accessory / Antenna
  let accessorySvg = "";
  if (accessoryVariant === 0) {
    // Top antenna with glowing node
    accessorySvg = `
      <line x1="50" y1="24" x2="50" y2="12" stroke="${palette.accent}" stroke-width="3" />
      <circle cx="50" cy="10" r="4" fill="${palette.eyes}" />
    `;
  } else if (accessoryVariant === 1) {
    // Dual headphones / side modules
    accessorySvg = `
      <rect x="12" y="42" width="6" height="20" rx="3" fill="${palette.accent}" />
      <rect x="82" y="42" width="6" height="20" rx="3" fill="${palette.accent}" />
      <path d="M 16 44 Q 50 14 84 44" stroke="${palette.accent}" stroke-width="3" fill="none" />
    `;
  } else if (accessoryVariant === 2) {
    // Code badge </ >
    accessorySvg = `
      <rect x="36" y="8" width="28" height="14" rx="4" fill="#0b1120" stroke="${palette.accent}" stroke-width="1.5" />
      <text x="50" y="19" font-family="monospace" font-size="9" font-weight="bold" fill="${palette.eyes}" text-anchor="middle">&lt;/&gt;</text>
    `;
  } else {
    // Python energy crown
    accessorySvg = `
      <polygon points="40,24 45,14 50,22 55,14 60,24" fill="${palette.accent}" />
      <circle cx="50" cy="12" r="2.5" fill="${palette.eyes}" />
    `;
  }

  return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad_${hash}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${palette.bg1}" />
      <stop offset="100%" stop-color="${palette.bg2}" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="24" fill="url(#bgGrad_${hash})" />
  ${accessorySvg}
  ${headShapeSvg}
  ${eyesSvg}
  ${mouthSvg}
</svg>
`.trim();
}

module.exports = {
  generateUniqueAvatarSVG,
  COLOR_PALETTES
};

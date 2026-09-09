# ML-07: Three Roads — Stack Rationale & Empty but Live

**Author**: Kerem Özcan
**Date**: September 9, 2026
**Reference**: [AI Fluency Week 04 — Pick the Stack](https://aifluency.flyrank.ai/week-04.html)

---

## 1. Constraints

- **Cost:** Free only
- **Skill level:** I can read and write HTML/CSS with AI assistance. Python is my strength, not frontend. I am learning.
- **What it needs to do:** 4-page portfolio (Home, Work, How I Work, Contact) with a chart, code blocks, a repo link, and a prompt iteration log excerpt. No forms, no dynamic content at launch.
- **How my work must be shown:** Embedded notebook link (GitHub), a chart image, code blocks, and a repo tree screenshot. Long-form readable text matters more than visual galleries.
- **Dynamic at launch?** No. Static is fine.

---

## 2. Three options considered

### Option A — No-code (Carrd or Framer)

- **Build:** Drag and drop in a visual builder
- **Host:** Carrd/flyrank subdomain or Framer free tier
- **Backend:** No
- **Shows my work:** Poorly. My evidence is a GitHub notebook link, a chart with specific numbers, and code blocks. No-code builders make code embedding and precise typographic control harder, not easier.
- **Trade-off:** Fastest to publish, but I fight the builder every time I need to place a code block or control the chart's size. The tool decides how my figures look.

### Option B — Plain HTML + CSS with AI, on Netlify

- **Build:** Hand-written HTML + CSS, AI-assisted. One `index.html` + a stylesheet.
- **Host:** Netlify free tier (drag and drop, no Git required)
- **Backend:** No
- **Shows my work:** Well. Code blocks, monospace numbers (IBM Plex Mono), hairline rules, and chart images are all native to HTML. I control every margin. The notebook link is just an `<a>` tag.
- **Trade-off:** I write the markup myself (with AI). Slower start than no-code, but every change is a text edit I understand. If I outgrow it, I port the content into a framework — the HTML doesn't lock me in.

### Option C — Next.js on Vercel

- **Build:** React components, a build step, node_modules
- **Host:** Vercel free tier
- **Backend:** Could add API routes later, but not needed now
- **Shows my work:** Well, but the component overhead is real — a 4-page static portfolio does not need a framework, a router, or hydration.
- **Trade-off:** Most powerful, but I spend the build week fighting build config and component structure instead of showing my work. Maintenance is higher: dependencies update, breaking changes happen. "Can I maintain this?" — yes, but the cost is time I should spend on content.

---

## 3. Decision

**Chosen: Option B — Plain HTML + CSS on Netlify.**

**Why not A (no-code):** My portfolio's evidence is code, numbers, and a chart. No-code builders optimize for visual layouts and image galleries. I need precise control over code blocks and monospace typography. Fighting a builder to embed a GitHub link is slower than writing `<a href="...">`.

**Why not C (Next.js):** A 4-page static site with no dynamic content does not need a framework, a router, or React. The build week is two weeks. I should spend them on content and clarity, not on `npm install` and hydration errors. If I need interactivity later (a demo embed), I can add a single `<script>` tag or port to Next.js — the content moves, the HTML doesn't lock me in.

**Can I maintain this?** Yes. The site is text files. No dependencies, no build step, no version conflicts. Edits are typing. Deploys are dragging a folder onto Netlify.

---

## 4. Empty but live

**Live URL:** https://keremozcn.github.io/flyrank-ml-internship-submission/

The page is a near-blank HTML file with:
- My name in IBM Plex Sans 600, ink on paper
- The one-line claim below it
- The favicon SVG linked
- The palette applied (ink `#16191C`, paper `#F6F7F5`, slate teal `#2A5D63`)

Confirmed reachable on a second device (phone).

---

## 5. AI workspace loaded

The following are in the repo for the build week:

| Artifact | File |
|---|---|
| Identity kit | `work/fl05_identity_kit.md` |
| Image set & rejection note | `work/fl06_image_set.md` |
| Content map & CTAs | `work/fl07_content_map.md` |
| Framed cases (copy) | `work/fl04_framed_cases.md` |
| Favicon SVG | `work/favicon.svg` |
| Style note | `work/fl05_identity_kit.md` §4 |

---

## 6. Pass / Revise Checklist

- [x] Three genuine options with trade-offs considered — A, B, C each with build/host/backend/shows-work/trade-off
- [x] Chosen stack is free, matched to real needs, displays work properly — plain HTML + CSS on Netlify
- [x] Rationale in own words, includes "can I maintain this" — yes, text files, no dependencies
- [x] Backend question answered honestly — no, not yet
- [x] Real reachable URL exists — see deliverable links
- [x] AI workspace has identity kit, case studies, and content map loaded
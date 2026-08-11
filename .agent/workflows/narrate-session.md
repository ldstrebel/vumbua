---
description: Generate a multi-voice ElevenLabs audiobook for a Vumbua campaign session
---

# Narrate Session — Multi-Voice Audiobook Generation

Use this workflow to generate (or regenerate) the ElevenLabs multi-voice audiobook for a session. This assumes `sN-clean-story.md` already exists and is in good shape. If it doesn't yet exist, complete **Steps 4a–4b** of `/add-session` first.

---

## Overview

Every Vumbua session produces:
- A **multi-voice MP3 audiobook** with distinct voice actors per character
- **Per-chapter MP3 tracks** for flexible playback
- A **Blinkist-style sync JSON** (`sN_sync_timestamps.json`) for real-time text highlighting
- A **WebVTT subtitle track** (`sN_subtitles.vtt`) for web/mobile players

**Single source of truth:** `sessions/transcripts/clean/sN-clean-story.md`  
**Script:** `sessions/scripts/generate_audiobook.py`  
**Audit tool:** `sessions/scripts/parse_audit.py`

---

## Voice Cast

| Character | Voice ID | ElevenLabs Type | Notes |
|-----------|----------|-----------------|-------|
| Narrator  | `pNInz6obpgDQGcFmaJgB` | Premade (Adam) | Deep cinematic fantasy narrator |
| Loami     | `IM5qdLwbG2AX3RiVX0Of` | Custom | Italian-American Boston mechanic |
| Pip       | `386eQBpmCgw3emfoqL5n` | Custom | Hyperactive pixie gnome |
| Iggy      | `hxEheaxKsMWuFhE8lXGW` | Custom | Timid deadpan clay-kin with lisp |
| Ignatious | `iP95p4xoKVk53GoZ742B` | Premade (Chris) | Youthful passionate 17yo male |
| Britt     | `21m00Tcm4TlvDq8ikWAM` | Premade (Rachel) | Determined athletic female |
| Aggie     | `AZnzlk1XvdvUeBnXmlld` | Premade (Domi) | Gentle thoughtful female |

---

## Step 1 — Read the source file

```powershell
# Verify the story file exists and review its structure
Get-Item sessions/transcripts/clean/sN-clean-story.md
```

Check that it has:
- ✅ YAML front matter (`title`, `author`, `campaign`, `genre`)
- ✅ H1 title (`# TITLE HERE`) — this becomes the Narrator's opening title card
- ✅ `## CHAPTER N: NAME` headers (these split into separate MP3 tracks)
- ✅ No bracketed TTS tags (`[screaming]`, `[panicked]`) — ElevenLabs reads them aloud

---

## Step 2 — Generate Audio Manifest JSON (MANDATORY — Zero Credits)

```powershell
python sessions/scripts/generate_audio_manifest.py `
  --story sessions/transcripts/clean/sN-clean-story.md `
  --transcript sessions/transcripts/clean/sN-clean.md `
  --output sessions/audio/sN/sN_audio_manifest.json
```

Generates `sN_audio_manifest.json` by processing `sN-clean-story.md` and cross-referencing `sN-clean.md` transcript for 100% ground-truth context.

---

## Step 3 — Run 100% Parity & Speaker Audit (MANDATORY — Zero Credits)

```powershell
python sessions/scripts/audit_manifest.py `
  --manifest sessions/audio/sN/sN_audio_manifest.json `
  --story sessions/transcripts/clean/sN-clean-story.md `
  --report sessions/audio/sN/manifest_audit_report.md
```

Opens `sessions/audio/sN/manifest_audit_report.md`. You must see:

```
> ✅ PASSED 100% PARITY & INTEGRITY AUDIT!
> All story text reconstituted 100% verbatim. Zero dropped words, zero invalid speakers.
```

---

## Step 4 — Clean old output files (if regenerating)

```powershell
Remove-Item 'sessions/audio/sN/segment_*.mp3' -Recurse -Force
```

---

## Step 5 — Generate Audio via ElevenLabs

```powershell
python sessions/scripts/generate_audiobook.py `
  --manifest sessions/audio/sN/sN_audio_manifest.json `
  --output-dir sessions/audio/sN `
  --generate
```

The script reads the pre-audited manifest JSON directly, bypassing internal text parsing, and synthesizes each block sequentially via ElevenLabs API.

The script synthesizes each block sequentially, logs progress, then auto-merges all segments.

**Expected generation time:** ~8–12 minutes for a full session (149 blocks).

---

## Step 5 — Verify output

```powershell
Get-ChildItem sessions/audio/sN/ | Select-Object Name, Length
```

Expected files:

```
sN_audiobook_full.mp3         ~20 MB
Prologue.mp3
CHAPTER_1__*.mp3
CHAPTER_2__*.mp3
...
sN_sync_timestamps.json       (N entries, one per spoken line)
sN_subtitles.vtt
segment_001_Narrator.mp3
segment_002_Narrator.mp3
...
segment_NNN_Speaker.mp3
```

Check credit usage in the console output:
```
💳 ELEVENLABS CREDIT USAGE SUMMARY
  • Characters Used in This Run :  ~19,675 credits
  • Remaining Credit Budget    : XXXXXX credits (XX.X%)
```

---

## Credit Budget

| Session | Approx. Credits | Budget Remaining |
|---------|----------------|-----------------|
| Per session | ~19,000–20,000 | ~9–10% of 200,000 |
| Session 11 (done) | 19,675 | 180,325 (90.2%) |

---

## YAML Front Matter Reference

Every `sN-clean-story.md` must open with exactly this structure:

```yaml
---
title: "Session N: Title Here"
author: "Novel Adaptation in the Style of Brandon Sanderson"
campaign: Vumbua
genre: Epic Fantasy / Sci-Fantasy
---

# TITLE IN ALL CAPS (H1 — becomes Narrator title card)

---

## CHAPTER 1: CHAPTER NAME
```

**Parser behaviour by line type:**

| Line type | Parser action |
|-----------|---------------|
| `---` (YAML fence) | Skipped |
| `title:` / `author:` / `campaign:` / `genre:` | Skipped |
| `# Title` (H1 only) | → Narrator block (opening title card) |
| `## CHAPTER N: NAME` | → Chapter marker (splits MP3 track) |
| `### ` or deeper headers | Skipped |
| Plain prose (no quotes) | → Narrator block |
| `"Dialogue," Name verb.` | → Character block (NAME + verb detection) |

---

## Prose Grammar Rules for TTS Accuracy

These rules must be followed when writing `sN-clean-story.md` to ensure the parser assigns every line correctly:

1. **Every dialogue line must have a speaking character's name** in the narration text outside the quotes, immediately adjacent to a speech verb.
   - ✅ `"You saw that?!" Aggie gasped, staring at Britt.`
   - ❌ `"You saw that?!"` (bare — no attribution, triggers fallback warning)

2. **No bracketed TTS tags** — they are read aloud by ElevenLabs v2.
   - ✅ `"I DON'T BELIEVE YOU!" Pip screamed.`
   - ❌ `"[screaming] I don't believe you!" Pip said.`

3. **Ambient quotes (signs, speakers, echoes) use italics without inner quotes.**
   - ✅ `The stadium speakers crackled: *Just hold on!*`
   - ❌ `The stadium speakers crackled: *"Just hold on!"*`

4. **Dialect is baked into the prose**, not added as tags.
   - ✅ `"We nevah should've come up here," Loami muttered.`
   - ❌ `"We never should've come up here," Loami muttered. [Boston accent]`

---

## Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| YAML fields being narrated (`"campaign Vumbua"`) | Old parser missing `campaign:` / `genre:` skip | Update `generate_audiobook.py` — both are in skip list |
| Wrong voice on a line | Multiple character names in narration tag | Ensure the actual speaker's name is within 5 chars of the speech verb |
| Title card missing | H1 was skipped | Confirm title uses `# ` (H1), not `## ` (H2) |
| Repeated lines at start | Segments from old run still in output dir | Clean `sessions/audio/sN/` before regenerating |
| Tags read aloud | `[panicked]` in story file | Search for `\[` in the file; remove all bracketed tags |

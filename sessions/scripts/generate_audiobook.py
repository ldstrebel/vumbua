#!/usr/bin/env python3
"""
Vumbua ElevenLabs Audiobook Generator
-------------------------------------
Parses novelized session story files (e.g. s11-clean-story.md) into structured speaker blocks
and synthesizes multi-voice audiobooks using the ElevenLabs Text-to-Speech API.

Usage:
  1. Add your ElevenLabs API key to .env:
     ELEVENLABS_API_KEY=your_key_here

  2. List available ElevenLabs voices on your account:
     python sessions/scripts/generate_audiobook.py --check-voices

  3. Dry-run parse s11-clean-story.md (no API quota used):
     python sessions/scripts/generate_audiobook.py --input sessions/transcripts/clean/s11-clean-story.md --parse-only

  4. Generate audiobook MP3s:
     python sessions/scripts/generate_audiobook.py --input sessions/transcripts/clean/s11-clean-story.md --output-dir sessions/audio/s11
"""

import os
import re
import sys
import json
import argparse
import requests
import base64
from pathlib import Path

# Ensure UTF-8 output formatting for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load .env file manually if python-dotenv is not installed
def load_env_file():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

load_env_file()
API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")

# Default Voice Mappings (Can be overridden via voice_map.json or CLI flags)
# Voice names correspond to default ElevenLabs public library voices or custom clones
DEFAULT_VOICE_MAP = {
    "Narrator": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam (Deep, engaging fantasy narrator)
        "description": "Rich, deep, cinematic narrator voice",
        "stability": 0.65,
        "similarity_boost": 0.80,
        "style": 0.15
    },
    "Loami": {
        "voice_id": "IM5qdLwbG2AX3RiVX0Of",  # Custom Loami (NJ Mechanic)
        "description": "Custom created New Jersey working-class mechanic voice",
        "stability": 0.50,                  
        "similarity_boost": 0.85,
        "style": 0.0                        # 0.0 style preserves pure custom voice model without distortion
    },
    "Pip": {
        "voice_id": "386eQBpmCgw3emfoqL5n",  # Custom Pip (Vibrant Halfling/Pixie)
        "description": "Custom created vibrant, hyperactive pixie/halfling gnome female",
        "stability": 0.45,                  
        "similarity_boost": 0.85,
        "style": 0.0                        # 0.0 style preserves pure custom voice model
    },
    "Ignatious": {
        "voice_id": "iP95p4xoKVk53GoZ742B",  # Chris (Youthful, energetic 17yo male - distinct from Narrator)
        "description": "Youthful 17yo Ember Islander male, passionate and fiery",
        "stability": 0.40,
        "similarity_boost": 0.75,
        "style": 0.35
    },
    "Britt": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (Determined, cool female)
        "description": "Determined, athletic turtle-kin female with root dreadlocks",
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.30
    },
    "Aggie": {
        "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi (Gentle, calm female)
        "description": "Gentle, thoughtful turtle-mushroom hybrid female",
        "stability": 0.60,
        "similarity_boost": 0.75,
        "style": 0.20
    },
    "Iggy": {
        "voice_id": "hxEheaxKsMWuFhE8lXGG",  # Custom Iggy (Young Timid Deadpan Lisp Clay-Kin)
        "description": "Custom created timid, deadpan young clay-and-soil-kin male with a lisp",
        "stability": 0.50,
        "similarity_boost": 0.85,
        "style": 0.0                        # 0.0 style preserves pure custom voice model
    }
}

def create_custom_voice(character, description):
    """Creates a custom synthetic voice via ElevenLabs Text-to-Voice Design API from a text prompt."""
    if not API_KEY:
        print("❌ Error: ELEVENLABS_API_KEY is missing!")
        return

    sample_texts = {
        "Loami": "Gotta say I am shocked we were able to get our way here at all... but here we are! I am Loami and I fix engines in the Mizizi forest.",
        "Pip": "NO! MY BISCUITS! THESE ARE MINE, STUPID BIRD! WHAT THE SHIT WAS THAT, MR TURTLE!?",
        "Iggy": "The trees... they have eyes! Ethereal Wall! Please don't let the big branches touch me!",
        "Ignatious": "So I might have forgotten that I can fly this entire time! I literally was like, Oh wait, I can fly now!"
    }
    sample_text = sample_texts.get(character, f"Hello, I am {character} and this is a custom voice sample generated for the Vumbua audiobook project.")
    if len(sample_text) < 100:
        sample_text += " This sample sentence is extended so that ElevenLabs has sufficient characters to synthesize the preview audio cleanly."

    url = "https://api.elevenlabs.io/v1/text-to-voice/create-previews"
    payload = {
        "voice_description": description,
        "text": sample_text
    }
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

    print(f"\n🎨 Designing Custom Voice for [{character}] via API...")
    print(f"📝 Prompt: \"{description}\"\n")

    try:
        res = requests.post(url, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        previews = data.get("previews", [])

        out_path = Path("sessions/audio/samples")
        out_path.mkdir(parents=True, exist_ok=True)

        print(f"✅ Generated {len(previews)} custom voice previews:")
        for idx, prev in enumerate(previews):
            vid = prev.get("generated_voice_id")
            audio_b64 = prev.get("audio_base_64") or prev.get("audio_base64")
            if audio_b64:
                audio_bytes = base64.b64decode(audio_b64)
                filename = out_path / f"custom_{character}_preview_{idx+1}.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"  • Preview {idx+1}: {filename.name} (Size: {len(audio_bytes):,} bytes)")
                print(f"    └─ Generated Voice ID: {vid}")

        print(f"\n💡 Listen to the MP3 previews in sessions/audio/samples/!")
        print(f"To use a preview Voice ID for {character}, pass: python generate_audiobook.py --cast-sample --set-voice {character} <VOICE_ID>\n")

    except Exception as e:
        print(f"❌ Failed to create custom voice: {e}")

def search_shared_voices(query):
    """Searches ElevenLabs shared voice library for specific accents/archetypes."""
    url = f"https://api.elevenlabs.io/v1/shared-voices?search={query}"
    headers = {"xi-api-key": API_KEY} if API_KEY else {}
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        voices = data.get("voices", [])
        
        print(f"\n🔍 Found {len(voices)} voices matching '{query}' in ElevenLabs Shared Library:\n")
        print(f"{'Name':<25} {'Voice ID':<35} {'Accent/Descr':<30}")
        print("-" * 90)
        for v in voices[:15]:  # Top 15 results
            name = v.get("name", "Unknown")
            vid = v.get("voice_id", "")
            accent = v.get("accent", v.get("description", "N/A"))[:30]
            print(f"{name:<25} {vid:<35} {accent:<30}")
        print("\n💡 To use any Voice ID, pass: python generate_audiobook.py --cast-sample --set-voice Loami VOICE_ID\n")
    except Exception as e:
        print(f"❌ Failed to search shared voices: {e}")

def check_elevenlabs_voices():
    """Queries ElevenLabs API to list available voices for user selection."""
    if not API_KEY or API_KEY == "your_elevenlabs_api_key_here":
        print("❌ Error: ELEVENLABS_API_KEY is missing or invalid in your .env file!")
        print("Please add your key to d:\\Code\\vumbua\\.env:\n  ELEVENLABS_API_KEY=your_actual_key_here\n")
        return

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        voices = data.get("voices", [])
        
        print(f"\n✅ Connected to ElevenLabs API! Found {len(voices)} voices on your account:\n")
        print(f"{'Voice Name':<25} {'Voice ID':<35} {'Category':<15}")
        print("-" * 75)
        for v in voices:
            name = v.get("name", "Unknown")
            vid = v.get("voice_id", "")
            cat = v.get("category", "premade")
            print(f"{name:<25} {vid:<35} {cat:<15}")
            
        print("\n💡 You can assign any Voice ID above to Loami, Pip, Narrator, etc. in voice_map.json!\n")
    except Exception as e:
        print(f"❌ Failed to fetch voices from ElevenLabs: {e}")

def parse_story_into_blocks(story_path):
    """Parses markdown story file into structured audio blocks with exact sequential speaker attribution."""
    with open(story_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip YAML frontmatter entirely if present
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]

    lines = text.splitlines()
    current_chapter = "CHAPTER 1: THE NIGHT OF EMBERS"
    blocks = []
    
    speakers = ["Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"]
    last_speaking_character = None

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue

        # Skip main title lines entirely (do NOT emit title cards to ElevenLabs)
        if line.startswith("# ") and not line.startswith("## "):
            continue

        if line.startswith("## CHAPTER"):
            current_chapter = line.replace("##", "").strip()
            continue

        # Skip any other markdown headers (###, ####, etc.)
        if line.startswith("#"):
            continue

def detect_quote_speaker(pre_tag, post_tag, speakers, last_speaking_character):
    dialogue_verbs = r'(?:said|asked|screamed|replied|gasped|yelled|announced|noted|shouted|exclaimed|muttered|offered|shrugged|grunted|grinned|whispered|recalled|snarled|hissed|roared|cried|spat|mused|complained|corrected|warned|countered|admitted|laughed|groaned|sighed|breathed|confirmed|interrupted|finished|added|continued|insisted|pleaded|stated|declared|demanded|urged|agreed|protested|objected|called|bellowed|chortled|chimed|snickered|exulted|whimpered|scolded|grumbled|mumbled|rasped|quipped|sputtered|retorted|gushed|beamed|barked|snapped|howled|chirped)'

    # 1a. Check pre_tag for immediate speech verb (e.g. "...carry Pip down, who grumbled, "Quote" / Ignatious roared, "Quote")
    pre_verbs = list(re.finditer(dialogue_verbs, pre_tag, re.IGNORECASE))
    if pre_verbs:
        last_verb = pre_verbs[-1]
        dist_to_quote = len(pre_tag) - last_verb.end()
        if dist_to_quote <= 35:
            closest_spk = None
            min_dist = float('inf')
            for spk in speakers:
                for m in re.finditer(r'\b' + spk + r'\b', pre_tag, re.IGNORECASE):
                    dist = abs(last_verb.start() - m.start())
                    if dist < min_dist:
                        min_dist = dist
                        closest_spk = spk
            m_natty = list(re.finditer(r'\bNatty\b', pre_tag, re.IGNORECASE))
            for m in m_natty:
                dist = abs(last_verb.start() - m.start())
                if dist < min_dist:
                    min_dist = dist
                    closest_spk = "Ignatious"
            if closest_spk and min_dist <= 45:
                return closest_spk

    # 1b. Check post_tag for immediate speech verb (e.g. "Quote," Pip announced / "Quote," gasped Britt)
    post_verbs = list(re.finditer(dialogue_verbs, post_tag, re.IGNORECASE))
    if post_verbs:
        first_verb = post_verbs[0]
        if first_verb.start() <= 35:
            closest_spk = None
            min_dist = float('inf')
            for spk in speakers:
                for m in re.finditer(r'\b' + spk + r'\b', post_tag[:first_verb.end() + 25], re.IGNORECASE):
                    dist = abs(first_verb.start() - m.start())
                    if dist < min_dist:
                        min_dist = dist
                        closest_spk = spk
            m_natty = list(re.finditer(r'\bNatty\b', post_tag[:first_verb.end() + 25], re.IGNORECASE))
            for m in m_natty:
                dist = abs(first_verb.start() - m.start())
                if dist < min_dist:
                    min_dist = dist
                    closest_spk = "Ignatious"
            if closest_spk and min_dist <= 30:
                return closest_spk

    # 2. PROXIMITY MATCHING
    candidates = []
    pre_len = len(pre_tag)
    for spk in speakers:
        for m in re.finditer(r'\b' + spk + r'\b', pre_tag, re.IGNORECASE):
            dist = pre_len - m.end()
            candidates.append((dist, spk))
        for m in re.finditer(r'\b' + spk + r'\b', post_tag, re.IGNORECASE):
            dist = m.start()
            candidates.append((dist, spk))

    m_natty_pre = list(re.finditer(r'\bNatty\b', pre_tag, re.IGNORECASE))
    for m in m_natty_pre:
        candidates.append((pre_len - m.end(), "Ignatious"))
    m_natty_post = list(re.finditer(r'\bNatty\b', post_tag, re.IGNORECASE))
    for m in m_natty_post:
        candidates.append((m.start(), "Ignatious"))

    if candidates:
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]

    # 3. PRONOUN TRACKING
    combined_tag = pre_tag + " " + post_tag
    if re.search(r'\b(he|his|him)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Loami", "Ignatious", "Iggy"]:
        return last_speaking_character
    elif re.search(r'\b(she|her)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Britt", "Aggie", "Pip"]:
        return last_speaking_character

    # 4. FALLBACK
    return last_speaking_character if last_speaking_character else "Loami"


def parse_story_into_blocks(story_path):
    """Parses markdown story file into structured audio blocks with per-quote local speaker attribution."""
    with open(story_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip YAML frontmatter entirely if present
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]

    lines = text.splitlines()
    current_chapter = "CHAPTER 1: THE NIGHT OF EMBERS"
    blocks = []
    
    speakers = ["Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"]
    last_speaking_character = None

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue

        if line.startswith("# ") and not line.startswith("## "):
            continue

        if line.startswith("## CHAPTER"):
            current_chapter = line.replace("##", "").strip()
            continue

        if line.startswith("#"):
            continue

        match_quotes = list(re.finditer(r'"([^"]+)"', line))
        if not match_quotes:
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": "Narrator",
                "text": line
            })
            continue

        curr_idx = 0
        for idx, match in enumerate(match_quotes):
            start, end = match.span()
            pre_tag = line[curr_idx:start]
            post_tag = line[end:match_quotes[idx+1].start()] if idx + 1 < len(match_quotes) else line[end:]

            detected_speaker = detect_quote_speaker(pre_tag, post_tag, speakers, last_speaking_character)
            last_speaking_character = detected_speaker

            # Narration before quote
            if start > curr_idx:
                narr_text = line[curr_idx:start].strip()
                if narr_text.strip(" *_\t\n"):
                    blocks.append({
                        "line_num": line_num,
                        "chapter": current_chapter,
                        "speaker": "Narrator",
                        "text": narr_text
                    })

            # Quote segment
            quote_text = f'"{match.group(1).strip()}"'
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": detected_speaker,
                "text": quote_text
            })
            curr_idx = end

        # Trailing narration
        if curr_idx < len(line):
            narr_text = line[curr_idx:].strip()
            if narr_text.strip(" *_\t\n"):
                blocks.append({
                    "line_num": line_num,
                    "chapter": current_chapter,
                    "speaker": "Narrator",
                    "text": narr_text
                })

    return blocks

import struct

def get_exact_mp3_duration(filepath):
    """Calculates exact MP3 duration in seconds from MPEG frame headers."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        i = 0
        duration = 0.0
        while i < len(data) - 4:
            if data[i] == 0xFF and (data[i+1] & 0xE0) == 0xE0:
                header = struct.unpack('>I', data[i:i+4])[0]
                bitrate_index = (header >> 12) & 0xF
                samplerate_index = (header >> 10) & 0x3
                padding = (header >> 9) & 0x1
                
                bitrates = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
                samplerates = [44100, 48000, 32000, 0]
                
                br = bitrates[bitrate_index] * 1000
                sr = samplerates[samplerate_index]
                
                if br > 0 and sr > 0:
                    frame_len = int(144 * br / sr) + padding
                    duration += 1152.0 / sr
                    i += max(frame_len, 1)
                    continue
            i += 1
        return duration if duration > 0 else os.path.getsize(filepath) / 16000.0
    except Exception:
        return os.path.getsize(filepath) / 16000.0

def export_sync_timestamps(blocks, segment_files, out_path):
    """Generates Blinkist-style JSON and WebVTT subtitle sync files for real-time text highlighting."""
    print("\n⏱️  Calculating millisecond-accurate line-by-line sync timestamps...")
    
    sync_data = []
    current_time_sec = 0.0
    
    vtt_lines = ["WEBVTT\n"]
    
    def fmt_vtt_time(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

    for idx, (block, seg_file) in enumerate(zip(blocks, segment_files)):
        dur_sec = get_exact_mp3_duration(seg_file)
        start_sec = current_time_sec
        end_sec = start_sec + dur_sec
        current_time_sec = end_sec

        entry = {
            "id": idx + 1,
            "chapter": block["chapter"],
            "speaker": block["speaker"],
            "text": block["text"],
            "file": seg_file.name,
            "start_time_sec": round(start_sec, 3),
            "end_time_sec": round(end_sec, 3),
            "duration_sec": round(dur_sec, 3),
            "start_time_ms": int(start_sec * 1000),
            "end_time_ms": int(end_sec * 1000)
        }
        sync_data.append(entry)

        # WebVTT formatting
        vtt_lines.append(f"{idx + 1}")
        vtt_lines.append(f"{fmt_vtt_time(start_sec)} --> {fmt_vtt_time(end_sec)}")
        vtt_lines.append(f"<v {block['speaker']}>{block['text']}\n")

    # Save JSON Sync File
    prefix = out_path.name if out_path.name.startswith("s") else "audiobook"
    json_path = out_path / f"{prefix}_sync_timestamps.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=2, ensure_ascii=False)
    print(f"  └─ 📊 Blinkist Sync JSON created: {json_path.name} ({len(sync_data)} lines tracked)")

    # Save WebVTT Subtitle File
    vtt_path = out_path / f"{prefix}_subtitles.vtt"
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_lines))
    print(f"  └─ 📜 WebVTT Subtitle Track created: {vtt_path.name}")

def print_credit_summary(chars_used, total_budget=200000):
    """Prints a clear summary of ElevenLabs credits used in this run and remaining budget."""
    remaining = total_budget - chars_used
    percent_remaining = (remaining / total_budget) * 100 if total_budget > 0 else 0
    print("\n" + "=" * 65)
    print("💳 ELEVENLABS CREDIT USAGE SUMMARY")
    print("-" * 65)
    print(f"  • Characters Used in This Run : {chars_used:>7,} credits")
    print(f"  • Total Credit Budget        : {total_budget:>7,} credits")
    print(f"  • Remaining Credit Budget    : {remaining:>7,} credits ({percent_remaining:.1f}%)")
    print("=" * 65 + "\n")

def write_clean_mp3_concat(target_file, segment_files):
    """Concatenates MP3 segment files into a single master MP3, stripping mid-stream ID3 headers so HTTP Range seeking works seamlessly."""
    clean_bytes = bytearray()
    for seg_file in segment_files:
        with open(seg_file, "rb") as f:
            data = f.read()

        start_offset = 0
        if data.startswith(b"ID3"):
            header = data[:10]
            size = ((header[6] & 0x7F) << 21) | ((header[7] & 0x7F) << 14) | ((header[8] & 0x7F) << 7) | (header[9] & 0x7F)
            start_offset = 10 + size
            if header[5] & 0x10:
                start_offset += 10

        end_offset = len(data)
        if data.endswith(b"TAG") or (len(data) >= 128 and data[-128:-125] == b"TAG"):
            end_offset -= 128

        raw_audio = data[start_offset:end_offset]
        sync_idx = 0
        while sync_idx < len(raw_audio) - 1:
            if raw_audio[sync_idx] == 0xFF and (raw_audio[sync_idx+1] & 0xE0) == 0xE0:
                break
            sync_idx += 1

        clean_bytes.extend(raw_audio[sync_idx:])

    with open(target_file, "wb") as f:
        f.write(clean_bytes)

def generate_audiobook(blocks, output_dir, voice_map, clean_existing=False):
    """Calls ElevenLabs API to generate MP3 files per chapter."""
    if not API_KEY or API_KEY == "your_elevenlabs_api_key_here":
        print("❌ Error: ELEVENLABS_API_KEY is not set in .env! Cannot generate audio.")
        return

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    if clean_existing:
        print("🧹 Cleaning old segment MP3 files before fresh generation...")
        for old_seg in out_path.glob("segment_*.mp3"):
            try:
                old_seg.unlink()
            except Exception:
                pass

    print(f"\n🎧 Starting ElevenLabs Audiobook Generation...")
    print(f"📁 Output Directory: {out_path.resolve()}\n")

    total_chars_generated = 0

    for i, block in enumerate(blocks):
        chapter = block["chapter"]
        speaker = block["speaker"]
        display_text = block["text"]
        tts_text = block.get("tts_text", display_text)
        # Strip any bracketed tags (e.g. [panicked], [screaming]) so ElevenLabs never reads them out loud
        text = re.sub(r'\[.*?\]', '', tts_text).strip()
        if not text:
            continue
        total_chars_generated += len(text)

        # Voice config lookup
        voice_info = voice_map.get(speaker, voice_map["Narrator"])
        voice_id = voice_info["voice_id"]
        
        print(f"[{i+1}/{len(blocks)}] Generating [{speaker}] in {chapter}: \"{text[:40]}...\"")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": voice_info.get("stability", 0.5),
                "similarity_boost": voice_info.get("similarity_boost", 0.75),
                "style": voice_info.get("style", 0.0),
                "use_speaker_boost": True
            }
        }

        seg_filename = f"segment_{i+1:03d}_{speaker}.mp3"
        seg_path = out_path / seg_filename

        if seg_path.exists() and seg_path.stat().st_size > 0:
            print(f"  └─ ⏩ Using existing segment file: {seg_filename}")
        else:
            try:
                res = requests.post(url, json=payload, headers=headers)
                res.raise_for_status()
                with open(seg_path, "wb") as f:
                    f.write(res.content)
                print(f"  └─ ✅ Synthesized: {seg_filename} ({len(res.content):,} bytes)")
            except Exception as e:
                print(f"  └─ ❌ Failed to generate audio segment: {e}")

    # Merge individual segments into master & per-chapter tracks cleanly
    segment_files = sorted(
        [out_path / f for f in os.listdir(out_path) if f.startswith("segment_") and f.endswith(".mp3")],
        key=lambda x: int(re.search(r'segment_(\d+)', x.name).group(1))
    )
    
    if segment_files:
        print("\n🎛️  Assembling master and per-chapter audio tracks with clean MPEG frame merging...")
        prefix = out_path.name if out_path.name.startswith("s") else "audiobook"
        
        # 1. Master Audiobook File (Full Session)
        master_file = out_path / f"{prefix}_audiobook_full.mp3"
        write_clean_mp3_concat(master_file, segment_files)
        print(f"  └─ 🏆 Master Audiobook created: {master_file.name}")

        # 2. Per-Chapter Audiobook Files
        chapters = {}
        for block, seg_file in zip(blocks, segment_files):
            ch_name = block["chapter"].replace("##", "").replace(":", "_").replace(" ", "_")
            ch_clean = re.sub(r'[^\w_]', '', ch_name)
            if ch_clean not in chapters:
                chapters[ch_clean] = []
            chapters[ch_clean].append(seg_file)

        for ch_clean, segs in chapters.items():
            ch_file = out_path / f"{ch_clean}.mp3"
            write_clean_mp3_concat(ch_file, segs)
            print(f"  └─ 📖 Chapter Track created: {ch_file.name}")

        # 3. Blinkist-style Line-by-Line Interactive Audio Sync Timestamps (JSON & WebVTT)
        export_sync_timestamps(blocks, segment_files, out_path)

    print("\n✨ All audiobook tracks successfully generated and merged!")
    print_credit_summary(total_chars_generated)

def main():
    parser = argparse.ArgumentParser(description="Vumbua ElevenLabs Audiobook Generator")
    parser.add_argument("--check-voices", action="store_true", help="List available ElevenLabs voices on your account")
    parser.add_argument("--manifest", help="Path to pre-audited Audio Manifest JSON (e.g. sessions/audio/s11/s11_audio_manifest.json)")
    parser.add_argument("--input", default="sessions/transcripts/clean/s11-clean-story.md", help="Path to story markdown file")
    parser.add_argument("--output-dir", default="sessions/audio/s11", help="Output directory for MP3 files")
    parser.add_argument("--parse-only", action="store_true", help="Parse script and print speaker breakdown without calling API")
    parser.add_argument("--generate", action="store_true", help="Generate full audio files via ElevenLabs API")
    parser.add_argument("--clean", action="store_true", help="Delete existing segment MP3 files in output directory before generation to prevent stale file reuse")

    parser.add_argument("--hello-world", action="store_true", help="Generate a quick 3-line voice sample (Narrator, Loami, Pip) using under 150 credits")
    parser.add_argument("--create-voice", nargs=2, metavar=("CHARACTER", "DESCRIPTION_PROMPT"), help="Generate new custom synthetic voices via API from a text description (e.g. --create-voice Loami 'Deep rugged male mechanic from New Jersey with thick Brooklyn accent')")
    parser.add_argument("--cast-sample", action="store_true", help="Generate 1 iconic sample line for EVERY character in the cast to test voices")
    parser.add_argument("--search-voice", type=str, help="Search ElevenLabs shared voice library for specific accents/archetypes (e.g. 'new jersey', 'older male', 'pixie')")
    parser.add_argument("--set-voice", nargs=2, metavar=("CHARACTER", "VOICE_ID"), help="Override a character's Voice ID (e.g. --set-voice Loami VOICE_ID_HERE)")

    args = parser.parse_args()

    if args.check_voices:
        check_elevenlabs_voices()
        return

    if args.create_voice:
        char_name, prompt_desc = args.create_voice
        create_custom_voice(char_name, prompt_desc)
        return

    if args.hello_world:
        sample_blocks = [
            {"chapter": "Hello World", "speaker": "Narrator", "text": "Welcome to Vumbua Session Eleven: Don't Touch My Biscuits."},
            {"chapter": "Hello World", "speaker": "Loami", "text": "Gotta say, I'm shocked we were able to get our way here at all... but here we are!"},
            {"chapter": "Hello World", "speaker": "Pip", "text": "NO! MY BISCUITS! THESE ARE MINE, STUPID BIRD!"}
        ]
        print("\n🧪 Running Hello World Voice Test (3 sample lines)...")
        generate_audiobook(sample_blocks, "sessions/audio/test", DEFAULT_VOICE_MAP)
        print("\n🎉 Hello World test complete! Audio saved to: sessions/audio/test/\n")
        return

    if args.search_voice:
        search_shared_voices(args.search_voice)
        return

    if args.cast_sample:
        sample_blocks = [
            {"chapter": "Cast Sample", "speaker": "Narrator", "text": "8:00 AM. The air in the Mizizi basin changed without warning as an unnatural tempest rolled over the giant petrified canopy."},
            {"chapter": "Cast Sample", "speaker": "Loami", "text": "Well... I'm definitely not staying up here alone! Gotta say I've fallen from further!"},
            {"chapter": "Cast Sample", "speaker": "Pip", "text": "WHAT THE SHIT WAS THAT, MR TURTLE!? DON'T TOUCH MY BISCUITS!"},
            {"chapter": "Cast Sample", "speaker": "Ignatious", "text": "So I might have forgotten that I can fly this entire time! I literally was like, Oh wait, I can fly now!"},
            {"chapter": "Cast Sample", "speaker": "Britt", "text": "DOES ANYBODY HAVE A LAZIZI?! What a Kazy boy!"},
            {"chapter": "Cast Sample", "speaker": "Aggie", "text": "Touching Mwaza-Kasa is taboo, but in absence of the trees, it acts as a physical anchor! Three, two, one!"},
            {"chapter": "Cast Sample", "speaker": "Iggy", "text": "The trees have eyes! The trees have eyes! Ethereal Wall!"}
        ]
        
        # Apply voice override if specified
        if args.set_voice:
            char_name, new_vid = args.set_voice
            if char_name in DEFAULT_VOICE_MAP:
                DEFAULT_VOICE_MAP[char_name]["voice_id"] = new_vid
                print(f"🔄 Overriding [{char_name}] Voice ID to: {new_vid}")

        print("\n🎭 Generating 7-Character Cast Audio Samples...")
        generate_audiobook(sample_blocks, "sessions/audio/samples", DEFAULT_VOICE_MAP)
        print("\n🎉 Cast samples complete! Listen to files in: sessions/audio/samples/\n")
        return

    if args.manifest:
        with open(args.manifest, "r", encoding="utf-8") as f:
            blocks = json.load(f)
        print(f"\n📖 Loaded {len(blocks)} blocks directly from Audio Manifest JSON: {args.manifest}")
        print("⚡ Zero regex parsing performed!")
    else:
        blocks = parse_story_into_blocks(args.input)

    if not blocks:
        return

    # Speaker breakdown
    speakers = set(b["speaker"] for b in blocks)
    print(f"\n📖 Audio blocks ready: {len(blocks)} blocks across {len(set(b['chapter'] for b in blocks))} chapters.")
    print(f"🗣️  Detected Speakers: {', '.join(sorted(speakers))}\n")

    print("🎙️  Voice Cast Configuration:")
    for spk in sorted(speakers):
        vinfo = DEFAULT_VOICE_MAP.get(spk, DEFAULT_VOICE_MAP["Narrator"])
        print(f"  - {spk:<12}: {vinfo['description']} (Voice ID: {vinfo['voice_id']})")

    if args.parse_only:
        print("\n✅ Parse-only run complete. No ElevenLabs API credits were used!")
        return

    if args.generate:
        generate_audiobook(blocks, args.output_dir, DEFAULT_VOICE_MAP, clean_existing=args.clean)

if __name__ == "__main__":
    main()

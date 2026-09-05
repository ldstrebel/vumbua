import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    manifest_path = "campaign/audio/s11/s11_audio_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        blocks = json.load(f)

    total_chars = 0
    speaker_chars = {}
    speaker_blocks = {}

    for b in blocks:
        txt = b["text"].strip()
        spk = b["speaker"]
        chars = len(txt)
        total_chars += chars
        speaker_chars[spk] = speaker_chars.get(spk, 0) + chars
        speaker_blocks[spk] = speaker_blocks.get(spk, 0) + 1

    print("=" * 80)
    print("ELEVENLABS CREDIT USAGE PROJECTION (Session 11 Regeneration)")
    print("=" * 80)
    print(f"Total Audio Blocks : {len(blocks)}")
    print(f"Total Text Length  : {total_chars:,} characters\n")

    print(f"{'Voice Actor':<15} {'Blocks':<10} {'Characters':<15} {'Percentage':<12}")
    print("-" * 55)
    for spk, count in sorted(speaker_chars.items(), key=lambda x: x[1], reverse=True):
        b_count = speaker_blocks[spk]
        pct = (count / total_chars) * 100
        print(f"{spk:<15} {b_count:<10} {count:<15,} {pct:.1f}%")
    
    print("=" * 80)
    print(f"💳 Total ElevenLabs Credits Required : {total_chars:,} credits")
    print(f"📊 % of Standard Monthly Quota (200,000 credits) : {(total_chars / 200000) * 100:.1f}%")
    print(f"⏱️ Estimated Synthesis Time (API speed ~300 char/sec) : ~{round(total_chars / 300 / 60, 1)} minutes")
    print("=" * 80)

if __name__ == "__main__":
    main()

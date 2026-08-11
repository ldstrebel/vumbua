import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    with open('sessions/audio/s11/s11_audio_manifest.json', 'r', encoding='utf-8') as f:
        blocks = json.load(f)

    iggy_blocks = [b for b in blocks if b['speaker'] == 'Iggy']
    print(f"Total Iggy Blocks Found: {len(iggy_blocks)}\n")
    for b in iggy_blocks:
        print(f"L{b['line_num']} Display Text : {b['text']}")
        print(f"L{b['line_num']} Current TTS   : {b['tts_text']}\n")

if __name__ == "__main__":
    main()

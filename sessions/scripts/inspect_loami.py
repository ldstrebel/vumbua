import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    with open('sessions/audio/s11/s11_audio_manifest.json', 'r', encoding='utf-8') as f:
        blocks = json.load(f)

    print('--- LOAMI SAMPLE BLOCKS (VERBATIM DISPLAY TEXT vs ELEVENLABS TTS TEXT) ---')
    loami_blocks = [b for b in blocks if b['speaker'] == 'Loami'][:8]
    for b in loami_blocks:
        print(f"L{b['line_num']} Display Text : {b['text']}")
        print(f"L{b['line_num']} ElevenLabs TTS: {b['tts_text']}\n")

if __name__ == "__main__":
    main()

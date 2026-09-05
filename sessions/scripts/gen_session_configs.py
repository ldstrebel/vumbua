"""Generate sN-session-config.json for s2+ from observed diarization labels,
then run prep_raw for each. Shared mics are declared only where the raw labels
show ambiguity ('GM or Aggie', 'Luke S or Kristina'). Solo 'Luke S' streams may
still silently carry Kristina (Failure Mode 5) — flagged in config notes.
"""
import json, re, glob, collections, subprocess, sys, os
from pathlib import Path

ROOT = Path('sessions')
PC = {'Sophie': 'Britt', 'Kristina': 'Aggie', 'John': 'Ignatius',
      'Luke F': 'Lomi', 'Holly': 'Iggy'}
LABELS = {
    'Sophie Foreman Noone': 'Sophie', 'John Hagey': 'John',
    'Luke Foreman': 'Luke F', 'Holly Strebel': 'Holly',
    'Kristina Raine': 'Kristina', "John Hagey's Presentation": 'John',
    'GM or Aggie': 'Luke S', 'GM or [[Aggie]]': 'Luke S',
    'Luke S or Kristina': 'Luke S',
    'Loami or Britt': 'Luke F', 'Loami or [[Britt]]': 'Luke F',
}
PRESENT = {  # observed people per session (from label scan)
    's2':   ['Luke S', 'Luke F', 'John', 'Sophie', 'Kristina'],
    's4':   ['Luke S', 'Holly', 'Luke F', 'John'],
    's4.5': ['Luke S', 'Sophie', 'Kristina'],
    's5':   ['John', 'Luke S', 'Luke F', 'Holly'],
    's6':   ['Luke S', 'Holly', 'Sophie', 'Luke F'],
    's7':   ['Luke S', 'Kristina', 'John', 'Luke F', 'Holly'],
    's8':   ['Luke S', 'Holly', 'Sophie', 'Luke F'],
    's9':   ['Luke S', 'Holly', 'Sophie', 'Luke F', 'John'],
    's10':  ['Luke S', 'Holly', 'Sophie', 'Luke F', 'John'],
    's11':  ['Luke S', 'Holly', 'Sophie', 'Luke F', 'John'],
}
SHARED = {  # mic label -> [people carried], only where raw labels show it
    's2':   [('Luke S', 'Luke S', 'GM', 'gm'), ('Luke S', 'Kristina', 'Aggie', 'player_character')],
    's4.5': [('Luke S', 'Luke S', 'GM', 'gm'), ('Luke S', 'Kristina', 'Aggie', 'player_character')],
}
fm5 = ("'Luke S' stream is solo-labeled here; s0 proved Kristina can hide on "
       "it. Review for silent-speaker absorption during attribution.")

for sid, people in PRESENT.items():
    players = {p: PC[p] for p in people if p != 'Luke S'}
    shared = []
    seen = set()
    for mic, person, ident, kind in SHARED.get(sid, []):
        if mic in seen: continue
        seen.add(mic)
        shared.append({
            'mic_label': mic,
            'note': 'Ambiguous diarization label observed in raw.' +
                    (' ' + fm5 if kind == 'gm' else ''),
            'carries': [
                {'person': person, 'identity': ident, 'kind': kind}
                for mic2, person, ident, kind in SHARED[sid] if mic2 == mic],
        })
    cfg = {
        'session_id': sid,
        'gm': 'Luke S',
        'players': players,
        'shared_mics': shared,
        'raw_speaker_labels': {k: v for k, v in LABELS.items() if v in people},
        '_note': ('Auto-generated from observed diarization labels. ' +
                  ('' if shared else fm5)),
    }
    out = ROOT / 'config' / f'{sid}-session-config.json'
    out.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
    print('wrote', out)

for sid in PRESENT:
    r = subprocess.run(
        [sys.executable, 'sessions/scripts/prep_raw.py', sid],
        capture_output=True, text=True, encoding='utf-8')
    print('=' * 20, sid, 'rc=%d' % r.returncode)
    tail = (r.stdout + r.stderr).strip().splitlines()
    print('\n'.join(tail[-8:]))

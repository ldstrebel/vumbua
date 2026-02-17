---
description: Generate a radio recap script for a game session
---

1.  **Identify the Session**: Determine which session(s) the user wants to recap (e.g., Session 2, Session 2.5).
2.  **Identify the Persona**: Confirm the character voice (default: **Valerius "Val" Sterling** - Arrogant, Polished, Charismatic).
3.  **Gather Context**:
    -   Read the `session-[number].md` or `session-[number]-transcript.md` files for key events.
    -   Identify major plot points, cliffhangers, and world updates.
4.  **Draft the Script**:
    -   Create a new file in `docs/radio-scripts/` named `session-[number]-recap.md`.
    -   **ElevenLabs Formatting Guide (Crucial for Natural Performance)**:
        -   **Punctuation & Prosody**:
            -   `FULL CAPS`: Use for the "Big Reveal" or significant stress (e.g., "The SPECTACULAR gala!").
            -   `"Quotation Marks"`: Subtle emphasis/inflection change (sarcasm or specific terms).
            -   `-` (Hyphen with spaces): Brief, snappy pause.
            -   `—` (Em Dash): Strong break/reset of intonation.
            -   `...` (Ellipses): Weighty pause for anticipation.
            -   `;` (Semicolon): Short energy-maintaining pause.
            -   `!` / `!!!`: Increased pitch and excitement.
        -   **Audio Tags (Eleven v3)**:
            -   Use bracketed tags for specific instructions: `[excited]`, `[loudly]`, `[shouting]`, `[whispering]`, `[laughs]`, `[rapid-fire]`, `[deliberate]`.
            -   Accents: `[Transatlantic accent]` for that old-timey radio feel if needed.
        -   **Pacing & Pauses (Clean)**:
            -   **Preferred**: Use `...` (ellipses) or paragraph breaks for natural pauses.
            -   **Alternative**: Use `<break time="1.5s" />` ONLY if you are sure the selected model supports SSML (some models read this as text).
        -   **Phonetics**:
            -   Use phonetic spelling for complex names if necessary (e.g., "Voom-boo-uh").
    -   **Structure**:
        -   **Hook**: Attention-grabbing opening (use `[excited]` or `[loudly]`).
        -   **Recap**: Briefly touch on 2-3 major events.
        -   **Tease/Forecast**: What's coming next.
        -   **Sign-off**: Character signature.
5.  **Review**: Present the script to the user for tone checks.

#!/usr/bin/env python
"""
selfplay_xor.py
===============

PURE XOR selfplay using Meta's embeddings.

NO TRAINING. Just:
- Frozen embeddings → scalar positions
- XOR tension resolution
- TSP walk through attractors

This is the minimal viable VINE proof.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vine_pure_xor import VinePureXOR, PHI
import utils


def run_xor_selfplay():
    """Run pure XOR selfplay with real embeddings."""
    print("=" * 60)
    print("PURE XOR SELFPLAY")
    print("Meta embeddings + XOR navigation")
    print("ZERO training")
    print("=" * 60)

    # Load Meta model for embeddings only
    print("\nLoading embeddings...")
    model = utils.load_model('./alice/models/rnn_model.th')
    embeddings = model.word_encoder.weight.data.cpu().numpy()
    word_dict = model.word_dict

    # Build word list
    word_list = [word_dict.get_word(i) for i in range(len(word_dict))]

    print(f"  Embeddings: {embeddings.shape}")
    print(f"  Vocabulary: {len(word_list)} words")

    # Create two XOR agents with SAME starting state
    # (they'll diverge through conversation)
    alice = VinePureXOR(embeddings, word_list)
    bob = VinePureXOR(embeddings, word_list)

    # Load contexts
    with open('./data/negotiate/selfplay.txt', 'r') as f:
        contexts = f.readlines()

    print("\n" + "=" * 60)
    print("STARTING XOR SELFPLAY")
    print("=" * 60)

    for i, ctx_line in enumerate(contexts[:10]):
        tokens = ctx_line.strip().split()
        if len(tokens) < 6:
            continue

        ctx = tokens[:6]

        print(f"\n{'='*60}")
        print(f"Dialog {i+1}: {' '.join(ctx)}")
        print("-" * 60)

        # Initialize both agents
        alice.feed_context(ctx)
        bob.feed_context(ctx)

        # Alternate turns
        agents = [alice, bob]
        names = ["Alice", "Bob"]

        for turn in range(6):
            writer = agents[turn % 2]
            reader = agents[(turn + 1) % 2]
            name = names[turn % 2]

            response = writer.write(max_words=20)

            # Filter out special tokens
            response = [w for w in response if not w.startswith('<')]

            print(f"{name}: {' '.join(response[:15])}")
            print(f"  [glyph={writer._get_dominant_glyph()}, "
                  f"tension={writer._get_total_tension():.2f}]")

            if len(response) < 3:
                break

            reader.read(response[:10])

        # Show glyph states
        alice_drifts = [g.drift for g in alice.glyphs[:8]]
        bob_drifts = [g.drift for g in bob.glyphs[:8]]

        print(f"\nAlice glyphs[0:8]: {[f'{d:.2f}' for d in alice_drifts]}")
        print(f"Bob glyphs[0:8]:   {[f'{d:.2f}' for d in bob_drifts]}")

    print("\n" + "=" * 60)
    print("PURE XOR RESULTS")
    print("=" * 60)
    print("\nNo training was used.")
    print("All decisions via XOR tension resolution.")
    print("Memory via drift accumulation.")


if __name__ == "__main__":
    run_xor_selfplay()

import numpy as np
from collections import Counter
import heapq

def run_length_encode(zigzagged):
    """
    Run-length encoding for AC coefficients (everything except index 0).
    Returns a list of (run_length, value) pairs.
    Index 0 (DC) is kept as is for simplicity.
    """
    dc_coeff = zigzagged[0]
    ac_coeffs = zigzagged[1:]

    rle = []
    run = 0
    # Find the last non-zero index to add EOB (End of Block)
    last_nonzero = -1
    for i in range(len(ac_coeffs) - 1, -1, -1):
        if ac_coeffs[i] != 0:
            last_nonzero = i
            break

    if last_nonzero == -1:
        # All AC are zero
        rle.append((0, 0)) # EOB
    else:
        for i in range(last_nonzero + 1):
            if ac_coeffs[i] == 0:
                run += 1
                if run == 16:
                    rle.append((15, 0)) # ZRL (Zero Run Length)
                    run = 0
            else:
                rle.append((run, ac_coeffs[i]))
                run = 0
        if last_nonzero < len(ac_coeffs) - 1:
            rle.append((0, 0)) # EOB

    return dc_coeff, rle

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    if len(priority_queue) == 0:
        return None
    if len(priority_queue) == 1:
        node = heapq.heappop(priority_queue)
        root = HuffmanNode(None, node.freq)
        root.left = node
        return root

    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(priority_queue, merged)

    return heapq.heappop(priority_queue)

def generate_huffman_codes(node, prefix="", codes={}):
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = prefix
    generate_huffman_codes(node.left, prefix + "0", codes)
    generate_huffman_codes(node.right, prefix + "1", codes)
    return codes

def huffman_encode(data):
    """
    Apply Huffman coding to a list of symbols.
    For simplicity, we build a tree based on the provided data.
    """
    if not data:
        return "", {}

    frequencies = Counter(data)
    root = build_huffman_tree(frequencies)
    codes = generate_huffman_codes(root, "", {})

    encoded_str = "".join(codes[symbol] for symbol in data)
    return encoded_str, codes

import streamlit as st

# ======================
# Cipher Decoding Logic
# ======================

def decode_morse(code):
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----':'0', '.----':'1', '..---':'2', '...--':'3',
        '....-':'4', '.....':'5', '-....':'6', '--...':'7', '---..':'8', '----.':'9'
    }
    return ''.join(morse_dict.get(char, '?') for char in code.strip().split(' '))

def decode_binary(code):
    try:
        chars = []
        for b in code.strip().split():
            if len(b) != 5 or not all(c in '01' for c in b):
                chars.append('?')
                continue
            val = int(b, 2)
            if 1 <= val <= 26:
                chars.append(chr(val + 64))  # A=65
            else:
                chars.append('?')
        return ''.join(chars)
    except:
        return "❌ Invalid binary input (expect space-separated 5-digit binary numbers for A-Z)."

def decode_caesar(code, shift=3):
    result = ''
    for char in code:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            result += char
    return result

def decode_a1z26(code):
    try:
        return ''.join(chr(int(num) + 64) if num.isdigit() else ' ' for num in code.strip().split())
    except:
        return "Invalid A1Z26 input."


def semaphore_visual_input():
    import itertools
    # CSS to support grid-like button layout
    st.markdown("""
        <style>
        .semaphore-grid {
            display: grid;
            grid-template-columns: repeat(3, 50px);
            gap: 10px;
            justify-content: center;
            margin-bottom: 16px;
        }

        .semaphore-grid .stCheckbox>div {
            transform: scale(1.5);
            transform-origin: center;
        }

        label[data-testid="stCheckboxLabel"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Define valid positions (excluding center)
    positions = {
        1: 'Top Left',     2: 'Top Center',     3: 'Top Right',
        4: 'Middle Left',                     6: 'Middle Right',
        7: 'Bottom Left',  8: 'Bottom Center', 9: 'Bottom Right'
    }

    # Display 3x3 grid, center disabled
    grid = {}
    for row in [(1, 2, 3), (4, 5, 6), (7, 8, 9)]:
        cols = st.columns(3)
        for idx, pos in zip(row, cols):
            with pos:
                if idx == 5:
                    st.markdown("⬛", unsafe_allow_html=True)  # Center blocked
                else:
                    grid[idx] = st.checkbox("", key=f"sem_{idx}", label_visibility="collapsed")

    # Collect selected positions
    selected = [idx for idx, checked in grid.items() if checked]

    # Enforce only two positions selected
    if len(selected) != 2:
        st.info("Please select exactly two flag positions.")
        return

    # Always sort positions so order doesn't matter
    selected_key = tuple(sorted(selected))

    # Define mapping from position pairs to letters
    semaphore_map = {
        (7, 8): 'A', (4, 8): 'B', (1, 8): 'C', (2, 8): 'D', (3, 8): 'E', (6, 8): 'F',
        (8, 9): 'G', (4, 7): 'H', (1, 7): 'I', (2, 6): 'J', (2, 7): 'K', (3, 7): 'L',
        (6, 7): 'M', (7, 9): 'N', (1, 4): 'O', (2, 4): 'P', (3, 4): 'Q', (4, 6): 'R',
        (4, 9): 'S', (1, 2): 'T', (1, 3): 'U', (2, 9): 'V', (3, 6): 'W', (3, 9): 'X',
        (1, 6): 'Y', (6, 9): 'Z'
    }

    # Look up letter
    letter = semaphore_map.get(selected_key, '?')

    st.markdown(f"<h3 style='text-align:center;'>🧭 Flags at {selected_key} → {letter}</h3>", unsafe_allow_html=True)

    # Reset button (safe way)
    def reset_semaphore_state():
        for i in positions.keys():
            st.session_state[f"sem_{i}"] = False

    st.button("Reset", on_click=reset_semaphore_state)

def braille_visual_input():
    st.markdown("""
        <style>
        .braille-grid {
            display: flex;
            flex-wrap: wrap;
            max-width: 180px;
            margin: 0 auto 16px auto;
            justify-content: center;
            gap: 10px;
        }

        .braille-grid .stCheckbox {
            width: 40px;
            height: 40px;
        }

        .braille-grid .stCheckbox>div {
            transform: scale(1.8);
            transform-origin: center;
        }

        label[data-testid="stCheckboxLabel"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    bit_values = []
    st.markdown('<div class="braille-grid">', unsafe_allow_html=True)

    # Braille pattern: 3 rows × 2 columns

    for row in [(1, 4), (2, 5), (3, 6)]:
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            b1 = st.checkbox("", key=f"dot{row[0]}", label_visibility="collapsed")
            bit_values.append('1' if b1 else '0')
        with col2:
            b2 = st.checkbox("", key=f"dot{row[1]}", label_visibility="collapsed")
            bit_values.append('1' if b2 else '0')

    braille_bits = ''.join(bit_values)

    # Braille dictionary
    braille_dict = {
        '100000': 'A', '101000': 'B', '110000': 'C', '110100': 'D',
        '100100': 'E', '111000': 'F', '111100': 'G', '101100': 'H',
        '011000': 'I', '011100': 'J', '100010': 'K', '101010': 'L',
        '110010': 'M', '110110': 'N', '100110': 'O', '111010': 'P',
        '111110': 'Q', '101110': 'R', '011010': 'S', '011110': 'T',
        '100011': 'U', '101011': 'V', '011101': 'W', '110011': 'X',
        '110111': 'Y', '100111': 'Z'
    }

    decoded = braille_dict.get(braille_bits, '?')
    st.markdown(f"<h3 style='text-align:center;'>Translating Braille `{braille_bits}` → {decoded}</h3>", unsafe_allow_html=True)

    # Reset button (safe way)
    def reset_braille_state():
        for i in [1,2,3,4,5,6]:
            st.session_state[f"dot{i}"] = False

    st.button("Reset", on_click=reset_braille_state)

def decode_ternary(code):
    """Decodes 3-digit ternary numbers to A-Z using 1–26 mapping"""
    try:
        chars = []
        for t in code.strip().split():
            if len(t) != 3 or not all(c in '012' for c in t):
                chars.append('?')
                continue
            val = int(t, 3)
            if 1 <= val <= 26:
                chars.append(chr(val + 64))  # A=1 → 65
            else:
                chars.append('?')
        return ''.join(chars)
    except:
        return "❌ Invalid ternary input (use space-separated 3-digit base-3 numbers for A–Z)."


# ======================
# Streamlit App UI
# ======================

# Set page config
st.set_page_config(page_title="Cipher Decoder", layout="centered")

st.title("🧩 The RSVPuzzle Decoder")

# Cipher selection
cipher_type = st.selectbox(
    "Select a cipher to decode:",
    ["Morse", "Binary", "A1Z26", "Semaphore", "Braille", "Ternary", "Caesar Shift"]
)

# Only show text input for non-Braille types
if cipher_type != "Braille" and cipher_type != "Semaphore" and cipher_type != "Caesar Shift":
    user_input = st.text_area("Enter your encoded message:")

    if st.button("Decode"):
        if not user_input.strip():
            st.warning("Please enter some input to decode.")
        else:
            # Call appropriate decoder based on type
            if cipher_type == "Morse":
                result = decode_morse(user_input)
            elif cipher_type == "Binary":
                result = decode_binary(user_input)
            elif cipher_type == "A1Z26":
                result = decode_a1z26(user_input)
            elif cipher_type == "Ternary":
                result = decode_ternary(user_input)
            else:
                result = "Unsupported cipher."

            st.success(f"Decoded Output: `{result}`")

elif cipher_type == "Braille":
    # Render 2×3 braille visual input instead of text box
    braille_visual_input()

elif cipher_type == "Semaphore":
    semaphore_visual_input()

elif cipher_type == "Caesar Shift":
    st.write("### 🏛️ Caesar Cipher Decoder")

    message = st.text_area("Enter the message to decode:")

    shift_mode = st.radio("Choose shift mode:", ["Select a shift", "Bruteforce all shifts"])

    if shift_mode == "Select a shift":
        shift = st.slider("Caesar Shift", min_value=-25, max_value=25, value=0)
        if st.button("Decode"):
            def decode_caesar(text, shift):
                result = ''
                for char in text:
                    if char.isalpha():
                        offset = 65 if char.isupper() else 97
                        result += chr((ord(char) - offset + shift) % 26 + offset)
                    else:
                        result += char
                return result

            decoded = decode_caesar(message, shift)
            st.success(f"🔓 Shift {shift}: `{decoded}`")

    else:  # Brute-force all shifts
        if st.button("Bruteforce Decode"):
            def decode_caesar(text, shift):
                result = ''
                for char in text:
                    if char.isalpha():
                        offset = 65 if char.isupper() else 97
                        result += chr((ord(char) - offset + shift) % 26 + offset)
                    else:
                        result += char
                return result

            for s in range(1, 26):
                decoded = decode_caesar(message, s)
                st.markdown(f"**Shift {s:>2}** → `{decoded}`")

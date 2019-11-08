import heapq
import pickle
import sys

PADDING_LENGTH = 8


def read_content(file_name):
    with open(file_name) as file:
        return file.read()


def print_bytes_to_file(file_name, content):
    f = open(file_name, "wb")
    f.write(content)
    f.close()


def print_str_to_file(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()


def prepare_compressed_file_name(old_name):
    return '_compressed_' + old_name


def prepare_decompressed_file_name(old_name):
    return '_decompressed_' + old_name


class Leaf:

    def __init__(self, char, count):
        self.char = char
        self.count = count
        self.code = ''

    def __lt__(self, other):
        if other is None:
            return -1
        if not isinstance(other, Leaf):
            return -1
        return self.count < other.count

    def __str__(self):
        if self.char is None:
            return '' + ': ' + str(self.count)
        return self.char + ': ' + str(self.count)

    def __repr__(self):
        return str(self)

    def add_left_leaf(self, leaf):
        self.left = leaf

    def add_right_leaf(self, right):
        self.right = right


def build_frequency_dictionary(content):
    frequency_dictionary = {}
    current_index = 0
    while current_index < len(content):
        coding_word = content[current_index:current_index + CODING_LENGTH]
        if coding_word not in frequency_dictionary.keys():
            frequency_dictionary[coding_word] = 1
        else:
            frequency_dictionary[coding_word] += 1
        current_index += CODING_LENGTH
    return frequency_dictionary


def build_heap_from_frequency_dictionary(frequency_dictionary):
    heap = []
    for key in frequency_dictionary:
        heapq.heappush(heap, Leaf(key, frequency_dictionary[key]))
    return heap


def build_binary_tree_from_heap(heap):
    while len(heap) > 1:
        left_leaf = heapq.heappop(heap)
        right_leaf = heapq.heappop(heap)
        new_leaf = Leaf(count=left_leaf.count + right_leaf.count, char=None)
        new_leaf.add_left_leaf(left_leaf)
        new_leaf.add_right_leaf(right_leaf)
        heapq.heappush(heap, new_leaf)
    return heapq.heappop(heap)


def assign_codes_foo(root):
    codes = {}
    reverse_codes = {}
    assign_codes_for_leaf(root, '', codes, reverse_codes)
    return codes, reverse_codes


def assign_codes_for_leaf(leaf, code, codes, reverse_codes):
    if leaf is None:
        return

    if leaf.char is not None:
        leaf.code = code
        codes[leaf.char] = code
        reverse_codes[code] = leaf.char
        return

    assign_codes_for_leaf(leaf.left, code + "0", codes, reverse_codes)
    assign_codes_for_leaf(leaf.right, code + "1", codes, reverse_codes)


def encode_text(codes, text):
    encoded_text = ""
    current_index = 0
    while current_index < len(text):
        coding_word = text[current_index:current_index + CODING_LENGTH]
        encoded_text += codes[coding_word]
        current_index += CODING_LENGTH
    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = PADDING_LENGTH - len(encoded_text) % PADDING_LENGTH
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def convert_to_bytearray(padded_encoded_text):
    if len(padded_encoded_text) % PADDING_LENGTH != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), PADDING_LENGTH):
        byte = padded_encoded_text[i:i + PADDING_LENGTH]
        b.append(int(byte, 2))
    return bytes(b)


def huffman(content):
    frequency_dictionary = build_frequency_dictionary(content)
    heap = build_heap_from_frequency_dictionary(frequency_dictionary)
    binary_tree_root = build_binary_tree_from_heap(heap)
    codes, reverse_codes_out = assign_codes_foo(binary_tree_root)
    encoded_text = encode_text(codes, content)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = convert_to_bytearray(padded_encoded_text)
    return byte_array, reverse_codes_out


def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text


def decode_text(encoded_text, reverse_codes_in):
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes_in:
            character = reverse_codes_in[current_code]
            decoded_text += character
            current_code = ""

    return decoded_text


def decompress(input_path, reverse_codes_in):
    decompressed_content = ''
    with open(input_path, 'rb') as file:
        bit_string = ""

        byte = file.read(1)
        while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
        encoded_text = remove_padding(bit_string)
        decompressed_content += decode_text(encoded_text, reverse_codes_in)

    return decompressed_content


CODING_LENGTH = 1


def save_as_pkl(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pkl(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    action = sys.argv[1]
    file_name = sys.argv[2]
    CODING_LENGTH = int(sys.argv[3])
    if 'c' in action:
        content = read_content(file_name)
        if not len(content):
            raise Exception('Empty input file!')
        compressed_content, reverse_codes = huffman(content)
        output_filename = prepare_compressed_file_name(file_name)
        print_bytes_to_file(output_filename, compressed_content)
        save_as_pkl(reverse_codes, 'reverse_codes_compressed_' + file_name)
        print((len(content) - len(compressed_content)) / len(content))
    elif 'd' in action:
        reverse_codes_from_pkl = load_pkl('reverse_codes' + file_name)
        decompressed = decompress(file_name, reverse_codes_from_pkl)
        print_str_to_file(prepare_decompressed_file_name(file_name), decompressed)

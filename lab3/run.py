import heapq
import time

ENCODING_LENGHT = 8


def read_content(file_name):
    with open(file_name) as file:
        return file.read()


def print_to_file(file_name, content):
    f = open(file_name, "wb")
    f.write(content)
    f.close()


def prepare_file_name(old_name):
    return str(time.ctime()).replace(' ', '_').replace(':', '-') + '_compressed_' + old_name


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

    def init_prefix(self, prefix):
        self.prefix = prefix

    def add_left_leaf(self, leaf):
        self.left = leaf

    def add_right_leaf(self, right):
        self.right = right


def build_frequency_dictionary(content):
    frequency_dictionary = {}
    for char in content:
        if char not in frequency_dictionary.keys():
            frequency_dictionary[char] = 1
        else:
            frequency_dictionary[char] += 1
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


def assign_codes(leaf, code, codes):
    if leaf is None:
        return

    if leaf.char is not None:
        leaf.code = code
        codes[leaf.char] = code
        return

    assign_codes(leaf.left, code + "0", codes)
    assign_codes(leaf.right, code + "1", codes)


def encode_text(codes, text):
    encoded_text = ""
    for character in text:
        encoded_text += codes[character]
    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = ENCODING_LENGHT - len(encoded_text) % ENCODING_LENGHT
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % ENCODING_LENGHT != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), ENCODING_LENGHT):
        byte = padded_encoded_text[i:i + ENCODING_LENGHT]
        b.append(int(byte, 2))
    return bytes(b)


def huffman(content):
    frequency_dictionary = build_frequency_dictionary(content)
    heap = build_heap_from_frequency_dictionary(frequency_dictionary)
    binary_tree_root = build_binary_tree_from_heap(heap)
    codes = {}
    assign_codes(binary_tree_root, '', codes)
    encoded_text = encode_text(codes, content)
    pad_encoded_text(encoded_text)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)
    return byte_array


if __name__ == '__main__':
    file_name = 'seneca.txt'
    content = read_content(file_name)
    if not len(content):
        raise Exception('Empty input file!')
    compressed_content = huffman(content)
    print_to_file(prepare_file_name(file_name), compressed_content)
    print((len(content) - len(compressed_content)) / len(content))

from heapq import *
import array

try:
    from collections import defaultdict
except ImportError:
    class defaultdict(dict):
        def __init__(self, default_factory=None, *a, **kw):
            if (default_factory is not None and
                not hasattr(default_factory, '__call__')):
                raise TypeError('first argument must be callable')
            dict.__init__(self, *a, **kw)
            self.default_factory = default_factory
        def __getitem__(self, key):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                return self.__missing__(key)
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            self[key] = value = self.default_factory()
            return value
        def __reduce__(self):
            if self.default_factory is None:
                args = tuple()
            else:
                args = self.default_factory,
            return type(self), args, None, None, self.items()
        def copy(self):
            return self.__copy__()
        def __copy__(self):
            return type(self)(self.default_factory, self)
        def __deepcopy__(self, memo):
            import copy
            return type(self)(self.default_factory,
                              copy.deepcopy(self.items()))
        def __repr__(self):
            return 'defaultdict(%s, %s)' % (self.default_factory,
                                            dict.__repr__(self))


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
        nedbatchelder.com
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

try:
    bin
except NameError:
    def bin(a):
        s=''
        t={'0':'000','1':'001','2':'010','3':'011',
        '4':'100','5':'101','6':'110','7':'111'}
        if a == 0:
            return '000'
        for c in oct(a)[1:]:
            s+=t[c]
        return s

class Huffman:

    def __init__(self):
        self.key = {}
        self.rKey = {}

    def build(self, phrase):
        self.detFrequency(phrase)
        self.buildTree()
        self.buildKey()

    def detFrequency(self, phrase):
        self.frequency = defaultdict(int)
        for c in phrase:
            self.frequency[c] += 1

    def buildTree(self):
        self.heap = [[v, k] for k, v in self.frequency.iteritems()]
        heapify(self.heap)
        while len(self.heap) > 1:
            left, right = heappop(self.heap), heappop(self.heap)
            heappush(self.heap, [left[0] + right[0], left, right])

    def buildKey(self, root=None, code=''):
        if root is None:
            self.buildKey(self.heap[0])
            for k,v in self.key.iteritems():
                self.rKey[v] = k
        elif len(root) == 2:
            self.key[root[1]] = code
        else:
            self.buildKey(root[1], code+'0')
            self.buildKey(root[2], code+'1')

    def encode(self, phrase):
        return ''.join([self.key[c] for c in phrase])

    def encodeToFile(self, phrase, filename):
        enc = self.encode(phrase)
        fill = 8 - (len(enc) % 8)
        if fill == 8:
            fill = 0
        data = array.array('B')
        data.append(fill)
        enc = enc.zfill(len(enc)+fill)
        for byte in chunks(enc,8):
            data.append(int(byte, 2))
        f = open(filename, 'wb')
        data.tofile(f)
        f.close()

    def decode(self, binary):
        phrase = ''
        curr = ''
        for bit in binary:
            curr = '%s%s' % (curr, bit)
            if curr in self.rKey:
                phrase += self.rKey[curr]
                curr = ''
        return phrase

    def decodeFromFile(self, filename):
        f = open(filename, 'rb')
        data = array.array('B')
        while True:
            try:
                data.fromfile(f, 1024)
            except EOFError:
                break
        fill = data[0]
        binary = ''.join([bin(byte)[-8:].zfill(8) for byte in data[1:]])
        binary = binary[fill:]
        return self.decode(binary)

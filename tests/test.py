import unittest
from Huffman import *

class TestChunks(unittest.TestCase):

    def setUp(self):
        self.data = range(20)
        self.c = chunks(self.data, 8)

    def testSize(self):
        """ No chunk is bigger than chunk size """
        toobig = [chunk for chunk in self.c if len(chunk) > 8]
        self.assertEqual(toobig, [])

    def testLoss(self):
        """ All numbers are maintained in chunks """
        full = []
        for piece in self.c:
            full.extend(piece)
        self.assertEqual(full, self.data)

    def testFull(self):
        """ All (except last) chunks are full sized """
        notfull = [chunk for chunk in self.c if len(chunk) < 8]
        self.assert_(len(notfull) < 2)

class TestBin(unittest.TestCase):

    def setUp(self):
        pass

    def testValidity(self):
        """ Original integer equals the integer of the binary """
        for num in xrange(1024):
            self.assertEqual(num, int(bin(num), 2))

class TestHuffman(unittest.TestCase):

    def setUp(self):
        self.huffman = Huffman()
        self.phrase = 'The quick brown fox jumped over the lazy dog. Filler text to create a bigger shift in the character probabilities.'
        self.huffman.build(self.phrase)

    def testPhrase(self):
        self.huffman.build(self.phrase)
        enc = self.huffman.encode(self.phrase)
        self.assertEqual(self.phrase, self.huffman.decode(enc))
        
if __name__ == '__main__':
    unittest.main()

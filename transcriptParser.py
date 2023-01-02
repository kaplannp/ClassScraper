import re


class Parser:

    def __init__(self):
        self.stream = None

    def parseBlocks(self, filename, pattern):
        with open(filename) as file:
            self.stream = file.read()
        blocks = []
        while self.stream:
            block = self._consumeBlock(pattern)
            blocks.append(block)
        self.stream=None
        return blocks

    def _getBlockBounds(self, pattern):
        firstMatch = re.search(pattern, self.stream)
        secondMatch = re.search(pattern, self.stream[firstMatch.end():])
        end = firstMatch.end() + secondMatch.start() if secondMatch else \
              len(self.stream)
        return (firstMatch.start(), end)

    def _consumeUntil(self, i):
        self.stream = self.stream[i:]

    def _consumeBlock(self, pattern):
        bounds = self._getBlockBounds(pattern)
        data = self.stream[bounds[0]:bounds[1]]
        self._consumeUntil(bounds[1])
        return data

class BlockAnalyzer:

    def __init__(self):
        pass

    def getName(self, block, startPattern, endPattern):
        match = re.match(startPattern+'.*'+endPattern, block)
        matchGroup = match.group()
        startI = re.match(startPattern, matchGroup).end()
        endI = re.search(endPattern, matchGroup[startI:]).start() + startI
        return matchGroup[startI:endI]

class TranscriptAnalyzer:

    def __init__(self):
        self.parser = Parser()
        self.blockAnalyzer = BlockAnalyzer()

    def getParticipationCounts(self, filename, startPattern, endPattern):
        blocks = self.parser.parseBlocks(filename, startPattern)
        names = [self.blockAnalyzer.getName(block, startPattern, endPattern) \
                  for block in blocks]
        return self._countDistincts(names)

    def _countDistincts(self, l):
        counts = {}
        for item in l:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return counts
        
ta = TranscriptAnalyzer()
print(ta.getParticipationCounts("sampleTranscript.txt", 
                                r'\d?\d:\d\d:\d\d [ap]m - ', r':\n'))

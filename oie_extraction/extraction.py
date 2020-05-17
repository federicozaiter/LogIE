import spacy


class Extraction:
    """ arg1, (predicate, (arg2))"""
    
    __nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def __get_root(sentence):
        if sentence is None:
            return None
        doc = Extraction.__nlp(sentence)
        for token in doc:
            if token.dep_ == 'ROOT':
                return token.text
        return None

    def __init__(self, pred, arg1=None, arg2=None, sentence=None, confidence=None):
        self.pred = pred
        self.arg1 = arg1
        self.arg2 = arg2
        self.sentence = sentence
        self.confidence = confidence

    @classmethod
    def fromTuple(cls, tup, sentence=None, confidence=None):
        if len(tup) == 1:
            return cls(tup[0], arg1="", arg2="", sentence=sentence, confidence=None)
        elif len(tup) == 2:
            return cls(tup[1], arg1=tup[0], arg2="", sentence=sentence, confidence=None)
        elif len(tup) == 3:
            return cls(tup[1], arg1=tup[0], arg2=tup[2], sentence=sentence, confidence=None)
        raise ValueError("The tuple should have one to three elements.")

    def __str__(self):
        return str((self.arg1, self.pred, self.arg2))
        pprint = []
        if self.arg1:
            pprint.append(self.arg1)
        pprint.append(self.pred)
        if self.arg2:
            pprint.append(self.arg2)
        return str(tuple(pprint))
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Extraction):
            get_root = Extraction.__get_root
            return (
                get_root(self.pred) == get_root(other.pred)
                and get_root(self.arg1) == get_root(other.arg1)
                and get_root(self.arg2) == get_root(other.arg2)
            )
        return NotImplemented

    def __key(self):
        get_root = Extraction.__get_root
        return (
            get_root(self.arg1),
            get_root(self.pred),
            get_root(self.arg2),
            )

    def __hash__(self):
        return hash(self.__key())
    
    def __len__(self):
        length = 0
        if self.arg1:
            length += 1
        if self.pred:
            length += 1
        if self.arg2:
            length += 1
        return length
    
    def copy(self):
        return Extraction(
            str(self.pred),
            arg1=str(self.arg1),
            arg2=str(self.arg2),
            sentence=str(self.sentence) if self.sentence else None, 
            confidence=self.confidence,
            )


class UnstructuredExtraction:
    """(predicate, [*args])"""
    
    __nlp = spacy.load('en_core_web_sm')
    LEXICAL_THRESHOLD = 0.25

    @staticmethod
    def __get_root(sentence):
        if sentence is None:
            return None
        doc = UnstructuredExtraction.__nlp(sentence)
        for token in doc:
            if token.dep_ == 'ROOT':
                return token.text
        return None

    def __init__(self, pred, args=None, sentence=None, confidence=None):
        self.pred = pred
        self.args = args
        self.sentence = sentence
        self.confidence = confidence

    @classmethod
    def fromExtraction(cls, extraction):
        args = extraction.arg1.split() if extraction.arg1 else []
        args.extend(extraction.arg2.split() if extraction.arg2 else [])
        return cls(
            str(extraction.pred),
            args=[str(arg) for arg in args],
            sentence=str(extraction.sentence) if extraction.sentence else None,
            confidence=extraction.confidence
            )

    def __str__(self):
        return str((self.pred, self.args))
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, UnstructuredExtraction):
            self_res = self.pred.strip().split()
            other_res = other.pred.strip().split()
            if not set(self_res).intersection(set(other_res)):
                return False
            count_match = 0      
            for w1 in other.args:
                for w2 in self.args:
                    if w1 == w2:
                        count_match += 1
            # we consider both coverages in this case so that the eq
            # operator behaves symetrically
            coverage_self = count_match / len(self.args) if self.args else 0
            coverage_other = count_match / len(other.args) if other.args else 0
            if coverage_self > UnstructuredExtraction.LEXICAL_THRESHOLD\
                or\
                coverage_other > UnstructuredExtraction.LEXICAL_THRESHOLD:
                return True
            return False
        return NotImplemented

    def __key(self):
        get_root = UnstructuredExtraction.__get_root
        return (
            get_root(self.pred),
            ' '.join(self.args),
            )

    def __hash__(self):
        return hash(self.__key())
    
    def __len__(self):
        length = 0
        if self.pred:
            length += 1
        if self.args:
            length += len(self.args)
        return length
    
    def copy(self):
        return UnstructuredExtraction(
            str(self.pred),
            args=[str(arg) for arg in self.args],
            sentence=str(self.sentence) if self.sentence else None, 
            confidence=self.confidence,
            )
    
    @staticmethod
    def unstructure_extractions(extractions):
        unstructured = []
        for ext in extractions:
            if hasattr(ext, 'args'):
                unstructured.append(ext.copy())
            else:
                unstructured.append(UnstructuredExtraction.fromExtraction(ext))
        return unstructured


def main():
    one = Extraction('changed state to', arg1='VAR1', arg2='up',
                     sentence="Vlan-interface VAR1 changed state to up")
    two = Extraction('changed', arg1='VAR1', arg2='up',
                     sentence="Vlan-interface VAR1 changed state to up")
    gt = Extraction.fromTuple(('VAR1', 'changed to', 'up'),
                     sentence="Vlan-interface VAR1 changed state to up")
    
    print(one, two, gt)
    print(hash(one), hash(two), hash(gt))
    print(one == gt)
    a, b = set([one, two]), set([gt, two]) 
    print(a, b)
    print(a and b)
    print(two in a, two in b)
    


if __name__ == "__main__":
    main()

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

    def __init__(self, pred, arg1=None, arg2=None, sentence=None):
        self.pred = pred
        self.arg1 = arg1
        self.arg2 = arg2
        self.sentence = sentence

    @classmethod
    def fromTuple(cls, tup, sentence=None):
        if len(tup) == 1:
            return cls(tup[0], sentence=sentence)
        elif len(tup) == 2:
            return cls(tup[1], arg1=tup[0], sentence=sentence)
        elif len(tup) == 3:
            return cls(tup[1], arg1=tup[0], arg2=tup[2], sentence=sentence)
        raise ValueError("The tuple should have one to three elements.")

    def __str__(self):
        pprint = []
        if self.arg1:
            pprint.append(self.arg1)
        pprint.append(self.pred)
        if self.arg2:
            pprint.append(self.arg2)
        return str(tuple(pprint))

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

def main():
    one = Extraction('changed state to', arg1='VAR1', arg2='up',
                     sentence="Vlan-interface VAR1 changed state to up")
    gt = Extraction.fromTuple(('VAR1', 'changed to', 'up'),
                     sentence="Vlan-interface VAR1 changed state to up")
    
    print(one, gt)
    print(one == gt)
    print(bool(set([one]) & set([gt])))
    


if __name__ == "__main__":
    main()

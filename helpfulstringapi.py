import copy

def add_alphabet(cls):
    alphabet = "qwertyuiopasdfghjklzxcvbnm"
    alphabet += alphabet.upper()
    for i in alphabet:
        @property
        def newmethod(self,i=i):
            self.result += i
            return self
        setattr(cls,i,newmethod)
    return cls
    
@add_alphabet
class String:
    def __init__(self):
        self.result = ''
    @property
    def puts(self):
        print(self.result)
        return self
    @property
    def _(self):
        self.result += ' '
        return self
    @property
    def bang(self):
        self.result += '!'
        return self

String().H.e.l.l.o._.W.o.r.l.d.bang.puts
        

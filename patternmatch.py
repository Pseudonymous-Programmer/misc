import re

class ParseString:
    def __init__(self,string):
        self.str = string
        
    def munch(self,n):
        self.str = self.str[n:]
        
    def accept(self,n):
        result = re.match('^' + n,self.str)
        assert result
        self.munch(len(result.group(0)))
        return result.group(0)
    
    def done(self):
        return not self.str

    def dup(self):
        return ParseString(self.str)

    def undup(self,other):
        self.str = other.str

    def peek(self):
        return self.str[0]

    def whitespace(self):
        self.accept(r'\s*')

def any_matcher(possibilities):
    class Result:
        def __init__(self,pstr):
            self.matcher = None
            for i in possibilities:
                try:
                    new_pstr = pstr.dup()
                    self.matcher = i(new_pstr)
                    pstr.undup(new_pstr)
                    break
                except:
                    pass
            assert self.matcher
        def match(self,x):
            return self.matcher.match(x)
    return Result

class Pattern:
    @staticmethod
    def new(str_to_parse):
        parser = ParseString(str_to_parse)
        result = Pattern.Default(parser)
        assert parser.done()
        return result   

    class Any:
        def __init__(self,pstr):
            pstr.accept(r'\*')
        def match(self,x):
            return [x]

    class Ignore:
        def __init__(self,pstr):
            pstr.accept(r'_')
        def match(self,_):
            return []

    class NumLit:
        def __init__(self,pstr):
            self.num = int(pstr.accept(r'\d+'))
        def match(self,n):
            assert self.num == n
            return []

    class StrLit:
        def __init__(self,pstr):
            self.str = pstr.accept(r'"[^"]+"')[1:-1]
        def match(self,s):
            assert self.str == s
            return []

    class Parenthesized:
        def __init__(self,pstr):
            pstr.accept(r'\(')
            self.result = Pattern.Default(pstr)
            pstr.accept(r'\)')
        def match(self,x):
            return self.result.match(x)

    class Object:
        def __init__(self,pstr):
            self.attrs = {}
            pstr.accept('{')
            pstr.whitespace()
            attr = pstr.accept(r'[a-zA-Z]+')
            pstr.whitespace()
            pstr.accept('=')
            pstr.whitespace()
            val = Pattern.Complex(pstr)
            pstr.whitespace()
            self.attrs[attr] = val
            
            while(True):
                if(pstr.peek() == '}'):
                    pstr.munch(1)
                    return
                pstr.accept(',')
                pstr.whitespace()
                attr = pstr.accept(r'[a-zA-Z]+')
                pstr.whitespace()
                pstr.accept('=')
                pstr.whitespace()
                val = Pattern.Complex(pstr)
                pstr.whitespace()
                self.attrs[attr] = val

        def match(self,obj):
            for key in self.attrs:
                for val in self.attrs[key].match(getattr(obj,key)):
                    yield val
                    

    Atom = any_matcher([Any,Ignore,NumLit,StrLit,Parenthesized,Object])
    
    class List:
        def __init__(self,pstr):
            self.matchers = []
            pstr.accept(r'\[')
            if(pstr.peek() == ']'):
                pstr.munch(1)
                return
            self.matchers.append(Pattern.Default(pstr))
            while(True):
                if(pstr.peek() == ']'):
                    pstr.munch(1)
                    break
                pstr.accept(',')
                self.matchers.append(Pattern.Default(pstr))
                
        def match(self,x):
            assert len(self.matchers) == len(x)
            for matcher,i in zip(self.matchers,x):
                for val in matcher.match(i):
                    yield val

    class Cons:
        def __init__(self,pstr):
            self.match_head = Pattern.Atom(pstr)
            pstr.accept(':')
            self.match_tail = Pattern.Complex(pstr)
        def match(self,l):
            for i in self.match_head.match(l[0]): yield i
            for i in self.match_tail.match(l[1:]): yield i
            
    Complex = any_matcher([List,Cons,Atom])
    
    Default = Complex

def match(pattern,val):
    return list(Pattern.new(pattern).match(val))

def case1(*options):
    def result(x):
        for option,on_success in options:
            try:
                vals = match(option,x)
                return on_success(*vals)
            except:
                pass
        assert False,"pattern match fail"
    return result

def casen(arity,*options):
    def result(*xs):
        assert len(xs) == arity
        for *matchers,on_success in options:
            assert len(matchers) == arity
            try:
                vals = []
                for i,x in zip(matchers,xs):
                    vals += match(i,x)
                return on_success(*vals)
            except:
                pass
        assert False,"pattern match fail"
    return result

reverse = case1(
    ("[]",lambda:[]),
    ("*:*",lambda x,xs: reverse(xs) + [x])
    )

map_ = casen(2,
    ("[]","_",lambda:[]),
    ("*:*","*",lambda x,xs,f: [f(x)] + map_(xs,f)))
                

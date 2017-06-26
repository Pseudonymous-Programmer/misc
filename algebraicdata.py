import re
from types import new_class

def type_match(self,args,typedict):
    if(len(args) != len(typedict)): return False
    for key,tp in enumerate(list(typedict.values())):
        if(not isinstance(args[key],tp)):
            return False
    counter = 0
    for key in typedict:
        setattr(self,key,args[counter])
        counter += 1
    return True
        
    

def type_container(name,valid_types):
    result = new_class(name)
    def result_init(self,*args):
        for i in valid_types:
            if(type_match(self,args,i)):
                return
        raise RuntimeError("Incorrect types passed to '{}' class".format(name))
    result.__init__ = result_init
    return result
        
def stripped1(l):
    return [i.strip() for i in l]

def stripped2(l):
    return [stripped1(i) for i in l]

def stripped3(l):
    return [stripped2(i) for  i in l]

def splitted1(l,s):
    return [i.split(s) for i in l]

def splitted2(l,s):
    return [splitted1(i,s) for i in l]

def denest(l):
    return [i[0] for i in l]

def instantiate_abts(rules):
    class_defns = rules.split('\n')
    class_defns = stripped2(splitted1(class_defns,':='))
    result = {}
    class_names = []
    #instantiate classes
    for key,i in enumerate(class_defns):
        result[i[0]] = new_class(i[0])
        class_names.append(i[0])
        class_defns[key] = class_defns[key][1:]
    #parse dict
    class_defns = stripped3(splitted2(stripped2(splitted1(denest(class_defns),'|')),','))
    #create list of valid types and attach
    for key,i in enumerate(class_names):
        current_type = class_defns[key]
        valid_types = []
        for variation in current_type:
            types = {}
            for val in variation:
                name,tp = val.split('::')
                try:
                    types[name.strip()] = eval(tp.strip())
                except:
                    types[name.strip()] = result[tp.strip()]
            valid_types.append(types)
        def result_init(self,*args,valid_types=valid_types,n=i):
            for i in valid_types:
                if(type_match(self,args,i)):
                    return
            raise RuntimeError("Incorrect types passed to '{}' class".format(n))
        result[i].__init__ = result_init
    return result

test_rules = \
'''foo := a :: int | b :: bar, c :: str
bar := d :: str | e :: object'''

result = instantiate_abts(test_rules)

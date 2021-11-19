import re

COMMENT_SYMBOL = ';'
DELIM_SYMBOL = '>'

class FromMatcher(object):
    def __init__(self):
        self.vars = []

    def appendVarName(self, varname):
        self.vars.append(varname)

    def setFromReStr(self, s):
        self.fromReStr = s
        self.fromRe = re.compile(s)

    def getFromRe(self):
        return self.fromRe

    def __str__(self):
        return 'FromMatcher(%s)' % self.fromReStr

    def getVarDict(self, mo):
        return dict([(v, mo.group(v)) for v in self.vars])

class MarkovCompiler(object):
    FROM_VAR_PATTERN = re.compile(r'\{(?P<varname>[A-Z_][A-Za-z0-9_]*?)=(?P<chars>[^{}]+?)\}')
    SPECIAL_CHARS = re.compile(r'(?<!\\)([*?+\{\}\[\]\(\)])')
    REPLACE_GROUP_RE = re.compile(r'\{([^{}]+?)\}')

    @staticmethod
    def makeRe(from_s):
        fm = FromMatcher()

        class ResultHolder:
            def __init__(self):
                self.result = ''
                self.lastend = 0

        rh = ResultHolder()

        def processBetween(s):
            s = MarkovCompiler.SPECIAL_CHARS.sub(r'\\\1', s)
            return s

        def subf(mo):
            varname = mo.group('varname')
            fm.appendVarName(varname)
            chars = mo.group('chars')

            between_s = from_s[rh.lastend:mo.start()]
            rh.result += processBetween(between_s)
            rh.lastend = mo.end()

            rh.result += r'(?P<%s>[%s])' % (varname, chars)

        MarkovCompiler.FROM_VAR_PATTERN.sub(subf, from_s)

        rh.result += processBetween(from_s[rh.lastend:])

        fm.setFromReStr(rh.result)
        return fm

    @staticmethod
    def expandTo(to_s, var_dict):
        def subf(mo):
            #print 'Evaling:', '#'+mo.group(1)+'#' 
            return str(eval(mo.group(1), None, var_dict))

        return MarkovCompiler.REPLACE_GROUP_RE.sub(subf, to_s)


class Rule(object):
    def __init__(self, s):
        self.terminating = False
        self.parse(s)

    def parse(self, s):
        self._from, self._to = map(str.strip, s.split(DELIM_SYMBOL))

        if self._to[-1] == '.':
            self.terminating = True
            self._to = self._to[:-1]

        self.compile()

    def compile(self):
        self._fromMatcher = MarkovCompiler.makeRe(self._from)
#        print 'Compiled:', self._fromMatcher

    def match(self, s):
        self._mo = self._fromMatcher.getFromRe().search(s)

    def getMatch(self):
        return self._mo

    def expand(self):
        return MarkovCompiler.expandTo(self._to, self._fromMatcher.getVarDict(self._mo))

    def showVars(self):
        d = self._fromMatcher.getVarDict(self._mo)
        return ', '.join(['%s=%s' % (k, d[k]) for k in d])

    def __str__(self):
        return '%s: %s > %s' % (self.__class__.__name__, self._from, self._to)

    def isTerminating(self):
        return self.terminating

class Algorithm(object):
    def __init__(self, listOfStr):
        self.rules = list(map(Rule, listOfStr))

    def __str__(self):
        return '%s(\n\t' % self.__class__.__name__ + \
                '\n\t'.join(map(str, self.rules)) + \
                '\n)'
        
    def getRules(self):
        return self.rules

class Exit:
	pass

class Processor(object):
    def __init__(self, program=None, file=None):
        if type(program) == str:
            self.parse(program)
        elif type(program) == file:
            self.parse(program.read())
        elif file:
            self.parse(open(file).read())

    def parse(self, _s):
        _arr = [s.strip() for s in _s.split('\n') \
	                            if s.lstrip() \
	                            and s.lstrip()[0] != COMMENT_SYMBOL]
        self.setData(_arr[0])
        self.setAlgorithm(_arr[1:])

    def setData(self, initialData):
        self.initialData = initialData

    def setAlgorithm(self, algorithm):
        if type(algorithm) == str:
            self.parse('_\n'+algorithm)
            self.initialData = None
        if type(algorithm) in (list, tuple) :
            self.algorithm = Algorithm(algorithm)
        elif type(algorithm) == Algorithm:
            self.algorithm = algorithm

    def process(self, debug=True):
        _s = self.initialData

        if debug: print 'Initial data:\n', _s, '\n\nAlgorithm:\n', self.algorithm

        while True:
            try:
                _rule_applied = False

                for rule in self.algorithm.getRules():
                    rule.match(_s)
                    if rule.getMatch():
                        _rule_applied = True

                        if debug:
                            vars = rule.showVars()
                            print str(rule) + ['', ', vars: ' + vars + ':'][int(bool(vars))]
                        _s = _s[:rule.getMatch().start()] + rule.expand() + _s[rule.getMatch().end():]

                        if debug: print _s, '\n'; import time; time.sleep(.1)
                        if rule.isTerminating():
                            if debug: print 'Terminating rule...'
                            raise Exit()

                        break    

                if not _rule_applied:
                    print 'No rule matched...'
                    break

            except Exit:
                break

        if debug: print 'Result:\n', _s        
        return _s

    def solve(self, data):
        self.setData(data)
        return self.process(debug=False)


if __name__ == '__main__':
#    Processor(file='doubling_decimal2.txt').process()
#    print Processor(file='alg_reversing.txt').process(debug=False)
#    Processor(file='alg_decrementing.txt').process()
    Processor(file='adding.txt').process()
    #print 'Result : '+_s
    #print MarkovCompiler.makeRe('{Num=0-9A-Z_[]}*+{{Ost=0-1}}')
    #print MarkovCompiler.makeRe(r'[\\]$^+/()\\+?')
    #print MarkovCompiler.expandTo('#{A+B}#', {'A':5, 'B':2})


from markov_enhanced import Processor


DOUBLING_DECIMAL_ALGORITHM = """
{N1=0-9}[{N2=0-9}] > [{ (2*int(N1)+int(N2)) / 10 }]{ (2*int(N1)+int(N2)) % 10 }

^[0] > .
^[1] > 1.

$>[0]
"""

ADDING_DECIMAL_ALGORITHM = """
^@[{N=01}] > {N}

9@[1] > @[1]0

^%%%0 > %%%
^%%% > .

*%%% > %%%
{N=0-9}%%% > %%%{N}

+#$ > %%%

{N=0-9}@[1] > {int(N)+1}
{N=0-9}@[0] > {N}
{N1=0-9}*[{N2=1-9}] > @[{ (int(N1)+int(N2)) / 10 }]*{ (int(N1)+int(N2)) % 10 }

*%[{N=0-9}] > *[{N}]

{N1=0-9+}%[{N2=0-9}] > %[{N2}]{N1}

#{N=0-9+} > {N}#

{N=0-9}#$ > %[{N}]

* > *#
+ > *+
"""

REVERSING_ALGORITHM = """
%{A=\w} > {A}%
; \w - alphanumeric

%# > %
% > .

*{A=\w}{B=\w} > {B}*{A}

*{A=\w}* > *#{A}

**>%

>*
"""

REPEAT_ALGORITHM = """
*@{A=\w}>{A}*@

#{A=\w}>#![{A}]{A}

[{A=\w}]{B=\w*}>{B}[{A}]

[{A=\w}]@>{A}@

#!{A=\w}>{A}#

#*>%

%{A=\w}>{A}%
%@>.

>#*@
"""

INVERTING_ALGORITHM = """
*1>0*
*0>1*

*$>.

^>*
"""

ROT13_ALGORITHM = """
*{L=A-Ma-m} > { chr(ord(L)+13) }*
*{L=N-Zn-z} > { chr(ord(L)-13) }*
*{L=^A-Za-z} > {L}*

*$ > .
^ > *
"""

p = Processor()
setAlg = p.setAlgorithm
solve = p.solve

setAlg(DOUBLING_DECIMAL_ALGORITHM)
assert solve('27') == '54'
assert solve('123') == '246'
assert solve('999') == '1998'
assert solve('55456465464') == '110912930928'
print '.',

setAlg(ADDING_DECIMAL_ALGORITHM)
assert solve('199+11') == solve('12+198') == '210'
assert solve('11111+222') == solve('222+11111') == solve('1+11332') == '11333'
print '.',

setAlg(REVERSING_ALGORITHM)
assert solve('abcd') == 'dcba'
assert solve('1234567') == '7654321'
pal1 = 'arozaupalanalapuazora'
pal2 = 'liliputsomanamostupilil'
assert solve(pal1) == pal1
assert solve(pal2) == pal2
print '.',

setAlg(REPEAT_ALGORITHM)
assert solve('abc') == 'abcabc'
assert solve('aaaa') == solve(solve(solve('a')))
print '.',

setAlg(INVERTING_ALGORITHM)
assert solve('10100001') == '01011110'
from random import randint
s = ''.join([str(randint(0, 1)) for _ in range(100)])
assert solve(solve(s)) == s
print '.',

setAlg(ROT13_ALGORITHM)
assert solve('Hello World_Uryyb Jbeyq') == 'Uryyb Jbeyq_Hello World'
s = open('markov_enhanced_test.py').read().replace('\n', '_').replace('*', '_')
assert solve(solve(s)) == s
print '.'

print 'Pass.'


COMMENT_SYMBOL = ';'
DELIM_SYMBOL = '>'

import sys
if len(sys.argv) > 1:
	FILE_NAME = sys.argv[1]
else:
	FILE_NAME = 'alg.txt'

arr=[s for s in open(FILE_NAME, 'r').read().split('\n') \
	if s.lstrip() and s.lstrip()[0] != COMMENT_SYMBOL ]

DATA_STRING = arr[0]

ALG=arr[1:]

ALG_PAIRS=[ tuple(s.split(DELIM_SYMBOL)) for s in ALG ]

# algorithm:
_s = DATA_STRING

class Exit(BaseException):
	pass

while True:
	try:
		for i in range( len( ALG_PAIRS ) ):
			_rule_applied = False
			
			pair = ALG_PAIRS[i]
			
			if pair[0] in _s:
				_rule_applied = True
				
				_repl = pair[1]
				_term = False
				
				if _repl[-1]=='.': # this is terminating rule
					_term = True
					_repl = _repl[0:-1]
				
				print('    Applying rule', i, ALG[i])
				print(_s,'-> ',end='')
				
				_s = _s.replace(pair[0], _repl, 1)
				
				print(_s+'\n')
				
				if _term:
					print('   Terminating rule!')
					raise Exit()
					
				break
				
		if not _rule_applied:
			print('    No rules matched!')
			break # no one rules matched
			
	except Exit:
		break
		
print('Result : '+_s)

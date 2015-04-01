#!/usr/bin/env python
i = 0
while i < 100:
	i+=1
	if not i % 3:
		if not i % 5:
			print 'CracklePop'
		else:
			print 'Crackle'
	elif not i % 5:
		print 'Pop'
	else:
		print i
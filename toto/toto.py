


def add(*args):
	ret = args[0]
	for v in args:
		ret += v
	return v

if __name__ == '__main__':
	from pyannotate_runtime import collect_types
	collect_types.init_types_collection()
	with collect_types.collect():
	    print( add(1,2,3) )
	    print( add([1,2], [3,4]) )
	collect_types.dump_stats('type_info.json') 

def defunct_Read_CFDA_Nums_From_File(file):
	with open(file) as f:
		array = []
		for line in f:  # read rest of lines
			array.append(float(line))
	return array


def addRoundKey( state , key_round ): 
	return state ^ key_round 

mask = 0b1111
sBox = [12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2]

def sBoxLayer(state):
	newstate = 0
	for i in xrange(0,16):
		nibble = state & mask
		state >>=  4
		newstate +=  sBox[nibble] << ( 4 * i )
	return newstate

pLayerTable = [ 0,16,32,48, 1,17,33,49, 2,18,34,50, 3,19,35,51,
			    4,20,36,52, 5,21,37,53, 6,22,38,54, 7,23,39,55,
			    8,24,40,56, 9,25,41,57,10,26,42,58,11,27,43,59,
			   12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]

def pLayer(state):
	string_state = bin( state )[ 2: ].zfill(64)
	char_state = list( string_state )
	for i in xrange(0,len(string_state) ) :
		char_state[ pLayerTable[ i ] ] = string_state[ i ] 
	string_state = "".join(char_state)
	new_state = int( string_state , 2 )
	return new_state

def string_sbox(nibble):
	return bin( sBox [int ( nibble , 2 ) ] )[ 2: ].zfill(4)
def string_xor_counter(almost_nibble , counter):
	return bin( int(  almost_nibble, 2 ) ^ counter )[ 2: ].zfill(5)

#TODO do better without string only bitwise operations
def generateRoundKeys( key ):
	K = [] 
	string_key = bin( key )[ 2: ].zfill(80)
	K.append( int(  string_key[:64], 2 ) )
	for i in xrange(1,32):
		string_key = string_key[61:] +  string_key[:61]
		string_key = string_sbox ( string_key[:4]) + string_key[4:] 
		string_key = string_key[:60] +  string_xor_counter( string_key[60:65] , i  ) + string_key[65:]
		K.append( int(  string_key[:64], 2 ) )
	return K


def present_cipher(state, key):
	K = generateRoundKeys(key)
	for i in xrange(0,31):
		state = addRoundKey( state , K[i] )
		state = sBoxLayer( state )
		state = pLayer( state )
	state = addRoundKey( state, K[31] )
	return state

cipher_text = present_cipher(0x0000000000000000,0x00000000000000000000)
print( hex(cipher_text) )
cipher_text = present_cipher(0x0000000000000000,0xFFFFFFFFFFFFFFFFFFFF)
print( hex(cipher_text) )
cipher_text = present_cipher(0xFFFFFFFFFFFFFFFF,0x00000000000000000000)
print( hex(cipher_text) )
cipher_text = present_cipher(0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFFFFFF)
print( hex(cipher_text) )

from math import log
import sys


def generate_state_strings(self):
    #split M in r bits wide sub-strings
    states_str = {}
    for idx in range(0,len(self.M),self.r):
        if(idx + self.r >= len(self.M)):
            last_state =  True
        else:
            last_state = False
        states_str[idx/self.r] =self.pad_msg(self.M[idx:idx+self.r], last_state)
    return states_str

def pad_message(self, state, last_state):
    if(last_state):
        pad_block = '1' + (self.r-1-len(state)-8)*'0' + '00000001'
        padded_state = state + pad_block + (self.b-len(state)-len(pad_block))*'0'
    else:
        padded_state = state + ('0'*(self.b-len(state)))
    if(self.debug):
        print('############## Printing padded mesage : ####################')
        padd_list = [padded_state[i:i+128] for i in range(0, len(padded_state),128)]
        for item in padd_list:
            print(item)
    return padded_state

def display_state(self, state, state_format):
    arr = []
    if(state_format=='array'): #state is a 3d array
        st = self.arr_to_str(A)
    else:                     #state is an string
        st = state
    
    if(self.debug):
        print("############### Printing string format (bits): ####################")
        st_list = [st[i:i+128] for i in range(0, len(st),128)]
        for item in st_list:
            print(item)    
    
    byte = 0
    byte_cnt = 0
    row = []
    for i in range(len(st)):            
        byte += int(st[i]) << byte_cnt
        byte_cnt += 1
        if(byte_cnt==8):                
            row.append(format(byte,'02x')) #format doesn't work on all python versions
            #row.append(("%x"%(byte)).zfill(2)) #variant 2 - backup
            byte=0
            byte_cnt=0                
            if((len(row)==16) or (i==len(st)-1)):
                arr.append(row)
                row = []
    print('################## Printing table format (bytes) : ######################')
    for i in range(len(arr)):
        print(arr[i])       

def array_to_string (self, A):
    #initialize lanes na dplanes        
    Lane = [[] for x in xrange(25)]
    Plane = [[] for x in xrange(5)]
    
    #Generate Lanes
    for x in range(5):
        for y in range(5):
            for z in range(self.w):
                Lane[5*x+y] += chr(A[x][y][z] + 48) #convert int 0/1 to char "0"/"1"   
    
    #Generate Planes
    for j in range(5):        
        Plane[j] = ''.join(Lane[j]) + ''.join(Lane[j+5]) + ''.join(Lane[j+10]) + ''.join(Lane[j+15]) + ''.join(Lane[j+20])
    
    #Generate the string
    return (str(Plane[0]) + str(Plane[1]) + str(Plane[2]) + str(Plane[3]) + str(Plane[4]))
    
def string_to_array (self, S):
    #initialize state array    
    A = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    
    for x in range(5):        
        for y in range(5):
            for z in range(self.w):
                A[x][y][z] = int(S[(self.w)*(5*y+x)+z])    
    return A

def tetha_step(self, A):         
    
    C = [[0 for z in xrange(self.w)] for x in xrange(5)]
    D = [[0 for z in xrange(self.w)] for x in xrange(5)]
    Ap = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    for x in range(5):
        for z in range(self.w):
            C[x][z] = A[x][0][z] ^ A[x][1][z] ^ A[x][2][z] ^ A[x][3][z] ^ A[x][4][z]
    for x in range(5):
        for z in range(self.w):
            D[x][z] = C[(x-1)%5][z] ^ C[(x+1)%5][(z-1)%self.w]
    for x in range(5):        
        for y in range(5):
            for z in range(self.w):
                Ap[x][y][z] = A[x][y][z] ^ D[x][z]
    
    if(self.debug):
        print('################### Printing %s : #################'%' '.join(sys._getframe().f_code.co_name.split('_')))
        S = self.arr_to_str(Ap)        
        sha3.print_state(S,'string')   
    
    return Ap

def rho_step(self, A):
    Ap = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    x,y = 1,0
    
    for z in range(self.w): 
        Ap[0][0][z] = A[0][0][z]
    for t in range(24):
        for z in range(self.w):            
            zp = (z-(t+1)*(t+2)/2)%self.w            
            Ap[x][y][z] = A[x][y][zp]
        x,y = y,(2*x+3*y)%5
        
    if(self.debug):
        print('################### Printing %s : #################'%' '.join(sys._getframe().f_code.co_name.split('_')))
        S = self.arr_to_str(Ap)        
        sha3.print_state(S,'string')
    
    return Ap

def pii_step(self, A):
    Ap = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    for x in range(5):        
        for y in range(5):
            for z in range(self.w):
                Ap[x][y][z] = A[(x+3*y)%5][x][z]
                
    if(self.debug):
        print('################### Printing %s : #################'%' '.join(sys._getframe().f_code.co_name.split('_')))
        S = self.arr_to_str(Ap)        
        sha3.print_state(S,'string')
    
    return Ap  

def chi_step(self, A):
    Ap = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    for x in range(5):        
        for y in range(5):
            for z in range(self.w):
                Ap[x][y][z] = A[x][y][z] ^ ((A[(x+1)%5][y][z]^1) & A[(x+2)%5][y][z])
    
    if(self.debug):
        print('################### Printing %s : #################'%' '.join(sys._getframe().f_code.co_name.split('_')))
        S = self.arr_to_str(Ap)        
        sha3.print_state(S,'string')   
    
    return Ap

def iota_step(self, A, ir):       
    #initialize variables
    Ap = A
    RC_ct = [0 for i in range(self.w)]
    #Generate round constants
    for j in range(int(self.l)+1):
        RC_ct[2**j-1] = self.rc(j+7*ir)
    #Update state
    for z in range(self.w):
        Ap[0][0][z] = Ap[0][0][z]^RC_ct[z]   
    
    if(self.debug):
        print('################### Printing %s : #################'%' '.join(sys._getframe().f_code.co_name.split('_')))
        S = self.arr_to_str(Ap)        
        sha3.print_state(S,'string')        
        
    return Ap

def run_round(self, state, ir):
    Ap = self.iota(self.chi(self.pii(self.rho(self.tetha(state)))),ir)   
    return Ap  
    

def rc_fc(self,t):
    if(t%255==0):
        return 1
    R=[1,0,0,0,0,0,0,0]
    for i in range(int(t%255)):
        R.insert(0,0)        
        R[0] ^= R[8]
        R[4] ^= R[8]
        R[5] ^= R[8]
        R[6] ^= R[8]
        del R[-1] #Trunc8[R]
    return R[0]

def xored_states(self,A,Ap):
    Ax = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    for x in range(5):        
        for y in range(5):
            for z in range(self.w):    
                Ax[x][y][z] = A[x][y][z] ^ Ap[x][y][z]
    return Ax

def generate_hash(self):
    state_dict = self.gen_state_str()
    Ap = [[[0 for z in xrange(self.w)] for x in xrange(5)] for y in xrange(5)]
    for k in state_dict :    
        A = self.str_to_arr(state_dict[k])
        #Generate xored state
        A = self.xor_states(A,Ap)
        #Run 24 states
        for ir in range(int(2*self.l+12-self.nr), int(2*self.l+12-1)+1, 1): 
            if(self.debug): print("Round %d"%ir)
            Ap = self.Rnd(A,ir)
            A = Ap
    S = self.arr_to_str(Ap)
    hash_val = S[:d]
    return hash_val
   
            

class Keccak(object):
    def __init__(self, b, M, d, debug):
        self.M = M                 #input message
        self.b = b                 #state width [25, 50, 100, 200, 400, 800, 1600]
        self.w = b//25
        self.l = log(self.w,2)
        self.nr = 2*self.l + 12    #number of rounds for SHA3 functions
        self.d = d                 #digest length (in bits)
        self.c = 2*d               #capacity
        self.r = b - self.c        #rate
        self.debug = debug
  
    #split M in r bits wide sub-strings
    gen_state_str = generate_state_strings
    #Padd message
    pad_msg = pad_message 
    #Convert string state to array state  
    str_to_arr = string_to_array
    #Convert array state to string state 
    arr_to_str = array_to_string
    #Xor current state with previous state
    xor_states = xored_states
    #rc function
    rc = rc_fc
    #Tetha step
    tetha = tetha_step
    #Rho step
    rho = rho_step
    #Pi step
    pii = pii_step 
    #Chi step
    chi = chi_step 
    #Iota step
    iota = iota_step
    #Round
    Rnd = run_round
    #Printing utilities
    print_state = display_state
    #Other utilities
    str_byte_to_bit = string_byte_to_bit
    #Run sha3
    gen_hash = generate_hash
  
class SHA3(Keccak):
    """Implementation of SHA3 algorithm"""
    #SHA3 functions are a particular Keccak case (b=1600)
    def __init__(self,M,d,debug):
        Keccak.__init__(self,1600, M+'01', d, debug)
        print(self.__doc__)

      

########## Main program ###################    
debug = 0

#Message to be hashed
#M = "11001"
#M = "110010100001101011011110100110"

M = '1100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001'


#State width
#b = 1600
#digest length for SHA3_256/384/512
d = 224 #256#384#512
#SHA3 instance
#sha3 = Keccak(b, M, d, debug)
sha3 = SHA3(M,d,debug)
hash_val = sha3.gen_hash()
print('Printing Hash value')
sha3.print_state(hash_val,'string')









    

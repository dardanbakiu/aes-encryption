from AESdecryptfunc import * #import AESdecryptfunc module to use functions created for this program
import math #import math module to use function such as ceiling
import io

#check that script is running with the two text files as the two parameters or else quit
def decrypt(PassPhrase, message):
    while(len(PassPhrase)!=16):
        if(len(PassPhrase)<16):#check if less than 16 characters, if so add one space character until 16 chars
            while(len(PassPhrase)!=16):
                PassPhrase=PassPhrase+"\00"
        if(len(PassPhrase)>16):#check if bigger than 16 characters, if so then truncate it to be only 16 chars from [0:16]
            PassPhrase=PassPhrase[0:16]

    #set up some parameters
    start=0#set starting pointer for the part to decrypt of the ciphertext
    end=32#set ending pointer for the part to decrypt of the plaintex
    length=len(message)#check the entire size of the message
    loopmsg=0.00#create a decimal value
    loopmsg=math.ceil(length/32)+1#use formula to figure how long the message is and how many 16 character segmentss must be decrypted
    outputhex=""#setup output message segment in hex
    asciioutput=""#setup compilation of output message in ascii

    #need to setup roundkeys here
    PassPhrase=BitVector(textstring=PassPhrase)
    roundkey1=findroundkey(PassPhrase.get_bitvector_in_hex(),1)
    roundkey2=findroundkey(roundkey1,2)
    roundkey3=findroundkey(roundkey2,3)
    roundkey4=findroundkey(roundkey3,4)
    roundkey5=findroundkey(roundkey4,5)
    roundkey6=findroundkey(roundkey5,6)
    roundkey7=findroundkey(roundkey6,7)
    roundkey8=findroundkey(roundkey7,8)
    roundkey9=findroundkey(roundkey8,9)
    roundkey10=findroundkey(roundkey9,10)
    roundkeys=[roundkey1,roundkey2,roundkey3,roundkey4,roundkey5,roundkey6,roundkey7,roundkey8,roundkey9,roundkey10]

    # set up the segement message loop parameters
    for y in range(1, loopmsg): # loop to encrypt all segments of the message
        plaintextseg = message[start:end]

        # add round key
        bv1 = BitVector(hexstring=plaintextseg)
        bv2 = BitVector(hexstring=roundkeys[9])
        resultbv = bv1 ^ bv2
        myhexstring = resultbv.get_bitvector_in_hex()

        #inverse shift row
        myhexstring=invshiftrow(myhexstring)

        #inverse subbyte
        myhexstring=invsubbyte(myhexstring)

        for x in range(8, -1, -1):
            # add roundkey for current round
            bv1 = BitVector(hexstring=myhexstring)
            bv2 = BitVector(hexstring=roundkeys[x])
            resultbv = bv1 ^ bv2
            myhexstring = resultbv.get_bitvector_in_hex()

            # mix column
            bv3 = BitVector(hexstring=myhexstring)
            myhexstring=invmixcolumn(bv3)

            # shift rows
            myhexstring = invshiftrow(myhexstring)

            # sub byte
            myhexstring = invsubbyte(myhexstring)

        #add initial round key
        bv1 = BitVector(hexstring=myhexstring)
        bv2 = PassPhrase
        resultbv = bv1 ^ bv2
        myhexstring = resultbv.get_bitvector_in_hex()

        start = start + 32 #increment start pointer
        end = end + 32 #increment end pointer

        replacementptr = 0
        while (replacementptr < len(myhexstring)):
            if (myhexstring[replacementptr:replacementptr + 2] == '0d'):
                myhexstring = myhexstring[0:replacementptr] + myhexstring[replacementptr+2:len(myhexstring)]
            else:
                replacementptr = replacementptr + 2

        outputhex = BitVector(hexstring=myhexstring)
        asciioutput = outputhex.get_bitvector_in_ascii()
        asciioutput=asciioutput.replace('\x00','')
        return asciioutput
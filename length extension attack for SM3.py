


def zero_fill(a,n):
    if len(a)<n:
        a="0"*(n-len(a))+a
    return a
def cycle_shift_left( B, n):
    n=n%32
    return ((B << n) ^ (B >> (32 - n)))%(2**32)

def T(j):
    if j>=0 and j<=15:
        return int("79cc4519",16)
    elif j>=16 and j<=63:
        return int("7a879d8a",16)

def FF(X,Y,Z,j):
    if j>=0 and j<=15:
        return X^Y^Z
    elif j>=16 and j<=63:
        return (X&Y)|(X&Z)|(Y&Z)
def GG(X,Y,Z,j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    elif j >= 16 and j <= 63:
        return (X & Y) | (~X & Z)

def P0(x):
    return x^(cycle_shift_left(x,9))^cycle_shift_left(x,17)
def P1(x):
    return x^(cycle_shift_left(x,15))^cycle_shift_left(x,23)

def Message_extension(a):  #a的数一定要满足512bit,不够要补零!!  ,承接的是字符串
    W1 = []            #  W0-15
    W2=[]             #  W' 0-63
    #print("a消息扩展的a:",a)
    for i in range(int(len(a) / 8)):
        W1.append(int(a[8 * i:8 * i + 8],16))
        #print("W1的前16个",a[8 * i:8 * i + 8])
    for j in range(16,68):
        temp=P1(W1[j-16] ^ W1[j-9] ^ cycle_shift_left(W1[j-3],15)) ^cycle_shift_left(W1[j-13],7)^W1[j-6]
        #print("消息扩展：",hex(temp))
        W1.append(temp)

    for j in range(0,64):
        W2.append(W1[j]^W1[j+4])

    W1.append(W2)
    return W1

def CF(V,Bi):  #V是字符串
    Bi=zero_fill(Bi,128)
    W=[]
    W=Message_extension(Bi)   #消息扩展完的消息字
    #print("W:",W)
    A=int(V[0:8],16)
    #print("A:", hex(A))
    B = int(V[8:16], 16)
    C = int(V[16:24], 16)
    D = int(V[24:32], 16)
    E = int(V[32:40], 16)
    F = int(V[40:48], 16)
    G = int(V[48:56], 16)
    H = int(V[56:64], 16)
    for j in range(0,64):
        temp=(cycle_shift_left(A,12) + E +cycle_shift_left(T(j),j)) %(2**32)
        SS1=cycle_shift_left(temp,7)
        SS2=SS1 ^ cycle_shift_left(A,12)
        TT1=(FF(A,B,C,j) +D +SS2 +W[-1][j] ) %(2**32)
        TT2=(GG(E,F,G,j)+H+SS1+W[j])%(2**32)
        D=C
        C=cycle_shift_left(B,9)
        B=A
        A=TT1
        H=G
        G=cycle_shift_left(F,19)
        F=E
        E=P0(TT2)
        #print("B:", hex(B))
    t1=zero_fill(hex(A^int(V[0:8],16))[2:],8)
    t2 = zero_fill(hex(B ^ int(V[8:16], 16))[2:], 8)
    t3 = zero_fill(hex(C ^ int(V[16:24], 16))[2:], 8)
    t4 = zero_fill(hex(D ^ int(V[24:32], 16))[2:], 8)
    t5 = zero_fill(hex(E ^ int(V[32:40], 16))[2:], 8)
    t6 = zero_fill(hex(F ^ int(V[40:48], 16))[2:], 8)
    t7 = zero_fill(hex(G ^ int(V[48:56], 16))[2:], 8)
    t8 = zero_fill(hex(H ^ int(V[56:64], 16))[2:], 8)
    t=t1+t2+t3+t4+t5+t6+t7+t8
    return t

def SM3(plaintext):
    Vtemp=IV
    a=(len(plaintext)*4+1 ) % 512
    #print(a)
    k=0
    B=[]
    if a<=448:
        k=448-a
    elif a>448:
        k=512-a+448
    #print(k)
    m=plaintext+"8"+"0"*int((k+1)/4-1)+zero_fill(str(hex(len(plaintext)*4))[2:],16)
    #print(m)
    block_len=int((len(plaintext)*4 + k + 65) / 512)
    #print(block_len)
    for i in range(0,block_len):
        B.append(m[128*i:128*i+128])     #分组
    #print("B:",B)
    for i in range(0,block_len):
        Vtemp=CF(Vtemp,B[i])

    return Vtemp

def SM3_len_ex_ak(num_block,IV,plaintext):
    Vtemp=IV
    a=(len(plaintext)*4+1 ) % 512
    #print(a)
    k=0
    B=[]
    if a<=448:
        k=448-a
    elif a>448:
        k=512-a+448
    #print(k)
    m=plaintext+"8"+"0"*int((k+1)/4-1)+zero_fill(str(hex(len(plaintext)*4+num_block*512))[2:],16)
    #print(m)
    block_len=int((len(plaintext)*4 + k + 65) / 512)
    #print(block_len)
    for i in range(0,block_len):
        B.append(m[128*i:128*i+128])     #分组
    #print("B:",B)
    for i in range(0,block_len):
        Vtemp=CF(Vtemp,B[i])

    return Vtemp

IV="7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e"
IV2="66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
plaintext="616263"   #hash为IV2
num_block=1
plain_exten="61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018"
add="2022"
attack_plain=plain_exten+add

if SM3(attack_plain)==SM3_len_ex_ak(num_block,IV2,add):
    print(SM3(attack_plain))
    print(SM3_len_ex_ak(num_block,IV2,add))
    print("长度扩展攻击成功")
else:
    print("flase")




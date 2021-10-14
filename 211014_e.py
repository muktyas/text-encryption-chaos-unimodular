import numpy as np
from functools import reduce 
import time

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


#OBE
def r_ij(m, baris_i, baris_j, r):
    return m[baris_i] + r*m[baris_j]

##########################

#barisan logistic map
def log(x0, banyak):
    x = x0
    for i in range(1000):
        x = 3.9 * x * (1 - x)     # 3.9 bisa diganti bil. pada [3.7, 4]
    
    barisan = np.zeros(banyak, dtype=np.uint16)
    for i in range(banyak):
        x = 3.9 * x * (1 - x)     # 3.9 bisa diganti bil. pada [3.7, 4]
        barisan[i] = x*1000%55000
    return barisan
###########################

def kunci(n, x0):
    # matriks segitiga atas
    banyak = int(n * (n - 1)/2)
    barisan = log(x0, banyak + n - 1)
    

    msa = np.eye(n)
    
    indeks = 0
    for i in range(n):
        for j in range(i+1,n):
            msa[i,j] = barisan[indeks]
            indeks += 1
    
    # ~ print('kunci sebaran logistik')
    # ~ print(msa)
    # ~ print('@'*30)
    for baris_i in range(1,n):
        msa[baris_i] = r_ij(msa, baris_i, 0, barisan[indeks])%55000
        indeks += 1
        # ~ print(msa)
        # ~ print('-'*10)
    # ~ print('='*20)
    # ~ print(msa)
    # ~ augmented = np.zeros((n,2*n))
    # ~ augmented[:,:n]=msa
    
    # ~ augmented[:,n:]=np.eye(n)
    
    # ~ #OBE untuk dapatkan invers
    # ~ # mengenolkan segitiga bawah
    # ~ for kolom in range(n):
        # ~ for baris in range(kolom+1,n):
            # ~ augmented[baris] = r_ij(augmented, baris, kolom, -augmented[baris, kolom])%55000
    
    # ~ # mengenolkan segitiga atas
    # ~ for kolom in range(1,n):
        # ~ for baris in range(kolom):
            # ~ augmented[baris] = r_ij(augmented, baris, kolom, -augmented[baris, kolom])%55000
    
    # ~ mbalik = augmented[:,n:]

    return msa #, mbalik




# S = range(127)  semestanya Z_127

# input berupa teks
#nama_file = input('Masukkan nama file yang akan dienkripsi beserta ekstensinya.\
#\ncontoh: plainteks.txt\nnama file: ')
nama_file = "lorem.txt"
teks_asli = open(nama_file, 'r', encoding = 'utf-8')
teks = teks_asli.read()
#teks = "Assalaamu'alaikum"


n_teks = len(teks)
#print(n_teks)
# menghindari adanya n_teks prima
if (n_teks % 2 == 1):
	teks = teks + "."
n_teks = len(teks)
#print(n_teks)
#print(teks)

# convert teks ke bilangan bulat
mteks = [ ord(i) for i in teks ]
np_teks = np.array(mteks)

#print(np_teks)


f = factors(n_teks)
faktor = list(f)
print(faktor[1:])

str_password1 = input("Please choose one of the numbers in the set above as Password 1: ")
password1 = int(str_password1)
# ~ print(password1)

while password1 not in faktor:
	print("Your choice are {}".format(password1))
	print("Not in the given list.")
	print("-"*50, "\nThe list of numbers are: ")
	print(faktor)
	password1 = input("Please choose again the right one: ")
# ~ print("Your Password 1 is: ", password1, "\n")
pw2 = input("Enter Password 2 in the form of a number, maximum 14 digits (example: 22021985)\nPassword 2: ")

# ~ print("Your Password 2 is: ", pw2)
password2 = float("0." + pw2 + "1")

waktu_awal = time.time()

# membuat matriks persegi sebagai kunci berukuran password1 x password1
ukuran = password1
x0 = password2

kunciku = kunci(ukuran, x0)
print(f'Using password1: {password1} and password2: {password2}, the unimodular matrix generated is:')
print(kunciku)
print('='*20)


print(f'maks = {np_teks.max()}')
print(np_teks)
np_teks_reshape = np_teks.reshape((ukuran, int(np_teks.size/ukuran)))
#print(np_teks_reshape)

print(f'len: {np_teks.shape}')
print(f'len: {kunciku.shape}')
print(f'len: {np_teks_reshape.shape}')

# ~ np_kali = np.dot(kunciku, np_teks_reshape)%55000
np_kali = (kunciku @ np_teks_reshape)%55000
#print(np_kali)
np_chiper = np_kali.reshape(n_teks).astype(np.uint16)
print(np_chiper)
#print('hasil enkripsinya adalah:')
#print(''.join([chr(i) for i in np_dechiper]))
pwdchiper = open('password_enkripsi.txt','w', encoding = 'utf-8')
pwdchiper.write("Message:\n")
pwdchiper.write(teks + "\n")
pwdchiper.write("-"*30 + "\n\n")
pwdchiper.write("password1: ")
pwdchiper.write(str(password1) + "\n")
pwdchiper.write("password2: ")
pwdchiper.write(str(pw2) + "\n\n")
pwdchiper.write(f'waktu enkripsi: {time.time() - waktu_awal} detik')
pwdchiper.close()

chiper = open('enkripsi.txt','w', encoding = 'utf-8')
chiper.write(''.join([chr(i) for i in np_chiper]))
chiper.close()

print('Congratulation. Encryption process finish.\n')
print(f'waktu enkripsi: {time.time() - waktu_awal} detik')
print('Your encrypted message saved in file: enkripsi.txt')
print('Password saved in file: password_enkripsi.txt')

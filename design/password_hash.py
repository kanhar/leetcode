import uuid
import hashlib
 
def enc(s):
    return s.encode(encoding='UTF-8',errors='strict')
 
def hash_password(password):    
    salt = uuid.uuid4().hex
    return hashlib.sha256(enc(salt)+ enc(password)).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(enc(salt) + enc(user_password)).hexdigest()
 
new_pass = "test_pwd" 
hashed_password = hash_password(new_pass)
print('Converted ', new_pass, ' to ' + hashed_password)
check_pass = "test_pwd"
if check_password(hashed_password, check_pass):
    print('Confirmed ', check_pass, ' ==', hashed_password)


#print(hashlib.algorithms_guaranteed)
hash_object = hashlib.md5(b'Hello World')
print(hash_object.digest())

from .AbstractSplittedSecret import AbstractSplittedSecret
import json
class Decryption(AbstractSplittedSecret):
    
    def __init__(self):
        self.user_id='0';
        self.user_password=''
        super(Decryption, self).__init__()
    
    def initializeUser(self,user_id):
        self.user_id=str(user_id)
        self.user_file_decrypted_path = self.getUserFilePath(self.user_id,"decrypted")

    def initializeUserDataDecryption(self):
        self.decryptUserFile()
        self.user_data = self.loadJsonFile(self.user_file_decrypted_path)
        self.initializeNeededDecryptersAmount()
        self.initializeValidDecrypterIds()

    def initializeNeededDecryptersAmount(self):
        self.needed_decrypters_amount = len(str(list(self.user_data['groups'].keys())[0]))
    
    def initializeValidDecrypterIds(self):
        self.valid_decrypter_ids = []
        self.valid_decrypter_ids.append(int(self.user_id))
        for contact_id in self.user_data['contacts']:
            self.valid_decrypter_ids.append(int(contact_id)) 
    
    def setUserPassword(self,user_password):
        self.user_password = str(user_password)
        
    def resetDecrypterIds(self):
        self.decrypter_ids = []
        self.addDecrypterId(self.user_id)
    
    def addDecrypterId(self,decrypter_id):
        decrypter_id = int(decrypter_id)
        if decrypter_id not in self.valid_decrypter_ids:
            raise Exception("The encrypter id is not valid. Valid encrypter ids are: " + str(self.valid_decrypter_ids))
        if len(self.decrypter_ids) >= self.needed_decrypters_amount:
            raise Exception("There are already sufficients decrypters (" + str(len(self.decrypter_ids)) + ") defined!")
        if decrypter_id in self.decrypter_ids:
            raise Exception("The decrypter is already in the list.")
        self.decrypter_ids.append(decrypter_id)
        
    def getDecryptersIds(self):
        return self.decrypter_ids
        
    def getNeededCoDecryptersAmount(self):
        return self.needed_decrypters_amount -1
    
    def loadJsonFile(self,file_path):
        file = open(file_path)
        data = json.load(file)
        file.close()
        return data
    
    def decryptFile(self,password,input_file_path,output_file_path):
        self.executeCommand('gpg --batch --passphrase "'+ password + '" -o "' + output_file_path +'" "'+ input_file_path+'"')
    
    def decryptUserFile(self):
        input_file_path = self.getUserFilePath(self.user_id,"encrypted")
        self.decryptFile(self.user_password, input_file_path, self.user_file_decrypted_path)
        
    def decryptAccumulatedFile(self):
        input_file_path = self.getAccumulatedFilePath("encrypted")
        output_file_path = self.getAccumulatedFilePath("decrypted")
        self.decryptFile(self.user_password, input_file_path, output_file_path)
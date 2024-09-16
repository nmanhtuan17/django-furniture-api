import bcrypt 
import cloudinary
import cloudinary.uploader

def serialize_mongo_document(doc):
  if '_id' in doc:
    doc['_id'] = str(doc['_id'])
  return doc

def hash_password(password):
  bytes = password.encode('utf-8') 
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(bytes, salt)

def check_password(password, hashPassword):
  userBytes = password.encode('utf-8')
  return bcrypt.checkpw(userBytes, hashPassword)

def upload_image(image):
  return cloudinary.uploader.upload(image)
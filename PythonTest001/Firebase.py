from firebase import firebase
firebase = firebase.FirebaseApplication("https://testod-3e067-default-rtdb.firebaseio.com/", None)
result = firebase.get('test', None)
print (result)

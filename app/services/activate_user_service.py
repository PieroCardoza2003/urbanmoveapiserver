import random

activate_users = {}

def set_activate_user(email: str, code: str, exp: str):
    activate_users[email] = {
        'code': code,
        'exp': exp
    }


def generate_random_code() -> str:
    number = random.randint(0, 99999)
    return f"{number:05d}"

'''
def generateCode():
    code = generate_random_code()
    exp = 


const generateCode = (email) => {
    const code = randomCode()
    const exp = getExpireTime() // Los codigos expiran en 5m

    dataStore[email] = { 
        code: code, 
        exp: exp
    };

    return code
};


user_data = {}

# Función para agregar o actualizar un usuario
def set_user(email: str, code: str, exp: str):
    user_data[email] = {
        'code': code,
        'exp': exp
    }

# Función para obtener la información del usuario
def get_user(email: str):
    return user_data.get(email, None)


def get_all_users():
    return user_data

def clear_users():
    user_data.clear()
    return {"message": "All user data cleared"}



'''
# Function to validate the password
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    mensajes = []
     
    if len(passwd) < 6:
        mensajes.append('Length should be at least 6.')
    
    if len(passwd) > 20:
        mensajes.append('Length should not be greater than 20.')
         
    if not any(char.isdigit() for char in passwd):
        mensajes.append('Password should have at least one numeral.')
         
    if not any(char.isupper() for char in passwd):
        mensajes.append('Password should have at least one uppercase letter.')
         
    if not any(char.islower() for char in passwd):
        mensajes.append('Password should have at least one lowercase letter.')
         
    if not any(char in SpecialSym for char in passwd):
        mensajes.append('Password should have at least one of the symbols $@#.')

    # Retorna una cadena vacía si no hay errores
    return "\n".join(mensajes) if mensajes else ""



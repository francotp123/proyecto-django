#Convertimos los datos str a int
def string_to_number(textNumber):
    if textNumber[-1] == 'M':
        num_str = textNumber.replace('M', '')
        num = float(num_str) * 1000000
    elif textNumber[-1] == 'K':
        num_str = textNumber.replace('K', '')
        num = float(num_str) * 1000
    else:
        num = float(textNumber)
    return int(num)


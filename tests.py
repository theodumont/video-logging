dictionnaire = {
    'Audio': ['.wav', '.mp3', '.raw', '.wma'],
    'Videos': ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv', '.MOV'],
    'Images': ['.jpeg', '.jpg', '.png', '.svg', '.bmp', '.gif'],
    'Documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx']
}

for i in range(4):
    print(f"--> i={i}")

    for j in range(4):
        print(f"j={j}")

        if j==2:
            print("j=5, on veut le prochain i")
            break

    print(f"suite de la boucle avec i={i}")

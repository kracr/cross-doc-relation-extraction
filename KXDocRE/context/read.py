with open('concatenated_file.txt','r') as sd:
    for line in sd:
        s,p=line.split("\t")
        print(s,p)

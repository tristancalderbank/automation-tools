file_list = []
print "Paste data:"

while True:
    line = raw_input()
    if line.strip() == "":
        break
    file_list.append(line)



i = 0
while i < len(file_list):
    if "/" not in file_list[i]:
        with open(file_list[i] + ".txt", "w") as open_file:
            i = i + 1
            while(i < len(file_list) and "/" in file_list[i]):
                for j in range(4):
                    open_file.write(file_list[i] + "\n")
                i = i + 1

print "Cheerio old chap"




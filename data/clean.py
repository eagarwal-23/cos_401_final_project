# Just used to do some data processing. Delete before final submission.

fd = open('fd_src.txt', 'r')
Lines = fd.readlines()

fdw = open('fd_english_kline.txt', 'w')
 
# Strips the newline character
ctr = 1
for line in Lines:
    # if line.strip("\n") != "":
    #   fdw.write(line)
    if (ctr % 3) != 0:
       fdw.write(line)
    ctr += 1


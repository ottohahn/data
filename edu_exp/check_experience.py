from experience import GetExp

if __name__ == '__main__':
    # create instance of GetExp class
    ge = GetExp()

    # open file with filenames
    file = open('files.txt', 'rU')
    lines = file.readlines()
    file.close()

    # create list of filenames and years experience
    lst = []
    for line in lines:
        lst.append(line.split("\n")[0]+', '+str(ge.chain_exp("data_exp/"+line.split("\n")[0]))+'\n')

    # write lines to file
    text_file = open('edu_output.txt', 'w')
    text_file.writelines(lst)
    text_file.close()

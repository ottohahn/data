from experience import GetExp

if __name__ == '__main__':
    # create instance of GetExp class
    ge = GetExp()

    response = raw_input("Please enter the filename: ")

    a=ge.get_exp_zero('data_exp/'+ response)
    print a
    print "____"
    b=ge.get_exp_one(a)
    print b
    print "____"
    c=ge.convert_dates(b)
    print c
    print "____"
    d=ge.remove_overlap(c)
    print d
    print "____"
    e=ge.get_yrs(d)
    print e


movieid = (123,1,44,55)
print("SELECT infolink,piclink,filmdate FROM filmtable WHERE movieid in (%s) ORDER BY filmdate desc" % (movieid[0:-1]))

BEGIN {
  Len--
  while (getline l) {
    print "line:"l,length(l)
    if (l~/^;/ || l~/^[ \t\r\n]*$/) { print "skip" } # comment or empty
    else if (l~/>/) {
      print "rule:"l
      split(l,parts,">")
      From[++Len] = parts[1]
      if ((r = parts[2]) ~ /\.$/) {
        Stop[Len]
        r = substr(r,1,length(r)-1)
      }
      To[Len] = r
    } else Input = l
  }
}
END {
  print Input, Len
  while(!stop){
    for (i=0; i<Len; i++) {
      if (idx = index(Input,f = From[i])) {
        print "    Applying rule " f ">" (r=To[i])
        I2 = substr(Input,1,idx) r substr(Input,idx + length(f))
        print Input " -> " I2
        Input = I2
        if (Stop[i]) {
          print "    Terminating rule!"
          stop=1
        }
        break
      }
    }
    if (i==Len) {
      print "    No rule matched!"
      stop=1
    }
  }
  print "Result : " Input
}
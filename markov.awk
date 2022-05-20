BEGIN {
  Len=0
  while (getline l) {
    if (l~/^;/ || l~/^[ \t]*$/) {} # comment or empty
    else if (l~/>/) {
#      print "rule:"l
      split(l,parts,">")
      From[Len] = parts[1]
      if ((r = parts[2]) ~ /\.$/) {
        Stop[Len]=1
        r = substr(r,1,length(r)-1)
      }
      To[Len++] = r
    } else Input = l
  }
}
END {
  print Input, Len
  while(!stop){
    for (i=0; i<Len; i++) {
#      print "attempt: ",From[i],">",To[i],"  ",Stop[i]
      if (idx = index(Input,f = From[i])) {
        print "    Applying rule " f ">" (r=To[i])
        I2 = substr(Input,1,idx-1) r substr(Input,idx + length(f))
        print Input " -> " I2
        Input = I2
        if (Stop[i]) {
          print "    Terminating rule!"
          stop=1
        }
        break
      }
    }
    if (i==Len) { # TODO check
      print "    No rule matched!"
      stop=1
    }
  }
  print "Result : " Input
}
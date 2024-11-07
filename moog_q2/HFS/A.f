	program A

	character*100 dum, line, lineh
 	real wave, ew, waveh, ewh

	open(unit=2,file="A.moog",status="old")
	open(unit=3,file="Ahfs.moog",status="old")
	open(unit=8,file="Ahfs.out",status="unknown")

	read(2,*) n, dum

	do 100 i=1,n
	read(2,222) wave,line,ew
  222   format(f9.3,a50,f8.1)
		do 300 j=1,930
	        read(3,333) waveh,lineh,ewh
	        write(*,333)waveh,lineh,ewh
  333           format(f9.3,a54,f5.1)
	        test = abs(abs(waveh) - abs(wave))
	        if ((waveh.ge.0.0).and.(test.le.0.2)) write (8,335) waveh, lineh, ew
	        if ((waveh.le.0.0).and.(test.le.0.2)) write (8,336) waveh, lineh
  335           format(f9.3,a54,f5.1)
  336           format(f9.3,a54)
  300          continue
	       rewind(unit=3)
  100   continue

	close(unit=2)
	close(unit=3)
	close(unit=8)
	end


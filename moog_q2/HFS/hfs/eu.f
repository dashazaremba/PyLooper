	program makehfs

	character*100 dum

	open(unit=2,file='a',status='old')
	open(unit=8,file='aa.out',status='unknown')

	do 100 i=1,300
	read(2,222) wave, rlgf, elem, reng, dum, iso, corr
  222   format(f10.4,f7.3,f6.3,f12.3,a70,i3,f6.3)
             rwave = wave*10.0
	     rlgfc = rlgf + corr
             rgfc = 10**(rlgfc)
	     write(8,228) rwave, elem, iso, reng, rgfc 
  228        format(f9.3,f8.2,i3,f10.2,1x,e9.3)
  100   continue

	close(unit=2)
	close(unit=8)
	end

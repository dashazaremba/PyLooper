	program sum

	character*80 line
	open (unit=3,file='test', status='old')
	
	gfsum=0.0

	do 500 i=1,21
	read (3,1000) wave, elem, chi, rgf
 1000   format (3f10.4,e10.3)
          gf = 10**(rgf)
          if (elem.eq.56.1350) gfsum = gfsum + gf
  500   continue

	rrgf = log10(gfsum)
	
	write(*,*) gfsum, rrgf
  100   end

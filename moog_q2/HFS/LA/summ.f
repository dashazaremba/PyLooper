	program sum

	character*80 line
	open (unit=3,file='test', status='old')
	
	gfsum=0.0

	do 500 i=1,13
	read (3,1000) wave, elem, chi, rgf
 1000   format (2f10.4,f11.2,f11.3)
          gf = 10**(rgf)
          if (elem.eq.57.1) gfsum = gfsum + gf
  500   continue

	rrgf = log10(gfsum)
	
	write(*,*) wave, rrgf
  100   end

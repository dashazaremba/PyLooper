	program sum

	character*80 line
	open (unit=3,file='test', status='old')
	
	gfsum=0.0

	do 500 i=1,12
	read (3,1000) wave, elem, chi, rgf
 1000   format (f9.3,f11.5,f10.3,f9.3)
          gf = 10**(rgf)
          if (elem.eq.56.01135) gfsum = gfsum + gf
  500   continue

	rrgf = log10(gfsum)
	
	write(*,*) gfsum, rrgf
  100   end

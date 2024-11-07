	program sum

	character*80 line
	open (unit=3,file='test', status='old')
	
	gfsum3=0.0
	gfsum5=0.0

	do 500 i=1,18
	read (3,1000) wave, elem, chi, rgf
 1000   format (f10.4,f11.6,f11.3,f11.3)
          gf = 10**(rgf)
          if (elem.eq.29.0063) gfsum3 = gfsum3 + gf
          if (elem.eq.29.0063) write (*,*), rgf 
          if (elem.eq.29.0065) gfsum5 = gfsum5 + gf
  500   continue

	rgf3 = log10(gfsum3)
	rgf5 = log10(gfsum5)
	
	write(*,*) wave, rgf3, rgf5
  100   end

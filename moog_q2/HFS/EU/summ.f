	program sum

	open (unit=3,file='test', status='old')
	
	gfsum1=0.0
	gfsum3=0.0

	do 500 i=1,30
	read (3,1000) wave, elem, chi, gf
 1000   format (f10.3,f10.4,f10.3,e10.3)
c         gf = 10**(rgf)
          if (elem.eq.63.1151) gfsum1 = gfsum1 + gf
          if (elem.eq.63.1153) gfsum3 = gfsum3 + gf
  500   continue

	rgf1 = log10(gfsum1)
	rgf3 = log10(gfsum3)
  
	
	write(*,*) wave, gfsum1, rgf1, gfsum3, rgf3
  100   end

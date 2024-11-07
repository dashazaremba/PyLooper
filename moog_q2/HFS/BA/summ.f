	program sum

	character*80 line
	open (unit=3,file='test', status='old')
	
	gftot=0.0
	gfsum4=0.0
	gfsum5=0.0
	gfsum6=0.0
	gfsum7=0.0
	gfsum8=0.0

	do 500 i=1,15
	read (3,1000) wave, elem, chi, rgf
 1000   format (2f10.4,f12.3,f11.3)
          gf = 10**(rgf)
          if (elem.eq.56.1134) gfsum4 = gfsum4 + gf
          if (elem.eq.56.1135) gfsum5 = gfsum5 + gf
          if (elem.eq.56.1136) gfsum6 = gfsum6 + gf
          if (elem.eq.56.1137) gfsum7 = gfsum7 + gf
          if (elem.eq.56.1138) gfsum8 = gfsum8 + gf
  500   continue

	rgf7 = log10(gfsum7)
	
	write(*,*) wave, rrgf, gfsum4, gfsum5, gfsum6, gfsum7, gfsum8, rgf7
  100   end

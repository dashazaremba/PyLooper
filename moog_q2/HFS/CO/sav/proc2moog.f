	program proc2moog

	character*4 dum
 	open(unit=2,file="proin",status="unknown")
	open(unit=8,file="proout",status="unknown")

        write(8,*) 'Cobalt'
	elem = 27.0

	do 500 i=1,12
	read(2,222) dum, wave, chi, rloggf
	write(*,222) dum, wave, chi, rloggf
  222   format(a4,f10.3,f6.3,f7.3)
        write(8,888) wave,elem, chi, rloggf	   
  888   format(f9.2, f8.1, f13.2, f8.3)
  500   continue

	close(unit=2)
	close(unit=8)
	end



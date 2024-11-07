	program proc2moog

	character*5 dum
 	open(unit=2,file="proin",status="unknown")
	open(unit=8,file="proout",status="unknown")

        write(8,*) 'Sc'
	elem = 21.1

	do 500 i=1,13
	read(2,222) dum, wave, chi, rloggf
	write(*,222) dum, wave, chi, rloggf
  222   format(a5,f9.3,f6.3,f7.3)
        write(8,888) '-',wave,elem, chi, rloggf	   
  888   format(a1, f9.3, f11.1, f10.3, f9.3)
  500   continue

	close(unit=2)
	close(unit=8)
	end



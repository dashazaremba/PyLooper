	program mk2mhz
c
c a routine to convert milli Kaysers (cm-1) to MHz
c
	c = 2.997925e+10

	write(6,'(a)')'Enter energy in mK'
	read(5,*)emk

        wavcm = 1000.0/emk
        ehz   = c/wavcm
        emhz = ehz/1.0e+06

        write(6,'(a,f10.4)')'Energy in MHz = ',emhz

	stop
	end

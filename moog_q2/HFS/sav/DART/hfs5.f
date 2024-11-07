	program hfs
c
c A routine to compute the wavelengths of hyperfine components given Jlo, Jup,
c I,  Alo, Blo, Bup, Aup (in MHz).
c
c  The routine has been extended to provide a MOOG format line list (my Moog 
c  input format), and so prompts for central wavelength, id, atom, eplow and
c  total loggf.
c 
c  NOTE!  I assume that EP(low) is the same for all hfs components, which
c  is not strictly true (although it is a very good approx.); to make this
c  improvement I would need to pass elo for all lines to subroutine make_moog
c
c Written by Andrew McWilliam
c
	implicit real (a-z)
        real dw(100),str(100)
	integer nflo,nfup,icount,iflo
        write(6,'(18h enter wavelength )')
	read(5,*)w
        write(6,'(9h enter I )')
	read(5,*)i
	write(6,'(16h enter Jlo, Jup )')
	read(5,*)jlo,jup
	write(6,'(23h enter Alo, Aup in MHz )')
	read(5,*)alo,aup
	write(6,'(23h enter Blo, Bup in MHz )')
	read(5,*)blo,bup
c
c  first compute range of F values in upper and lower state
c
	flomax = i + jlo
	flomin = abs(i - jlo)
	fupmax = i + jup
	fupmin = abs(i - jup)
	nflo = flomax - flomin + 1
	nfup = fupmax - fupmin + 1
c
c  now find the allowed transitions
c
        write(6,'(2x,3hFlo,2x,3hFup,3x,10h Elo(MHz) ,10hEup (MHz) ,
     %           10h E(up-lo) ,10h  Dlam (A),/)')
        sum = 0.0
        icount = 0
        flo = flomin
	do 100 iflo = 1,nflo
c case f -> f-1
           if(flo-1.0.ge.fupmin .and. flo-1.0.le.fupmax) then
              icount = icount + 1
              fup = flo-1.0
              klo =  flo*(flo+1.)-i*(i+1.)-jlo*(jlo+1.) 
              kup =  flo*(flo-1.)-i*(i+1.)-jup*(jup+1.) 
              elo = alo * klo/2.0 + blo * bterm(klo,jlo,i)
              eup = aup * kup/2.0 + bup * bterm(kup,jup,i)
              de = eup-elo
              dw(icount) = - (de/3.0e+04)  *  w**2 /1.0e+08
	      call strength(i,jlo,flo,jup,fup,str(icount))
	      sum = sum + str(icount)
              write(6,'(2f5.1,2x,3f10.2,2f10.4)')flo,fup,elo,eup,de,
     %                                        dw(icount),str(icount)
           endif
c case f -> f
           if(flo.ge.fupmin .and. flo.le.fupmax .and. flo.ne.0.0) then
              icount = icount + 1
              fup = flo
              klo = flo*(flo+1.)-i*(i+1.)-jlo*(jlo+1.) 
              kup = flo*(flo+1.)-i*(i+1.)-jup*(jup+1.) 
              elo = alo * klo/2.0 + blo * bterm(klo,jlo,i)
              eup = aup * kup/2.0 + bup * bterm(kup,jup,i)
              de = eup-elo
              dw(icount) = - (de/3.0e+04)  *  w**2 /1.0e+08
	      call strength(i,jlo,flo,jup,fup,str(icount))
	      sum = sum + str(icount)
              write(6,'(2f5.1,2x,3f10.2,2f10.4)')flo,fup,elo,eup,de,
     %                                        dw(icount),str(icount)
           endif
c case f -> f+1
           if(flo+1.ge.fupmin .and. flo+1.le.fupmax) then
              icount = icount + 1
              fup = flo+1.0
              klo = flo*(flo+1.)-i*(i+1.)-jlo*(jlo+1.) 
              kup = (flo+1.)*(flo+2.)-i*(i+1.)-jup*(jup+1.)
              elo = alo * klo/2.0 + blo * bterm(klo,jlo,i)
              eup = aup * kup/2.0 + bup * bterm(kup,jup,i)
              de = eup-elo
              dw(icount) = - (de/3.0e+04)  *  w**2 /1.0e+08
	      call strength(i,jlo,flo,jup,fup,str(icount))
	      sum = sum + str(icount)
              write(6,'(2f5.1,2x,3f10.2,2f10.4)')flo,fup,elo,eup,de,
     %                                        dw(icount),str(icount)
	   endif
c
           flo = flo + 1.0
 100	continue
        call make_moog(dw,str,icount)
	stop
	end


	real function bterm(k,j,i)
	implicit real (a-z)
	if (i.eq.0.5 .or. j.eq. 0.5) then
           bterm = 0.0
           return
        endif
        bterm = 0.75 * k*(k+1.) - j*(j+1.)*i*(i+1.)
	bterm = bterm / ( 2.0*i*(2.*i-1)*(2.*j-1.) )
	return
	end



	subroutine strength(s,l,j,lup,jup,str)
c
c  a program to compute multiplet line strengths: which should be
c  good for HFS too.
c
c  Note that you'll probably want to get strengths for all lines
c  in a multiplet, especially for hfs....
c
c  equations taken from Condon and Shortly, page 238
c
	real s,l,j,sup,lup,jup,str
	logical switch
c
c  At this point only computing the l = lup transitions
c
	switch = .false.
        if (lup.eq.l) then
           if (jup.eq.j) then
              str = (2*j+1.) * (j*(j+1.)-s*(s+1.)+l*(l+1.))**2 
     %              / (4.*j*(j+1.) )
           elseif (jup.lt.j) then
              str = (j-s+l)*(j+s-l)*(s+l+j+1.)*(s+l+1.-j)/(4.*j)
           elseif (jup.gt.j) then
              str = (j-s+l+1.)*(j+s-l+1.)*(s+l+j+2.)*(s+l-j)
     %             / (4.*(j+1.) )
           endif
c
c  Here consider the l = lup +/- 1 transitions
c
	else
c
c for l = lup - 1 switch lup with l and jup with j
c
	   if (lup.gt.l) then
              switch = .true.
              dum = l
              l   = lup
              lup = dum
              dum = j
              j   = jup
              jup = dum
           endif
c
           if (jup.eq.j) then
              str = (2*j+1.) * (j+l-s)*(j+s-l+1.)*(s+l+1.+j)*(s+l-j)
     %              / (4.*j*(j+1.) )
           elseif (jup.gt.j) then
              str = (j+s-l+1.)*(l+s-j)*(j+s-l+2.)*(l+s-j-1.) 
     %              /(4.*(j+1.))
           elseif (jup.lt.j) then
              str = (j+l-s-1.)*(j+l-s)*(s+l+j+1.)*(s+l+j)
     %              / (4.*j)
           endif
        endif
	if (switch) then
           dum = l
           l   = lup
           lup = dum
           dum = j
           j   = jup
           jup = dum
        endif
c
c       write(6,'(12h Strength = ,f10.4)')str
	return
	end



	subroutine make_moog(dw,str,icount)
c
c This program will take the hfs lists (with Dlam and strength), with user
c inputs of central wavelength, species, EPlow, and loggf(total), to produce
c a MOOG format line list.
c
	character*30 atom*5,id*5
	real dw(100),str(100),totstr,wav0,gflog,eplo,cofm
c
c get sum of strengths
c
        totstr = 0.0
	do 100 i = 1, icount
           totstr = totstr + str(i)
 100	continue
c
c read other line info.
c
	write(6,'(33h enter center of mass wavelength )')
	read(5,*)wav0
	write(6,'(38h enter species id, eg Fe I = 26.0 (a5) )')
	read(5,'(a5)')atom
        write(6,'(37h enter species ascii id in A5 format )')
        read(5,'(a5)')id
	write(6,'(19h enter EP low (eV) )')
	read(5,*)eplo
	write(6,'(21h enter loggf (total) )')
	read(5,*)gflog
c
c  first compute center of mass of computed HFS lines
c
	do 300 i = 1, icount
	   cofm = cofm + dw(i)*str(i)
 300	continue
	cofm = cofm / totstr
c
	do 200 i = 1, icount
           whfs = wav0 + dw(i) - cofm
           gf = 10.0**gflog * str(i)/totstr
	   write(6,50)id,whfs,atom,eplo,alog10(gf)
 200	continue
 50	format(a5,f10.3,5x,a5,f10.3,10x,f10.4)
	return
	end

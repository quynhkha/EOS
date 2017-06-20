function[I2, I3] = checkandshowsimple(II,LL,LLL, areaLL, indexLL)
	
	BL=double(LL);
	for ii=3:length(areaLL)
    	[aa bb]=find(LLL==indexLL(ii));
   	 N=length(aa);
    
   	 for jj=1:N
       		BL(aa(jj),bb(jj))=1;
        
    	end

	end
	BL=logical(BL);




	I2=II;
	I2(BL)=255;
	figure;imshow(I2);

	I3=II;
	I3(~BL)=255;
	figure;imshow(I3);


	
end

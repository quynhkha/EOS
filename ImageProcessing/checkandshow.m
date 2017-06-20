function[I3] = checkandshow(II, L, index)
	LL=L;
	LL(find(LL~=index))=0;
	LL(find(LL==index))=1;
	LL=logical(LL);

	bwxLL= im2bw(LL);
	[LLL,numlL]=bwlabel(~bwxLL,4);
	
	statsLL = regionprops(LLL,'Area');    %????????  area of your crystals
	areaLL = cat(1,statsLL.Area);

	[area_value indexLL]=sort(areaLL,'descend');
	%index = find(area == max(area));        %????????? sort the area


	%%%%%%%%%%%%%%%%%%%%%check and show the photo
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

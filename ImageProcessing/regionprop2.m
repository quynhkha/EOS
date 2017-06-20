function[area] = regionprop(L)
	stats = regionprops(L,'Area'); 
	area = cat(1,stats.Area);
	%index = find(area == max(area));       
end


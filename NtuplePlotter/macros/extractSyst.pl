my $ratio = 0.0;

while (<>){
	if(/final answer: cross section ratio:/){
	#if(/visible cross section ratio:/){
		my $line = <>;
		if ($ARGV eq "ratio_nominal.txt"){
			$ratio = 0 + $line;
			print "nominal: ",$ratio,"\n";
		}
		else {
			print $ARGV,"\n";
			print "this ratio is ",0+$line,"\n";
			print -100*($ratio - $line)/$ratio;
			print "%\n\n";
		}
	}	
}


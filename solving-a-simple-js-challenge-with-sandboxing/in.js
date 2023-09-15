function leastFactor(n) {
 if (isNaN(n) || !isFinite(n)) return NaN;
 if (typeof phantom !== 'undefined') return 'phantom';
 if (typeof module !== 'undefined' && module.exports) return 'node';
 if (n==0) return 0;
 if (n%1 || n*n<2) return 1;
 if (n%2==0) return 2;
 if (n%3==0) return 3;
 if (n%5==0) return 5;
 var m=Math.sqrt(n);
 for (var i=7;i<=m;i+=30) {
  if (n%i==0)      return i;
  if (n%(i+4)==0)  return i+4;
  if (n%(i+6)==0)  return i+6;
  if (n%(i+10)==0) return i+10;
  if (n%(i+12)==0) return i+12;
  if (n%(i+16)==0) return i+16;
  if (n%(i+22)==0) return i+22;
  if (n%(i+24)==0) return i+24;
 }
 return n;
}
function go() {
 var p=2185612406946; var s=2217339572; var n;
if ((s >> 2) & 1)/*
else p-=
*/p+=243959132*/*
p+= */5;/* 120886108*
*/else p-=/*
*13;
*/264526846* 3;/*
else p-=
*/if ((s >> 6) & 1)/* 120886108*
*/p+=/* 120886108*
*/131175911*/* 120886108*
*/9; else p-=/*
p+= */304259433*/*
*13;
*/7;/* 120886108*
*/if ((s >> 13) & 1)/* 120886108*
*/p+= 64425419*/*
else p-=
*/14;/*
*13;
*/else /*
p+= */p-=	9062475*
14;	if ((s >> 10) & 1)	p+=	64514889*/*
*13;
*/13;	else /*
p+= */p-=/*
*13;
*/36440016*	11;/*
p+= */if ((s >> 4) & 1)/*
else p-=
*/p+=
151053309*/* 120886108*
*/7; else  p-=/*
p+= */238417050*
5;	 p-=789963385;
 n=leastFactor(p);
{ document.cookie="KEY="+n+"*"+p/n+":"+s+":3564026287:1;path=/;";
  document.location.reload(true); }
}
//-->]]>

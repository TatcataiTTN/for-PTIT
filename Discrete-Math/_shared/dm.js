/* Thư viện thuật toán Toán rời rạc 1 (thuần JS, chạy được cả trình duyệt lẫn Node để kiểm thử) */
(function(root){
'use strict';
var DM={};
/* ---------- Fraction (BigInt) ---------- */
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){var t=a%b;a=b;b=t}return a}
function Fr(n,d){if(d===undefined)d=1n;n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}var g=gcd(n,d)||1n;this.n=n/g;this.d=d/g}
Fr.prototype.add=function(o){return new Fr(this.n*o.d+o.n*this.d,this.d*o.d)};
Fr.prototype.sub=function(o){return new Fr(this.n*o.d-o.n*this.d,this.d*o.d)};
Fr.prototype.mul=function(o){return new Fr(this.n*o.n,this.d*o.d)};
Fr.prototype.div=function(o){return new Fr(this.n*o.d,this.d*o.n)};
Fr.prototype.isZero=function(){return this.n===0n};
Fr.prototype.toString=function(){return this.d===1n?String(this.n):this.n+'/'+this.d};
Fr.prototype.toNumber=function(){return Number(this.n)/Number(this.d)};
DM.Fr=Fr;
/* ---------- Logic: bảng chân trị ---------- */
DM.parseLogic=function(src){
  var s=src.replace(/\s+/g,'').replace(/<=>|<->|⇔|↔/g,'#').replace(/=>|->|⇒|→/g,'>').replace(/⊕|\^/g,'+').replace(/∧|&&|&|\*/g,'&').replace(/∨|\|\||\|/g,'|').replace(/¬|~|!/g,'~');
  var pos=0,vars=[];
  function peek(){return s[pos]}
  function primary(){
    var c=peek();
    if(c==='('){pos++;var e=iff();if(peek()!==')')throw new Error('Thiếu dấu )');pos++;return e}
    if(c==='~'){pos++;var x=primary();return {t:'not',a:x}}
    if(c==='T'&&!/[a-z]/.test(s[pos+1]||'')){pos++;return {t:'const',v:true}}
    if(c==='F'&&!/[a-z]/.test(s[pos+1]||'')){pos++;return {t:'const',v:false}}
    if(c&&/[a-zA-Z]/.test(c)){pos++;if(vars.indexOf(c)<0)vars.push(c);return {t:'var',n:c}}
    throw new Error('Ký tự không hợp lệ: '+(c||'(hết chuỗi)'));
  }
  function and(){var l=primary();while(peek()==='&'){pos++;l={t:'and',a:l,b:primary()}}return l}
  function or(){var l=and();while(peek()==='|'){pos++;l={t:'or',a:l,b:and()}}return l}
  function xor(){var l=or();while(peek()==='+'){pos++;l={t:'xor',a:l,b:or()}}return l}
  function imp(){var l=xor();if(peek()==='>'){pos++;return {t:'imp',a:l,b:imp()}}return l}
  function iff(){var l=imp();while(peek()==='#'){pos++;l={t:'iff',a:l,b:imp()}}return l}
  var e=iff();if(pos<s.length)throw new Error('Thừa ký tự: '+s.slice(pos));
  return {ast:e,vars:vars.sort()};
};
DM.evalLogic=function(e,env){
  switch(e.t){case 'const':return e.v;case 'var':return !!env[e.n];case 'not':return !DM.evalLogic(e.a,env);
  case 'and':return DM.evalLogic(e.a,env)&&DM.evalLogic(e.b,env);case 'or':return DM.evalLogic(e.a,env)||DM.evalLogic(e.b,env);
  case 'xor':return DM.evalLogic(e.a,env)!==DM.evalLogic(e.b,env);case 'imp':return !DM.evalLogic(e.a,env)||DM.evalLogic(e.b,env);
  case 'iff':return DM.evalLogic(e.a,env)===DM.evalLogic(e.b,env)}
};
DM.truthTable=function(src){
  var p=DM.parseLogic(src),n=p.vars.length;if(n>6)throw new Error('Tối đa 6 biến');
  var rows=[];for(var m=0;m<(1<<n);m++){var env={},vals=[];for(var i=0;i<n;i++){var b=!!(m&(1<<(n-1-i)));env[p.vars[i]]=b;vals.push(b)}rows.push({vals:vals,res:DM.evalLogic(p.ast,env)})}
  var t=rows.every(function(r){return r.res}),f=rows.every(function(r){return !r.res});
  return {vars:p.vars,rows:rows,kind:t?'taut':(f?'contra':'contingent')};
};
DM.equivalent=function(a,b){
  var pa=DM.parseLogic(a),pb=DM.parseLogic(b),vs=Array.from(new Set(pa.vars.concat(pb.vars))).sort(),n=vs.length;if(n>6)throw new Error('Tối đa 6 biến');
  var rows=[],eq=true;for(var m=0;m<(1<<n);m++){var env={},vals=[];for(var i=0;i<n;i++){var v=!!(m&(1<<(n-1-i)));env[vs[i]]=v;vals.push(v)}var ra=DM.evalLogic(pa.ast,env),rb=DM.evalLogic(pb.ast,env);if(ra!==rb)eq=false;rows.push({vals:vals,a:ra,b:rb})}
  return {vars:vs,rows:rows,equivalent:eq};
};
/* ---------- Đếm ---------- */
DM.gcd=function(a,b){return b?DM.gcd(b,a%b):a};DM.lcm=function(a,b){return a/DM.gcd(a,b)*b};
DM.countDivisible=function(a,b,d){return Math.floor(b/d)-Math.floor((a-1)/d)};
DM.inclExclDivisible=function(a,b,ds){
  var k=ds.length,total=0,terms=[];
  for(var m=1;m<(1<<k);m++){var l=1,cnt=0,names=[];for(var i=0;i<k;i++)if(m&(1<<i)){l=DM.lcm(l,ds[i]);cnt++;names.push(ds[i])}
    var c=DM.countDivisible(a,b,l),sgn=cnt%2?1:-1;total+=sgn*c;terms.push({set:names,lcm:l,count:c,sign:sgn})}
  var brute=0;if(b-a<3e6){for(var x=a;x<=b;x++){for(var j=0;j<k;j++)if(x%ds[j]===0){brute++;break}}}else brute=null;
  return {total:total,terms:terms,brute:brute};
};
DM.binom=function(n,k){if(k<0||k>n)return 0n;var r=1n;k=Math.min(k,n-k);for(var i=1;i<=k;i++)r=r*BigInt(n-k+i)/BigInt(i);return r};
DM.boundedSolutions=function(N,lo,hi){
  /* số nghiệm nguyên x_i in [lo_i,hi_i] (hi=null: không chặn) tổng = N; trả về bù trừ + DP */
  var k=lo.length,base=N-lo.reduce(function(s,x){return s+x},0);
  if(base<0)return {count:0n,dp:0n,base:base,terms:[]};
  var cap=hi.map(function(h,i){return h===null?null:h-lo[i]});
  var idx=[];cap.forEach(function(c,i){if(c!==null)idx.push(i)});
  var terms=[],total=0n;
  for(var m=0;m<(1<<idx.length);m++){var s=0,names=[];for(var j=0;j<idx.length;j++)if(m&(1<<j)){s+=cap[idx[j]]+1;names.push(idx[j]+1)}
    var rem=base-s;var c=rem<0?0n:DM.binom(rem+k-1,k-1);var sg=names.length%2?-1n:1n;total+=sg*c;terms.push({vars:names,rem:rem,count:c,sign:Number(sg)})}
  var dp=new Array(N+1).fill(0n);dp[0]=1n;
  for(var i=0;i<k;i++){var nd=new Array(N+1).fill(0n);for(var t=0;t<=N;t++)if(dp[t]!==0n){var top=hi[i]===null?N-t:Math.min(hi[i],N-t);for(var v=lo[i];v<=top;v++)nd[t+v]+=dp[t]}dp=nd}
  return {count:total,dp:dp[N],base:base,terms:terms};
};
DM.pigeon=function(boxes,m){return boxes*(m-1)+1};
/* ---------- Truy hồi tuyến tính thuần nhất hệ số hằng ---------- */
DM.recSequence=function(c,a0,count){var s=a0.map(BigInt),k=c.length;for(var n=k;n<count;n++){var v=0n;for(var i=0;i<k;i++)v+=BigInt(c[i])*s[n-1-i];s.push(v)}return s};
function polyEval(c,r){/* r^k - c1 r^{k-1} - ... - ck */var k=c.length,v=BigInt(1),p=r**BigInt(k);var res=p;for(var i=0;i<k;i++)res-=BigInt(c[i])*(r**BigInt(k-1-i));return res}
DM.integerRoots=function(c){
  var k=c.length,ck=Math.abs(c[k-1]);var roots=[];
  if(ck===0)return null;
  var cands=[];for(var d=1;d<=Math.min(ck,5000);d++)if(ck%d===0){cands.push(d);cands.push(-d)}
  var poly=c.slice();
  /* chia dần để tìm bội */
  function evalP(coefs,r){/* coefs: đa thức đặc trưng dạng [1,-c1,...,-ck] */var v=0n;coefs.forEach(function(x){v=v*BigInt(r)+BigInt(x)});return v}
  var coefs=[1].concat(c.map(function(x){return -x}));
  cands.sort(function(a,b){return Math.abs(a)-Math.abs(b)||a-b});
  var seen={};
  for(var ci=0;ci<cands.length;ci++){var r=cands[ci];
    while(coefs.length>1&&evalP(coefs,r)===0n){roots.push(r);var nc=[coefs[0]];for(var i=1;i<coefs.length-1;i++)nc.push(coefs[i]+r*nc[i-1]);coefs=nc}}
  return {roots:roots,rest:coefs};
};
DM.solveRecurrence=function(c,a0){
  var k=c.length,info=DM.integerRoots(c);
  if(!info||info.rest.length>1)return {ok:false,msg:'Chưa tách hết nghiệm nguyên; chỉ hiển thị dãy số.'};
  var rs=info.roots,groups={};rs.forEach(function(r){groups[r]=(groups[r]||0)+1});
  var basis=[];Object.keys(groups).map(Number).sort(function(a,b){return a-b}).forEach(function(r){for(var j=0;j<groups[r];j++)basis.push({r:r,j:j})});
  /* giải hệ sum alpha_i * n^j * r^n = a_n, n=0..k-1 */
  var M=[];for(var n=0;n<k;n++){var row=basis.map(function(b){return new Fr(BigInt(b.r)**BigInt(n)*BigInt(n===0&&b.j>0?0:n)**BigInt(b.j===0?0:b.j)*(b.j===0?1n:1n))});row.push(new Fr(a0[n]));M.push(row)}
  /* xử lý 0^0 =1 */
  for(var n2=0;n2<k;n2++)for(var q=0;q<k;q++){var b=basis[q];var pw=BigInt(b.r)**BigInt(n2);var nn=(b.j===0)?1n:(BigInt(n2)**BigInt(b.j));if(b.j>0&&n2===0)nn=0n;M[n2][q]=new Fr(pw*nn)}
  for(var col=0;col<k;col++){var piv=col;while(piv<k&&M[piv][col].isZero())piv++;if(piv===k)return {ok:false,msg:'Hệ suy biến'};var tmp=M[col];M[col]=M[piv];M[piv]=tmp;
    var pv=M[col][col];for(var j2=col;j2<=k;j2++)M[col][j2]=M[col][j2].div(pv);
    for(var r2=0;r2<k;r2++)if(r2!==col&&!M[r2][col].isZero()){var f=M[r2][col];for(var j3=col;j3<=k;j3++)M[r2][j3]=M[r2][j3].sub(f.mul(M[col][j3]))}}
  var alphas=basis.map(function(_,i){return M[i][k]});
  var seq=DM.recSequence(c,a0,12),ok=true;
  for(var n3=0;n3<12;n3++){var v=new Fr(0);basis.forEach(function(b,i){var t=alphas[i].mul(new Fr(BigInt(b.r)**BigInt(n3)*(b.j===0?1n:(n3===0?0n:BigInt(n3)**BigInt(b.j)))));v=v.add(t)});if(!(v.d===1n&&v.n===seq[n3]))ok=false}
  return {ok:true,roots:groups,basis:basis,alphas:alphas,verified:ok,seq:seq};
};
DM.formatSolution=function(sol){
  var parts=[];
  sol.basis.forEach(function(b,i){var a=sol.alphas[i];if(a.isZero())return;
    var coef=a.toString();var neg=a.n<0n;var abs=neg?(new Fr(-a.n,a.d)).toString():coef;
    var term=(abs==='1'?'':abs+'·')+(b.j===0?'':(b.j===1?'n·':'n^'+b.j+'·'))+(b.r<0?'('+b.r+')ⁿ':(b.r===1?'':b.r+'ⁿ'));
    if(b.r===1&&abs==='1'&&b.j===0)term='1';else if(b.r===1&&b.j===0)term=abs;else if(b.r===1&&b.j>0)term=(abs==='1'?'':abs+'·')+(b.j===1?'n':'n^'+b.j);
    parts.push((neg?'−':(parts.length?'+':''))+' '+term)});
  var s=parts.join(' ').replace(/^\s*\+\s*/,'').trim();return (s||'0').replace(/^−\s+/,'−');
};
/* ---------- Sinh kế tiếp ---------- */
DM.nextBinary=function(a){var b=a.slice(),i=b.length-1;while(i>=0&&b[i]===1){b[i]=0;i--}if(i<0)return null;b[i]=1;return b};
DM.nextPerm=function(p){var a=p.slice(),i=a.length-2;while(i>=0&&a[i]>a[i+1])i--;if(i<0)return null;var j=a.length-1;while(a[j]<a[i])j--;var t=a[i];a[i]=a[j];a[j]=t;var l=i+1,r=a.length-1;while(l<r){t=a[l];a[l]=a[r];a[r]=t;l++;r--}return a};
DM.nextComb=function(c,n){var k=c.length,a=c.slice(),i=k-1;while(i>=0&&a[i]===n-k+i+1)i--;if(i<0)return null;a[i]++;for(var j=i+1;j<k;j++)a[j]=a[j-1]+1;return a};
DM.nextSteps=function(kind,cur,steps,n){var out=[],x=cur.slice();for(var s=0;s<steps;s++){var nx=kind==='bin'?DM.nextBinary(x):(kind==='perm'?DM.nextPerm(x):DM.nextComb(x,n));if(!nx)break;out.push(nx);x=nx}return out};
/* ---------- Quay lui: dãy sự kiện để hiển thị ---------- */
DM.backtrackTrace=function(mode,n,k){
  var ev=[],res=[],x=[];
  function rec(i,used){
    if(mode==='bin'){for(var v=0;v<=1;v++){x[i]=v;ev.push({t:'try',lvl:i,x:x.slice(0,i+1)});if(i===n-1){res.push(x.slice());ev.push({t:'out',lvl:i,x:x.slice()})}else rec(i+1)}}
    else if(mode==='perm'){for(var v2=1;v2<=n;v2++){if(used[v2]){ev.push({t:'skip',lvl:i,x:x.slice(0,i).concat([v2])});continue}x[i]=v2;used[v2]=true;ev.push({t:'try',lvl:i,x:x.slice(0,i+1)});if(i===n-1){res.push(x.slice());ev.push({t:'out',lvl:i,x:x.slice()})}else rec(i+1,used);used[v2]=false}}
    else{var start=i===0?1:x[i-1]+1;for(var v3=start;v3<=n-k+i+1;v3++){x[i]=v3;ev.push({t:'try',lvl:i,x:x.slice(0,i+1)});if(i===k-1){res.push(x.slice());ev.push({t:'out',lvl:i,x:x.slice()})}else rec(i+1)}}
  }
  rec(0,{});return {events:ev,results:res};
};
/* ---------- Cái túi: duyệt toàn bộ & nhánh cận ---------- */
DM.knapBrute=function(v,w,b){var n=v.length,rows=[],best=-1,bx=null;
  for(var m=0;m<(1<<n);m++){var x=[],W=0,V=0;for(var i=0;i<n;i++){var bit=(m>>(n-1-i))&1;x.push(bit);W+=bit*w[i];V+=bit*v[i]}var ok=W<=b;rows.push({x:x,W:W,V:V,ok:ok});if(ok&&V>best){best=V;bx=x}}
  return {rows:rows,best:best,x:bx};
};
DM.knapBB=function(v,w,b,opt){
  opt=opt||{};var unlimited=!!opt.unlimited;var n=v.length,ord=v.map(function(_,i){return i}).sort(function(i,j){return v[j]/w[j]-v[i]/w[i]||i-j});
  if(opt.keepOrder)ord=v.map(function(_,i){return i});
  var C=ord.map(function(i){return v[i]}),A=ord.map(function(i){return w[i]});
  var fopt=-Infinity,xopt=null,nodes=[],x=new Array(n).fill(0);
  function bound(k,delta,bk){return k<n?delta+C[k]*bk/A[k]:delta}  /* k = số thành phần đã gán */
  var root={id:0,x:[],delta:0,rem:b,g:bound(0,0,b),status:'root'};nodes.push(root);
  function rec(k,delta,bk,parent){
    var t=unlimited?Math.floor(bk/A[k]):Math.min(1,Math.floor(bk/A[k]));
    for(var j=t;j>=0;j--){
      x[k]=j;var d2=delta+C[k]*j,b2=bk-A[k]*j,g=bound(k+1,d2,b2);
      var node={id:nodes.length,x:x.slice(0,k+1),delta:d2,rem:b2,g:g,parent:parent};nodes.push(node);
      if(k===n-1){if(d2>fopt){fopt=d2;xopt=x.slice();node.status='record'}else node.status='leaf'}
      else if(g>fopt){node.status='expand';rec(k+1,d2,b2,node.id)}
      else node.status='pruned';
    }
  }
  if(n>0)rec(0,0,b,0);
  /* trả về theo thứ tự biến gốc */
  var xo=null;if(xopt){xo=new Array(n).fill(0);ord.forEach(function(orig,pos){xo[orig]=xopt[pos]})}
  return {order:ord,C:C,A:A,fopt:fopt,xopt:xo,nodes:nodes};
};
/* ---------- TSP ---------- */
var INF=Infinity;DM.INF=INF;
function reduceM(A,rows,cols){var s=0,i,j,m;
  for(var ri=0;ri<rows.length;ri++){i=rows[ri];m=INF;for(var cj=0;cj<cols.length;cj++)if(A[i][cols[cj]]<m)m=A[i][cols[cj]];if(m>0&&m<INF){s+=m;for(var c1=0;c1<cols.length;c1++)if(A[i][cols[c1]]<INF)A[i][cols[c1]]-=m}}
  for(var cj2=0;cj2<cols.length;cj2++){j=cols[cj2];m=INF;for(var r1=0;r1<rows.length;r1++)if(A[rows[r1]][j]<m)m=A[rows[r1]][j];if(m>0&&m<INF){s+=m;for(var r2=0;r2<rows.length;r2++)if(A[rows[r2]][j]<INF)A[rows[r2]][j]-=m}}
  return s;}
function bestEdge(A,rows,cols){var beta=-1,best=null;
  for(var ri=0;ri<rows.length;ri++)for(var cj=0;cj<cols.length;cj++){var i=rows[ri],j=cols[cj];if(A[i][j]!==0)continue;
    var mr=INF,mc=INF;for(var c2=0;c2<cols.length;c2++)if(cols[c2]!==j&&A[i][cols[c2]]<mr)mr=A[i][cols[c2]];for(var r2=0;r2<rows.length;r2++)if(rows[r2]!==i&&A[rows[r2]][j]<mc)mc=A[rows[r2]][j];
    var t=mr+mc;if(t>beta){beta=t;best=[i,j]}}
  return {edge:best,beta:beta};}
DM.tspBB=function(C){
  var n=C.length,best=INF,bestTour=null,log=[];
  function isTour(edges){var d={};edges.forEach(function(e){d[e[0]]=e[1]});var k=0,cnt=0;do{if(d[k]===undefined)return false;k=d[k];cnt++}while(k!==0&&cnt<=n);return cnt===n&&k===0}
  function snap(A,rows,cols,edges){return {mat:A.map(function(r){return r.slice()}),rows:rows.slice(),cols:cols.slice(),edges:edges.map(function(e){return [e[0]+1,e[1]+1]})}}
  function mk(o,A,rows,cols,edges){var z=snap(A,rows,cols,edges);for(var k in z)o[k]=z[k];return o}
  function node(A,rows,cols,edges,bound,depth,label){
    if(bound>=best){log.push(mk({depth:depth,label:label,bound:bound,status:'cut',best:best},A,rows,cols,edges));return}
    if(rows.length===2){var u=rows[0],v=rows[1],w=cols[0],x=cols[1];var opts=[[[u,w],[v,x]],[[u,x],[v,w]]];
      for(var oi=0;oi<2;oi++){var o=opts[oi];if(A[o[0][0]][o[0][1]]<INF&&A[o[1][0]][o[1][1]]<INF){var all=edges.concat(o);if(isTour(all)){var cost=0;all.forEach(function(e){cost+=C[e[0]][e[1]]});
        log.push(mk({depth:depth,label:label,bound:bound,status:cost<best?'record':'leaf',cost:cost,tour:all,best:best},A,rows,cols,edges));if(cost<best){best=cost;bestTour=all}return}}}
      log.push(mk({depth:depth,label:label,bound:bound,status:'dead'},A,rows,cols,edges));return}
    var be=bestEdge(A,rows,cols);if(!be.edge){log.push(mk({depth:depth,label:label,bound:bound,status:'dead'},A,rows,cols,edges));return}var r=be.edge[0],c=be.edge[1];
    log.push(mk({depth:depth,label:label,bound:bound,status:'branch',edge:[r+1,c+1],beta:be.beta,best:best},A,rows,cols,edges));
    /* nhánh trái: chứa (r,c) */
    var A1=A.map(function(x){return x.slice()}),e1=edges.concat([[r,c]]);
    var inv={};e1.forEach(function(e){inv[e[1]]=e[0]});var d1={};e1.forEach(function(e){d1[e[0]]=e[1]});
    var i1=r;while(inv[i1]!==undefined)i1=inv[i1];var jk=c;while(d1[jk]!==undefined)jk=d1[jk];
    var rows1=rows.filter(function(x){return x!==r}),cols1=cols.filter(function(x){return x!==c});
    if(rows1.indexOf(jk)>=0&&cols1.indexOf(i1)>=0)A1[jk][i1]=INF;
    var b1=bound+reduceM(A1,rows1,cols1);
    node(A1,rows1,cols1,e1,b1,depth+1,'chứa ('+(r+1)+','+(c+1)+')');
    /* nhánh phải: không chứa (r,c) */
    var A2=A.map(function(x){return x.slice()});A2[r][c]=INF;var b2=bound+reduceM(A2,rows,cols);
    node(A2,rows,cols,edges,b2,depth+1,'không chứa ('+(r+1)+','+(c+1)+')');
  }
  var A=C.map(function(row,i){return row.map(function(x,j){return i===j?INF:x})}),rows=[],cols=[];for(var i=0;i<n;i++){rows.push(i);cols.push(i)}
  var root=reduceM(A,rows,cols);log.push({depth:0,label:'gốc',bound:root,status:'root',mat:A.map(function(r){return r.slice()}),rows:rows.slice(),cols:cols.slice(),edges:[]});
  node(A,rows,cols,[],root,0,'gốc (sau rút gọn)');
  var tour=null;if(bestTour){var d={};bestTour.forEach(function(e){d[e[0]]=e[1]});tour=[1];var k=0;for(var s=0;s<n;s++){k=d[k];tour.push(k+1)}}
  return {cost:best,tour:tour,root:root,log:log};
};
DM.tspBrute=function(C){var n=C.length,best=INF,bt=null;var p=[];for(var i=1;i<n;i++)p.push(i);
  (function perm(a,k){if(k===a.length){var cost=C[0][a[0]];for(var j=0;j<a.length-1;j++)cost+=C[a[j]][a[j+1]];cost+=C[a[a.length-1]][0];if(cost<best){best=cost;bt=[1].concat(a.map(function(x){return x+1}),[1])}return}
    for(var j=k;j<a.length;j++){var t=a[k];a[k]=a[j];a[j]=t;perm(a,k+1);t=a[k];a[k]=a[j];a[j]=t}})(p,0);
  return {cost:best,tour:bt};};
DM.tspIdentity=function(C){var n=C.length,s=0,t=[1];for(var i=0;i<n;i++){s+=C[i][(i+1)%n];t.push((i+1)%n+1)}return {cost:s,tour:t}};
/* ---------- Hàm sinh ---------- */
DM.polyMul=function(a,b,trunc){var r=new Array(Math.min(a.length+b.length-1,trunc+1)).fill(0n);for(var i=0;i<a.length;i++)for(var j=0;j<b.length;j++){if(i+j>trunc)continue;r[i+j]+=a[i]*b[j]}return r};
DM.gfSolutions=function(N,lo,hi){var poly=[1n];lo.forEach(function(l,i){var h=hi[i]===null?N:hi[i];var f=new Array(h+1).fill(0n);for(var e=l;e<=h;e++)f[e]=1n;poly=DM.polyMul(poly,f,N)});return poly[N]||0n};
/* ---------- Tập hợp / bit ---------- */
DM.setToBits=function(S,U){return U.map(function(u){return S.indexOf(u)>=0?1:0})};
/* ---------- Độ phức tạp ---------- */
DM.growth=function(n){return {'log₂n':Math.log2(n),'n':n,'n·log₂n':n*Math.log2(n),'n²':n*n,'n³':n*n*n,'2ⁿ':Math.pow(2,n),'n!':(function(){var f=1;for(var i=2;i<=n;i++){f*=i;if(f>1e300)return Infinity}return f})()}};
if(typeof module!=='undefined'&&module.exports)module.exports=DM;else root.DM=DM;
})(typeof window!=='undefined'?window:globalThis);

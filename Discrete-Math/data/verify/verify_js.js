const DM=require('../../_shared/dm.js'); const fs=require('fs');
const C=JSON.parse(fs.readFileSync('cases.json','utf8')); let bad=0,tot=0;
function chk(ok,msg){tot++;if(!ok){bad++;if(bad<6)console.log('MISMATCH',msg)}}
C.incl.forEach(c=>{const r=DM.inclExclDivisible(c.a,c.b,c.ds);chk(r.total===c.ans&&r.brute===c.ans,'incl '+JSON.stringify(c))});
C.intsol.forEach(c=>{const r=DM.boundedSolutions(c.N,c.lo,c.hi);const g=DM.gfSolutions(c.N,c.lo,c.hi);chk(String(r.count)===c.ans&&String(r.dp)===c.ans&&String(g)===c.ans,'intsol '+JSON.stringify(c))});
C.knap.forEach(c=>{const r=DM.knapBB(c.v,c.w,c.b);const bf=DM.knapBrute(c.v,c.w,c.b);chk(r.fopt===c.fopt&&bf.best===c.fopt&&r.nodes.length===c.nodes+0&&r.nodes.filter(x=>x.status==='pruned').length===c.pruned,'knap '+JSON.stringify(c)+' js '+r.fopt+'/'+r.nodes.length)});
C.tsp.forEach(c=>{const r=DM.tspBB(c.C);const bf=DM.tspBrute(c.C);chk(r.cost===c.cost&&bf.cost===c.cost&&r.root===c.root,'tsp '+JSON.stringify(c.C)+' js '+r.cost+' py '+c.cost)});
function nextPerm(a){a=a.slice();let i=a.length-2;while(i>=0&&a[i]>a[i+1])i--;if(i<0)return null;let j=a.length-1;while(a[j]<a[i])j--;[a[i],a[j]]=[a[j],a[i]];const t=a.splice(i+1).reverse();return a.concat(t)}
C.next.forEach(c=>{const a=DM.nextPerm(c.x),b=nextPerm(c.x);chk(JSON.stringify(a)===JSON.stringify(b),'next '+c.x)});
// nghiệm truy hồi kiểm tra bằng dãy
const rec=[[[-14,-49],[3,35]],[[14,-59,70],[-7,-20,-100]],[[2,1,-2],[3,6,0]],[[-1,6],[1,5]],[[6,-9],[1,6]],[[5,-6],[3,8]]];
rec.forEach(([c,a])=>{const s=DM.solveRecurrence(c,a);chk(s.ok&&s.verified,'rec '+c)});
console.log('JS-vs-Python:',tot-bad,'/',tot,'khớp');process.exit(bad?1:0);

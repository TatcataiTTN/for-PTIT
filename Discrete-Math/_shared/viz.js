/* Hoạt ảnh từng bước (bước tới / lui / tự chạy) cho: sinh cấu hình kế tiếp, quay lui, nhánh cận cái túi, nhánh cận người du lịch.
   Mỗi widget: <div class="sim" data-viz="tên"></div>. Dùng DM (dm.js). */
(function(){
'use strict';
var DM=window.DM,NS='http://www.w3.org/2000/svg';
function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!==undefined)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function sv(tag,attrs,txt){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!==undefined)e.textContent=txt;return e}
function nums(s){return s.split(/[\s,;]+/).filter(Boolean).map(Number)}
function f2(x){if(x===Infinity)return '∞';if(Number.isInteger(x))return String(x);return (Math.round(x*100)/100).toString().replace('.',',')}
var COL={root:['#dae8fc','#6c8ebf'],try:['#fff2cc','#d6b656'],out:['#d5e8d4','#82b366'],skip:['#f8cecc','#b85450'],expand:['#fff2cc','#d6b656'],pruned:['#f8cecc','#b85450'],record:['#d5e8d4','#82b366'],leaf:['#eeeeee','#888888'],branch:['#fff2cc','#d6b656'],cut:['#f8cecc','#b85450'],dead:['#eeeeee','#888888']};
/* ---------- bộ điều khiển bước ---------- */
function Stepper(root,frames,draw){
  var i=0,timer=null,speed=900;
  var bar=el('div','row');bar.style.margin='8px 0';
  function btn(t,f,title){var b=el('button','btn alt',t);b.type='button';b.title=title||'';b.onclick=f;bar.appendChild(b);return b}
  var first=btn('⏮',function(){stop();go(0)},'Về đầu'),prev=btn('◀ Lùi',function(){stop();go(i-1)},'Lùi một bước'),next=btn('Tới ▶',function(){stop();go(i+1)},'Tới một bước'),last=btn('⏭',function(){stop();go(frames.length-1)},'Đến cuối');
  var play=btn('▶ Tự chạy',function(){if(timer)stop();else start()});play.classList.remove('alt');
  var sl=el('input');sl.type='range';sl.min=0;sl.max=Math.max(0,frames.length-1);sl.value=0;sl.style.flex='1';sl.style.minWidth='120px';sl.oninput=function(){stop();go(+sl.value)};bar.appendChild(sl);
  var cnt=el('span','viz-count');cnt.style.cssText='font-size:.85rem;color:var(--muted);min-width:70px';bar.appendChild(cnt);
  var spl=el('label',null,'Tốc độ ');var spd=el('select');[['1500','chậm'],['900','vừa'],['400','nhanh']].forEach(function(o){var op=el('option',null,o[1]);op.value=o[0];if(o[0]==='900')op.selected=true;spd.appendChild(op)});spd.onchange=function(){speed=+spd.value;if(timer){stop();start()}};spl.appendChild(spd);bar.appendChild(spl);
  var cap=el('div','callout');cap.style.margin='6px 0';var canvas=el('div');
  root.appendChild(bar);root.appendChild(cap);root.appendChild(canvas);
  function go(n){i=Math.max(0,Math.min(frames.length-1,n));sl.value=i;cnt.textContent='Bước '+(i+1)+'/'+frames.length;first.disabled=prev.disabled=(i===0);next.disabled=last.disabled=(i===frames.length-1);cap.innerHTML=frames[i].caption;draw(canvas,frames[i],i)}
  function start(){if(i>=frames.length-1)go(0);play.textContent='⏸ Dừng';timer=setInterval(function(){if(i>=frames.length-1){stop();return}go(i+1)},speed)}
  function stop(){if(timer){clearInterval(timer);timer=null}play.textContent='▶ Tự chạy'}
  root.tabIndex=0;root.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;if(e.key==='ArrowRight'){stop();go(i+1);e.preventDefault()}if(e.key==='ArrowLeft'){stop();go(i-1);e.preventDefault()}});
  go(0);return {stop:stop,go:go}
}
function frame(root,title,body){root.innerHTML='<div class="simh">🎬 '+title+'</div>'+body}
/* ---------- bố cục cây ---------- */
function layout(nodes){var ch={};nodes.forEach(function(n){ch[n.id]=[]});nodes.forEach(function(n){if(n.parent!==null&&n.parent!==undefined)ch[n.parent].push(n.id)});
  var pos={},leaf=0,maxd=0;(function go(id,d){var c=ch[id];if(d>maxd)maxd=d;if(!c.length){pos[id]={x:leaf++,y:d}}else{c.forEach(function(k){go(k,d+1)});var xs=c.map(function(k){return pos[k].x});pos[id]={x:(Math.min.apply(null,xs)+Math.max.apply(null,xs))/2,y:d}}})(nodes[0].id,0);
  return {pos:pos,leaves:Math.max(leaf,1),depth:maxd+1}}
function drawTree(host,nodes,vis,cur,opt){
  opt=opt||{};var L=layout(nodes),gx=opt.gx||64,gy=opt.gy||58,w=opt.w||26,h=opt.h||26,pad=40;
  var W=pad*2+(L.leaves-1)*gx+w,H=pad*2+(L.depth-1)*gy+h;
  var svg=sv('svg',{viewBox:'0 0 '+W+' '+H,width:Math.min(W,1000),height:H,role:'img'});svg.style.cssText='max-width:100%;height:auto;background:var(--card);border:1px solid var(--border);border-radius:10px';
  function P(id){return {x:pad+w/2+L.pos[id].x*gx,y:pad+h/2+L.pos[id].y*gy}}
  nodes.forEach(function(n){if(!vis[n.id]||n.parent===null||n.parent===undefined)return;var a=P(n.parent),b=P(n.id);svg.appendChild(sv('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,stroke:n.cls==='skip'||n.cls==='pruned'?'#b85450':'#777','stroke-width':1.5,'stroke-dasharray':n.cls==='skip'?'4 3':''}))});
  nodes.forEach(function(n){if(!vis[n.id])return;var p=P(n.id),c=COL[n.cls]||COL.try,isCur=(n.id===cur);
    var g=sv('g',{});
    if(opt.rect){var rw=opt.rw||h*3.2,rh=opt.rh||h*1.5;g.appendChild(sv('rect',{x:p.x-rw/2,y:p.y-rh/2,width:rw,height:rh,rx:7,fill:c[0],stroke:isCur?'#1f4e8c':c[1],'stroke-width':isCur?3.5:1.6}));
      (n.lines||[n.label]).forEach(function(t,k,arr){var tx=sv('text',{x:p.x,y:p.y+(k-(arr.length-1)/2)*13+4,'text-anchor':'middle','font-size':opt.fs||11,fill:'#222'},t);g.appendChild(tx)})}
    else{if(n.cls==='root')g.appendChild(sv('rect',{x:p.x-26,y:p.y-13,width:52,height:26,rx:7,fill:c[0],stroke:isCur?'#1f4e8c':c[1],'stroke-width':isCur?3.5:1.6}));else g.appendChild(sv('circle',{cx:p.x,cy:p.y,r:13,fill:c[0],stroke:isCur?'#1f4e8c':c[1],'stroke-width':isCur?3.5:1.6,'stroke-dasharray':n.cls==='skip'?'3 2':''}));
      g.appendChild(sv('text',{x:p.x,y:p.y+4,'text-anchor':'middle','font-size':12,'font-weight':isCur?'700':'400',fill:'#222'},n.label))}
    svg.appendChild(g)});
  host.innerHTML='';var wrap=el('div');wrap.style.overflow='auto';wrap.appendChild(svg);host.appendChild(wrap)}
/* ====== 1. QUAY LUI ====== */
function buildBT(mode,n,k){
  var nodes=[{id:0,parent:null,label:'Try(1)',cls:'root'}],ev=[],x=[],used={},res=[],len=mode==='comb'?k:n;
  ev.push({id:0,cur:0,cap:'Bắt đầu: gọi <b>Try(1)</b>. Quay lui chọn giá trị cho x[1], rồi x[2], … theo chiều sâu.',x:[],used:{}});
  function nn(par,label,cls){var o={id:nodes.length,parent:par,label:label,cls:cls};nodes.push(o);return o}
  function rec(i,pid){
    var cands=[];if(mode==='bin')cands=[0,1];else if(mode==='perm')for(var v=1;v<=n;v++)cands.push(v);else for(var v2=(i===0?1:x[i-1]+1);v2<=n-k+i+1;v2++)cands.push(v2);
    cands.forEach(function(v){
      if(mode==='perm'&&used[v]){var s=nn(pid,String(v),'skip');ev.push({id:s.id,cur:s.id,cap:'Try('+(i+1)+'): ứng viên <b>'+v+'</b> đã dùng (used['+v+'] = true) ⇒ <span class="no">bỏ qua</span>.',x:x.slice(0,i),used:Object.assign({},used)});return}
      x[i]=v;if(mode==='perm')used[v]=true;
      var nd=nn(pid,String(v),'try');
      ev.push({id:nd.id,cur:nd.id,cap:'Try('+(i+1)+'): thử <b>x['+(i+1)+'] = '+v+'</b>'+(mode==='perm'?', đánh dấu used['+v+'] = true':'')+(mode==='comb'?' (phải &gt; x['+i+'] và ≤ n − k + '+(i+1)+' = '+(n-k+i+1)+')':'')+'.',x:x.slice(0,i+1),used:Object.assign({},used)});
      if(i===len-1){nd.cls='out';res.push(x.slice(0,len));ev.push({id:nd.id,cur:nd.id,cap:'Đủ '+len+' thành phần ⇒ <b class="ok">in nghiệm ('+x.slice(0,len).join(', ')+')</b>.',x:x.slice(0,len),used:Object.assign({},used),out:res.length})}
      else rec(i+1,nd.id);
      ev.push({id:nd.id,cur:pid,cap:'Quay lui: xong nhánh x['+(i+1)+'] = '+v+(mode==='perm'?', <b>hoàn trả</b> used['+v+'] = false':'')+' ⇒ về '+(pid===0?'Try(1)':'Try('+(i+1)+')')+' thử ứng viên kế tiếp.',x:x.slice(0,i),used:(function(){var u=Object.assign({},used);if(mode==='perm')u[v]=false;return u})(),back:true});
      if(mode==='perm')used[v]=false;
    })}
  rec(0,0);
  var frames=[],vis={},cnt=0,outs=[];
  ev.forEach(function(e){vis[e.id]=true;if(e.out)outs.push(e.x.join(' '));frames.push({vis:Object.assign({},vis),cur:e.cur,caption:e.cap,x:e.x,used:e.used,outs:outs.slice(),len:len,mode:mode,n:n})});
  return {nodes:nodes,frames:frames,total:res.length}}
function drawBT(canvas,f,nodes){
  var wrap=el('div');var arr='<div style="margin:6px 0"><b>x[ ]</b> = ';for(var j=0;j<f.len;j++){var v=f.x[j];arr+='<span style="display:inline-block;min-width:26px;padding:2px 6px;margin:0 2px;border:1.5px solid '+(v!==undefined?'#d6b656':'var(--border)')+';background:'+(v!==undefined?'#fff2cc':'var(--code)')+';color:#222;text-align:center;border-radius:5px">'+(v!==undefined?v:'·')+'</span>'}arr+='</div>';
  if(f.mode==='perm'){arr+='<div style="margin:2px 0 6px"><b>used[ ]</b> = ';for(var u=1;u<=f.n;u++){arr+='<span style="display:inline-block;min-width:26px;padding:2px 6px;margin:0 2px;border:1.5px solid var(--border);background:'+(f.used[u]?'#f8cecc':'var(--code)')+';color:#222;text-align:center;border-radius:5px">'+u+':'+(f.used[u]?'T':'F')+'</span>'}arr+='</div>'}
  wrap.innerHTML=arr;var th=el('div');wrap.appendChild(th);canvas.innerHTML='';canvas.appendChild(wrap);drawTree(th,nodes,f.vis,f.cur,{gx:44,gy:52});
  var o=el('div');o.innerHTML='<b>Nghiệm đã in ('+f.outs.length+'):</b> <span class="mono">'+(f.outs.length?esc(f.outs.join(' · ')):'(chưa có)')+'</span>';o.style.margin='8px 0';canvas.appendChild(o)}
/* ====== 2. NHÁNH CẬN CÁI TÚI ====== */
function buildKnap(c,a,b,unl){
  var r=DM.knapBB(c,a,b,{unlimited:unl}),n=c.length,nodes=[],frames=[],fopt=-Infinity,vis={};
  var LIM=70;if(r.nodes.length>LIM)return {error:'Cây có '+r.nodes.length+' nút, quá lớn để vẽ (tối đa '+LIM+'). Giảm số vật hoặc sức chứa.'};
  r.nodes.forEach(function(nd,j){var lines=j===0?['gốc','g='+f2(nd.g)]:['('+nd.x.join(',')+')','δ='+nd.delta+' w='+nd.rem,'g='+f2(nd.g)];nodes.push({id:j,parent:j===0?null:nd.parent,label:lines[0],lines:lines,cls:'try'})});
  var ord='thứ tự xét (c/a giảm dần): '+r.order.map(function(i){return 'x'+(i+1)+' ('+c[i]+'/'+a[i]+'='+f2(c[i]/a[i])+')'}).join(', ');
  r.nodes.forEach(function(nd,j){
    vis[j]=true;var before=fopt,cap='',k=nd.x.length;
    var gtxt=k<n?'g = δ + c<sub>'+(k+1)+'</sub>·w/a<sub>'+(k+1)+'</sub> = '+nd.delta+' + '+r.C[k]+'·'+nd.rem+'/'+r.A[k]+' = <b>'+f2(nd.g)+'</b>':'(đã gán đủ biến) δ = <b>'+nd.delta+'</b>';
    if(j===0)cap='<b>Gốc</b>: chưa gán biến nào, FOPT = −∞. '+gtxt+'. ('+ord+')';
    else{var xs='x'+(k)+' = '+nd.x[k-1];cap='Nút <b>('+nd.x.join(', ')+')</b> (vừa gán '+xs+'): δ = '+nd.delta+', w (còn lại) = '+nd.rem+'. '+gtxt+'. FOPT hiện tại = '+(before===-Infinity?'−∞':before)+'. ';
      if(nd.status==='expand')cap+='⇒ g &gt; FOPT nên <b>mở rộng</b> nhánh này.';
      else if(nd.status==='pruned')cap+='⇒ g ≤ FOPT nên <b class="no">cắt nhánh</b> (không thể có phương án tốt hơn kỷ lục).';
      else if(nd.status==='record'){cap+='⇒ lá, δ = '+nd.delta+' &gt; FOPT ⇒ <b class="ok">kỷ lục mới: FOPT = '+nd.delta+'</b>.';fopt=nd.delta}
      else cap+='⇒ lá, δ = '+nd.delta+' ≤ FOPT, không cải thiện.'}
    var cls=nd.status==='root'?'root':nd.status;nodes[j].cls=cls;
    frames.push({vis:Object.assign({},vis),cur:j,caption:cap,fopt:fopt,stat:cls})});
  /* khung kết quả */
  frames.push({vis:Object.assign({},vis),cur:-1,caption:'<b>Kết thúc</b>: f* = <b>'+r.fopt+'</b>, x* = <b>('+r.xopt.join(', ')+')</b> (theo thứ tự biến gốc x₁…x'+(n)+').',fopt:fopt,stat:'end'});
  return {nodes:nodes,frames:frames,res:r}}
function drawKnap(canvas,f,nodes,res,c,a,b){
  /* node class tại thời điểm hiển thị: nút tương lai chưa vẽ */
  canvas.innerHTML='';var top=el('div');top.innerHTML='<b>FOPT</b> = '+(f.fopt===-Infinity?'−∞':f.fopt)+' &nbsp;|&nbsp; Sắp theo c/a: '+res.order.map(function(i){return 'x'+(i+1)+'('+c[i]+'/'+a[i]+')'}).join(' ≥ ')+' &nbsp;|&nbsp; túi b = '+b;top.style.margin='6px 0';canvas.appendChild(top);
  var th=el('div');canvas.appendChild(th);
  var nn=nodes.map(function(nd,j){var cl=nd.cls;if(!f.vis[j])return nd;/* nút xét sau FOPT cập nhật giữ màu cuối */return nd});
  drawTree(th,nn,f.vis,f.cur,{gx:112,gy:84,rect:true,rw:98,rh:46,w:98,h:46,fs:10.5})}
/* ====== 3. NHÁNH CẬN NGƯỜI DU LỊCH ====== */
function buildTSP(C){
  var r=DM.tspBB(C),log=r.log.slice();if(log.length>1&&log[1].depth===0){var f0=log[1];f0.status0=f0.status;log=[Object.assign({},f0,{status:'root'})].concat(log.slice(2));log[0].edge=f0.edge;log[0].beta=f0.beta}if(log.length>60)return {error:'Cây có '+log.length+' nút, quá lớn (tối đa 60).'};
  var nodes=[],stack=[],frames=[],vis={},best=Infinity;
  log.forEach(function(e,j){var par=null;if(j>0){par=stack[e.depth-1]}stack[e.depth]=j;
    var lines=[j===0?'gốc':e.label.replace('chứa','chứa').replace('không chứa','không chứa'),'cận '+f2(e.bound)];if(e.status==='record'||e.status==='leaf')lines.push('chi phí '+e.cost);
    nodes.push({id:j,parent:par,label:lines[0],lines:lines,cls:e.status==='root'?'root':e.status})});
  log.forEach(function(e,j){vis[j]=true;var cap='';
    if(e.status==='root')cap='<b>Gốc</b>: rút gọn ma trận (trừ min mỗi dòng rồi mỗi cột) ⇒ cận dưới = <b>'+f2(e.bound)+'</b>.'+(e.edge?' Chọn số 0 tại <b>('+e.edge.join(', ')+')</b> có β = min dòng + min cột = <b>'+e.beta+'</b> làm cạnh phân nhánh.':'');
    else if(e.status==='branch')cap='Nút <b>['+e.label+']</b>: cận dưới = '+f2(e.bound)+'. Chọn số 0 tại <b>('+e.edge.join(', ')+')</b> có β = min dòng + min cột = <b>'+e.beta+'</b> làm cạnh phân nhánh.'+(j>0?' ':'');
    else if(e.status==='cut')cap='Nút <b>['+e.label+']</b>: cận dưới = '+f2(e.bound)+' ≥ kỷ lục '+f2(e.best)+' ⇒ <b class="no">cắt nhánh</b>.';
    else if(e.status==='record'){cap='Nút <b>['+e.label+']</b>: ma trận còn 2×2 ⇒ kết nạp hai cạnh cuối, được hành trình đầy đủ chi phí <b>'+e.cost+'</b> &lt; kỷ lục ⇒ <b class="ok">cập nhật kỷ lục</b>.';best=e.cost}
    else if(e.status==='leaf')cap='Nút <b>['+e.label+']</b>: được hành trình chi phí '+e.cost+' nhưng không tốt hơn kỷ lục '+f2(e.best)+'.';
    else cap='Nút <b>['+e.label+']</b>: không tạo được hành trình hợp lệ.';
    frames.push({vis:Object.assign({},vis),cur:j,caption:cap,e:e,best:best,cs:C.length})});
  frames.push({vis:Object.assign({},vis),cur:-1,caption:'<b>Kết thúc</b>: hành trình tối ưu <b>'+r.tour.join('→')+'</b>, chi phí <b>'+r.cost+'</b>.',e:null,best:best,cs:C.length});
  return {nodes:nodes,frames:frames,res:r}}
function matHTML(e){if(!e)return '';var h='<table class="t" style="font-size:.85rem"><tr><th></th>'+e.cols.map(function(c){return '<th>'+(c+1)+'</th>'}).join('')+'</tr>';
  e.rows.forEach(function(r){h+='<tr><th>'+(r+1)+'</th>';e.cols.forEach(function(c){var v=e.mat[r][c],hl=e.edge&&e.edge[0]===r+1&&e.edge[1]===c+1;h+='<td style="'+(hl?'background:#fff2cc;color:#222;font-weight:800;outline:2px solid #d6b656':(v===0?'background:var(--goodbg)':''))+'">'+(v===Infinity?'∞':v)+'</td>'});h+='</tr>'});return h+'</table>'}
function drawTSP(canvas,f,nodes){canvas.innerHTML='';var row=el('div');row.style.cssText='display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start';var l=el('div');l.style.cssText='flex:2;min-width:300px';var r=el('div');r.style.cssText='flex:1;min-width:200px';
  var ed=f.e&&f.e.edges&&f.e.edges.length?'Cạnh đã chọn: '+f.e.edges.map(function(x){return '('+x.join(',')+')'}).join(' '):'';
  r.innerHTML='<b>Ma trận tại nút đang xét</b>'+(f.e?'<div style="font-size:.8rem;color:var(--muted)">Hàng/cột còn lại; ô 0 tô xanh'+(f.e.edge?'; ô chọn phân nhánh tô vàng':'')+'</div>'+matHTML(f.e)+'<div style="font-size:.85rem;margin-top:4px">'+ed+'</div>':'<p>(kết thúc)</p>')+'<div style="margin-top:6px"><b>Kỷ lục</b> = '+(f.best===Infinity?'∞ (chưa có)':f.best)+'</div>';
  row.appendChild(l);row.appendChild(r);canvas.appendChild(row);drawTree(l,nodes,f.vis,f.cur,{gx:132,gy:76,rect:true,rw:124,rh:42,w:124,h:42,fs:10.5})}
/* ====== 4. SINH CẤU HÌNH KẾ TIẾP ====== */
function cells(arr,cls){return '<div style="margin:4px 0">'+arr.map(function(v,i){var c=cls&&cls[i]||{};return '<span style="display:inline-block;min-width:30px;padding:4px 8px;margin:0 3px;text-align:center;border:2px solid '+(c.b||'var(--border)')+';background:'+(c.bg||'var(--code)')+';color:#222;border-radius:6px;font-weight:'+(c.bold?800:500)+'">'+v+(c.tag?'<sub style="font-size:.6em;color:#b3122f"> '+c.tag+'</sub>':'')+'</span>'}).join('')+'</div>'}
var Y={b:'#d6b656',bg:'#fff2cc'},R_={b:'#b85450',bg:'#f8cecc'},G={b:'#82b366',bg:'#d5e8d4'},B_={b:'#6c8ebf',bg:'#dae8fc'},GR={b:'#999',bg:'#eee'};
function buildGen(kind,x,steps,n){
  var frames=[],cur=x.slice(),hist=[x.slice()];
  for(var s=0;s<steps;s++){
    if(kind==='perm'){var a=cur.slice(),i=a.length-2;while(i>=0&&a[i]>a[i+1])i--;
      if(i<0){frames.push({caption:'<b>'+cur.join(' ')+'</b> đã là hoán vị cuối cùng (giảm dần hoàn toàn) ⇒ dừng.',row:cells(cur,cur.map(function(){return R_})),hist:hist.slice()});break}
      var j=a.length-1;while(a[j]<a[i])j--;
      var c1={};for(var q=i+1;q<a.length;q++)c1[q]=GR;c1[i]=Object.assign({tag:'i'},Y,{bold:1});
      frames.push({caption:'<b>Bước '+(s+1)+'</b>: tìm i lớn nhất sao cho p[i] &lt; p[i+1]: i = '+(i+1)+' (giá trị '+a[i]+'). Đoạn sau i (xám) đang giảm dần.',row:cells(a,a.map(function(_,t){return c1[t]})),hist:hist.slice()});
      var c2={};for(var q2=i+1;q2<a.length;q2++)c2[q2]=GR;c2[i]=Object.assign({tag:'i'},Y,{bold:1});c2[j]=Object.assign({tag:'j'},B_,{bold:1});
      frames.push({caption:'Tìm j lớn nhất sao cho p[j] &gt; p[i] = '+a[i]+': j = '+(j+1)+' (giá trị '+a[j]+').',row:cells(a,a.map(function(_,t){return c2[t]})),hist:hist.slice()});
      var b=a.slice(),t0=b[i];b[i]=b[j];b[j]=t0;var c3={};c3[i]=Object.assign({},Y,{bold:1});c3[j]=Object.assign({},B_,{bold:1});for(var q3=i+1;q3<b.length;q3++)if(q3!==j)c3[q3]=GR;
      frames.push({caption:'Đổi chỗ p[i] và p[j]: '+a[i]+' ↔ '+a[j]+'.',row:cells(b,b.map(function(_,t){return c3[t]})),hist:hist.slice()});
      var d=b.slice(0,i+1).concat(b.slice(i+1).reverse());var c4={};for(var q4=0;q4<d.length;q4++)c4[q4]=q4>i?G:{};
      cur=d;hist.push(d.slice());frames.push({caption:'Đảo ngược đoạn p[i+1..n] ⇒ hoán vị kế tiếp: <b>'+d.join(' ')+'</b>.',row:cells(d,d.map(function(_,t){return c4[t]})),hist:hist.slice()})}
    else if(kind==='comb'){var k=cur.length,i2=k-1;while(i2>=0&&cur[i2]===n-k+i2+1)i2--;
      if(i2<0){frames.push({caption:'<b>'+cur.join(' ')+'</b> là tổ hợp cuối (n − k + 1, …, n) ⇒ dừng.',row:cells(cur,cur.map(function(){return R_})),hist:hist.slice()});break}
      var cc={};for(var q5=i2+1;q5<k;q5++)cc[q5]=GR;cc[i2]=Object.assign({tag:'i'},Y,{bold:1});
      frames.push({caption:'<b>Bước '+(s+1)+'</b>: tìm i lớn nhất sao cho c[i] ≠ n − k + i (giá trị tối đa của vị trí đó). Ở đây i = '+(i2+1)+': c['+(i2+1)+'] = '+cur[i2]+' &lt; '+(n-k+i2+1)+'. Các phần tử sau i (xám) đã ở giá trị tối đa.',row:cells(cur,cur.map(function(_,t){return cc[t]})),hist:hist.slice()});
      var e2=cur.slice();e2[i2]++;var c6={};c6[i2]=Object.assign({},B_,{bold:1});frames.push({caption:'Tăng c['+(i2+1)+'] thêm 1: '+cur[i2]+' → '+e2[i2]+'.',row:cells(e2,e2.map(function(_,t){return c6[t]})),hist:hist.slice()});
      var f3=e2.slice();for(var q6=i2+1;q6<k;q6++)f3[q6]=f3[q6-1]+1;var c7={};for(var q7=i2+1;q7<k;q7++)c7[q7]=G;
      cur=f3;hist.push(f3.slice());frames.push({caption:'Đặt c[j] = c[j−1] + 1 cho mọi j &gt; i (các phần tử sau nhỏ nhất có thể) ⇒ tổ hợp kế tiếp: <b>'+f3.join(' ')+'</b>.',row:cells(f3,f3.map(function(_,t){return c7[t]})),hist:hist.slice()})}
    else{var m=cur.length-1;while(m>=0&&cur[m]===1)m--;
      if(m<0){frames.push({caption:'<b>'+cur.join('')+'</b> toàn bit 1 là xâu cuối ⇒ dừng.',row:cells(cur,cur.map(function(){return R_})),hist:hist.slice()});break}
      var cb={};for(var q8=m+1;q8<cur.length;q8++)cb[q8]=GR;cb[m]=Object.assign({tag:'k'},Y,{bold:1});
      frames.push({caption:'<b>Bước '+(s+1)+'</b>: tìm bit 0 phải nhất: k = '+(m+1)+'. Các bit sau k (xám) đều là 1.',row:cells(cur,cur.map(function(_,t){return cb[t]})),hist:hist.slice()});
      var nb=cur.slice();nb[m]=1;for(var q9=m+1;q9<nb.length;q9++)nb[q9]=0;var cd={};cd[m]=Object.assign({},B_,{bold:1});for(var q10=m+1;q10<nb.length;q10++)cd[q10]=G;
      cur=nb;hist.push(nb.slice());frames.push({caption:'Đổi x[k] thành 1 và mọi bit sau k thành 0 ⇒ xâu kế tiếp <b>'+nb.join('')+'</b> (chính là cộng 1 nhị phân: '+parseInt(nb.join(''),2)+').',row:cells(nb,nb.map(function(_,t){return cd[t]})),hist:hist.slice()})}
  }
  return frames}
function drawGen(canvas,f){canvas.innerHTML='';canvas.appendChild(el('div',null,f.row));var h=el('div');h.style.marginTop='8px';h.innerHTML='<b>Các cấu hình đã sinh:</b> <span class="mono">'+f.hist.map(function(a){return esc(a.join(' '))}).join(' → ')+'</span>';canvas.appendChild(h)}
/* ====== đăng ký widget ====== */
var W={};
W.gen=function(root){
  frame(root,'Sinh cấu hình kế tiếp: từng bước','<div class="row"><label>Loại: <select id="t"><option value="perm">Hoán vị</option><option value="comb">Tổ hợp chập k của {1..n}</option><option value="bin">Xâu nhị phân</option></select></label><label>Cấu hình hiện tại: <input id="x" size="26" value="5 6 8 3 9 7 4 2 1"></label><label>n = <input id="n" type="number" value="9" style="width:55px"></label><label>Số lần sinh: <input id="s" type="number" value="2" min="1" max="6" style="width:50px"></label><button class="btn" id="go">Dựng hoạt ảnh</button></div><div class="msg"></div><div class="stage"></div>');
  var T=root.querySelector('#t');T.onchange=function(){var t=T.value;root.querySelector('#x').value=t==='perm'?'5 6 8 3 9 7 4 2 1':(t==='comb'?'2 3 6 8 9':'1 0 1 1 0 0 1 1 1');root.querySelector('#n').value=t==='bin'?'':9;run()};
  function run(){var msg=root.querySelector('.msg'),st=root.querySelector('.stage');msg.innerHTML='';st.innerHTML='';
    try{var t=T.value,x=nums(root.querySelector('#x').value),n=+root.querySelector('#n').value,s=+root.querySelector('#s').value;
      if(t==='perm'){var so=x.slice().sort(function(a,b){return a-b});for(var i=0;i<so.length;i++)if(so[i]!==i+1)throw new Error('Hoán vị phải là hoán vị của 1..m')}
      if(t==='comb')for(var j=0;j<x.length;j++)if(x[j]<1||x[j]>n||(j&&x[j]<=x[j-1]))throw new Error('Tổ hợp phải tăng ngặt trong 1..n');
      if(t==='bin')x.forEach(function(b){if(b!==0&&b!==1)throw new Error('Xâu nhị phân chỉ gồm 0/1')});
      var fr=buildGen(t,x,s,n);Stepper(st,fr,drawGen)}catch(e){msg.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  root.querySelector('#go').onclick=run;run()};
W.bt=function(root){
  frame(root,'Quay lui: duyệt cây từng bước','<div class="row"><label>Bài toán: <select id="m"><option value="bin">Xâu nhị phân độ dài n</option><option value="perm">Hoán vị của 1..n</option><option value="comb">Tổ hợp chập k của 1..n</option></select></label><label>n = <input id="n" type="number" value="3" min="1" max="5" style="width:50px"></label><label>k = <input id="k" type="number" value="2" min="1" max="4" style="width:50px"></label><button class="btn" id="go">Dựng hoạt ảnh</button></div><div class="msg"></div><div class="stage"></div>');
  function run(){var msg=root.querySelector('.msg'),st=root.querySelector('.stage');msg.innerHTML='';st.innerHTML='';var m=root.querySelector('#m').value,n=+root.querySelector('#n').value,k=+root.querySelector('#k').value;
    if(m==='bin'&&n>4){msg.innerHTML='<p class="no">Xâu nhị phân: n ≤ 4 để cây vẫn đọc được.</p>';return}if(m==='perm'&&n>4){msg.innerHTML='<p class="no">Hoán vị: n ≤ 4.</p>';return}if(m==='comb'&&(k>n||n>6)){msg.innerHTML='<p class="no">Tổ hợp: k ≤ n ≤ 6.</p>';return}
    var b=buildBT(m,n,k);Stepper(st,b.frames,function(c,f){drawBT(c,f,b.nodes)})}
  root.querySelector('#go').onclick=run;run()};
W.knap=function(root){
  frame(root,'Nhánh cận cái túi: duyệt cây từng bước','<div class="row"><label>Giá trị c: <input id="v" value="10 5 3 6" size="12"></label><label>Trọng lượng a: <input id="w" value="5 3 2 4" size="12"></label><label>Sức chứa b: <input id="b" type="number" value="8" style="width:60px"></label><label><input id="u" type="checkbox" checked> số lượng không hạn chế (ví dụ giáo trình)</label><button class="btn" id="go">Dựng hoạt ảnh</button></div><div class="row"><button class="btn alt" id="e1">Ví dụ giáo trình</button><button class="btn alt" id="e2">Đề 2023–24 đề 01</button><button class="btn alt" id="e3">Đề 2023–24 đề 02</button></div><div class="msg"></div><div class="stage"></div>');
  function set(v,w,b,u){root.querySelector('#v').value=v;root.querySelector('#w').value=w;root.querySelector('#b').value=b;root.querySelector('#u').checked=u;run()}
  root.querySelector('#e1').onclick=function(){set('10 5 3 6','5 3 2 4',8,true)};root.querySelector('#e2').onclick=function(){set('3 5 7 4','2 4 3 2',9,false)};root.querySelector('#e3').onclick=function(){set('6 5 3 1','4 4 2 1',9,false)};
  function run(){var msg=root.querySelector('.msg'),st=root.querySelector('.stage');msg.innerHTML='';st.innerHTML='';
    try{var c=nums(root.querySelector('#v').value),a=nums(root.querySelector('#w').value),b=+root.querySelector('#b').value,u=root.querySelector('#u').checked;if(c.length!==a.length||c.length<1||c.length>7)throw new Error('c và a phải cùng độ dài (1–7).');if(a.some(function(x){return !(x>0)}))throw new Error('Trọng lượng phải dương.');
      var k=buildKnap(c,a,b,u);if(k.error)throw new Error(k.error);Stepper(st,k.frames,function(cv,f){drawKnap(cv,f,k.nodes,k.res,c,a,b)})}catch(e){msg.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  root.querySelector('#go').onclick=run;run()};
W.tsp=function(root){
  frame(root,'Người du lịch: nhánh cận từng bước','<div class="row"><small>Ma trận chi phí n×n (3 ≤ n ≤ 6), mỗi dòng một hàng; đường chéo bị coi là ∞.</small></div><textarea id="m" rows="6" style="font-family:monospace">0 3 93 13 33 9\n4 0 77 42 21 16\n45 17 0 36 16 28\n39 90 80 0 56 7\n28 46 88 33 0 25\n3 88 18 46 92 0</textarea><div class="row"><button class="btn" id="go">Dựng hoạt ảnh</button> <button class="btn alt" id="e1">Ví dụ giáo trình (n = 6)</button> <button class="btn alt" id="e2">Ngân hàng 4.4</button></div><div class="msg"></div><div class="stage"></div>');
  root.querySelector('#e1').onclick=function(){root.querySelector('#m').value='0 3 93 13 33 9\n4 0 77 42 21 16\n45 17 0 36 16 28\n39 90 80 0 56 7\n28 46 88 33 0 25\n3 88 18 46 92 0';run()};
  root.querySelector('#e2').onclick=function(){root.querySelector('#m').value='0 31 15 23 10 17\n16 0 24 7 12 12\n34 3 0 25 54 25\n15 20 33 0 50 40\n16 10 32 3 0 23\n18 20 13 28 21 0';run()};
  function run(){var msg=root.querySelector('.msg'),st=root.querySelector('.stage');msg.innerHTML='';st.innerHTML='';
    try{var C=root.querySelector('#m').value.trim().split(/\n+/).map(nums),n=C.length;if(n<3||n>6||C.some(function(r){return r.length!==n}))throw new Error('Ma trận phải vuông, 3 ≤ n ≤ 6.');
      var t=buildTSP(C);if(t.error)throw new Error(t.error);Stepper(st,t.frames,function(cv,f){drawTSP(cv,f,t.nodes)})}catch(e){msg.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  root.querySelector('#go').onclick=run;run()};
document.querySelectorAll('.sim[data-viz]').forEach(function(root){var f=W[root.getAttribute('data-viz')];if(f)f(root)});
})();

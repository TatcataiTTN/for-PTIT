/* Bộ mô phỏng tương tác (dùng dm.js). Mỗi widget: <div class="sim" data-sim="tên"></div> */
(function(){
'use strict';
var DM=window.DM;
function el(tag,attrs,html){var e=document.createElement(tag);if(attrs)for(var k in attrs)e.setAttribute(k,attrs[k]);if(html!==undefined)e.innerHTML=html;return e}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function frame(root,title,body){root.innerHTML='<div class="simh">🧪 '+title+'</div>'+body}
function $(root,sel){return root.querySelector(sel)}
function nums(s){return s.split(/[\s,;]+/).filter(Boolean).map(Number)}
function fnum(x){if(x===Infinity)return '∞';if(Number.isInteger(x))return String(x);return (Math.round(x*100)/100).toString()}
function tbl(head,rows,cls){return '<table class="t '+(cls||'')+'"><tr>'+head.map(function(h){return '<th>'+h+'</th>'}).join('')+'</tr>'+rows.map(function(r){var c='';if(r&&r.cls){c=' class="'+r.cls+'"';r=r.cells}return '<tr'+c+'>'+r.map(function(x){return '<td>'+x+'</td>'}).join('')+'</tr>'}).join('')+'</table>'}
var W={};
W.truth=function(root){
  frame(root,'Bảng chân trị & kiểm tra tương đương','<div class="row"><label>Công thức 1: <input id="f1" size="34" value="(p > q) & (q > r) > (p > r)"></label></div><div class="row"><label>Công thức 2 (tùy chọn, để kiểm tra tương đương): <input id="f2" size="30" value=""></label></div><div class="row"><small>Ký hiệu: ~ hoặc ! là ¬; & là ∧; | là ∨; > hoặc => là ⇒; # hoặc <=> là ⇔; + là ⊕. Cũng nhận ∧ ∨ ¬ ⇒ ⇔ ⊕. Tối đa 6 biến.</small></div><button class="btn" id="go">Lập bảng</button><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var a=$(root,'#f1').value,b=$(root,'#f2').value.trim();
    if(b){var r=DM.equivalent(a,b);out.innerHTML=tbl(r.vars.concat(['F₁','F₂']),r.rows.map(function(x){return {cls:x.a!==x.b?'pruned':'',cells:x.vals.map(function(v){return v?'Đ':'S'}).concat([x.a?'Đ':'S',x.b?'Đ':'S'])}}))+'<p class="'+(r.equivalent?'ok':'no')+'">'+(r.equivalent?'F₁ ≡ F₂ (tương đương logic)':'F₁ KHÔNG tương đương F₂ (các dòng tô đỏ là phản ví dụ)')+'</p>'}
    else{var t=DM.truthTable(a);out.innerHTML=tbl(t.vars.concat(['Kết quả']),t.rows.map(function(x){return {cls:x.res?'hl':'',cells:x.vals.map(function(v){return v?'Đ':'S'}).concat([x.res?'Đ':'S'])}}))+'<p><b>Loại:</b> '+({taut:'<span class="ok">hằng đúng (tautology)</span>',contra:'<span class="no">mâu thuẫn (hằng sai)</span>',contingent:'thỏa được nhưng không hằng đúng'}[t.kind])+'. Số dòng Đúng: '+t.rows.filter(function(x){return x.res}).length+'/'+t.rows.length+'.</p>'}}
    catch(e){out.innerHTML='<p class="no">Lỗi: '+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.incl=function(root){
  frame(root,'Nguyên lý bù trừ: đếm số chia hết','<div class="row"><label>Từ <input id="a" type="number" value="542" style="width:80px"> đến <input id="b" type="number" value="7761" style="width:80px"></label><label>Các số chia (cách nhau bởi dấu cách): <input id="ds" value="3 7 14" size="14"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){var a=+$(root,'#a').value,b=+$(root,'#b').value,ds=nums($(root,'#ds').value).filter(function(x){return x>0});if(ds.length<1||ds.length>5||b<a){$(root,'.out').innerHTML='<p class="no">Nhập 1–5 số chia dương và đoạn hợp lệ.</p>';return}
    var r=DM.inclExclDivisible(a,b,ds);
    $(root,'.out').innerHTML=tbl(['Tập số chia','BCNN','Số bội trong đoạn','Dấu'],r.terms.map(function(t){return [t.set.join(', '),t.lcm,t.count,t.sign>0?'+':'−']}))+'<p><b>Tổng bù trừ = '+r.total+'</b>'+(r.brute!==null?' &nbsp;|&nbsp; Kiểm tra bằng đếm trực tiếp: <b>'+r.brute+'</b> '+(r.brute===r.total?'<span class="ok">✓ khớp</span>':'<span class="no">✗ lệch</span>'):'')+'.</p><p>Số KHÔNG chia hết cho số nào: '+((b-a+1)-r.total)+'.</p>'}
  $(root,'#go').onclick=run;run();
};
W.intsol=function(root){
  frame(root,'Đếm nghiệm nguyên có cận (bù trừ + quy hoạch động + hàm sinh)','<div class="row"><label>Số biến k = <input id="k" type="number" value="6" min="2" max="8" style="width:50px"></label><label>Tổng N = <input id="n" type="number" value="41" style="width:60px"></label></div><div class="row"><small>Nhập cận cho từng biến dạng <code>lo-hi</code> (hi có thể để trống = không chặn), mỗi biến một mục cách nhau bởi dấu cách. Ví dụ: <code>4-7 7- 3-9 0- 0- 0-</code></small></div><div class="row"><input id="bd" size="40" value="4-7 7- 3-9 0- 0- 0-"> <button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var k=+$(root,'#k').value,N=+$(root,'#n').value,parts=$(root,'#bd').value.trim().split(/\s+/);if(parts.length!==k)throw new Error('Cần đúng '+k+' mục cận.');
    var lo=[],hi=[];parts.forEach(function(p){var m=p.match(/^(\d+)-(\d*)$/);if(!m)throw new Error('Cận sai định dạng: '+p);lo.push(+m[1]);hi.push(m[2]===''?null:+m[2])});
    var r=DM.boundedSolutions(N,lo,hi),g=DM.gfSolutions(N,lo,hi);
    var rows=r.terms.map(function(t){return [t.vars.length?('vượt cận biến '+t.vars.join(', ')):'không cận trên',t.rem<0?'—':('C('+(t.rem+k-1)+','+(k-1)+')'),String(t.count),t.sign>0?'+':'−']});
    out.innerHTML='<p>Đổi biến yᵢ = xᵢ − loᵢ: tổng còn <b>'+r.base+'</b> trên '+k+' biến.</p>'+tbl(['Trường hợp (bù trừ)','Tổ hợp','Giá trị','Dấu'],rows)+'<p><b>Kết quả bù trừ = '+r.count+'</b> | quy hoạch động = '+r.dp+' | hệ số hàm sinh = '+g+' '+((r.count===r.dp&&r.dp===g)?'<span class="ok">✓ ba phương pháp khớp</span>':'<span class="no">✗ lệch</span>')+'</p>'}
    catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.pigeon=function(root){
  frame(root,'Máy tính nguyên lý Dirichlet','<div class="row"><label>Số "hộp" (số loại/mức) k = <input id="k" type="number" value="41" style="width:70px"></label><label>Muốn chắc chắn có m đối tượng cùng hộp, m = <input id="m" type="number" value="12" style="width:60px"></label><button class="btn" id="go">Tính</button></div><div class="out"></div><p><small>Bài thi trắc nghiệm: nếu đề có q câu thì số mức điểm là k = q + 1. Bi có L loại × C màu: k = L·C.</small></p>');
  function run(){var k=+$(root,'#k').value,m=+$(root,'#m').value;$(root,'.out').innerHTML='<p>Cần ít nhất <b>N = k·(m − 1) + 1 = '+k+'·'+(m-1)+' + 1 = '+DM.pigeon(k,m)+'</b> đối tượng.</p><p>Kiểm tra: với '+(DM.pigeon(k,m)-1)+' đối tượng có thể chia đều mỗi hộp '+(m-1)+' đối tượng mà chưa có hộp nào đủ '+m+'.</p>'}
  $(root,'#go').onclick=run;run();
};
W.rec=function(root){
  frame(root,'Giải hệ thức truy hồi tuyến tính thuần nhất (hệ số nguyên)','<div class="row"><label>Bậc k: <select id="k"><option>2</option><option selected>3</option><option>1</option></select></label><label>Hệ số c₁…c_k (aₙ = c₁aₙ₋₁ + …): <input id="c" value="14 -59 70" size="14"></label><label>Điều kiện đầu a₀…a_(k−1): <input id="a" value="-7 -20 -100" size="14"></label><button class="btn" id="go">Giải</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var c=nums($(root,'#c').value),a=nums($(root,'#a').value),k=c.length;if(a.length!==k)throw new Error('Cần đúng '+k+' điều kiện đầu.');if(k<1||k>4)throw new Error('Bậc 1–4.');
    var poly='r'+(k>1?'^'+k:'')+c.map(function(x,i){var p=k-1-i;return (x>0?' − ':' + ')+(Math.abs(x)===1&&p>0?'':Math.abs(x))+(p>0?'r'+(p>1?'^'+p:''):'')}).join('')+' = 0';
    var sol=DM.solveRecurrence(c,a),seq=DM.recSequence(c,a,12);
    var html='<p>Phương trình đặc trưng: <b>'+poly+'</b></p>';
    if(sol.ok){var rs=Object.keys(sol.roots).map(Number).sort(function(x,y){return x-y});html+='<p>Nghiệm: '+rs.map(function(r){return 'r = '+r+(sol.roots[r]>1?' (bội '+sol.roots[r]+')':'')}).join('; ')+'</p><p><b>'+DM.formatSolution(sol)+'</b> '+(sol.verified?'<span class="ok">✓ khớp 12 số hạng đầu</span>':'<span class="no">✗ không khớp</span>')+'</p>'}else html+='<p class="no">'+sol.msg+'</p>';
    html+=tbl(['n'].concat(seq.map(function(_,i){return i})),[['aₙ'].concat(seq.map(String))]);out.innerHTML=html}
    catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.gen=function(root){
  frame(root,'Sinh cấu hình kế tiếp theo thứ tự từ điển','<div class="row"><label>Loại: <select id="t"><option value="perm">Hoán vị</option><option value="comb">Tổ hợp chập k của {1..n}</option><option value="bin">Xâu nhị phân</option></select></label><label>Cấu hình hiện tại: <input id="x" size="26" value="5 6 8 3 9 7 4 2 1"></label><label>n = <input id="n" type="number" value="9" style="width:50px"></label><label>Số bước: <input id="s" type="number" value="4" style="width:50px"></label><button class="btn" id="go">Sinh</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var t=$(root,'#t').value,x=nums($(root,'#x').value),n=+$(root,'#n').value,s=+$(root,'#s').value;var steps=[],cur=x.slice(),lines=[];
    if(t==='perm'){var sorted=x.slice().sort(function(a,b){return a-b});for(var i=0;i<sorted.length;i++)if(sorted[i]!==i+1)throw new Error('Hoán vị phải là một hoán vị của 1..m')}
    if(t==='comb'){for(var j=0;j<x.length;j++){if(x[j]<1||x[j]>n||(j&&x[j]<=x[j-1]))throw new Error('Tổ hợp phải tăng ngặt, trong 1..n')}}
    if(t==='bin'){x.forEach(function(b){if(b!==0&&b!==1)throw new Error('Xâu nhị phân chỉ chứa 0/1')})}
    for(var q=0;q<s;q++){var nx=t==='perm'?DM.nextPerm(cur):(t==='comb'?DM.nextComb(cur,n):DM.nextBinary(cur));if(!nx){lines.push('<tr><td>'+(q+1)+'</td><td colspan="2"><b>Đã là cấu hình cuối cùng</b></td></tr>');break}
      var why='';if(t==='perm'){var i2=cur.length-2;while(i2>=0&&cur[i2]>cur[i2+1])i2--;var j2=cur.length-1;while(cur[j2]<cur[i2])j2--;why='i = vị trí '+(i2+1)+' (giá trị '+cur[i2]+'); j = vị trí '+(j2+1)+' (giá trị '+cur[j2]+'); đổi chỗ rồi đảo đoạn sau vị trí '+(i2+1)}
      else if(t==='comb'){var k=cur.length,i3=k-1;while(i3>=0&&cur[i3]===n-k+i3+1)i3--;why='i = vị trí '+(i3+1)+' (giá trị '+cur[i3]+' &lt; '+(n-k+i3+1)+'); tăng lên '+(cur[i3]+1)+', các phần tử sau = liền kề tăng dần'}
      else{var i4=cur.length-1;while(i4>=0&&cur[i4]===1)i4--;why='bit 0 phải nhất ở vị trí '+(i4+1)+' đổi thành 1, các bit sau đổi thành 0'}
      lines.push('<tr><td>'+(q+1)+'</td><td class="mono">('+nx.join(', ')+')</td><td style="text-align:left">'+why+'</td></tr>');cur=nx}
    out.innerHTML=tbl(['Bước','Cấu hình kế tiếp','Giải thích'],[]).replace('</table>',lines.join('')+'</table>').replace('<tr><th>Bước','<tr><th>Bước')}
    catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;
  $(root,'#t').onchange=function(){var t=this.value;$(root,'#x').value=t==='perm'?'5 6 8 3 9 7 4 2 1':(t==='comb'?'2 3 6 8 9':'0 1 1 0 1 1 0');$(root,'#n').value=t==='bin'?'':9;run()};run();
};
W.bt=function(root){
  frame(root,'Quay lui: quan sát từng bước duyệt cây','<div class="row"><label>Bài toán: <select id="m"><option value="bin">Xâu nhị phân độ dài n</option><option value="perm">Hoán vị của 1..n</option><option value="comb">Tổ hợp chập k của 1..n</option></select></label><label>n = <input id="n" type="number" value="3" min="1" max="6" style="width:50px"></label><label>k = <input id="k" type="number" value="2" min="1" max="5" style="width:50px"></label><button class="btn" id="go">Chạy</button> <button class="btn alt" id="stp">Bước tiếp ▶</button> <button class="btn alt" id="all">Hiện tất cả</button></div><div class="out"></div>');
  var ev=[],pos=0;
  function build(){var m=$(root,'#m').value,n=+$(root,'#n').value,k=+$(root,'#k').value;var r=DM.backtrackTrace(m,n,k);ev=r.events;pos=0;show(r.results.length)}
  function line(e){var pad=new Array(e.lvl+1).join('│&nbsp;&nbsp;');var s=e.t==='out'?'<b class="ok">★ in ra ('+e.x.join(', ')+')</b>':(e.t==='skip'?'<span class="no">✗ bỏ qua '+e.x[e.x.length-1]+' (đã dùng)</span>':'thử x['+(e.lvl+1)+'] = '+e.x[e.x.length-1]+' → ('+e.x.join(', ')+')');return '<div class="mono">'+pad+s+'</div>'}
  function show(total){$(root,'.out').innerHTML='<p>Tổng số sự kiện: '+ev.length+' | số kết quả: '+total+'</p><div id="lg" style="max-height:260px;overflow:auto;border:1px solid var(--border);border-radius:8px;padding:6px"></div>';step(1)}
  function step(k){var lg=$(root,'#lg');for(var i=0;i<k&&pos<ev.length;i++){lg.insertAdjacentHTML('beforeend',line(ev[pos]));pos++}lg.scrollTop=lg.scrollHeight}
  $(root,'#go').onclick=build;$(root,'#stp').onclick=function(){step(1)};$(root,'#all').onclick=function(){step(ev.length)};build();
};
W.knap=function(root){
  frame(root,'Cái túi: duyệt toàn bộ và nhánh cận (từng nút)','<div class="row"><label>Giá trị c: <input id="v" value="3 5 7 4" size="14"></label><label>Trọng lượng a: <input id="w" value="2 4 3 2" size="14"></label><label>Sức chứa b: <input id="b" type="number" value="9" style="width:60px"></label><label><input id="u" type="checkbox"> số lượng không hạn chế</label><button class="btn" id="go">Giải</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var v=nums($(root,'#v').value),w=nums($(root,'#w').value),b=+$(root,'#b').value,u=$(root,'#u').checked;if(v.length!==w.length||v.length<1||v.length>8)throw new Error('c và a phải cùng độ dài (1–8).');
    var r=DM.knapBB(v,w,b,{unlimited:u});var html='<p>Thứ tự xét (c/a giảm dần): '+r.order.map(function(i){return 'x'+(i+1)+' ('+v[i]+'/'+w[i]+'='+fnum(v[i]/w[i])+')'}).join(', ')+'</p>';
    html+=tbl(['Nút (thành phần đã gán)','δ (giá trị)','w (còn lại)','g (cận trên)','Trạng thái'],r.nodes.map(function(nd){var st={root:'gốc',expand:'mở rộng',pruned:'✗ cắt (g ≤ FOPT)',record:'★ kỷ lục',leaf:'lá'}[nd.status];return {cls:nd.status==='pruned'?'pruned':(nd.status==='record'?'hl':''),cells:['('+nd.x.join(', ')+')',nd.delta===undefined?'0':nd.delta,nd.rem,fnum(nd.g),st]}}));
    html+='<p><b>f* = '+r.fopt+', x* = ('+r.xopt.join(', ')+')</b> (theo thứ tự biến gốc).</p>';
    if(!u&&v.length<=6){var bf=DM.knapBrute(v,w,b);html+='<details><summary>Đối chiếu duyệt toàn bộ ('+bf.rows.length+' phương án)</summary>'+tbl(['x','Σ a·x','Σ c·x','Khả thi?'],bf.rows.map(function(x){var wt=x.W;return {cls:x.ok&&x.V===bf.best?'hl':(x.ok?'':'pruned'),cells:['('+x.x.join(',')+')',x.W,x.V,x.ok?'✓':'✗ vượt']}}))+'<p>Tối ưu duyệt toàn bộ: '+bf.best+' '+(bf.best===r.fopt?'<span class="ok">✓ khớp nhánh cận</span>':'<span class="no">✗</span>')+'</p></details>'}
    out.innerHTML=html}catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.tsp=function(root){
  frame(root,'Người du lịch: rút gọn ma trận + nhánh cận (giáo trình PTIT)','<div class="row"><small>Nhập ma trận chi phí n×n, mỗi dòng một hàng (đường chéo bất kỳ, sẽ bị coi là ∞). Tối đa n = 8.</small></div><textarea id="m" rows="6">0 3 93 13 33 9\n4 0 77 42 21 16\n45 17 0 36 16 28\n39 90 80 0 56 7\n28 46 88 33 0 25\n3 88 18 46 92 0</textarea><div class="row"><button class="btn" id="go">Giải</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var C=$(root,'#m').value.trim().split(/\n+/).map(nums),n=C.length;if(n<3||n>8||C.some(function(r){return r.length!==n}))throw new Error('Ma trận phải vuông, 3 ≤ n ≤ 8.');
    var r=DM.tspBB(C),id=DM.tspIdentity(C),bf=n<=8?DM.tspBrute(C):null;
    var html='<p>Cận dưới ở gốc (sau rút gọn): <b>'+r.root+'</b>.</p>'+tbl(['Nút','Cận dưới','Kết quả'],r.log.map(function(e){var t={root:'gốc',branch:'phân nhánh theo cạnh ('+(e.edge||[]).join(',')+'), β = '+e.beta,cut:'✗ cắt (cận ≥ kỷ lục)',record:'★ hành trình, chi phí '+e.cost,leaf:'hành trình, chi phí '+e.cost+' (không cải thiện)',dead:'✗ không hợp lệ'}[e.status];return {cls:e.status==='cut'?'pruned':(e.status==='record'?'hl':''),cells:[new Array(e.depth+1).join('… ')+e.label,e.bound,t]}}));
    html+='<p><b>Hành trình tối ưu: '+r.tour.join('→')+', chi phí '+r.cost+'</b> '+(bf&&bf.cost===r.cost?'<span class="ok">✓ khớp vét cạn ('+bf.tour.join('→')+')</span>':'')+'</p><p>Ghi chú: hành trình 1→2→…→n→1 có chi phí '+id.cost+' (thường là phương án đầu tiên khi duyệt theo chỉ số tăng dần, như trong bộ trắc nghiệm ôn PTIT).</p>';out.innerHTML=html}
    catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.gf=function(root){
  frame(root,'Hàm sinh: hệ số của xᴺ','<div class="row"><label>Tổng N = <input id="n" type="number" value="12" style="width:60px"></label><label>Cận từng biến lo-hi (hi trống = ∞): <input id="bd" size="36" value="1-4 2-6 0-8"></label><button class="btn" id="go">Tính hệ số</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var N=+$(root,'#n').value,parts=$(root,'#bd').value.trim().split(/\s+/),lo=[],hi=[];parts.forEach(function(p){var m=p.match(/^(\d+)-(\d*)$/);if(!m)throw new Error('Sai định dạng: '+p);lo.push(+m[1]);hi.push(m[2]===''?null:+m[2])});
    var poly=[1n];lo.forEach(function(l,i){var h=hi[i]===null?N:hi[i];var f=new Array(h+1).fill(0n);for(var e=l;e<=h;e++)f[e]=1n;poly=DM.polyMul(poly,f,N)});
    var f=lo.map(function(l,i){return '('+(hi[i]===null?'x^'+l+'/(1−x)':(l===hi[i]?'x^'+l:'x^'+l+'+…+x^'+hi[i]))+')'}).join('');
    out.innerHTML='<p>Hàm sinh: <span class="mono">'+f+'</span></p><p><b>Hệ số của x^'+N+' = '+(poly[N]||0n)+'</b></p>'+tbl(['k'].concat(poly.map(function(_,i){return i})),[['[xᵏ]'].concat(poly.map(String))])}
    catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;run();
};
W.bits=function(root){
  frame(root,'Biểu diễn tập hợp bằng xâu bit','<div class="row"><label>Tập vũ trụ U = {1..<input id="n" type="number" value="9" style="width:50px">}</label><label>A: <input id="A" value="2 3 5 7" size="12"></label><label>B: <input id="B" value="1 3 5 7 9" size="12"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){var n=+$(root,'#n').value,A=nums($(root,'#A').value),B=nums($(root,'#B').value),U=[];for(var i=1;i<=n;i++)U.push(i);
    var a=DM.setToBits(A,U),b=DM.setToBits(B,U);function s(x){return x.join('')}function set(bits){var r=U.filter(function(_,i){return bits[i]});return '{'+r.join(', ')+'}'}
    var or=a.map(function(x,i){return x|b[i]}),and=a.map(function(x,i){return x&b[i]}),xor=a.map(function(x,i){return x^b[i]}),diff=a.map(function(x,i){return x&(1-b[i])}),ca=a.map(function(x){return 1-x});
    $(root,'.out').innerHTML=tbl(['Phép','Xâu bit','Tập'],[['A',s(a),set(a)],['B',s(b),set(b)],['A ∪ B (OR)',s(or),set(or)],['A ∩ B (AND)',s(and),set(and)],['A \\ B (A AND NOT B)',s(diff),set(diff)],['A △ B (XOR)',s(xor),set(xor)],['Aᶜ (NOT A)',s(ca),set(ca)]])}
  $(root,'#go').onclick=run;run();
};
W.growth=function(root){
  frame(root,'So sánh bậc tăng trưởng','<div class="row"><label>n = <input id="n" type="number" value="30" style="width:70px"></label><button class="btn" id="go">So sánh</button></div><div class="out"></div>');
  function run(){var n=+$(root,'#n').value,g=DM.growth(n),keys=Object.keys(g);$(root,'.out').innerHTML=tbl(['Hàm','Giá trị','Thời gian nếu 10⁹ phép/giây'],keys.map(function(k){var v=g[k];var t=v/1e9;var ts=!isFinite(v)?'∞':(t<1e-3?'< 1 ms':(t<60?t.toFixed(3)+' giây':(t<3600?(t/60).toFixed(1)+' phút':(t<86400*365?(t/3600).toFixed(1)+' giờ':(t/86400/365).toExponential(2)+' năm'))));return [k,!isFinite(v)?'∞ (quá lớn)':(v>1e12?v.toExponential(3):fnum(v)),ts]}))}
  $(root,'#go').onclick=run;run();
};

W.quant=function(root){
  var PR=[['x là số chẵn',function(x){return x%2===0}],['x là số lẻ',function(x){return x%2===1}],['x là số nguyên tố',function(x){if(x<2)return false;for(var d=2;d*d<=x;d++)if(x%d===0)return false;return true}],['x chia hết cho 3',function(x){return x%3===0}],['x > 3',function(x){return x>3}],['x < 6',function(x){return x<6}],['x² < 30',function(x){return x*x<30}],['x là số chính phương',function(x){var r=Math.round(Math.sqrt(x));return r*r===x}]];
  var opts=PR.map(function(p,i){return '<option value="'+i+'">'+p[0]+'</option>'}).join('');
  frame(root,'Đánh giá lượng từ trên miền hữu hạn','<div class="row"><label>Miền D (số nguyên): <input id="d" size="24" value="1 2 3 4 5 6 7 8"></label></div><div class="row"><label>P(x): <select id="p">'+opts+'</select></label><label>Q(x): <select id="q">'+opts.replace('value="0"','value="0"').replace('<option value="2">','<option value="2" selected>')+'</select></label><button class="btn" id="go">Đánh giá</button></div><div class="out"></div><hr><div class="row"><small>Quan hệ R(x,y): nhập các cặp "x,y" cách nhau bởi dấu cách (trên cùng miền D):</small></div><div class="row"><input id="r" size="44" value="1,1 1,2 2,2 2,3 3,3 3,1"><button class="btn alt" id="go2">Đánh giá lượng từ lồng nhau</button></div><div class="out2"></div>');
  function run(){var D=nums($(root,'#d').value),P=PR[+$(root,'#p').value],Q=PR[+$(root,'#q').value];if(!D.length){return}
    function all(f){return D.every(f)}function any(f){return D.some(f)}var p=P[1],q=Q[1];
    var rows=[['∀x P(x)',all(p)],['∃x P(x)',any(p)],['∀x Q(x)',all(q)],['∃x Q(x)',any(q)],['∀x (P(x) ⇒ Q(x))',all(function(x){return !p(x)||q(x)})],['∃x (P(x) ∧ Q(x))',any(function(x){return p(x)&&q(x)})],['∀x (P(x) ∨ Q(x))',all(function(x){return p(x)||q(x)})],['∃x (P(x) ∧ ¬Q(x))',any(function(x){return p(x)&&!q(x)})],['¬∀x P(x)  ≡  ∃x ¬P(x)',!all(p)]];
    $(root,'.out').innerHTML='<p>Thỏa P: {'+D.filter(p).join(', ')+'} &nbsp; Thỏa Q: {'+D.filter(q).join(', ')+'}</p>'+tbl(['Mệnh đề','Giá trị'],rows.map(function(r){return {cls:r[1]?'hl':'pruned',cells:[r[0],r[1]?'Đúng':'Sai']}}))}
  function run2(){var D=nums($(root,'#d').value),R={};$(root,'#r').value.trim().split(/\s+/).forEach(function(s){var m=s.split(',');if(m.length===2)R[m[0]+','+m[1]]=true});
    function r(x,y){return !!R[x+','+y]}
    var rows=[['∀x ∃y R(x,y)',D.every(function(x){return D.some(function(y){return r(x,y)})})],['∃y ∀x R(x,y)',D.some(function(y){return D.every(function(x){return r(x,y)})})],['∃x ∀y R(x,y)',D.some(function(x){return D.every(function(y){return r(x,y)})})],['∀y ∃x R(x,y)',D.every(function(y){return D.some(function(x){return r(x,y)})})],['∀x ∀y R(x,y)',D.every(function(x){return D.every(function(y){return r(x,y)})})],['∃x ∃y R(x,y)',Object.keys(R).length>0]];
    $(root,'.out2').innerHTML=tbl(['Mệnh đề','Giá trị'],rows.map(function(r0){return {cls:r0[1]?'hl':'pruned',cells:[r0[0],r0[1]?'Đúng':'Sai']}}))}
  $(root,'#go').onclick=run;$(root,'#go2').onclick=run2;run();run2();
};
W.strcount=function(root){
  var F={ 'no11':['Không chứa 2 bit 1 liên tiếp',function(s){return s.indexOf('11')<0}],'no111':['Không chứa 3 bit 1 liên tiếp',function(s){return s.indexOf('111')<0}],'has11':['Có chứa 2 bit 1 liên tiếp',function(s){return s.indexOf('11')>=0}],'has111':['Có chứa 3 bit 1 liên tiếp',function(s){return s.indexOf('111')>=0}],'no00':['Không chứa 2 bit 0 liên tiếp',function(s){return s.indexOf('00')<0}],'even0':['Có số CHẴN bit 0',function(s){return (s.split('0').length-1)%2===0}],'s1has00':['Bắt đầu bằng 1 và chứa 2 bit 0 liên tiếp',function(s){return s[0]==='1'&&s.indexOf('00')>=0}]};
  frame(root,'Đếm xâu nhị phân bằng liệt kê và kiểm tra hệ thức truy hồi','<div class="row"><label>Tính chất: <select id="f">'+Object.keys(F).map(function(k){return '<option value="'+k+'">'+F[k][0]+'</option>'}).join('')+'</select></label><label>n tối đa: <input id="N" type="number" value="12" min="4" max="16" style="width:50px"></label><button class="btn" id="go">Đếm</button></div><div class="out"></div><hr><div class="row"><small>Kiểm tra hệ thức thử: aₙ = α·aₙ₋₁ + β·aₙ₋₂ + γ·aₙ₋₃ + δ·2^(n−m) (bỏ trống = 0):</small></div><div class="row"><label>α <input id="al" value="1" size="3"></label><label>β <input id="be" value="1" size="3"></label><label>γ <input id="ga" value="0" size="3"></label><label>δ <input id="de" value="0" size="3"></label><label>m <input id="mm" value="2" size="3"></label><label>từ n = <input id="n0" value="3" size="3"></label><button class="btn alt" id="chk">Kiểm tra</button></div><div class="out2"></div>');
  var a=[];
  function count(){var f=F[$(root,'#f').value][1],N=+$(root,'#N').value;a=[];for(var n=1;n<=N;n++){var c=0;for(var m=0;m<(1<<n);m++){var s=(m+(1<<n)).toString(2).slice(1);if(f(s))c++}a[n]=c}
    $(root,'.out').innerHTML=tbl(['n'].concat(a.slice(1).map(function(_,i){return i+1})),[['aₙ'].concat(a.slice(1))])}
  function check(){var al=+$(root,'#al').value||0,be=+$(root,'#be').value||0,ga=+$(root,'#ga').value||0,de=+$(root,'#de').value||0,mm=+$(root,'#mm').value||0,n0=+$(root,'#n0').value||3;var bad=[];
    for(var n=Math.max(n0,1);n<a.length;n++){var v=al*(a[n-1]||0)+be*(a[n-2]||0)+ga*(a[n-3]||0)+de*Math.pow(2,n-mm);if(n-3<1&&ga)continue;if(v!==a[n])bad.push('n='+n+': công thức cho '+v+', đếm được '+a[n])}
    $(root,'.out2').innerHTML=bad.length?'<p class="no">Không khớp: '+bad.slice(0,4).join('; ')+'</p>':'<p class="ok">✓ Hệ thức khớp mọi n từ '+n0+' đến '+(a.length-1)+'.</p>'}
  $(root,'#go').onclick=count;$(root,'#f').onchange=count;$(root,'#chk').onclick=function(){if(!a.length)count();check()};count();
};
document.querySelectorAll('.sim[data-sim]').forEach(function(root){var f=W[root.getAttribute('data-sim')];if(f)f(root)});
})();

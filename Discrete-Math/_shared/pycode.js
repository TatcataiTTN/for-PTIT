/* Luyện code Python từng bài: danh sách lọc, đề + trình soạn thảo hai cột, chạy mẫu / nộp / input riêng, gợi ý, lời giải. */
(function(){
var root=document.getElementById('pyroot');if(!root)return;
var U=window.PyUI,el=U.el,META=JSON.parse(document.getElementById('py-meta').textContent);
var KEY='ptit-trr1:py',CK='ptit-trr1:pycode:',P=[],busy=false,st={mod:'all',lv:'all',stat:'all',q:''};
var LV={1:'Cơ bản',2:'Vừa',3:'Khó'};
function S(){return U.jget(KEY,{})}
fetch('../../data/python/problems.json').then(function(r){return r.json()}).then(function(d){P=d;route();window.addEventListener('hashchange',route)}).catch(function(e){root.textContent='Không tải được đề: '+e});
function route(){var h=decodeURIComponent(location.hash.slice(1));var p=P.filter(function(x){return x.id===h})[0];if(p)showProblem(p);else showList()}
function statusOf(p,s){return s[p.id]&&s[p.id].ok?'ok':(s[p.id]&&s[p.id].viewed?'viewed':'todo')}
function showList(){
  root.innerHTML='';var s=S(),done=P.filter(function(p){return statusOf(p,s)==='ok'}).length;
  var top=el('div','row');top.appendChild(el('span','badge','Đã giải '+done+' / '+P.length+' bài'));
  var pg=el('div','py-prog');pg.appendChild(el('i'));pg.firstChild.style.width=Math.round(100*done/Math.max(1,P.length))+'%';top.appendChild(pg);
  var rnd=el('button','btn alt','🎲 Bài chưa giải ngẫu nhiên');rnd.onclick=function(){var t=P.filter(function(p){return statusOf(p,S())!=='ok'});if(t.length)location.hash='#'+t[Math.floor(Math.random()*t.length)].id};top.appendChild(rnd);
  var ex=el('a','btn','⏱ Thi thử có đồng hồ');ex.href='../thi-thu-python/index.html';ex.style.textDecoration='none';top.appendChild(ex);
  root.appendChild(top);
  function chips(label,items,key){var r=el('div');r.appendChild(el('b',null,label+' '));items.forEach(function(it){var c=el('span','py-chip'+(st[key]===it[0]?' on':''),it[1]);c.onclick=function(){st[key]=it[0];showList()};r.appendChild(c)});root.appendChild(r)}
  chips('Module:',[['all','Tất cả']].concat(META.mods),'mod');
  chips('Mức:',[['all','Mọi mức'],['1','Cơ bản'],['2','Vừa'],['3','Khó']],'lv');
  chips('Trạng thái:',[['all','Tất cả'],['todo','Chưa giải'],['ok','Đã giải'],['viewed','Đã xem lời giải']],'stat');
  var sq=el('input');sq.type='search';sq.placeholder='Tìm bài…';sq.value=st.q;sq.style.cssText='margin:8px 0;padding:7px 12px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);font:inherit;width:100%;max-width:340px';
  var box=el('div','grid');box.id='pycards';sq.oninput=function(){st.q=sq.value;fill()};root.appendChild(sq);root.appendChild(box);
  function fill(){box.innerHTML='';var n=0;P.forEach(function(p){
    if(!((st.mod==='all'||p.mod===st.mod)&&(st.lv==='all'||String(p.lv)===st.lv)&&(st.stat==='all'||statusOf(p,s)===st.stat)&&(!st.q||(p.title+' '+p.stmt).toLowerCase().indexOf(st.q.toLowerCase())>=0)))return;n++;
    var a=el('a','mod-card');a.href='#'+p.id;var t=statusOf(p,s);
    a.innerHTML='<span class="num">'+META.modname[p.mod]+' · '+LV[p.lv]+(t==='ok'?' · ✅ đã giải':(t==='viewed'?' · 👁 đã xem lời giải':''))+'</span><h3>'+p.title+'</h3><p>'+p.tests.length+' test'+(s[p.id]&&s[p.id].last?' · lần nộp gần nhất '+s[p.id].last:'')+'</p>';box.appendChild(a)});
    if(!n)box.appendChild(el('p','lead','Không có bài phù hợp.'))}
  fill();
  var b=el('button','btn alt','⚙️ Tải sẵn môi trường Python (~10 MB, lần đầu)');b.style.marginTop='10px';b.onclick=function(){b.disabled=true;b.textContent='Đang tải…';PyJudge.ready().then(function(){b.textContent='✔ Python đã sẵn sàng'}).catch(function(){b.textContent='Lỗi tải Python (kiểm tra mạng)'})};root.appendChild(b);
}
function showProblem(p){
  root.innerHTML='';var idx=P.indexOf(p);
  var nav=el('div','row');var back=el('a',null,'← Danh sách bài');back.href='#';nav.appendChild(back);
  if(idx>0){var pa=el('a',null,'‹ '+P[idx-1].title);pa.href='#'+P[idx-1].id;pa.style.marginLeft='auto';nav.appendChild(pa)}
  if(idx<P.length-1){var na=el('a',null,P[idx+1].title+' ›');na.href='#'+P[idx+1].id;if(idx===0)na.style.marginLeft='auto';nav.appendChild(na)}
  root.appendChild(nav);
  var sp=el('div','py-split'),L=el('div','py-left'),Rr=el('div','py-right');sp.appendChild(L);sp.appendChild(Rr);root.appendChild(sp);
  L.appendChild(el('h2',null,p.title));
  var tags=el('p');tags.innerHTML='<span class="tag">'+META.modname[p.mod]+'</span><span class="tag">'+LV[p.lv]+'</span><span class="tag"><a href="../modules/'+META.slugs[p.mod]+'/index.html">Mở bài giảng module</a></span>';L.appendChild(tags);
  var s=el('div');s.innerHTML='<p>'+p.stmt+'</p><p><b>Dữ liệu vào.</b> '+p.inp+'</p><p><b>Kết quả.</b> '+p.out+'</p><p><b>Giới hạn.</b> '+p.cons+'</p>';L.appendChild(s);
  p.tests.filter(function(t){return t.pub}).forEach(function(t,i){
    var d=el('div','sim');d.innerHTML='<div class="simh">Ví dụ '+(i+1)+'</div>';
    var g=el('div');g.style.cssText='display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px';
    [['Vào',t.i],['Ra',t.o]].forEach(function(x){var c=el('div');c.appendChild(el('b',null,x[0]));var pr=el('div','py-out');pr.textContent=x[1];c.appendChild(pr);g.appendChild(c)});d.appendChild(g);L.appendChild(d)});
  var hint=el('div','callout');hint.style.display='none';hint.innerHTML='<b class="t">Gợi ý</b>'+p.hint;L.appendChild(hint);
  var sol=el('div');sol.style.display='none';L.appendChild(sol);
  Rr.appendChild(el('h3',null,'Bài làm của bạn'));
  var edBox=el('div');Rr.appendChild(edBox);
  var ed=U.makeEditor(edBox,U.sget(CK+p.id)||p.starter,{onChange:function(v){U.sset(CK+p.id,v)},onRun:function(){bs.onclick()},onSubmit:function(){bj.onclick()}});
  var bar=el('div','row');
  var bs=el('button','btn alt','▶ Chạy ví dụ'),bj=el('button','btn','✓ Nộp bài ('+p.tests.length+' test)'),bc=el('button','btn alt','🧪 Input riêng'),bh=el('button','btn alt','💡 Gợi ý'),bv=el('button','btn alt','📖 Lời giải'),br=el('button','btn alt','↺ Đặt lại');
  [bs,bj,bc,bh,bv,br].forEach(function(b){bar.appendChild(b)});Rr.appendChild(bar);
  var info=el('p','lead');info.textContent=window.Worker?'Python chạy trong trình duyệt. Ctrl/Cmd+Enter: chạy ví dụ; Shift+Ctrl/Cmd+Enter: nộp. Lần đầu cần tải ~10 MB.':'Trình duyệt không hỗ trợ Web Worker nên không chạy được Python.';Rr.appendChild(info);
  var custom=el('div');custom.style.display='none';var ci=el('textarea');ci.rows=5;ci.placeholder='Nhập dữ liệu vào (như nội dung file input)…';ci.style.cssText='width:100%;box-sizing:border-box;font:13px ui-monospace,Menlo,monospace;padding:8px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)';
  var cr=el('button','btn','Chạy');custom.appendChild(ci);custom.appendChild(cr);Rr.appendChild(custom);
  var res=el('div');Rr.appendChild(res);
  function lock(v){busy=v;[bs,bj,bc,cr,br].forEach(function(b){b.disabled=v})}
  function status(t){info.textContent=t}
  bh.onclick=function(){hint.style.display=hint.style.display==='none'?'':'none'};
  br.onclick=function(){if(confirm('Xóa mã hiện tại và quay về bản khởi đầu?'))ed.set(p.starter)};
  bc.onclick=function(){custom.style.display=custom.style.display==='none'?'':'none';if(!ci.value)ci.value=(p.tests[0]||{}).i||''};
  bv.onclick=function(){
    if(sol.style.display==='none'){var s0=S();s0[p.id]=s0[p.id]||{};s0[p.id].viewed=true;U.jset(KEY,s0);
      sol.innerHTML='<div class="callout warn"><b class="t">Lời giải mẫu</b><p>Hãy tự thử trước; đọc xong nên tự viết lại không nhìn.</p></div>';
      var pr=el('pre'),cd=el('code');cd.textContent=p.sol;pr.appendChild(cd);sol.appendChild(pr);var e2=el('div','callout good');e2.innerHTML='<b class="t">Giải thích</b>'+p.expl;sol.appendChild(e2);sol.style.display=''}
    else sol.style.display='none'};
  function judge(tests,submit){
    if(busy)return;lock(true);status('Đang chạy… (lần đầu phải tải Python, có thể mất vài chục giây)');
    U.runTests(ed.get(),tests,8000,function(rows){status('Đã chạy '+rows.length+' / '+tests.length+' test…');res.innerHTML='';res.appendChild(U.resultTable(rows,false))}).then(function(rows){
      status('Xong.');res.innerHTML='';res.appendChild(U.resultTable(rows,false));
      var all=rows.every(function(r){return r.v==='AC'});
      if(submit){var s0=S();s0[p.id]=s0[p.id]||{};if(all)s0[p.id].ok=true;s0[p.id].t=Date.now();s0[p.id].last=rows.filter(function(r){return r.v==='AC'}).length+'/'+rows.length;U.jset(KEY,s0)}
      if(submit&&all){var ok=el('div','callout good');ok.innerHTML='<b class="t">🎉 Hoàn thành bài!</b>';if(idx<P.length-1){var n=el('a',null,'Làm bài tiếp theo: '+P[idx+1].title+' ›');n.href='#'+P[idx+1].id;ok.appendChild(n)}res.insertBefore(ok,res.firstChild)}
    }).catch(function(e){status('Không chạy được Python: '+(e&&e.message||e)+'. Kiểm tra mạng (cần tải Pyodide từ CDN).')}).then(function(){lock(false)})}
  bs.onclick=function(){judge(p.tests.filter(function(t){return t.pub}),false)};
  bj.onclick=function(){judge(p.tests,true)};
  cr.onclick=function(){if(busy)return;lock(true);status('Đang chạy…');PyJudge.run(ed.get(),ci.value.replace(/\r/g,''),8000).then(function(r){res.innerHTML='';[['Kết quả',r.tle?'(quá 8 giây)':r.out||'(trống)']].concat(r.err?[['Thông báo lỗi',r.err]]:[]).forEach(function(x){res.appendChild(el('b',null,x[0]));var pr=el('div','py-out');pr.textContent=x[1];res.appendChild(pr)});status('Xong ('+r.ms+' ms).')}).catch(function(e){status('Lỗi: '+(e&&e.message||e))}).then(function(){lock(false)})};
  window.scrollTo(0,0);setTimeout(function(){ed.refresh()},80);
}
})();

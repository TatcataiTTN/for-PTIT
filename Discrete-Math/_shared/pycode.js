/* Giao diện luyện code Python: danh sách bài, trình soạn thảo, chạy mẫu / chạy input riêng / chấm đủ test, gợi ý, lời giải. */
(function(){
var root=document.getElementById('pyroot');if(!root)return;
var META=JSON.parse(document.getElementById('py-meta').textContent);
var KEY='ptit-trr1:py',CK='ptit-trr1:pycode:',P=[],cur=null,busy=false;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
function getCode(id){try{return localStorage.getItem(CK+id)}catch(e){return null}}
function setCode(id,c){try{localStorage.setItem(CK+id,c)}catch(e){}}
function norm(s){var L=s.replace(/\r/g,'').split('\n').map(function(x){return x.replace(/\s+$/,'')});while(L.length&&L[L.length-1]==='')L.pop();return L.join('\n')}
var LV={1:'Cơ bản',2:'Vừa',3:'Khó'};
var st={mod:'all',lv:'all',q:''};
fetch('../../data/python/problems.json').then(function(r){return r.json()}).then(function(d){P=d;route();window.addEventListener('hashchange',route)}).catch(function(e){root.textContent='Không tải được đề: '+e});
function route(){var h=decodeURIComponent(location.hash.slice(1));var p=P.filter(function(x){return x.id===h})[0];if(p)showProblem(p);else showList()}
function showList(){
  cur=null;root.innerHTML='';var S=load();
  var done=P.filter(function(p){return S[p.id]&&S[p.id].ok}).length;
  var top=el('div','row');top.appendChild(el('span','badge','Đã giải '+done+' / '+P.length+' bài'));
  var eng=el('span','badge','');eng.id='pyeng';top.appendChild(eng);root.appendChild(top);
  var f=el('div','row');
  var sm=el('select');sm.appendChild(new Option('Mọi module','all'));META.mods.forEach(function(m){sm.appendChild(new Option(m[1],m[0]))});sm.value=st.mod;sm.onchange=function(){st.mod=sm.value;renderCards()};
  var sl=el('select');[['all','Mọi mức'],['1','Cơ bản'],['2','Vừa'],['3','Khó']].forEach(function(o){sl.appendChild(new Option(o[1],o[0]))});sl.value=st.lv;sl.onchange=function(){st.lv=sl.value;renderCards()};
  var sq=el('input');sq.type='search';sq.placeholder='Tìm bài…';sq.value=st.q;sq.oninput=function(){st.q=sq.value;renderCards()};
  f.appendChild(sm);f.appendChild(sl);f.appendChild(sq);root.appendChild(f);
  var box=el('div','grid');box.id='pycards';root.appendChild(box);renderCards();
  if(window.PyJudge){var b=el('button','btn alt','⚙️ Tải sẵn môi trường Python (~10 MB, lần đầu)');b.onclick=function(){b.disabled=true;b.textContent='Đang tải…';PyJudge.ready().then(function(){b.textContent='✔ Python đã sẵn sàng'}).catch(function(){b.textContent='Lỗi tải Python (kiểm tra mạng)'})};root.appendChild(b)}
}
function renderCards(){
  var box=document.getElementById('pycards');if(!box)return;box.innerHTML='';var S=load();
  P.filter(function(p){return (st.mod==='all'||p.mod===st.mod)&&(st.lv==='all'||String(p.lv)===st.lv)&&(!st.q||(p.title+' '+p.stmt).toLowerCase().indexOf(st.q.toLowerCase())>=0)}).forEach(function(p,i){
    var a=el('a','mod-card');a.href='#'+p.id;var s=S[p.id];
    a.innerHTML='<span class="num">'+META.modname[p.mod]+' · '+LV[p.lv]+(s&&s.ok?' · ✅ đã giải':(s&&s.viewed?' · 👁 đã xem lời giải':''))+'</span><h3>'+p.title+'</h3><p>'+p.tests.length+' test · '+(p.tests.filter(function(t){return t.pub}).length)+' mẫu</p>';
    box.appendChild(a)});
  if(!box.children.length)box.appendChild(el('p','lead','Không có bài phù hợp.'));
}
function showProblem(p){
  cur=p;root.innerHTML='';
  var back=el('a',null,'← Danh sách bài');back.href='#';back.style.display='inline-block';back.style.marginBottom='8px';root.appendChild(back);
  var h=el('h2',null,p.title);root.appendChild(h);
  var tags=el('p');tags.innerHTML='<span class="tag">'+META.modname[p.mod]+'</span><span class="tag">'+LV[p.lv]+'</span><span class="tag"><a href="../modules/'+META.slugs[p.mod]+'/index.html">Mở bài giảng module</a></span>';root.appendChild(tags);
  var s=el('div');s.innerHTML='<p>'+p.stmt+'</p><p><b>Dữ liệu vào.</b> '+p.inp+'</p><p><b>Kết quả.</b> '+p.out+'</p><p><b>Giới hạn.</b> '+p.cons+'</p>';root.appendChild(s);
  p.tests.filter(function(t){return t.pub}).forEach(function(t,i){
    var d=el('div','sim');d.innerHTML='<div class="simh">Ví dụ '+(i+1)+'</div>';
    var g=el('div');g.style.cssText='display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px';
    [['Vào',t.i],['Ra',t.o]].forEach(function(x){var c=el('div');c.appendChild(el('b',null,x[0]));var pr=el('pre');pr.textContent=x[1];c.appendChild(pr);g.appendChild(c)});d.appendChild(g);root.appendChild(d)});
  var ed=el('textarea');ed.id='pyed';ed.spellcheck=false;ed.rows=Math.max(14,Math.min(30,p.starter.split('\n').length+6));
  ed.style.cssText='width:100%;box-sizing:border-box;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;padding:10px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);tab-size:4;white-space:pre';
  ed.value=getCode(p.id)||p.starter;ed.oninput=function(){setCode(p.id,ed.value)};
  ed.onkeydown=function(e){if(e.key==='Tab'){e.preventDefault();var a=ed.selectionStart;ed.value=ed.value.slice(0,a)+'    '+ed.value.slice(ed.selectionEnd);ed.selectionStart=ed.selectionEnd=a+4;setCode(p.id,ed.value)}};
  root.appendChild(el('h3',null,'Bài làm của bạn'));root.appendChild(ed);
  var bar=el('div','row');
  var bs=el('button','btn alt','▶ Chạy ví dụ'),bj=el('button','btn','✓ Nộp bài (chấm '+p.tests.length+' test)'),bc=el('button','btn alt','🧪 Chạy với input riêng'),bh=el('button','btn alt','💡 Gợi ý'),bv=el('button','btn alt','📖 Xem lời giải'),br=el('button','btn alt','↺ Đặt lại mã');
  [bs,bj,bc,bh,bv,br].forEach(function(b){bar.appendChild(b)});root.appendChild(bar);
  var info=el('p','lead');info.id='pyinfo';info.textContent=window.Worker?'Python chạy ngay trong trình duyệt của bạn. Lần chạy đầu cần tải môi trường (~10 MB).':'Trình duyệt này không hỗ trợ Web Worker nên không thể chạy Python.';root.appendChild(info);
  var custom=el('div');custom.style.display='none';var ci=el('textarea');ci.rows=5;ci.placeholder='Nhập dữ liệu vào ở đây (giống nội dung file input)…';ci.style.cssText='width:100%;box-sizing:border-box;font:13px ui-monospace,Menlo,monospace;padding:8px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)';
  var cr=el('button','btn','Chạy');custom.appendChild(ci);custom.appendChild(cr);root.appendChild(custom);
  var res=el('div');res.id='pyres';root.appendChild(res);
  var hint=el('div','callout');hint.style.display='none';hint.innerHTML='<b class="t">Gợi ý</b>'+p.hint;root.appendChild(hint);
  var sol=el('div');sol.style.display='none';root.appendChild(sol);
  bh.onclick=function(){hint.style.display=hint.style.display==='none'?'':'none'};
  br.onclick=function(){if(confirm('Xóa mã hiện tại và quay về bản khởi đầu?')){ed.value=p.starter;setCode(p.id,ed.value)}};
  bc.onclick=function(){custom.style.display=custom.style.display==='none'?'':'none';if(!ci.value)ci.value=(p.tests[0]||{}).i||''};
  bv.onclick=function(){
    if(sol.style.display==='none'){var S=load();S[p.id]=S[p.id]||{};S[p.id].viewed=true;save(S);
      sol.innerHTML='<div class="callout warn"><b class="t">Lời giải mẫu</b><p>Hãy tự thử trước; đọc xong nên tự viết lại không nhìn.</p></div>';
      var pr=el('pre');var cd=el('code');cd.textContent=p.sol;pr.appendChild(cd);sol.appendChild(pr);var e2=el('div','callout good');e2.innerHTML='<b class="t">Giải thích</b>'+p.expl;sol.appendChild(e2);sol.style.display=''}
    else sol.style.display='none'};
  function lock(v){busy=v;[bs,bj,bc,cr,br].forEach(function(b){b.disabled=v})}
  function status(t){document.getElementById('pyinfo').textContent=t}
  function runOne(t,limit){return PyJudge.run(ed.value,t.i,limit)}
  function verdict(t,r){if(r.tle)return 'TLE';if(r.err)return 'RE';return norm(r.out)===norm(t.o)?'AC':'WA'}
  function show(rows,final){
    res.innerHTML='';var tb=el('table','t left');tb.innerHTML='<tr><th>Test</th><th>Loại</th><th>Kết quả</th><th>Thời gian</th></tr>';
    rows.forEach(function(r,i){var tr=el('tr');var lab={AC:'✅ Đúng',WA:'❌ Sai kết quả',RE:'💥 Lỗi chạy',TLE:'⏱ Quá giờ'}[r.v];
      tr.innerHTML='<td>'+(i+1)+'</td><td>'+(r.t.pub?'ví dụ':'ẩn')+'</td><td>'+lab+'</td><td>'+(r.r.tle?'> '+r.limit/1000+' s':r.r.ms+' ms')+'</td>';tb.appendChild(tr);
      if(r.v!=='AC'){var td=el('tr');var c=el('td');c.colSpan=4;var d=el('details');d.open=(i===rows.findIndex(function(x){return x.v!=='AC'}));
        d.appendChild(el('summary',null,'Chi tiết test '+(i+1)));
        [['Dữ liệu vào',r.t.i],['Kết quả đúng',r.t.o],['Kết quả của bạn',r.r.out||'(trống)']].concat(r.r.err?[['Thông báo lỗi',r.r.err]]:[]).forEach(function(x){d.appendChild(el('b',null,x[0]));var pr=el('pre');pr.textContent=x[1].length>2000?x[1].slice(0,2000)+'\n…(cắt bớt)':x[1];d.appendChild(pr)});
        c.appendChild(d);td.appendChild(c);tb.appendChild(td)}});
    var w=el('div');w.style.overflowX='auto';w.appendChild(tb);
    var ok=rows.filter(function(r){return r.v==='AC'}).length;var head=el('p');head.innerHTML='<b>'+ok+' / '+rows.length+' test đúng</b>'+(final&&ok===rows.length?' 🎉 Hoàn thành bài!':'');res.appendChild(head);res.appendChild(w)}
  function judge(tests,limit,submit){
    if(busy)return;lock(true);status('Đang chạy… (lần đầu phải tải Python, có thể mất vài chục giây)');var rows=[];
    PyJudge.ready().then(function(){
      var chain=Promise.resolve();
      tests.forEach(function(t){chain=chain.then(function(){status('Đang chạy test '+(rows.length+1)+' / '+tests.length+'…');return runOne(t,limit).then(function(r){rows.push({t:t,r:r,v:verdict(t,r),limit:limit});show(rows,false)})})});
      return chain}).then(function(){
        status('Xong.');show(rows,true);
        if(submit){var S=load();S[p.id]=S[p.id]||{};var ok=rows.every(function(r){return r.v==='AC'});if(ok)S[p.id].ok=true;S[p.id].t=Date.now();S[p.id].last=rows.filter(function(r){return r.v==='AC'}).length+'/'+rows.length;save(S)}
      }).catch(function(e){status('Không chạy được Python: '+(e&&e.message||e)+'. Kiểm tra kết nối mạng (cần tải Pyodide từ CDN).')}).then(function(){lock(false)})}
  bs.onclick=function(){judge(p.tests.filter(function(t){return t.pub}),8000,false)};
  bj.onclick=function(){judge(p.tests,8000,true)};
  cr.onclick=function(){if(busy)return;lock(true);status('Đang chạy…');PyJudge.run(ed.value,ci.value.replace(/\r/g,''),8000).then(function(r){res.innerHTML='';[['Kết quả',r.tle?'(quá 8 giây)':r.out||'(trống)']].concat(r.err?[['Thông báo lỗi',r.err]]:[]).forEach(function(x){res.appendChild(el('b',null,x[0]));var pr=el('pre');pr.textContent=x[1];res.appendChild(pr)});status('Xong ('+r.ms+' ms).')}).catch(function(e){status('Lỗi: '+(e&&e.message||e))}).then(function(){lock(false)})};
  window.scrollTo(0,0);
}
})();

/* Sổ lỗi & ôn tập cách quãng & bảng tiến độ toàn khóa. Đọc dữ liệu từ Store; nội dung câu hỏi lấy từ data/qbank/*.json */
(function(){
var root=document.getElementById('review');if(!root)return;
var META=JSON.parse(document.getElementById('review-meta').textContent),S=window.Store,cache={},tab='progress',sess=null,filt={m:'all',q:''};
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!==undefined)e.textContent=txt;return e}
function loadMod(m){if(cache[m])return Promise.resolve(cache[m]);return fetch('../../data/qbank/'+m+'.json').then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(d){var map={};d.items.forEach(function(it){map[it.id]=it});cache[m]=map;return map})}
function getQ(id,rec){if(rec&&rec.snap)return Promise.resolve(rec.snap);var m=id.split('-')[0];if(!META.mods[m])return Promise.resolve(null);return loadMod(m).then(function(map){return map[id]||null}).catch(function(){return null})}
var NAME={};Object.keys(META.mods).forEach(function(m){NAME[m]=META.mods[m].name});NAME.exam='Đề luyện tập';NAME.pl='Kiểm tra đầu vào';
function modLabel(m){return META.mods[m]?('M'+parseInt(m.slice(1),10)+' · '+META.mods[m].name):(NAME[m]||m)}
function pct(a,b){return b?Math.round(100*a/b):0}
function bar(p,cls){var o=el('div');o.style.cssText='height:10px;background:var(--border);border-radius:6px;overflow:hidden;min-width:120px';var i=el('div');i.style.cssText='height:100%;width:'+p+'%;background:'+(cls||'var(--accent2)');o.appendChild(i);return o}
function render(){root.innerHTML='';
  var tabs=el('div','row');[['progress','📊 Tiến độ toàn khóa'],['today','🔁 Ôn tập hôm nay'],['book','📓 Sổ lỗi'],['backup','💾 Sao lưu']].forEach(function(t){var b=el('button','btn'+(tab===t[0]?'':' alt'),t[1]);b.onclick=function(){tab=t[0];sess=null;render()};tabs.appendChild(b)});root.appendChild(tabs);
  var box=el('div');root.appendChild(box);
  if(tab==='progress')renderProgress(box);else if(tab==='today')renderToday(box);else if(tab==='book')renderBook(box);else renderBackup(box)}
function renderProgress(box){
  var st=S.stats(),due=S.due().length,wrong=S.wrong().length;
  var top=el('div','sim');top.innerHTML='<div class="simh">Tổng quan</div>';
  var kv=[['Câu đã làm',st.tot.items],['Tỉ lệ đúng (mọi lượt)',pct(st.tot.c,st.tot.n)+'%'],['Câu đang sai',wrong],['Đến hạn ôn lại',due],['Tự luận đã làm được',st.ess],['Chuỗi ngày học',st.streak+' ngày']];
  var g=el('div','grid');g.style.gridTemplateColumns='repeat(auto-fill,minmax(150px,1fr))';kv.forEach(function(x){var c=el('div','mod-card');c.style.cursor='default';c.innerHTML='<span class="num">'+x[0]+'</span><h3 style="font-size:1.4rem;margin:.2em 0">'+x[1]+'</h3>';g.appendChild(c)});top.appendChild(g);
  var go=el('button','btn','🔁 Ôn '+due+' câu đến hạn ngay');go.style.marginTop='10px';go.disabled=!due;go.onclick=function(){tab='today';render()};top.appendChild(go);box.appendChild(top);
  var tb=el('table','t left');tb.innerHTML='<tr><th>Module</th><th>Đã làm</th><th>Tiến độ</th><th>Tỉ lệ đúng</th><th>Đang sai</th><th>Tự luận</th><th></th></tr>';
  Object.keys(META.mods).forEach(function(m){var M=META.mods[m],b=st.by[m]||{items:0,correct:0,wrong:0,att:0,ok:0},st0=S.load(),ess=0;for(var k in st0.ess)if(k.indexOf(m+'-')===0)ess++;
    var tr=el('tr');var td=function(h){var c=el('td');if(typeof h==='string')c.innerHTML=h;else c.appendChild(h);tr.appendChild(c)};
    td('<a href="../modules/'+M.slug+'/index.html">M'+parseInt(m.slice(1),10)+' · '+M.name+'</a>');td(b.items+' / '+M.n);var pb=bar(pct(b.items,M.n));td(pb);td(b.att?pct(b.ok,b.att)+'%':'–');td(b.wrong?'<b style="color:var(--bad)">'+b.wrong+'</b>':'0');td(ess+' / '+M.e);td('<a href="../modules/'+M.slug+'/luyen-tap/index.html">Luyện →</a>');tb.appendChild(tr)});
  box.appendChild(el('h3',null,'Theo module'));var w=el('div');w.style.overflowX='auto';w.appendChild(tb);box.appendChild(w);
  /* chủ đề yếu */
  var weak=[];Object.keys(st.by).forEach(function(m){var t=st.by[m].topics;Object.keys(t).forEach(function(k){var x=t[k];if(x.n>=3&&x.c/x.n<0.6)weak.push({m:m,t:k,acc:x.c/x.n,n:x.n})})});weak.sort(function(a,b){return a.acc-b.acc});
  box.appendChild(el('h3',null,'Chủ đề cần củng cố (đúng < 60%, đã làm ≥ 3 lượt)'));
  if(!weak.length){box.appendChild(el('p','lead',st.tot.items?'Chưa có chủ đề nào dưới 60%. Tiếp tục phát huy!':'Chưa có dữ liệu. Hãy làm quiz hoặc ngân hàng câu hỏi; kết quả sẽ hiện ở đây.'))}
  else{var ul=el('ul');weak.slice(0,12).forEach(function(w0){var li=el('li');var M=META.mods[w0.m];li.innerHTML='<b>'+w0.t+'</b> ('+(M?('Module '+parseInt(w0.m.slice(1),10)):NAME[w0.m]||w0.m)+'): đúng '+Math.round(w0.acc*100)+'% / '+w0.n+' lượt'+(M?' — <a href="../modules/'+M.slug+'/index.html#chi-tiet">đọc lại ví dụ</a> · <a href="../modules/'+M.slug+'/luyen-tap/index.html">luyện tiếp</a>':'');ul.appendChild(li)});box.appendChild(ul)}
  /* lịch ôn */
  var s0=S.load(),now=Date.now(),b1=0,b3=0,b7=0,later=0;for(var id in s0.items){var it=s0.items[id];var d=S.dueAt(it)-now;if(S.isDue(it,now))continue;if(d<=86400000)b1++;else if(d<=3*86400000)b3++;else if(d<=7*86400000)b7++;else later++}
  box.appendChild(el('h3',null,'Lịch ôn sắp tới'));box.appendChild(el('p',null,'Hôm nay: '+due+' câu · trong 1 ngày tới: '+b1+' · 2–3 ngày: '+b3+' · 4–7 ngày: '+b7+' · muộn hơn: '+later+'. (Ôn cách quãng: đúng thì hẹn lại 1 → 3 → 7 → 14 → 30 ngày, sai thì quay về hộp 1.)'));
  /* hoạt động 14 ngày */
  var days=[],d0=new Date();for(var i=13;i>=0;i--){var x=new Date(d0);x.setDate(x.getDate()-i);var k=x.getFullYear()+'-'+('0'+(x.getMonth()+1)).slice(-2)+'-'+('0'+x.getDate()).slice(-2);days.push([k.slice(5),st.days[k]||0])}
  var mx=Math.max.apply(null,days.map(function(a){return a[1]}).concat([1])),ac=el('div');ac.style.cssText='display:flex;gap:4px;align-items:flex-end;height:70px;margin:8px 0';days.forEach(function(a){var c=el('div');c.title=a[0]+': '+a[1]+' lượt';c.style.cssText='flex:1;background:var(--accent2);opacity:'+(a[1]?1:.2)+';height:'+Math.max(4,Math.round(60*a[1]/mx))+'px;border-radius:3px';ac.appendChild(c)});
  box.appendChild(el('h3',null,'Hoạt động 14 ngày qua (số lượt trả lời)'));box.appendChild(ac)}
/* ---------- thẻ câu hỏi dùng chung ---------- */
function card(id,rec,q,onDone,opts){
  var c=el('div','qitem');var head=el('div');head.innerHTML='<span class="tag">'+id+'</span><span class="tag">'+modLabel((rec&&rec.m)||id.split('-')[0])+'</span>'+(q&&q.topic?'<span class="tag">'+q.topic+'</span>':'')+'<span class="tag">hộp '+((rec&&rec.box)||1)+'/6</span>';c.appendChild(head);
  var t=el('div','qtxt');t.style.cssText='font-weight:600;margin-top:6px';t.textContent=q.q;c.appendChild(t);
  var ex=el('div','explain');
  function show(ch){var os=c.querySelectorAll('.opt');[].forEach.call(os,function(o){o.dataset.done='1'});os[ch].classList.add(ch===q.correct?'correct':'wrong');if(ch!==q.correct)os[q.correct].classList.add('correct');ex.innerHTML='';var h=el('div',null,ch===q.correct?'✅ Chính xác!':'❌ Chưa đúng. Đáp án đúng: '+'ABCD'[q.correct]+'.');h.style.fontWeight='800';ex.appendChild(h);ex.appendChild(document.createTextNode(q.explain||''));ex.classList.add('show')}
  q.opts.forEach(function(o,oi){var b=el('button','opt','ABCD'[oi]+'. '+o);b.type='button';b.onclick=function(){if(b.dataset.done)return;var ok=oi===q.correct;S.record(id,ok,{m:id.split('-')[0],topic:q.topic,lvl:q.level,ch:oi});show(oi);if(onDone)onDone(ok)};c.appendChild(b)});
  c.appendChild(ex);if(opts&&opts.showPrev&&rec&&rec.ch!==undefined){show(rec.ch)}
  return c}
function renderToday(box){
  if(!sess){var ids=S.due(),st=S.load();ids.sort(function(a,b){var x=st.items[a],y=st.items[b];return (x.ok-y.ok)||((x.box||1)-(y.box||1))||(S.dueAt(x)-S.dueAt(y))});
    var intro=el('div','sim');intro.innerHTML='<div class="simh">Ôn tập hôm nay</div><p>Có <b>'+ids.length+'</b> câu đến hạn ôn (câu đang sai luôn đến hạn). Mỗi phiên tối đa 15 câu, ưu tiên câu sai trước.</p>';
    if(!ids.length){intro.innerHTML+='<p class="ok">Hôm nay không có câu nào đến hạn. Hãy làm thêm bài ở các module hoặc quay lại vào ngày mai.</p>';box.appendChild(intro);return}
    var go=el('button','btn','▶ Bắt đầu phiên ôn tập ('+Math.min(15,ids.length)+' câu)');go.onclick=function(){sess={ids:ids.slice(0,15),i:0,ok:0,done:0};render()};intro.appendChild(go);box.appendChild(intro);return}
  if(sess.i>=sess.ids.length){var f=el('div','sim');f.innerHTML='<div class="simh">Kết thúc phiên</div><p>Đã ôn <b>'+sess.done+'</b> câu, đúng <b>'+sess.ok+'</b> ('+pct(sess.ok,sess.done)+'%). Câu đúng được hẹn ôn lại sau 1–30 ngày tùy hộp; câu sai quay về hộp 1.</p>';var nb=el('button','btn','Xong');nb.onclick=function(){sess=null;render()};f.appendChild(nb);box.appendChild(f);return}
  var id=sess.ids[sess.i],rec=S.load().items[id];
  box.appendChild(el('p','lead','Câu '+(sess.i+1)+'/'+sess.ids.length+' · đúng '+sess.ok+'/'+sess.done));
  var slot=el('div');box.appendChild(slot);
  getQ(id,rec).then(function(q){if(!q){slot.appendChild(el('p','no','Không tải được nội dung câu '+id+' (cần mở qua máy chủ web).'));var sk=el('button','btn alt','Bỏ qua');sk.onclick=function(){sess.i++;render()};slot.appendChild(sk);return}
    var answered=false,c=card(id,rec,q,function(ok){answered=true;sess.done++;if(ok)sess.ok++;nx.disabled=false});slot.appendChild(c);
    var nx=el('button','btn',sess.i===sess.ids.length-1?'Hoàn thành ▶':'Câu tiếp ▶');nx.disabled=true;nx.onclick=function(){sess.i++;render()};slot.appendChild(nx);
    var sk=el('button','btn alt','Bỏ qua câu này');sk.style.marginLeft='6px';sk.onclick=function(){sess.i++;render()};slot.appendChild(sk)})}
function renderBook(box){
  var st=S.load(),ids=S.wrong();
  var f=el('div','row');var sm=el('select');var o0=el('option','', 'Mọi module');o0.value='all';sm.appendChild(o0);Object.keys(META.mods).concat(['exam','pl']).forEach(function(m){var n=ids.filter(function(i){return st.items[i].m===m||i.split('-')[0]===m}).length;if(n){var o=el('option',null,modLabel(m)+' ('+n+')');o.value=m;if(filt.m===m)o.selected=true;sm.appendChild(o)}});sm.onchange=function(){filt.m=sm.value;render()};f.appendChild(sm);
  var inp=el('input');inp.placeholder='Tìm trong câu hỏi…';inp.value=filt.q;inp.size=24;inp.oninput=function(){filt.q=inp.value};inp.onkeydown=function(e){if(e.key==='Enter')render()};f.appendChild(inp);var sb=el('button','btn alt','Tìm');sb.onclick=render;f.appendChild(sb);box.appendChild(f);
  if(filt.m!=='all')ids=ids.filter(function(i){return i.split('-')[0]===filt.m||st.items[i].m===filt.m});
  box.appendChild(el('p','lead',ids.length+' câu đang sai. Bấm đáp án để thử lại ngay; làm đúng là câu được đưa ra khỏi sổ lỗi.'));
  if(!ids.length){box.appendChild(el('p','ok','Sổ lỗi trống. Tuyệt vời!'));return}
  var by={};ids.forEach(function(i){var it=st.items[i],k=(it.m||i.split('-')[0])+'|'+(it.topic||'(khác)');(by[k]=by[k]||[]).push(i)});
  Object.keys(by).sort().forEach(function(k){var parts=k.split('|'),det=el('details');det.open=Object.keys(by).length<=4;var sum=el('summary',null,modLabel(parts[0])+' — '+parts[1]+' ('+by[k].length+')');sum.style.cssText='cursor:pointer;font-weight:700;margin:8px 0';det.appendChild(sum);
    by[k].forEach(function(id){var slot=el('div');det.appendChild(slot);getQ(id,st.items[id]).then(function(q){if(!q){return}
      if(filt.q&&q.q.toLowerCase().indexOf(filt.q.toLowerCase())<0){return}
      slot.appendChild(card(id,st.items[id],q,null,{showPrev:true}));var info=el('div',null,'Đã làm '+st.items[id].n+' lượt, đúng '+st.items[id].c+'.');info.style.cssText='font-size:.8rem;color:var(--muted);margin:-4px 0 8px';slot.appendChild(info)})});
    box.appendChild(det)})}
function renderBackup(box){
  var p=el('div','sim');p.innerHTML='<div class="simh">Sao lưu / khôi phục tiến độ</div><p>Tiến độ lưu trong trình duyệt này (localStorage) nên sẽ mất nếu xóa dữ liệu trình duyệt hoặc dùng cửa sổ ẩn danh, và không tự đồng bộ giữa các thiết bị. Hãy xuất file để lưu hoặc chuyển sang thiết bị khác.</p>';
  var ex=el('button','btn','⬇ Xuất tiến độ (JSON)');ex.onclick=function(){var a=el('a');a.href=URL.createObjectURL(new Blob([S.exportJSON()],{type:'application/json'}));a.download='trr1-tien-do-'+S.today()+'.json';a.click()};p.appendChild(ex);
  var fi=el('input');fi.type='file';fi.accept='application/json';fi.style.marginLeft='8px';fi.onchange=function(){var r=new FileReader();r.onload=function(){try{if(!confirm('Thay thế toàn bộ tiến độ hiện tại bằng file này?'))return;S.importJSON(r.result);alert('Đã nhập tiến độ.');render()}catch(e){alert('Lỗi: '+e.message)}};r.readAsText(fi.files[0])};p.appendChild(fi);
  var rs=el('button','btn alt','🗑 Xóa toàn bộ tiến độ');rs.style.marginLeft='8px';rs.onclick=function(){if(confirm('Xóa TOÀN BỘ tiến độ, sổ lỗi và kết quả kiểm tra đầu vào? Không thể hoàn tác.')){S.reset();render()}};p.appendChild(rs);box.appendChild(p)}
render();
})();

/* Thi thử Python có đồng hồ: chọn đề (đề cố định / ngẫu nhiên), đồng hồ theo mốc thời gian (reload không reset), bảng câu hỏi,
   chấm cuối bằng mọi test, xuất kết quả (tải JSON / sao chép), gửi về máy chủ nếu cấu hình, lịch sử các lần thi. */
(function(){
var root=document.getElementById('pyexam');if(!root)return;
var U=window.PyUI,el=U.el,META=JSON.parse(document.getElementById('py-meta').textContent);
var CUR='ptit-trr1:pyexam:cur',HIST='ptit-trr1:pyexam:hist',P=[],E=[],CFG={submitUrl:''},byId={},tick=null,ed=null,busy=false;
var LV={1:'Cơ bản',2:'Vừa',3:'Khó'},LIMIT=8000;
Promise.all([fetch('../../data/python/problems.json').then(function(r){return r.json()}),fetch('../../data/python/exams.json').then(function(r){return r.json()}),fetch('../../data/python/config.json').then(function(r){return r.json()}).catch(function(){return {submitUrl:''}})])
.then(function(a){P=a[0];E=a[1].sets;CFG=a[2]||CFG;P.forEach(function(p){byId[p.id]=p});boot()}).catch(function(e){root.textContent='Không tải được dữ liệu: '+e});
function boot(){var c=U.jget(CUR,null);if(c&&!c.done){if(Date.now()>=c.deadline)runExam(c,true);else runExam(c,false)}else start()}
function pad(n){return n<10?'0'+n:n}
function dt(ts){var d=new Date(ts);return pad(d.getDate())+'/'+pad(d.getMonth()+1)+'/'+d.getFullYear()+' '+pad(d.getHours())+':'+pad(d.getMinutes())}
/* ---------- màn hình chọn đề ---------- */
function start(){
  root.innerHTML='';if(tick){clearInterval(tick);tick=null}
  root.appendChild(el('h2',null,'Chọn đề thi thử'));
  var rules=el('div','callout');rules.innerHTML='<b class="t">Quy chế thi thử</b><ul><li>Đồng hồ đếm ngược theo mốc thời gian: tải lại trang hoặc đóng tab <b>không</b> làm đồng hồ dừng; hết giờ hệ thống tự chấm bằng mã hiện tại.</li><li>Không có gợi ý, không xem lời giải trong lúc thi. Nút “Chấm thử” chỉ cho biết đạt bao nhiêu test, <b>không lộ</b> dữ liệu và đáp án của test ẩn.</li><li>Điểm = Σ (số test đúng / tổng test) × điểm của bài; thang 10, chia đều các bài. Chỉ để tham khảo, không phải điểm thi thật.</li><li>Mỗi test giới hạn 8 giây trên trình duyệt (chậm hơn máy thật khoảng 2 đến 3 lần).</li></ul>';
  root.appendChild(rules);
  var opt=el('div','row');opt.appendChild(el('b',null,'Thời gian:'));
  var sel=el('select');[20,30,45,60,90,120].forEach(function(m){sel.appendChild(new Option(m+' phút',m))});sel.value='60';opt.appendChild(sel);
  var def=el('label');def.innerHTML='<input type="checkbox" id="pydef" checked> dùng thời gian gợi ý của đề';opt.appendChild(def);root.appendChild(opt);
  var g=el('div','grid');
  E.forEach(function(s){var a=el('a','mod-card');a.href='javascript:void 0';
    var levels=s.ids.map(function(i){return LV[byId[i].lv]}).join(' · ');
    a.innerHTML='<span class="num">'+s.minutes+' phút · '+s.ids.length+' bài</span><h3>'+s.title+'</h3><p>'+s.desc+'</p><p style="font-size:.82rem;color:var(--muted)">'+levels+'</p>';
    a.onclick=function(){begin(s.id,s.title,s.ids,document.getElementById('pydef').checked?s.minutes:+sel.value)};g.appendChild(a)});
  /* đề ngẫu nhiên */
  var rc=el('div','mod-card');rc.style.cursor='default';rc.innerHTML='<span class="num">ĐỀ NGẪU NHIÊN</span><h3>🎲 Tự bốc đề</h3><p>Chọn số bài; hệ thống bốc bài theo mức khó tăng dần, khác module.</p>';
  var rr=el('div','row');var nb=el('select');[3,4,5].forEach(function(n){nb.appendChild(new Option(n+' bài',n))});var go=el('button','btn','Bốc đề và bắt đầu');rr.appendChild(nb);rr.appendChild(go);rc.appendChild(rr);
  go.onclick=function(){var n=+nb.value,ids=randomSet(n);begin('random','Đề ngẫu nhiên',ids,document.getElementById('pydef').checked?20*n:+sel.value)};
  g.appendChild(rc);root.appendChild(g);
  var h=U.jget(HIST,[]);
  if(h.length){root.appendChild(el('h3',null,'Lịch sử thi thử'));var tb=el('table','t left');tb.innerHTML='<tr><th>Thời điểm</th><th>Đề</th><th>Điểm</th><th>Test đúng</th><th>Thời gian dùng</th></tr>';
    h.slice().reverse().forEach(function(x){var tr=el('tr');tr.innerHTML='<td>'+dt(x.finishedAt)+'</td><td>'+x.setTitle+'</td><td><b>'+x.score.toFixed(2)+'</b> / 10</td><td>'+x.passed+'/'+x.total+'</td><td>'+U.fmt(x.usedSec)+' / '+x.minutes+' phút</td>';tb.appendChild(tr)});
    var w=el('div');w.style.overflowX='auto';w.appendChild(tb);root.appendChild(w);
    var cl=el('button','btn alt','Xóa lịch sử');cl.onclick=function(){if(confirm('Xóa toàn bộ lịch sử thi thử?')){U.jset(HIST,[]);start()}};root.appendChild(cl)}
  var back=el('p');back.innerHTML='<a href="../lap-trinh-python/index.html">← Về luyện từng bài</a>';root.appendChild(back);
}
function randomSet(n){
  var pat={3:[1,2,3],4:[1,2,2,3],5:[1,2,2,3,3]}[n],used={},ids=[];
  pat.forEach(function(lv){var pool=P.filter(function(p){return p.lv===lv&&!used[p.mod]&&ids.indexOf(p.id)<0});if(!pool.length)pool=P.filter(function(p){return p.lv===lv&&ids.indexOf(p.id)<0});
    var p=pool[Math.floor(Math.random()*pool.length)];ids.push(p.id);used[p.mod]=1});return ids}
function begin(setId,title,ids,minutes){
  var now=Date.now();var c={aid:'a'+now,setId:setId,title:title,ids:ids,minutes:minutes,start:now,deadline:now+minutes*60000,code:{},graded:{},done:false,cur:0};
  U.jset(CUR,c);runExam(c,false)}
/* ---------- đang thi ---------- */
function save(c){U.jset(CUR,c)}
function runExam(c,expired){
  root.innerHTML='';var idx=c.cur||0,timer=el('div','py-timer','--:--');
  var bar=el('div','py-bar');bar.appendChild(el('b',null,c.title));bar.appendChild(timer);
  var pal=el('div','py-pal');bar.appendChild(pal);
  var fin=el('button','btn','Nộp bài');fin.style.marginLeft='auto';bar.appendChild(fin);root.appendChild(bar);
  var main=el('div');root.appendChild(main);
  function palette(){pal.innerHTML='';c.ids.forEach(function(id,i){var b=el('button',(i===idx?'cur ':'')+((c.graded[id]||{}).cls||''),(i+1)+'');b.title=byId[id].title;b.onclick=function(){go(i)};pal.appendChild(b)})}
  function go(i){idx=i;c.cur=i;save(c);show()}
  function show(){
    palette();main.innerHTML='';var p=byId[c.ids[idx]];var sp=el('div','py-split'),L=el('div','py-left'),Rr=el('div','py-right');sp.appendChild(L);sp.appendChild(Rr);main.appendChild(sp);
    L.appendChild(el('h2',null,'Bài '+(idx+1)+'/'+c.ids.length+': '+p.title));
    var s=el('div');s.innerHTML='<p>'+p.stmt+'</p><p><b>Dữ liệu vào.</b> '+p.inp+'</p><p><b>Kết quả.</b> '+p.out+'</p><p><b>Giới hạn.</b> '+p.cons+'</p>';L.appendChild(s);
    p.tests.filter(function(t){return t.pub}).forEach(function(t,i){var d=el('div','sim');d.innerHTML='<div class="simh">Ví dụ '+(i+1)+'</div>';var g=el('div');g.style.cssText='display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px';[['Vào',t.i],['Ra',t.o]].forEach(function(x){var q=el('div');q.appendChild(el('b',null,x[0]));var pr=el('div','py-out');pr.textContent=x[1];q.appendChild(pr);g.appendChild(q)});d.appendChild(g);L.appendChild(d)});
    var eb=el('div');Rr.appendChild(eb);var saveT=null;
    ed=U.makeEditor(eb,c.code[p.id]||p.starter,{onChange:function(v){c.code[p.id]=v;clearTimeout(saveT);saveT=setTimeout(function(){save(c)},400)},onRun:function(){bs.onclick()},onSubmit:function(){bg.onclick()}});
    var br=el('div','row');var bs=el('button','btn alt','▶ Chạy ví dụ'),bg=el('button','btn','✓ Chấm thử'),bc=el('button','btn alt','🧪 Input riêng');
    var pv=el('button','btn alt','‹ Bài trước'),nx=el('button','btn alt','Bài sau ›');pv.disabled=idx===0;nx.disabled=idx===c.ids.length-1;
    [bs,bg,bc,pv,nx].forEach(function(b){br.appendChild(b)});Rr.appendChild(br);pv.onclick=function(){go(idx-1)};nx.onclick=function(){go(idx+1)};
    var info=el('p','lead');info.textContent='Ctrl/Cmd+Enter: chạy ví dụ · Shift+Ctrl/Cmd+Enter: chấm thử.';Rr.appendChild(info);
    var cu=el('div');cu.style.display='none';var ci=el('textarea');ci.rows=4;ci.placeholder='Dữ liệu vào…';ci.style.cssText='width:100%;box-sizing:border-box;font:13px ui-monospace,Menlo,monospace;padding:8px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)';var cr=el('button','btn','Chạy');cu.appendChild(ci);cu.appendChild(cr);Rr.appendChild(cu);
    var res=el('div');Rr.appendChild(res);
    function lock(v){busy=v;[bs,bg,bc,cr].forEach(function(b){b.disabled=v})}
    bc.onclick=function(){cu.style.display=cu.style.display==='none'?'':'none';if(!ci.value)ci.value=p.tests[0].i};
    cr.onclick=function(){if(busy)return;lock(true);info.textContent='Đang chạy…';PyJudge.run(ed.get(),ci.value.replace(/\r/g,''),LIMIT).then(function(r){res.innerHTML='';[['Kết quả',r.tle?'(quá 8 giây)':r.out||'(trống)']].concat(r.err?[['Thông báo lỗi',r.err]]:[]).forEach(function(x){res.appendChild(el('b',null,x[0]));var o=el('div','py-out');o.textContent=x[1];res.appendChild(o)});info.textContent='Xong.'}).catch(function(e){info.textContent='Lỗi: '+(e&&e.message||e)}).then(function(){lock(false)})};
    function run(tests,record){if(busy)return;lock(true);info.textContent='Đang chạy… (lần đầu phải tải Python)';
      U.runTests(ed.get(),tests,LIMIT,function(rows){res.innerHTML='';res.appendChild(U.resultTable(rows,true))}).then(function(rows){info.textContent='Xong.';res.innerHTML='';res.appendChild(U.resultTable(rows,true));
        if(record){var ok=rows.filter(function(r){return r.v==='AC'}).length;c.graded[p.id]={p:ok,t:rows.length,cls:ok===rows.length?'ok':(ok?'part':'bad')};save(c);palette()}})
        .catch(function(e){info.textContent='Không chạy được Python: '+(e&&e.message||e)}).then(function(){lock(false)})}
    bs.onclick=function(){run(p.tests.filter(function(t){return t.pub}),false)};bg.onclick=function(){run(p.tests,true)};
    setTimeout(function(){ed.refresh()},80);
  }
  function update(){var left=(c.deadline-Date.now())/1000;timer.textContent=U.fmt(left);timer.className='py-timer'+(left<120?' bad':(left<Math.max(300,c.minutes*60*.15)?' warn':''));if(left<=0){clearInterval(tick);tick=null;finish(true)}}
  fin.onclick=function(){var left=Math.max(0,Math.round((c.deadline-Date.now())/60000));if(confirm('Nộp bài ngay? Còn khoảng '+left+' phút. Sau khi nộp không sửa được.'))finish(false)};
  function finish(auto){
    if(c.done)return;c.done=true;c.finishedAt=Math.min(Date.now(),c.deadline);save(c);window.removeEventListener('beforeunload',warn);
    if(ed)ed.readOnly(true);grade(c,auto)}
  function warn(e){e.preventDefault();e.returnValue=''}
  window.addEventListener('beforeunload',warn);
  if(expired){finish(true);return}
  show();update();if(tick)clearInterval(tick);tick=setInterval(update,500);
}
/* ---------- chấm cuối ---------- */
function grade(c,auto){
  root.innerHTML='';root.appendChild(el('h2',null,auto?'Hết giờ, đang chấm bài…':'Đang chấm bài…'));
  var info=el('p','lead','Chấm toàn bộ test (kể cả test ẩn). Lần đầu cần tải Python.');root.appendChild(info);var out=[];var i=0;
  function next(){
    if(i>=c.ids.length)return Promise.resolve();var p=byId[c.ids[i]];info.textContent='Đang chấm bài '+(i+1)+'/'+c.ids.length+': '+p.title+'…';
    return U.runTests(c.code[p.id]||p.starter,p.tests,LIMIT).then(function(rows){out.push({p:p,rows:rows});i++;return next()})}
  PyJudge.ready().then(next).then(function(){showResult(c,out)}).catch(function(e){info.textContent='Không chấm được: '+(e&&e.message||e)+'. Mã của bạn vẫn được giữ; tải lại trang để chấm lại.';c.done=false;save(c)});
}
function showResult(c,out){
  var per=10/c.ids.length,passed=0,total=0,score=0,probs=[];
  out.forEach(function(o){var ok=o.rows.filter(function(r){return r.v==='AC'}).length;passed+=ok;total+=o.rows.length;var pts=per*ok/o.rows.length;score+=pts;
    probs.push({id:o.p.id,title:o.p.title,passed:ok,total:o.rows.length,points:+pts.toFixed(3),verdicts:o.rows.map(function(r){return r.v}).join(','),code:c.code[o.p.id]||o.p.starter})});
  var used=Math.round((c.finishedAt-c.start)/1000);
  var rec={v:1,kind:'ptit-trr1-py-exam',attempt:c.aid,setId:c.setId,setTitle:c.title,minutes:c.minutes,startedAt:c.start,finishedAt:c.finishedAt,usedSec:used,score:+score.toFixed(3),max:10,passed:passed,total:total,problems:probs};
  var h=U.jget(HIST,[]);h=h.filter(function(x){return x.attempt!==c.aid});h.push({attempt:c.aid,setTitle:c.title,finishedAt:c.finishedAt,score:rec.score,passed:passed,total:total,usedSec:used,minutes:c.minutes});U.jset(HIST,h.slice(-30));
  root.innerHTML='';root.appendChild(el('h2',null,'Kết quả: '+c.title));
  var big=el('p');big.innerHTML='<span class="py-score">'+score.toFixed(2)+' / 10</span> &nbsp; '+passed+'/'+total+' test đúng · dùng '+U.fmt(used)+' / '+c.minutes+' phút';root.appendChild(big);
  var tb=el('table','t left');tb.innerHTML='<tr><th>Bài</th><th>Test đúng</th><th>Điểm</th><th>Từng test</th><th></th></tr>';
  probs.forEach(function(x,k){var tr=el('tr');tr.innerHTML='<td>'+(k+1)+'. '+x.title+'</td><td>'+x.passed+'/'+x.total+'</td><td>'+x.points.toFixed(2)+' / '+per.toFixed(2)+'</td><td>'+x.verdicts.split(',').map(function(v){return '<span class="py-ver '+v+'">'+v+'</span>'}).join('')+'</td><td><a href="../lap-trinh-python/index.html#'+x.id+'">xem lời giải</a></td>';tb.appendChild(tr)});
  var w=el('div');w.style.overflowX='auto';w.appendChild(tb);root.appendChild(w);
  var act=el('div','row');
  var dl=el('button','btn','💾 Tải kết quả (.json)');dl.onclick=function(){U.download('ket-qua-thi-thu-'+c.aid+'.json',JSON.stringify(withUser(rec),null,1))};
  var cp=el('button','btn alt','📋 Sao chép tóm tắt');cp.onclick=function(){var t='Thi thử Python TRR1 – '+c.title+'\nĐiểm: '+score.toFixed(2)+'/10 ('+passed+'/'+total+' test), '+U.fmt(used)+' / '+c.minutes+' phút\n'+probs.map(function(x,k){return (k+1)+'. '+x.title+': '+x.passed+'/'+x.total}).join('\n');
    (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){cp.textContent='✔ Đã sao chép'}).catch(function(){prompt('Sao chép thủ công:',t)})};
  var again=el('button','btn alt','🔁 Thi đề khác');again.onclick=function(){U.jset(CUR,null);start()};
  [dl,cp,again].forEach(function(b){act.appendChild(b)});root.appendChild(act);
  /* gửi về máy chủ (tùy chọn) */
  var box=el('div','sim');box.innerHTML='<div class="simh">Gửi kết quả về máy chủ (tùy chọn)</div>';root.appendChild(box);
  function withUser(r){var o=JSON.parse(JSON.stringify(r));o.name=(document.getElementById('pyname')||{}).value||'';o.sid=(document.getElementById('pysid')||{}).value||'';return o}
  if(!CFG.submitUrl){box.appendChild(el('p',null,'Trang này chưa được cấu hình máy chủ nhận bài nên kết quả chỉ nằm trong trình duyệt của bạn. Hãy tải file .json hoặc sao chép tóm tắt để gửi cho giảng viên/người tổ chức. (Người tổ chức: xem hướng dẫn nối Google Sheet bên dưới.)'))}
  else{
    box.innerHTML+='<p>Gửi điểm và <b>mã nguồn các bài</b> của bạn tới máy chủ của người tổ chức. Dữ liệu chỉ gồm các mục dưới đây; không gửi gì khác.</p><label>Họ tên: <input id="pyname" style="padding:5px 8px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text)"></label> <label>Mã SV: <input id="pysid" style="padding:5px 8px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text)"></label><p><label><input type="checkbox" id="pyok"> Tôi đồng ý gửi họ tên, mã SV, điểm và mã nguồn đến máy chủ của người tổ chức.</label></p>';
    var send=el('button','btn','📤 Gửi kết quả');var msg=el('p');box.appendChild(send);box.appendChild(msg);
    send.onclick=function(){if(!document.getElementById('pyok').checked){msg.textContent='Hãy tích ô đồng ý trước khi gửi.';return}
      send.disabled=true;msg.textContent='Đang gửi…';
      fetch(CFG.submitUrl,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(withUser(rec))}).then(function(){msg.textContent='Đã gửi (trình duyệt không cho đọc phản hồi của máy chủ khác miền nên không xác nhận được). Hãy giữ file .json làm bản dự phòng.';U.jset('ptit-trr1:pyexam:sent:'+c.aid,Date.now())}).catch(function(e){msg.textContent='Gửi thất bại: '+(e&&e.message||e)+'. Hãy tải file .json và gửi thủ công.';send.disabled=false})}}
  var home=el('p');home.innerHTML='<a href="../lap-trinh-python/index.html">← Về luyện từng bài</a>';root.appendChild(home);
}
})();

/* Ngân hàng câu hỏi: lọc nguồn/mức/chủ đề/chỉ câu sai/đến hạn ôn, phân trang, chấm ngay + giải thích,
   làm lại từng câu/toàn bộ, xáo trộn. Tiến độ ghi vào Store (dùng chung với Sổ lỗi & ôn tập). */
(function(){
var root=document.getElementById('bank');if(!root)return;
var D=JSON.parse(document.getElementById('bank-data').textContent),S=window.Store;
var state={level:'all',topic:'all',origin:'all',tab:'mcq',page:0,view:'all',order:D.items.map(function(_,i){return i}),size:15};
/* chuyển tiến độ cũ (nếu có) sang Store */
try{var old=JSON.parse(localStorage.getItem('bank:'+D.module)||'null');if(old&&old.ans){var st0=S.load();D.items.forEach(function(it){var v=old.ans[it.id];if(v!==undefined&&!st0.items[it.id])S.record(it.id,v===it.correct,{m:D.module,topic:it.topic,lvl:it.level,ch:v})});if(old.ess)for(var k in old.ess)S.setEssay(k,true);localStorage.removeItem('bank:'+D.module)}}catch(e){}
var topics=[];D.items.forEach(function(i){if(topics.indexOf(i.topic)<0)topics.push(i.topic)});
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!==undefined)e.textContent=txt;return e}
function rec(id){return S.load().items[id]}
function stats(){var st=S.load(),n=D.items.length,a=0,c=0;D.items.forEach(function(it){var r=st.items[it.id];if(r){a++;if(r.ok)c++}});return {n:n,a:a,c:c}}
function filtered(){var st=S.load(),now=Date.now();return state.order.map(function(i){return D.items[i]}).filter(function(it){
  if(state.origin!=='all'&&it.origin!==state.origin)return false;if(state.level!=='all'&&String(it.level)!==state.level)return false;if(state.topic!=='all'&&it.topic!==state.topic)return false;
  var r=st.items[it.id];
  if(state.view==='wrong')return !!r&&!r.ok;if(state.view==='todo')return !r;if(state.view==='due')return !!r&&S.isDue(r,now);return true})}
function statLine(){var st=stats();return 'Tiến độ: đã làm '+st.a+'/'+st.n+' câu · đúng '+st.c+' · sai '+(st.a-st.c)+(st.a?' · tỉ lệ đúng '+Math.round(100*st.c/st.a)+'%':'')}
function render(){
  root.innerHTML='';
  var top=el('div','sim');top.innerHTML='<div class="simh">Bảng điều khiển</div>';
  var row=el('div','row');
  function sel(lbl,opts,val,cb){var l=el('label');l.appendChild(document.createTextNode(lbl+' '));var s=el('select');opts.forEach(function(o){var op=el('option',null,o[1]);op.value=o[0];if(o[0]===val)op.selected=true;s.appendChild(op)});s.onchange=function(){cb(s.value)};l.appendChild(s);row.appendChild(l)}
  sel('Hiển thị:',[['all','Tất cả'],['todo','Chưa làm'],['wrong','Đã làm sai'],['due','Đến hạn ôn lại']],state.view,function(v){state.view=v;state.page=0;render()});
  sel('Nguồn:',[['all','Tất cả'],['goc','Câu gốc từ tài liệu ('+D.items.filter(function(i){return i.origin==='goc'}).length+')'],['tham_khao','Tham khảo ngoài PTIT ('+D.items.filter(function(i){return i.origin==='tham_khao'}).length+')'],['bo_sung','Bổ sung ('+D.items.filter(function(i){return i.origin==='bo_sung'}).length+')']],state.origin,function(v){state.origin=v;state.page=0;render()});
  sel('Mức độ:',[['all','Tất cả'],['1','Cơ bản (1)'],['2','Vừa (2)'],['3','Khó (3)']],state.level,function(v){state.level=v;state.page=0;render()});
  sel('Chủ đề:',[['all','Tất cả ('+D.items.length+')']].concat(topics.map(function(t){return [t,t+' ('+D.items.filter(function(i){return i.topic===t}).length+')']})),state.topic,function(v){state.topic=v;state.page=0;render()});
  top.appendChild(row);
  var row2=el('div','row');
  var b1=el('button','btn alt','🔀 Xáo trộn thứ tự');b1.onclick=function(){var o=state.order.slice();for(var i=o.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=o[i];o[i]=o[j];o[j]=t}state.order=o;state.page=0;render()};
  var b3=el('button','btn alt','⟲ Về thứ tự gốc');b3.onclick=function(){state.order=D.items.map(function(_,i){return i});state.page=0;render()};
  var b2=el('button','btn','↺ Làm lại toàn bộ module này');b2.onclick=function(){if(confirm('Xóa kết quả của ngân hàng này (kể cả các câu trong Sổ lỗi) và làm lại từ đầu?')){D.items.forEach(function(it){S.forget(it.id)});D.essays.forEach(function(e){S.setEssay(e.id,false)});state.page=0;render()}};
  var nb=el('a','btn alt','📓 Mở Sổ lỗi & ôn tập');nb.href='../../../so-loi/index.html';nb.style.textDecoration='none';
  row2.appendChild(b1);row2.appendChild(b3);row2.appendChild(b2);row2.appendChild(nb);top.appendChild(row2);
  top.appendChild(el('div','quiz-score',statLine()));
  root.appendChild(top);
  var tabs=el('div','row');[['mcq','Trắc nghiệm ('+D.items.length+')'],['ess','Tự luận ('+D.essays.length+')']].forEach(function(t){var b=el('button','btn'+(state.tab===t[0]?'':' alt'),t[1]);b.onclick=function(){state.tab=t[0];state.page=0;render()};tabs.appendChild(b)});root.appendChild(tabs);
  if(state.tab==='mcq')renderMcq();else renderEss();
}
function renderMcq(){
  var list=filtered(),pages=Math.max(1,Math.ceil(list.length/state.size));if(state.page>=pages)state.page=pages-1;
  root.appendChild(el('p','lead','Hiển thị '+list.length+' câu — trang '+(state.page+1)+'/'+pages));
  list.slice(state.page*state.size,(state.page+1)*state.size).forEach(function(it){
    var box=el('div','qitem');box.id=it.id;
    var head=el('div');head.innerHTML='<span class="tag">'+it.id+'</span><span class="tag">Môn: TRR1</span><span class="tag">'+it.topic+'</span><span class="tag'+(it.level===3?' exam':'')+'">mức '+it.level+'</span>';box.appendChild(head);
    var sr=el('div',null,(it.origin==='goc'?'📎 Câu gốc · ':(it.origin==='tham_khao'?'📚 Tham khảo ngoài PTIT · ':'➕ '))+it.src);sr.style.fontSize='.78rem';sr.style.color='var(--muted)';box.appendChild(sr);
    var t=el('div','qtxt');t.textContent=it.q;t.style.marginTop='6px';t.style.fontWeight='600';box.appendChild(t);
    var ex=el('div','explain'),r0=rec(it.id);
    function showResult(c){
      var opts=box.querySelectorAll('.opt');[].forEach.call(opts,function(o){o.dataset.done='1'});
      opts[c].classList.add(c===it.correct?'correct':'wrong');if(c!==it.correct)opts[it.correct].classList.add('correct');
      ex.innerHTML='';var h=el('div',null,c===it.correct?'✅ Chính xác!':'❌ Chưa đúng. Đáp án đúng: '+'ABCD'[it.correct]+'.');h.style.fontWeight='800';ex.appendChild(h);ex.appendChild(document.createTextNode(it.explain));ex.classList.add('show')}
    it.opts.forEach(function(o,oi){var b=el('button','opt','ABCD'[oi]+'. '+o);b.type='button';b.onclick=function(){if(b.dataset.done)return;S.record(it.id,oi===it.correct,{m:D.module,topic:it.topic,lvl:it.level,ch:oi});showResult(oi);var q=root.querySelector('.quiz-score');if(q)q.textContent=statLine()};box.appendChild(b)});
    box.appendChild(ex);
    var rb=el('button','btn alt','↺ Làm lại câu này');rb.type='button';rb.style.marginTop='6px';rb.onclick=function(){S.forget(it.id);render()};box.appendChild(rb);
    root.appendChild(box);
    if(r0&&r0.ch!==undefined)showResult(r0.ch);
  });
  var nav=el('div','row');
  var pv=el('button','btn alt','◀ Trang trước');pv.disabled=state.page===0;pv.onclick=function(){state.page--;render();window.scrollTo(0,0)};
  var nx=el('button','btn alt','Trang sau ▶');nx.disabled=state.page>=pages-1;nx.onclick=function(){state.page++;render();window.scrollTo(0,0)};
  nav.appendChild(pv);nav.appendChild(nx);root.appendChild(nav);
}
function renderEss(){
  var st=S.load();
  var list=D.essays.filter(function(e){return (state.origin==='all'||e.origin===state.origin)&&(state.level==='all'||String(e.level)===state.level)&&(state.topic==='all'||e.topic===state.topic)});
  root.appendChild(el('p','lead','Tự luận: hãy tự làm nháp trước, rồi bấm "Xem lời giải" để đối chiếu từng bước. Đánh dấu bài đã làm được để theo dõi tiến độ.'));
  var done=D.essays.filter(function(e){return st.ess[e.id]}).length;root.appendChild(el('div','quiz-score','Đã làm được '+done+'/'+D.essays.length+' bài tự luận'));
  list.forEach(function(e){
    var box=el('div','qitem');var head=el('div');head.innerHTML='<span class="tag">'+e.id+'</span><span class="tag">Môn: TRR1</span><span class="tag">'+e.topic+'</span><span class="tag'+(e.level===3?' exam':'')+'">mức '+e.level+'</span>';box.appendChild(head);
    var sr=el('div',null,(e.origin==='goc'?'📎 Câu gốc · ':(e.origin==='tham_khao'?'📚 Tham khảo ngoài PTIT · ':'➕ '))+e.src);sr.style.fontSize='.78rem';sr.style.color='var(--muted)';box.appendChild(sr);
    var t=el('div','qtxt');t.textContent=e.q;t.style.fontWeight='600';t.style.marginTop='6px';box.appendChild(t);
    var sol=el('div','explain');sol.textContent=e.sol;box.appendChild(sol);
    var sb=el('button','btn alt','👁 Xem lời giải');sb.type='button';sb.onclick=function(){sol.classList.toggle('show');sb.textContent=sol.classList.contains('show')?'🙈 Ẩn lời giải':'👁 Xem lời giải'};
    var on=!!st.ess[e.id];var mk=el('button','btn'+(on?'':' alt'),on?'✔ Đã làm được (bấm để bỏ)':'Đánh dấu: tôi đã làm được');mk.type='button';mk.style.marginLeft='6px';mk.onclick=function(){S.setEssay(e.id,!on);render()};
    box.appendChild(sb);box.appendChild(mk);root.appendChild(box)});
}
render();
})();

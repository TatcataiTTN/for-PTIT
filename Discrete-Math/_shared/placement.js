/* Kiểm tra đầu vào: mỗi kỹ năng chọn ngẫu nhiên PER câu từ ngân hàng, xáo phương án, chấm điểm theo kỹ năng, gợi ý lộ trình. */
(function(){
var root=document.getElementById('placement');if(!root)return;
var D=JSON.parse(document.getElementById('placement-data').textContent),S=window.Store,PER=3,qs=[],ans={},done=false;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function shuf(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
function start(){qs=[];ans={};done=false;D.skills.forEach(function(sk){shuf(sk.qs.map(function(q,i){return i})).slice(0,PER).forEach(function(i){var q=sk.qs[i],o=shuf([q.ans].concat(q.wrong));qs.push({sk:sk.id,id:'pl-'+sk.id+'-'+i,q:q.q,opts:o,c:o.indexOf(q.ans),expl:q.expl})})});qs=shuf(qs);render()}
function render(){root.innerHTML='';
  var h=el('div','row');h.appendChild(el('span','badge',qs.length+' câu · '+D.skills.length+' kỹ năng · không giới hạn thời gian'));root.appendChild(h);
  qs.forEach(function(q,i){var c=el('div','q');c.appendChild(el('p',null,(i+1)+'. '+q.q));var wrap=el('div','opts');
    q.opts.forEach(function(o,k){var b=el('button','opt',String.fromCharCode(65+k)+'. '+o);if(ans[i]===k)b.style.borderColor='var(--accent)';
      if(done){b.disabled=true;if(k===q.c)b.className+=' correct';else if(ans[i]===k)b.className+=' wrong'}
      b.onclick=function(){if(done)return;ans[i]=k;render()};wrap.appendChild(b)});c.appendChild(wrap);
    if(done){var e=el('div','explain show',(ans[i]===q.c?'✔ Đúng. ':(ans[i]===undefined?'Chưa trả lời. ':'✘ Sai. '))+q.expl);c.appendChild(e)}root.appendChild(c)});
  var bar=el('div','row');
  if(!done){var n=Object.keys(ans).length,b=el('button','btn','Nộp bài ('+n+'/'+qs.length+')');b.onclick=submit;bar.appendChild(b)}
  var r=el('button','btn alt','🔄 Đổi bộ câu / làm lại');r.onclick=function(){window.scrollTo(0,0);start()};bar.appendChild(r);root.appendChild(bar);
  if(done)result()}
function submit(){done=true;var res={},st={};qs.forEach(function(q,i){var ok=ans[i]===q.c;(st[q.sk]=st[q.sk]||{n:0,c:0}).n++;if(ok)st[q.sk].c++;
  if(S)try{S.record(q.id,ok,{m:'pl',topic:q.sk,lvl:1,snap:{q:q.q,opts:q.opts,correct:q.c,explain:q.expl}})}catch(e){}});
  Object.keys(st).forEach(function(k){res[k]=Math.round(100*st[k].c/st[k].n)});if(S&&S.setPlacement)try{S.setPlacement({t:Date.now(),res:res})}catch(e){}
  window.__pl=st;render();root.scrollIntoView()}
function result(){var st=window.__pl,box=el('div','sim');box.innerHTML='<div class="simh">Kết quả theo kỹ năng</div>';
  var tb=el('table','t left');tb.innerHTML='<tr><th>Kỹ năng</th><th>Đúng</th><th>Đánh giá</th><th>Nên làm</th></tr>';var weak={},total=0,okn=0;
  D.skills.forEach(function(sk){var s=st[sk.id]||{n:0,c:0};total+=s.n;okn+=s.c;var p=s.n?s.c/s.n:0,lv=p>=1?'Vững':(p>=0.67?'Khá':'Cần ôn'),tr=el('tr');
    tr.innerHTML='<td>'+sk.name+'</td><td>'+s.c+'/'+s.n+'</td><td>'+(p>=1?'🟢 ':p>=0.67?'🟡 ':'🔴 ')+lv+'</td><td>'+(p<0.67?sk.refresh:'—')+'</td>';tb.appendChild(tr);
    if(p<0.67)sk.mods.forEach(function(m){weak[m]=(weak[m]||0)+1})});
  box.appendChild(el('p',null,'Tổng: '+okn+'/'+total+' câu đúng.'));var w=el('div');w.style.overflowX='auto';w.appendChild(tb);box.appendChild(w);
  var ms=Object.keys(weak).sort();box.appendChild(el('h3',null,'Lộ trình đề xuất'));
  if(!ms.length){box.appendChild(el('p',null,'Nền tảng tốt. Bạn có thể học theo thứ tự Module 1 → 13.'))}
  else{var p=el('p');p.innerHTML='Ôn trước các module nền: '+ms.map(function(m){var n=parseInt(m.slice(1),10);return '<a href="../modules/'+D.slugs[m]+'/index.html">Module '+n+'</a>'}).join(', ')+'. Sau đó học theo thứ tự thông thường; những mục “Cần ôn” ở trên là lý do chọn các module này.';box.appendChild(p)}
  box.appendChild(el('p','lead','Kết quả được lưu trong trình duyệt (và hiện ở trang Sổ lỗi). Câu sai tự vào Sổ lỗi để ôn cách quãng.'));root.appendChild(box)}
start()})();

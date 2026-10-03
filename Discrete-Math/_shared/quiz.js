/* Quiz nhanh trong trang module: rút 10 câu từ kho ~40 câu, có nút "Đổi bộ câu hỏi", 3 chế độ chọn câu,
   chấm ngay + luôn giải thích, làm lại từng câu / cả bài. Kết quả ghi vào Store (Sổ lỗi & ôn tập). */
(function(){
  var S=window.Store;
  document.querySelectorAll('script.quiz-data').forEach(function(dataEl){
    var D=JSON.parse(dataEl.textContent),root=document.getElementById(dataEl.getAttribute('data-root'));if(!root)return;
    var PICK=D.pick||10,mode='random',cur=[],seen={},fixedSet=null;
    function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
    function choose(){
      if(fixedSet){var k=fixedSet;fixedSet=null;return k}
      var st=S?S.load():{items:{}},now=Date.now(),pool=D.items.slice();
      var score=function(it){var r=st.items[it.id];
        if(mode==='todo')return r?1:0;
        if(mode==='review'){if(!r)return 1;return S.isDue(r,now)?(r.ok?0.3:0):2}
        return 0};
      pool=shuffle(pool);
      pool.forEach(function(it){it._s=score(it)+(seen[it.id]?0.5:0)});
      pool.sort(function(a,b){return a._s-b._s});
      var pick=[],byLv={1:[],2:[],3:[]};pool.forEach(function(it){byLv[it.level||2].push(it)});
      var want=[1,1,2,2,2,3,3,2,1,3];
      for(var i=0;i<PICK;i++){var lv=want[i%want.length],c=byLv[lv].shift()||byLv[2].shift()||byLv[1].shift()||byLv[3].shift();if(c)pick.push(c)}
      return shuffle(pick)}
    function build(){
      cur=choose();cur.forEach(function(it){seen[it.id]=1});root.innerHTML='';var score=0,done=0;
      var ctl=document.createElement('div');ctl.className='row';ctl.style.marginBottom='8px';
      var lab=document.createElement('label');lab.appendChild(document.createTextNode('Chọn câu: '));
      var sel=document.createElement('select');[['random','Ngẫu nhiên'],['todo','Ưu tiên câu chưa làm'],['review','Ưu tiên câu sai / đến hạn ôn']].forEach(function(o){var op=document.createElement('option');op.value=o[0];op.textContent=o[1];if(o[0]===mode)op.selected=true;sel.appendChild(op)});
      sel.onchange=function(){mode=sel.value;build()};lab.appendChild(sel);ctl.appendChild(lab);
      var nb=document.createElement('button');nb.type='button';nb.className='btn alt';nb.textContent='🔀 Đổi bộ câu hỏi';nb.onclick=function(){if(done>0&&done<cur.length&&!confirm('Bộ này chưa làm xong. Vẫn đổi bộ mới?'))return;build()};ctl.appendChild(nb);
      var info=document.createElement('span');info.style.fontSize='.82rem';info.style.color='var(--muted)';info.textContent='Kho '+D.items.length+' câu của module này; mỗi lần rút '+PICK+' câu.';ctl.appendChild(info);
      root.appendChild(ctl);
      var bar=document.createElement('div');bar.className='quiz-score';root.appendChild(bar);
      function upd(){bar.textContent='Điểm: '+score+'/'+cur.length+'  ('+done+'/'+cur.length+' câu đã làm)'}
      cur.forEach(function(q,qi){
        var box=document.createElement('div');box.className='qitem';
        var t=document.createElement('div');t.className='qtxt';var b=document.createElement('b');b.textContent=(qi+1)+'. ';t.appendChild(b);t.appendChild(document.createTextNode(q.q));box.appendChild(t);
        var ex=document.createElement('div');ex.className='explain';ex.textContent=q.explain||'';
        var answered=false;
        q.opts.forEach(function(opt,oi){
          var btn=document.createElement('button');btn.type='button';btn.className='opt';btn.textContent='ABCD'[oi]+'. '+opt;
          btn.addEventListener('click',function(){
            if(btn.dataset.done)return;
            [].forEach.call(box.querySelectorAll('.opt'),function(x){x.dataset.done='1'});
            var ok=oi===q.correct;btn.classList.add(ok?'correct':'wrong');
            if(!ok)box.querySelectorAll('.opt')[q.correct].classList.add('correct');
            var head=document.createElement('div');head.style.fontWeight='800';head.textContent=ok?'✅ Chính xác!':'❌ Chưa đúng. Đáp án đúng: '+'ABCD'[q.correct]+'.';
            ex.insertBefore(head,ex.firstChild);ex.classList.add('show');if(ok)score++;done++;answered=ok?1:2;upd();
            if(S&&q.id)S.record(q.id,ok,{m:q.m,topic:q.topic,lvl:q.level,ch:oi});
          });box.appendChild(btn);
        });
        var rb=document.createElement('button');rb.type='button';rb.className='btn alt';rb.style.marginTop='6px';rb.textContent='↺ Làm lại câu này';
        rb.addEventListener('click',function(){if(!answered)return;if(answered===1)score--;done--;answered=false;
          [].forEach.call(box.querySelectorAll('.opt'),function(x){x.classList.remove('correct','wrong');delete x.dataset.done});
          ex.classList.remove('show');ex.textContent=q.explain||'';if(S&&q.id)S.forget(q.id);upd();});
        box.appendChild(ex);box.appendChild(rb);root.appendChild(box);
      });
      var r=document.createElement('button');r.type='button';r.className='btn';r.textContent='↺ Làm lại toàn bộ bài (giữ bộ câu hiện tại)';
      r.addEventListener('click',function(){if(done>0&&!confirm('Xóa kết quả của bộ này và làm lại?'))return;cur.forEach(function(q){if(S&&q.id)S.forget(q.id)});fixedSet=cur.slice();build();});root.appendChild(r);
      var nl=document.createElement('a');nl.href='luyen-tap/index.html';nl.className='btn alt';nl.style.textDecoration='none';nl.style.marginLeft='6px';nl.textContent='Luyện sâu hơn với ngân hàng →';root.appendChild(nl);
      upd();
    }
    build();
  });
})();

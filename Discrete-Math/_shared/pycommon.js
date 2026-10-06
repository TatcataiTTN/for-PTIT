/* Tiện ích dùng chung cho luyện code và thi thử Python: DOM, lưu trữ, trình soạn thảo (CodeMirror, có dự phòng textarea), chạy test, bảng kết quả. */
(function(){
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function jget(k,d){try{var v=JSON.parse(localStorage.getItem(k));return v==null?d:v}catch(e){return d}}
function jset(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function sget(k){try{return localStorage.getItem(k)}catch(e){return null}}
function sset(k,v){try{localStorage.setItem(k,v)}catch(e){}}
function norm(s){var L=String(s).replace(/\r/g,'').split('\n').map(function(x){return x.replace(/\s+$/,'')});while(L.length&&L[L.length-1]==='')L.pop();return L.join('\n')}
function verdict(t,r){if(r.tle)return 'TLE';if(r.err)return 'RE';return norm(r.out)===norm(t.o)?'AC':'WA'}
var LAB={AC:'✅ Đúng',WA:'❌ Sai kết quả',RE:'💥 Lỗi chạy',TLE:'⏱ Quá giờ'};
function makeEditor(parent,value,o){
  o=o||{};var api;
  if(window.CodeMirror){
    var keys={Tab:function(c){if(c.somethingSelected())c.indentSelected('add');else c.replaceSelection('    ','end')},'Shift-Tab':function(c){c.indentSelected('subtract')}};
    if(o.onRun){keys['Ctrl-Enter']=o.onRun;keys['Cmd-Enter']=o.onRun}
    if(o.onSubmit){keys['Shift-Ctrl-Enter']=o.onSubmit;keys['Shift-Cmd-Enter']=o.onSubmit}
    var cm=CodeMirror(parent,{value:value,mode:'python',theme:'ptit',lineNumbers:true,indentUnit:4,tabSize:4,indentWithTabs:false,matchBrackets:true,autoCloseBrackets:true,styleActiveLine:true,lineWrapping:false,extraKeys:keys,viewportMargin:Infinity});
    cm.on('change',function(){o.onChange&&o.onChange(cm.getValue())});
    api={get:function(){return cm.getValue()},set:function(v){cm.setValue(v)},focus:function(){cm.focus()},readOnly:function(b){cm.setOption('readOnly',b?'nocursor':false)},refresh:function(){cm.refresh()}};
    setTimeout(function(){cm.refresh()},50);
  }else{
    var ta=el('textarea');ta.spellcheck=false;ta.rows=16;ta.value=value;
    ta.style.cssText='width:100%;box-sizing:border-box;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;padding:10px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);tab-size:4;white-space:pre';
    ta.oninput=function(){o.onChange&&o.onChange(ta.value)};
    ta.onkeydown=function(e){if(e.key==='Tab'){e.preventDefault();var a=ta.selectionStart;ta.value=ta.value.slice(0,a)+'    '+ta.value.slice(ta.selectionEnd);ta.selectionStart=ta.selectionEnd=a+4;ta.oninput()}
      else if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();(e.shiftKey?o.onSubmit:o.onRun)&&(e.shiftKey?o.onSubmit:o.onRun)()}};
    parent.appendChild(ta);
    api={get:function(){return ta.value},set:function(v){ta.value=v},focus:function(){ta.focus()},readOnly:function(b){ta.readOnly=!!b},refresh:function(){}};
  }
  return api;
}
/* chạy lần lượt các test; onProgress(rows) sau mỗi test; trả Promise(rows) */
function runTests(code,tests,limit,onProgress){
  return PyJudge.ready().then(function(){
    var rows=[],chain=Promise.resolve();
    tests.forEach(function(t){chain=chain.then(function(){return PyJudge.run(code,t.i,limit).then(function(r){rows.push({t:t,r:r,v:verdict(t,r),limit:limit});onProgress&&onProgress(rows)})})});
    return chain.then(function(){return rows})});
}
/* bảng kết quả; hide=true: không lộ vào/ra của test ẩn (chế độ thi) */
function resultTable(rows,hide){
  var box=el('div');var ok=rows.filter(function(r){return r.v==='AC'}).length;
  var head=el('p');head.innerHTML='<b>'+ok+' / '+rows.length+' test đúng</b>';box.appendChild(head);
  var strip=el('p');rows.forEach(function(r){var s=el('span','py-ver '+r.v,r.v);s.title=(r.t.pub?'ví dụ':'ẩn');strip.appendChild(s)});box.appendChild(strip);
  var tb=el('table','t left');tb.innerHTML='<tr><th>Test</th><th>Loại</th><th>Kết quả</th><th>Thời gian</th></tr>';
  var firstBad=rows.findIndex(function(x){return x.v!=='AC'&&(!hide||x.t.pub)});
  rows.forEach(function(r,i){var tr=el('tr');tr.innerHTML='<td>'+(i+1)+'</td><td>'+(r.t.pub?'ví dụ':'ẩn')+'</td><td>'+LAB[r.v]+'</td><td>'+(r.r.tle?'> '+r.limit/1000+' s':r.r.ms+' ms')+'</td>';tb.appendChild(tr);
    if(r.v!=='AC'&&(!hide||r.t.pub)){var td=el('tr'),c=el('td');c.colSpan=4;var d=el('details');d.open=(i===firstBad);d.appendChild(el('summary',null,'Chi tiết test '+(i+1)));
      [['Dữ liệu vào',r.t.i],['Kết quả đúng',r.t.o],['Kết quả của bạn',r.r.out||'(trống)']].concat(r.r.err?[['Thông báo lỗi',r.r.err]]:[]).forEach(function(x){d.appendChild(el('b',null,x[0]));var pr=el('div','py-out');pr.textContent=x[1].length>2000?x[1].slice(0,2000)+'\n…(cắt bớt)':x[1];d.appendChild(pr)});
      c.appendChild(d);td.appendChild(c);tb.appendChild(td)}});
  var w=el('div');w.style.overflowX='auto';w.appendChild(tb);box.appendChild(w);return box;
}
function download(name,text,type){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:type||'application/json'}));a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
function fmt(sec){sec=Math.max(0,Math.floor(sec));var m=Math.floor(sec/60),s=sec%60;return (m<10?'0':'')+m+':'+(s<10?'0':'')+s}
window.PyUI={el:el,jget:jget,jset:jset,sget:sget,sset:sset,norm:norm,verdict:verdict,makeEditor:makeEditor,runTests:runTests,resultTable:resultTable,download:download,fmt:fmt,LAB:LAB};
})();

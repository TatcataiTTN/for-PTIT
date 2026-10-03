/* Kho tiến độ dùng chung (localStorage). Mọi thành phần (quiz, ngân hàng, đề, kiểm tra đầu vào) ghi vào đây;
   trang "Sổ lỗi & ôn tập" đọc ra. Lược đồ: {v:1, items:{id:{m,topic,lvl,n,c,last,box,ok,snap?}}, ess:{id:1}, placement:{}, days:{YYYY-MM-DD:n}} */
(function(root){
var KEY='ptit-trr1:v1',INTERVAL=[0,0,1,3,7,14,30]; /* ngày, theo hộp 1..6 */
function today(){var d=new Date();return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
function load(){try{var s=JSON.parse(localStorage.getItem(KEY)||'null');if(s&&s.v===1)return s}catch(e){}return {v:1,items:{},ess:{},placement:null,days:{}}}
function save(s){try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}}
var Store={
  KEY:KEY,load:load,save:save,today:today,
  /* ghi nhận một lần trả lời; meta: {m,topic,lvl,snap} (snap: bản sao câu hỏi cho câu không có trong ngân hàng) */
  record:function(id,ok,meta){var s=load(),it=s.items[id]||{n:0,c:0,box:0};meta=meta||{};
    if(meta.ch!==undefined)it.ch=meta.ch;it.m=meta.m||it.m;it.topic=meta.topic||it.topic;it.lvl=meta.lvl||it.lvl;if(meta.snap)it.snap=meta.snap;
    it.n++;if(ok)it.c++;it.ok=!!ok;it.last=Date.now();
    if(!ok)it.box=1;else it.box=it.box?Math.min(it.box+1,6):3;
    s.items[id]=it;var d=today();s.days[d]=(s.days[d]||0)+1;save(s);return it},
  forget:function(id){var s=load();delete s.items[id];save(s)},
  setEssay:function(id,on){var s=load();if(on)s.ess[id]=1;else delete s.ess[id];save(s)},
  dueAt:function(it){return (it.last||0)+INTERVAL[it.box||1]*86400000},
  isDue:function(it,now){return !it.ok||Store.dueAt(it)<=(now||Date.now())},
  wrong:function(){var s=load(),o=[];for(var id in s.items)if(!s.items[id].ok)o.push(id);return o},
  due:function(now){var s=load(),o=[];for(var id in s.items){var it=s.items[id];if(Store.isDue(it,now))o.push(id)}return o},
  streak:function(){var s=load(),d=new Date(),n=0;function k(x){return x.getFullYear()+'-'+('0'+(x.getMonth()+1)).slice(-2)+'-'+('0'+x.getDate()).slice(-2)}
    if(!s.days[k(d)])d.setDate(d.getDate()-1);while(s.days[k(d)]){n++;d.setDate(d.getDate()-1)}return n},
  /* thống kê theo module và chủ đề */
  stats:function(){var s=load(),by={},tot={n:0,c:0,items:0};
    for(var id in s.items){var it=s.items[id],m=it.m||id.split('-')[0];by[m]=by[m]||{items:0,correct:0,wrong:0,att:0,ok:0,topics:{}};
      var b=by[m];b.items++;if(it.ok)b.correct++;else b.wrong++;b.att+=it.n;b.ok+=it.c;
      var t=it.topic||'(khác)';b.topics[t]=b.topics[t]||{n:0,c:0,items:0,okItems:0};b.topics[t].n+=it.n;b.topics[t].c+=it.c;b.topics[t].items++;if(it.ok)b.topics[t].okItems++;
      tot.n+=it.n;tot.c+=it.c;tot.items++}
    return {by:by,tot:tot,ess:Object.keys(s.ess).length,streak:Store.streak(),days:s.days}},
  exportJSON:function(){return JSON.stringify(load())},
  importJSON:function(txt){var o=JSON.parse(txt);if(!o||o.v!==1||typeof o.items!=='object')throw new Error('File không đúng định dạng');save(o)},
  reset:function(){try{localStorage.removeItem(KEY)}catch(e){}},
  setPlacement:function(p){var s=load();s.placement=p;save(s)},
  getPlacement:function(){return load().placement}
};
root.Store=Store;
})(window);

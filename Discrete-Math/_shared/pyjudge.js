/* Chạy Python ngay trong trình duyệt (Pyodide/WebAssembly) trong Web Worker để có thể ngắt khi quá giờ.
   API: PyJudge.run(code,input,ms) -> Promise({out,err,ms,tle}); PyJudge.ready() ; PyJudge.state */
(function(){
var PYODIDE='https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
var SETUP=[
'import sys, io, json, time, traceback',
'sys.setrecursionlimit(6000)',
'def _run(code, inp):',
'    o_in, o_out, o_err = sys.stdin, sys.stdout, sys.stderr',
'    sys.stdin = io.StringIO(inp); buf = io.StringIO(); sys.stdout = buf; sys.stderr = buf',
'    err = ""; t = time.time()',
'    try:',
'        exec(compile(code, "main.py", "exec"), {"__name__": "__main__"})',
'    except SystemExit:',
'        pass',
'    except BaseException:',
'        tb = traceback.format_exc().splitlines()',
'        i = next((k for k, l in enumerate(tb) if "main.py" in l), None)',
'        err = ("Traceback (most recent call last):\\n" + "\\n".join(tb[i:])) if i is not None else "\\n".join(tb[-1:])',
'    finally:',
'        sys.stdin, sys.stdout, sys.stderr = o_in, o_out, o_err',
'    return json.dumps({"out": buf.getvalue()[:200000], "err": err, "ms": int((time.time() - t) * 1000)})'
].join('\n');
var WORKER='importScripts('+JSON.stringify(PYODIDE+'pyodide.js')+');\n'+
'var py=null,ready=null;var SETUP='+JSON.stringify(SETUP)+';\n'+
'function init(){if(!ready)ready=loadPyodide({indexURL:'+JSON.stringify(PYODIDE)+'}).then(function(p){py=p;py.runPython(SETUP)});return ready}\n'+
'onmessage=function(e){var m=e.data;init().then(function(){\n'+
' if(m.type==="init"){postMessage({type:"ready"});return}\n'+
' py.globals.set("_c",m.code);py.globals.set("_i",m.input);var r=py.runPython("_run(_c,_i)");postMessage({type:"result",id:m.id,res:r});\n'+
'}).catch(function(err){postMessage({type:"fatal",id:m.id,msg:String(err)})})};';
var worker=null,readyP=null,seq=0,pending={},api={state:'idle'};
function spawn(){
  var url=URL.createObjectURL(new Blob([WORKER],{type:'text/javascript'}));
  worker=new Worker(url);api.state='loading';
  readyP=new Promise(function(res,rej){
    worker.onmessage=function(e){var m=e.data;
      if(m.type==='ready'){api.state='ready';res()}
      else if(m.type==='result'){var p=pending[m.id];if(p){delete pending[m.id];clearTimeout(p.t);var r=JSON.parse(m.res);r.tle=false;p.res(r)}}
      else if(m.type==='fatal'){api.state='error';var p2=m.id&&pending[m.id];if(p2){delete pending[m.id];clearTimeout(p2.t);p2.res({out:'',err:'Lỗi môi trường Python: '+m.msg,ms:0,tle:false})}else rej(new Error(m.msg))}};
    worker.onerror=function(ev){api.state='error';rej(new Error(ev.message||'worker error'))};
    worker.postMessage({type:'init'});
  });
  return readyP;
}
api.ready=function(){if(!worker)spawn();return readyP};
api.run=function(code,input,ms){
  return api.ready().then(function(){return new Promise(function(res){
    var id=++seq,w=worker;
    var t=setTimeout(function(){delete pending[id];try{w.terminate()}catch(e){}worker=null;readyP=null;api.state='idle';res({out:'',err:'',ms:ms,tle:true})},ms||8000);
    pending[id]={res:res,t:t};w.postMessage({type:'run',id:id,code:code,input:input});
  })});
};
api.stop=function(){if(worker){try{worker.terminate()}catch(e){}worker=null;readyP=null;api.state='idle'}};
window.PyJudge=api;
})();

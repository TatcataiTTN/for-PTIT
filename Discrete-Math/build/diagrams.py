import os, html, subprocess
OUT=os.path.join(os.path.dirname(__file__),'..','assets','diagrams')
PAL={'blue':('#dae8fc','#6c8ebf'),'yellow':('#fff2cc','#d6b656'),'green':('#d5e8d4','#82b366'),'red':('#f8cecc','#b85450'),'purple':('#e1d5e7','#9673a6'),'orange':('#ffe6cc','#d79b00'),'grey':('#f5f5f5','#666666')}
class D:
    def __init__(self,name,w=1100,h=700): self.name=name; self.cells=[]; self.n=2; self.w=w; self.h=h
    def _id(self): self.n+=1; return f'c{self.n}'
    def box(self,x,y,w,h,text,color='blue',bold=False,fs=14,rounded=True,extra=''):
        i=self._id(); f,s=PAL[color]
        st=f'rounded={1 if rounded else 0};whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontSize={fs};fontFamily=PT Sans;'+('fontStyle=1;' if bold else '')+extra
        self.cells.append(f'<mxCell id="{i}" value="{html.escape(text,quote=True).replace(chr(10),"&#10;")}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'); return i
    def text(self,x,y,w,h,text,fs=13,bold=False,color='#333333',align='center'):
        i=self._id(); st=f'text;html=1;align={align};verticalAlign=middle;fillColor=none;strokeColor=none;fontSize={fs};fontFamily=PT Sans;fontColor={color};'+('fontStyle=1;' if bold else '')
        self.cells.append(f'<mxCell id="{i}" value="{html.escape(text,quote=True).replace(chr(10),"&#10;")}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'); return i
    def bar(self,x,y,w,h,text,color='#1f4e8c'):
        i=self._id(); st=f'rounded=0;whiteSpace=wrap;html=1;fillColor={color};strokeColor={color};fontColor=#ffffff;fontSize=16;fontStyle=1;fontFamily=PT Sans;'
        self.cells.append(f'<mxCell id="{i}" value="{html.escape(text,quote=True)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'); return i
    def edge(self,a,b,label='',color='#555555',dashed=False,fs=12,straight=False):
        i=self._id(); st=f'endArrow=classic;html=1;strokeColor={color};fontSize={fs};fontFamily=PT Sans;'+('' if straight else 'edgeStyle=orthogonalEdgeStyle;rounded=0;')+('dashed=1;' if dashed else '')
        self.cells.append(f'<mxCell id="{i}" value="{html.escape(label,quote=True)}" style="{st}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>'); return i
    def ellipse(self,x,y,w,h,text,color='blue',fs=13):
        i=self._id(); f,s=PAL[color]; st=f'ellipse;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontSize={fs};fontFamily=PT Sans;opacity=70;'
        self.cells.append(f'<mxCell id="{i}" value="{html.escape(text,quote=True).replace(chr(10),"&#10;")}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'); return i
    def save(self):
        xml=f'<mxfile host="app.diagrams.net"><diagram name="{self.name}" id="{self.name}"><mxGraphModel dx="{self.w}" dy="{self.h}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'+''.join(self.cells)+'</root></mxGraphModel></diagram></mxfile>'
        os.makedirs(OUT,exist_ok=True); p=os.path.join(OUT,self.name+'.drawio'); open(p,'w',encoding='utf-8').write(xml)
        import xml.etree.ElementTree as ET; ET.parse(p)
        subprocess.run(['drawio','--export','--format','png','--scale','2','--output',os.path.join(OUT,self.name+'.png'),p],capture_output=True)
        return p
def course_map():
    d=D('course-map',1120,640)
    d.bar(20,15,1080,36,'Toán rời rạc 1 (INT1358): bốn loại bài toán tổ hợp và 13 module')
    cols=[('Nền tảng','blue',['M1 Logic mệnh đề','M2 Vị từ, lượng từ','M3 Tập hợp, độ phức tạp'],'Chương 1'),
          ('Bài toán ĐẾM','yellow',['M4 Nguyên lý đếm','M5 Tổ hợp, nghiệm nguyên','M7 Lập truy hồi','M8 Giải truy hồi','M9 Hàm sinh'],'Chương 2'),
          ('Bài toán TỒN TẠI','purple',['M6 Dirichlet, phản chứng'],'Chương 5'),
          ('Bài toán LIỆT KÊ','green',['M10 Phương pháp sinh','M11 Quay lui'],'Chương 3'),
          ('Bài toán TỐI ƯU','red',['M12 Cái túi: duyệt toàn bộ, nhánh cận','M13 Người du lịch'],'Chương 4')]
    x=20; w=205
    for title,c,mods,ch in cols:
        d.box(x,80,w,50,f'{title}\n({ch})',c,True,15)
        y=150
        for m in mods:
            d.box(x+8,y,w-16,58,m,c,False,13); y+=76
        x+=w+14
    d.text(20,560,1080,50,'Toán rời rạc 2 (đồ thị: DFS/BFS, Euler, Hamilton, cây bao trùm, đường đi ngắn nhất, luồng) KHÔNG nằm trong sơ đồ này.',13,True,'#b85450')
    return d.save()
def venn3():
    d=D('venn-3-tap',760,520)
    d.bar(20,10,720,34,'Nguyên lý bù trừ ba tập: |A∪B∪C|')
    d.ellipse(150,70,280,280,'A','blue',20); d.ellipse(320,70,280,280,'B','yellow',20); d.ellipse(235,200,280,280,'C','green',20)
    d.text(190,150,80,30,'chỉ A',13); d.text(485,150,80,30,'chỉ B',13); d.text(340,410,80,30,'chỉ C',13)
    d.text(315,120,70,30,'A∩B',13,True); d.text(255,270,70,30,'A∩C',13,True); d.text(420,270,70,30,'B∩C',13,True); d.text(340,215,70,30,'A∩B∩C',12,True,'#b85450')
    d.text(20,490,720,26,'|A∪B∪C| = |A|+|B|+|C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|',14,True)
    return d.save()
def rec_flow():
    d=D('giai-truy-hoi',900,640)
    d.bar(20,10,860,34,'Quy trình giải hệ thức truy hồi tuyến tính thuần nhất')
    a=d.box(300,60,300,54,'aₙ = c₁aₙ₋₁ + … + c_kaₙ₋ₖ\ncùng k điều kiện đầu','blue',True)
    b=d.box(300,140,300,54,'Phương trình đặc trưng\nr^k − c₁r^(k−1) − … − c_k = 0','yellow')
    c=d.box(300,225,300,54,'Tìm mọi nghiệm r (kể cả bội)','yellow')
    d1=d.box(40,330,240,80,'Nghiệm phân biệt\naₙ = α₁r₁ⁿ + α₂r₂ⁿ + …','green')
    d2=d.box(330,330,240,80,'Nghiệm r bội m\n(α₀ + α₁n + … + α_(m−1)n^(m−1))·rⁿ','green')
    d3=d.box(620,330,240,80,'Nghiệm phức\n(ngoài phạm vi TRR1)','grey')
    e=d.box(300,450,300,54,'Thay n = 0, 1, … giải hệ tìm α','purple')
    f=d.box(300,535,300,54,'Kiểm tra: a₂, a₃ từ hệ thức\ntrùng với công thức','red',True)
    d.edge(a,b); d.edge(b,c); d.edge(c,d1); d.edge(c,d2); d.edge(c,d3,dashed=True); d.edge(d1,e); d.edge(d2,e); d.edge(e,f)
    return d.save()
def bt_tree():
    d=D('cay-quay-lui',1100,560)
    d.bar(20,10,1060,34,'Cây quay lui liệt kê xâu nhị phân độ dài 3 (Try(i): thử 0 rồi 1)')
    root=d.box(490,60,120,40,'Try(1)','blue',True)
    xs1=[290,690]; l1=[]
    for k,x in enumerate(xs1):
        l1.append(d.box(x,150,120,40,f'x₁ = {k}','yellow')); d.edge(root,l1[-1])
    l2=[]
    xs2=[190,390,590,790]
    for k,x in enumerate(xs2):
        l2.append(d.box(x,250,120,40,f'x₂ = {k%2}','yellow')); d.edge(l1[k//2],l2[-1])
    xs3=[140,240,340,440,540,640,740,840]
    for k,x in enumerate(xs3):
        n=d.box(x-5,350,100,44,f'x₃ = {k%2}\n'+format(k,'03b'),'green',True,12); d.edge(l2[k//2],n)
    d.text(20,420,1060,50,'Số lời gọi Try: 1 + 2 + 4 = 7 = 2³ − 1; số nghiệm in ra: 2³ = 8. Thứ tự in trùng thứ tự từ điển.',14,True)
    d.text(20,470,1060,40,'Nhánh có điều kiện chấp nhận (ví dụ không cho hai bit 1 liền nhau) bị cắt ngay tại nút vi phạm.',13,False,'#666666')
    return d.save()
def knap_tree():
    d=D('cay-cai-tui',1100,640)
    d.bar(20,10,1060,34,'Cây nhánh cận: 10x₁ + 5x₂ + 3x₃ + 6x₄ → max; 5x₁ + 3x₂ + 2x₃ + 4x₄ ≤ 8 (giáo trình 2016)')
    root=d.box(430,60,220,50,'Gốc: FOPT = −∞\ng = 16','blue',True)
    n1=d.box(150,160,230,60,'x₁ = 1: δ = 10, w = 3\ng = 15 → mở rộng','yellow')
    n0=d.box(700,160,230,60,'x₁ = 0: δ = 0, w = 8\ng = 40/3 ≈ 13,33 ✗ cắt','red')
    n11=d.box(60,270,230,60,'x₁=1, x₂=1: δ = 15, w = 0\ng = 15 → mở rộng','yellow')
    n10=d.box(330,270,240,60,'x₁=1, x₂=0: δ = 10, w = 3\ng = 14,5 ✗ cắt (g ≤ 15)','red')
    n110=d.box(60,380,230,60,'x₃ = 0: δ = 15, w = 0\ng = 15 → mở rộng','yellow')
    n1100=d.box(60,490,230,66,'x₄ = 0: lá\nKỷ lục FOPT = 15\nx* = (1,1,0,0)','green',True)
    d.edge(root,n1,'x₁ = 1'); d.edge(root,n0,'x₁ = 0'); d.edge(n1,n11,'x₂ = 1'); d.edge(n1,n10,'x₂ = 0'); d.edge(n11,n110,'x₃ = 0'); d.edge(n110,n1100,'x₄ = 0')
    d.text(340,470,700,90,'Quy tắc: g = δ + c_{k+1}·w/a_{k+1}. Mở rộng khi g > FOPT, cắt khi g ≤ FOPT.\nCác vật đã sắp c/a giảm dần: 10/5, 5/3, 3/2, 6/4.',13,False,'#333333','left')
    return d.save()
def tsp_tree():
    d=D('cay-nguoi-du-lich',1100,640)
    d.bar(20,10,1060,34,'Cây nhánh cận TSP (ví dụ giáo trình 2016, n = 6): hành trình tối ưu 1→4→6→3→5→2→1, chi phí 104')
    r=d.box(430,60,240,52,'Gốc: cận dưới = 81\nchọn cạnh (6,3), β = 48','blue',True)
    a=d.box(60,160,260,60,'Chứa (6,3): cận 81\nchọn (4,6), β = 32','yellow')
    b=d.box(800,160,260,60,'Không chứa (6,3): cận 81 + 48 = 129\n✗ cắt sau khi có kỷ lục 104','red')
    a1=d.box(60,270,260,60,'Chứa (4,6): cận 81\nchọn (2,1), β = 20','yellow')
    a2=d.box(560,270,260,60,'Không chứa (4,6): cận 81 + 32 = 113\n✗ cắt (≥ 104)','red')
    a11=d.box(60,380,260,60,'Chứa (2,1): cận 84\nchọn (1,4)','yellow')
    a12=d.box(560,380,260,60,'Không chứa (2,1): cận 101 < 104\nxét sau, không cải thiện','orange')
    a111=d.box(60,490,260,72,'Chứa (1,4): ma trận 2×2\nkết nạp (3,5),(5,2)\nHành trình 104 ★ kỷ lục','green',True)
    d.edge(r,a,'chứa',straight=True); d.edge(r,b,'không chứa',straight=True); d.edge(a,a1,'chứa'); d.edge(a,a2,'không chứa',straight=True)
    d.edge(a1,a11,'chứa'); d.edge(a1,a12,'không chứa',straight=True); d.edge(a11,a111)
    d.text(640,500,420,100,'Nhánh chứa luôn đi trước; nhánh không chứa có cận dưới tăng đúng β.\nCắt khi cận dưới ≥ kỷ lục.',13,False,'#333333','left')
    return d.save()
def pigeon():
    d=D('dirichlet',900,420)
    d.bar(20,10,860,34,'Nguyên lý Dirichlet: N vật vào k hộp ⇒ có hộp chứa ≥ ⌈N/k⌉ vật')
    for i in range(4):
        d.box(60+i*200,90,170,120,f'Hộp {i+1}','yellow',True,15)
    for i,(x,y) in enumerate([(90,140),(120,175),(260,150),(470,150),(500,175),(530,140),(660,160),(690,180),(720,140)]):
        d.ellipse(x,y,26,26,'','blue')
    d.text(60,230,800,60,'9 vật vào 4 hộp: ⌈9/4⌉ = 3 ⇒ chắc chắn có hộp chứa ≥ 3 vật (ở hình: hộp 3 chứa 3 vật).',14,True)
    d.text(60,300,800,80,'Để CHẮC CHẮN có m vật cùng hộp trong k hộp cần N = k·(m − 1) + 1 vật.\nVí dụ đề thi: 40 câu ⇒ 41 mức điểm; cần 12 thí sinh cùng điểm: 41·11 + 1 = 452.',13,False,'#333333')
    return d.save()
if __name__=='__main__':
    for f in (course_map,venn3,rec_flow,bt_tree,knap_tree,tsp_tree,pigeon): print(f())

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import random
import json
import os

# TAM EKRAN AYARLARI - Android için optimize
Window.fullscreen = True
Window.clearcolor = (0.05, 0.05, 0.1, 1)

# ============================================================
# VERİ YÖNETİMİ - Geliştirilmiş
# ============================================================
class DataManager:
    def __init__(self):
        self.file = "fm_data.json"
        self.default_data = {
            'money': 5000000,
            'team': 'FC KRAL',
            'season': 1,
            'played': 0, 'won': 0, 'drawn': 0, 'lost': 0,
            'points': 0, 'goals_for': 0, 'goals_against': 0,
            'position': 1,
            'players': [],
            'trophies': []
        }
        self.data = self.default_data.copy()
        self.load()
    
    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Veri bütünlüğü kontrolü
                    for key in self.default_data:
                        if key not in loaded:
                            loaded[key] = self.default_data[key]
                    self.data = loaded
            except:
                self.data = self.default_data.copy()
                self.save()
        else:
            self.save()
    
    def save(self):
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except:
            pass

# ============================================================
# FUTBOLCU SINIFI - Geliştirilmiş
# ============================================================
class Player:
    def __init__(self, name="", pos="", rating=0):
        self.id = random.randint(10000, 99999)  # Daha büyük ID aralığı
        self.name = name or self.gen_name()
        self.pos = pos or random.choice(['GK','CB','LB','RB','CM','CDM','CAM','LW','RW','ST'])
        self.rating = rating or random.randint(55, 85)
        self.potential = min(99, self.rating + random.randint(0, 20))
        self.age = random.randint(17, 35)
        self.value = self.rating * 12000 + random.randint(0, 50000)
        self.goals = 0
        self.assists = 0
        self.apps = 0
        self.fitness = random.randint(70, 100)
        self.morale = random.randint(60, 100)
        self.injury = 0
        self.skills = {
            'hiz': random.randint(50,95),
            'sut': random.randint(50,95),
            'pas': random.randint(50,95),
            'defans': random.randint(50,95),
            'fizik': random.randint(50,95)
        }
    
    def gen_name(self):
        first = ['Ahmet','Mehmet','Ali','Veli','Emre','Can','Burak','Deniz','Efe','Kaan','Mert','Yiğit','Arda','Kerem','Hakan','Okan','Serkan','Murat','Fatih','Uğur']
        last = ['Yılmaz','Demir','Çelik','Aydın','Öztürk','Kaya','Polat','Şahin','Kurt','Kılıç','Acar','Aksoy','Arslan','Koç','Taş','Kara','Akın','Doğan','Erdem']
        return f"{random.choice(first)} {random.choice(last)}"
    
    def pos_text(self):
        m = {'GK':'Kaleci','CB':'Stoper','LB':'Sol Bek','RB':'Sağ Bek','CM':'Orta Saha','CDM':'Defans O.S.','CAM':'Ofans O.S.','LW':'Sol Kanat','RW':'Sağ Kanat','ST':'Santrafor'}
        return m.get(self.pos, self.pos)
    
    def to_dict(self):
        return {
            'id':self.id,'name':self.name,'pos':self.pos,'rating':self.rating,
            'potential':self.potential,'age':self.age,'value':self.value,
            'goals':self.goals,'assists':self.assists,'apps':self.apps,
            'fitness':self.fitness,'morale':self.morale,'injury':self.injury,
            'skills':self.skills
        }
    
    @staticmethod
    def from_dict(d):
        p = Player(d['name'], d['pos'], d['rating'])
        p.id=d['id']; p.potential=d['potential']; p.age=d['age']; p.value=d['value']
        p.goals=d['goals']; p.assists=d['assists']; p.apps=d['apps']
        p.fitness=d['fitness']; p.morale=d['morale']; p.injury=d['injury']
        p.skills=d['skills']
        return p

# ============================================================
# ÖZEL WIDGET - Canvas güncellemesi için
# ============================================================
class RoundedBox(BoxLayout):
    def __init__(self, color=(0.1,0.1,0.2,1), radius=[5], **kwargs):
        super().__init__(**kwargs)
        self.bg_color = color
        self.radius = radius
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
    
    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# ============================================================
# MENÜ EKRANI - Tam ekran
# ============================================================
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=8, padding=[20, 25, 20, 25])
        
        # Takım adı
        main.add_widget(Label(text=f'⚽ {self.dm.data["team"]}', font_size=36, color=(1,0.8,0.2,1), bold=True, size_hint=(1,0.1)))
        
        # İstatistikler
        stats = BoxLayout(size_hint=(1,0.07), spacing=15)
        stats.add_widget(Label(text=f'💰 {self.dm.data["money"]:,}₺', font_size=16, color=(0.2,0.9,0.2,1), bold=True))
        stats.add_widget(Label(text=f'🏆 #{self.dm.data["position"]}', font_size=16, color=(1,0.8,0.2,1), bold=True))
        stats.add_widget(Label(text=f'📊 {self.dm.data["points"]}P', font_size=16, color=(1,1,1,1), bold=True))
        main.add_widget(stats)
        
        # Sezon
        main.add_widget(Label(text=f'Sezon {self.dm.data["season"]} | {self.dm.data["played"]} Maç', 
                             font_size=14, color=(0.5,0.5,0.7,1), size_hint=(1,0.05)))
        
        # Butonlar
        btns = [
            ('📋 KADRO', (0.15,0.3,0.6,1)),
            ('🏆 MAÇ', (0.1,0.7,0.2,1)),
            ('📊 LİG', (0.7,0.5,0.1,1)),
            ('🛒 TRANSFER', (0.7,0.1,0.5,1)),
            ('📈 ANTRENMAN', (0.6,0.4,0.1,1)),
            ('🏆 KUPA', (0.8,0.6,0.2,1))
        ]
        
        for text, color in btns:
            btn = Button(text=text, font_size=22, bold=True,
                        size_hint=(0.9,0.08), pos_hint={'center_x':0.5},
                        background_color=color, color=(1,1,1,1), background_normal='')
            btn.bind(on_press=self.make_go(text))
            main.add_widget(btn)
        
        # Alt bilgi
        main.add_widget(Label(text='⚡ Futbol Menajerlik', font_size=11, color=(0.3,0.3,0.5,1), size_hint=(1,0.04)))
        
        self.add_widget(main)
    
    def make_go(self, text):
        def go(instance):
            if 'KADRO' in text: self.manager.current = 'squad'
            elif 'MAÇ' in text: self.manager.current = 'match'
            elif 'LİG' in text: self.manager.current = 'league'
            elif 'TRANSFER' in text: self.manager.current = 'transfer'
            elif 'ANTRENMAN' in text: self.manager.current = 'training'
            elif 'KUPA' in text: self.manager.current = 'trophies'
        return go
    
    def on_enter(self): 
        self.dm = DataManager()
        self.build()

# ============================================================
# KADRO EKRANI - Tam ekran
# ============================================================
class SquadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=5, padding=[15, 20, 15, 20])
        
        # Başlık
        header = BoxLayout(size_hint=(1,0.08), spacing=10)
        header.add_widget(Label(text='📋 KADRO', font_size=28, color=(1,0.8,0.2,1), bold=True))
        main.add_widget(header)
        
        # Geri
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        # Liste
        sc = ScrollView(size_hint=(1,0.80))
        box = BoxLayout(orientation='vertical', spacing=3, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        if not self.dm.data['players']:
            box.add_widget(Label(text='Henüz futbolcu yok!', font_size=18, color=(0.5,0.5,0.5,1), size_hint_y=None, height=50))
        else:
            for p in self.dm.data['players']:
                row = RoundedBox(color=(0.1,0.1,0.2,1), radius=[5], size_hint_y=None, height=40, spacing=2)
                row.add_widget(Label(text=p['name'][:14], font_size=14, color=(1,1,1,1), size_hint=(0.35,1)))
                row.add_widget(Label(text=p['pos'][:3], font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.13,1)))
                c = (0.2,0.9,0.2,1) if p['rating']>=80 else (0.9,0.9,0.2,1) if p['rating']>=70 else (0.9,0.5,0.2,1)
                row.add_widget(Label(text=f'⭐{p["rating"]:.0f}', font_size=15, color=c, size_hint=(0.13,1), bold=True))
                row.add_widget(Label(text=f'{p["age"]}', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.09,1)))
                row.add_widget(Label(text=f'€{p["value"]:,}', font_size=12, color=(0.2,0.9,0.2,1), size_hint=(0.2,1)))
                box.add_widget(row)
        
        sc.add_widget(box)
        main.add_widget(sc)
        self.add_widget(main)
    
    def on_enter(self): 
        self.dm = DataManager()
        self.build()

# ============================================================
# MAÇ EKRANI - Tam ekran
# ============================================================
class MatchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.match_played = False
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=5, padding=[15, 20, 15, 20])
        
        main.add_widget(Label(text='🏆 MAÇ', font_size=30, color=(1,0.8,0.2,1), size_hint=(1,0.07), bold=True))
        
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        self.opp = Label(text='⚡ Rakip seç!', font_size=18, color=(0.8,0.8,0.9,1), size_hint=(1,0.06))
        main.add_widget(self.opp)
        
        self.score = Label(text='', font_size=44, color=(1,1,1,1), size_hint=(1,0.12), bold=True)
        main.add_widget(self.score)
        
        self.stats = Label(text='', font_size=13, color=(0.6,0.6,0.8,1), size_hint=(1,0.05))
        main.add_widget(self.stats)
        
        self.ev = ScrollView(size_hint=(1,0.45))
        self.eb = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
        self.eb.bind(minimum_height=self.eb.setter('height'))
        self.ev.add_widget(self.eb)
        main.add_widget(self.ev)
        
        self.btn2 = Button(text='🔄 MAÇ BAŞLAT', font_size=22, size_hint=(0.85,0.08), pos_hint={'center_x':0.5},
                     background_color=(0.2,0.7,0.3,1), color=(1,1,1,1), background_normal='')
        self.btn2.bind(on_press=self.play)
        main.add_widget(self.btn2)
        
        self.add_widget(main)
        self.match_played = False
    
    def play(self, i):
        if self.match_played:
            return
        
        teams = ['GALATASARAY','FENERBAHÇE','BEŞİKTAŞ','TRABZONSPOR','BAŞAKŞEHİR','SİVASSPOR','KAYSERİSPOR','KONYASPOR','GAZİANTEP','ANTALYASPOR']
        opp = random.choice(teams)
        self.opp.text = f'{self.dm.data["team"]} 🆚 {opp}'
        
        # Maç simülasyonu
        t1 = 80 + random.randint(-15,15)
        t2 = 70 + random.randint(-15,15)
        g1 = max(0, int(t1/25 + random.uniform(0,1.8)))
        g2 = max(0, int(t2/28 + random.uniform(0,1.5)))
        
        self.score.text = f'{g1} - {g2}'
        self.stats.text = f'Şut: {random.randint(5,18)} - {random.randint(3,14)} | Top: {random.randint(42,68)}% - {random.randint(32,58)}%'
        
        # İstatistik güncelleme
        self.dm.data['played'] += 1
        if g1 > g2:
            self.dm.data['won'] += 1
            self.dm.data['points'] += 3
            self.eb.add_widget(Label(text='🎉 ZAFER!', font_size=20, color=(0.2,0.9,0.2,1), size_hint_y=None, height=30))
        elif g1 == g2:
            self.dm.data['drawn'] += 1
            self.dm.data['points'] += 1
            self.eb.add_widget(Label(text='🤝 BERABERLİK', font_size=20, color=(0.9,0.9,0.2,1), size_hint_y=None, height=30))
        else:
            self.dm.data['lost'] += 1
            self.eb.add_widget(Label(text='😞 MAĞLUBİYET', font_size=20, color=(0.9,0.2,0.2,1), size_hint_y=None, height=30))
        
        self.dm.data['goals_for'] += g1
        self.dm.data['goals_against'] += g2
        
        # Pozisyon hesaplama
        pos = 1
        for i in range(1, 19):
            if self.dm.data['points'] < (i * 3):
                pos = i + 1
                break
        self.dm.data['position'] = min(20, pos)
        
        # Şampiyonluk kontrolü
        if self.dm.data['position'] <= 1 and self.dm.data['played'] >= 10:
            trophy_count = sum(1 for t in self.dm.data['trophies'] if t == 'Lig Şampiyonu')
            if trophy_count == 0:
                self.dm.data['trophies'].append('Lig Şampiyonu')
                self.eb.add_widget(Label(text='🏆 LİG ŞAMPİYONU!', font_size=22, color=(1,0.8,0.2,1), size_hint_y=None, height=35))
        
        self.dm.save()
        self.match_played = True
        self.btn2.text = '✅ MAÇ TAMAMLANDI'
    
    def on_enter(self):
        self.dm = DataManager()
        self.eb.clear_widgets()
        self.match_played = False
        self.build()

# ============================================================
# LİG EKRANI - Tam ekran ve geliştirilmiş
# ============================================================
class LeagueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=4, padding=[15, 20, 15, 20])
        
        main.add_widget(Label(text='📊 LİG DURUMU', font_size=28, color=(1,0.8,0.2,1), size_hint=(1,0.07), bold=True))
        
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        info = BoxLayout(size_hint=(1,0.06))
        info.add_widget(Label(text=f"🏆 {self.dm.data['team']}", font_size=18, color=(1,0.8,0.2,1), bold=True))
        info.add_widget(Label(text=f"#{self.dm.data['position']}", font_size=16, color=(0.8,0.8,0.9,1)))
        main.add_widget(info)
        
        st = BoxLayout(size_hint=(1,0.05))
        st.add_widget(Label(text=f"O:{self.dm.data['played']}", font_size=13, color=(0.6,0.6,0.8,1)))
        st.add_widget(Label(text=f"G:{self.dm.data['won']}", font_size=13, color=(0.2,0.9,0.2,1)))
        st.add_widget(Label(text=f"B:{self.dm.data['drawn']}", font_size=13, color=(0.9,0.9,0.2,1)))
        st.add_widget(Label(text=f"M:{self.dm.data['lost']}", font_size=13, color=(0.9,0.2,0.2,1)))
        st.add_widget(Label(text=f"PTS:{self.dm.data['points']}", font_size=14, color=(1,1,1,1), bold=True))
        main.add_widget(st)
        
        sc = ScrollView(size_hint=(1,0.70))
        box = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        # Takımlar - gerçek verilerle
        teams = ['GALATASARAY','FENERBAHÇE','BEŞİKTAŞ','TRABZONSPOR','BAŞAKŞEHİR','SİVASSPOR','KAYSERİSPOR','KONYASPOR','GAZİANTEP','ANTALYASPOR']
        table = []
        user_team = self.dm.data['team']
        
        for t in teams:
            if t == user_team:
                # Kullanıcı takımı gerçek veriler
                p = self.dm.data['played']
                w = self.dm.data['won']
                d = self.dm.data['drawn']
                l2 = self.dm.data['lost']
                pts = self.dm.data['points']
                table.append({'team':t,'p':p,'w':w,'d':d,'l':l2,'pts':pts,'me':True})
            else:
                # Rakipler - tutarlı şekilde
                base = self.dm.data['played']
                if base > 0:
                    p = max(0, min(base + random.randint(-1, 1), base + 2))
                    w = max(0, min(int(p * random.uniform(0.3, 0.6)), p))
                    d = max(0, min(int(p * random.uniform(0.1, 0.3)), p - w))
                    l2 = p - w - d
                    pts = w*3 + d
                else:
                    p = 0; w = 0; d = 0; l2 = 0; pts = 0
                table.append({'team':t,'p':p,'w':w,'d':d,'l':l2,'pts':pts,'me':False})
        
        table.sort(key=lambda x:x['pts'], reverse=True)
        
        # Başlık satırı
        header = RoundedBox(color=(0.15,0.15,0.25,1), radius=[3], size_hint_y=None, height=25)
        header.add_widget(Label(text='#', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
        header.add_widget(Label(text='Takım', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.35,1)))
        header.add_widget(Label(text='O', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
        header.add_widget(Label(text='G', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
        header.add_widget(Label(text='P', font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
        box.add_widget(header)
        
        for i, t in enumerate(table,1):
            row = RoundedBox(color=(0.2,0.2,0.3,1) if t['me'] else (0.1,0.1,0.2,1), radius=[3], size_hint_y=None, height=28)
            row.add_widget(Label(text=str(i), font_size=13, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
            nm = f"⭐ {t['team']}" if t['me'] else t['team']
            row.add_widget(Label(text=nm[:14], font_size=13, color=(1,0.8,0.2,1) if t['me'] else (0.8,0.8,0.9,1), size_hint=(0.35,1)))
            row.add_widget(Label(text=str(t['p']), font_size=12, color=(0.6,0.6,0.8,1), size_hint=(0.08,1)))
            row.add_widget(Label(text=str(t['w']), font_size=12, color=(0.2,0.9,0.2,1), size_hint=(0.08,1)))
            row.add_widget(Label(text=str(t['pts']), font_size=13, color=(1,0.8,0.2,1) if t['me'] else (0.8,0.8,0.9,1), size_hint=(0.08,1), bold=True))
            box.add_widget(row)
        
        sc.add_widget(box)
        main.add_widget(sc)
        self.add_widget(main)
    
    def on_enter(self):
        self.dm = DataManager()
        self.build()

# ============================================================
# TRANSFER EKRANI - Tam ekran
# ============================================================
class TransferScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.available = []
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=4, padding=[15, 20, 15, 20])
        
        header = BoxLayout(size_hint=(1,0.08))
        header.add_widget(Label(text='🛒 TRANSFER', font_size=28, color=(1,0.8,0.2,1), bold=True))
        header.add_widget(Label(text=f'💰 {self.dm.data["money"]:,}₺', font_size=16, color=(0.2,0.9,0.2,1), bold=True))
        main.add_widget(header)
        
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        if not self.available:
            self.generate_players()
        
        sc = ScrollView(size_hint=(1,0.80))
        box = BoxLayout(orientation='vertical', spacing=3, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        for p in self.available:
            row = RoundedBox(color=(0.1,0.1,0.2,1), radius=[5], size_hint_y=None, height=40, spacing=2)
            row.add_widget(Label(text=p.name[:14], font_size=13, color=(1,1,1,1), size_hint=(0.35,1)))
            row.add_widget(Label(text=p.pos[:3], font_size=11, color=(0.6,0.6,0.8,1), size_hint=(0.12,1)))
            row.add_widget(Label(text=f'⭐{p.rating:.0f}', font_size=13, color=(0.9,0.9,0.2,1), size_hint=(0.13,1)))
            row.add_widget(Label(text=f'€{p.value:,}', font_size=12, color=(0.2,0.9,0.2,1), size_hint=(0.2,1)))
            buy_btn = Button(text='🛒', font_size=14, size_hint=(0.15,0.85), background_color=(0.2,0.7,0.3,1), color=(1,1,1,1), background_normal='')
            buy_btn.bind(on_press=lambda x, pl=p: self.buy(pl))
            row.add_widget(buy_btn)
            box.add_widget(row)
        
        sc.add_widget(box)
        main.add_widget(sc)
        self.add_widget(main)
    
    def generate_players(self):
        self.available = []
        existing_ids = {p['id'] for p in self.dm.data['players']}
        for _ in range(10):
            p = Player()
            # ID çakışmasını önle
            while p.id in existing_ids:
                p.id = random.randint(10000, 99999)
            self.available.append(p)
    
    def buy(self, player):
        if self.dm.data['money'] >= player.value:
            self.dm.data['money'] -= player.value
            self.dm.data['players'].append(player.to_dict())
            self.dm.save()
            self.available.remove(player)
            self.build()
            self.show_popup('✅ Başarılı!', f'{player.name} kadroda!')
        else:
            self.show_popup('❌ Yetersiz!', f'{player.value:,}₺ gerekli')
    
    def show_popup(self, title, msg):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=msg, font_size=18, color=(1,1,1,1)))
        btn = Button(text='TAMAM', font_size=18, size_hint=(0.4,0.3), pos_hint={'center_x':0.5}, background_normal='', background_color=(0.2,0.7,0.3,1), color=(1,1,1,1))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.8,0.35))
        btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def on_enter(self):
        self.dm = DataManager()
        self.build()

# ============================================================
# ANTRENMAN EKRANI - Tam ekran
# ============================================================
class TrainingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=6, padding=[15, 20, 15, 20])
        
        main.add_widget(Label(text='📈 ANTRENMAN', font_size=30, color=(1,0.8,0.2,1), size_hint=(1,0.07), bold=True))
        
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        # Oyuncu sayısı bilgisi
        count = len(self.dm.data['players'])
        main.add_widget(Label(text=f'👥 {count} oyuncu', font_size=14, color=(0.6,0.6,0.8,1), size_hint=(1,0.04)))
        
        for t in ['Hız','Şut','Pas','Defans','Fizik']:
            bt = Button(text=f'⚡ {t} Antrenmanı', font_size=20, size_hint=(0.85,0.08), pos_hint={'center_x':0.5},
                       background_color=(0.2,0.4,0.6,1), color=(1,1,1,1), background_normal='')
            bt.bind(on_press=lambda x, tt=t: self.train(tt))
            main.add_widget(bt)
        
        self.res = Label(text='Bir antrenman seç', font_size=16, color=(0.8,0.8,0.9,1), size_hint=(1,0.06))
        main.add_widget(self.res)
        
        self.add_widget(main)
    
    def train(self, ttype):
        if not self.dm.data['players']:
            self.res.text = '❌ Futbolcu yok!'
            return
        
        p_data = self.dm.data['players'][0]
        skill_map = {'Hız':'hiz','Şut':'sut','Pas':'pas','Defans':'defans','Fizik':'fizik'}
        skill_key = skill_map.get(ttype)
        
        if skill_key and skill_key in p_data['skills']:
            # Skill gelişimi
            old_val = p_data['skills'][skill_key]
            new_val = min(99, old_val + random.randint(1,4))
            p_data['skills'][skill_key] = new_val
            
            # Rating güncelleme - skill ortalamasına göre
            avg_skill = sum(p_data['skills'].values()) / 5
            p_data['rating'] = int(avg_skill * 0.8 + random.randint(10, 20))
            p_data['rating'] = max(50, min(99, p_data['rating']))
            
            self.dm.save()
            self.res.text = f'✅ {ttype} antrenmanı tamam! (+{new_val-old_val})'
        else:
            self.res.text = '❌ Hata!'
    
    def on_enter(self):
        self.dm = DataManager()
        self.build()

# ============================================================
# KUPA EKRANI - Tam ekran
# ============================================================
class TrophiesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        self.build()
    
    def build(self):
        self.clear_widgets()
        
        main = BoxLayout(orientation='vertical', spacing=6, padding=[15, 20, 15, 20])
        
        main.add_widget(Label(text='🏆 KUPA DOLABI', font_size=30, color=(1,0.8,0.2,1), size_hint=(1,0.07), bold=True))
        
        btn = Button(text='⬅ GERİ', font_size=18, size_hint=(0.3,0.07), background_color=(0.5,0.2,0.2,1), color=(1,1,1,1), background_normal='')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        main.add_widget(btn)
        
        total = len(self.dm.data['trophies'])
        main.add_widget(Label(text=f'🏆 Toplam {total} Kupa', font_size=22, color=(1,0.8,0.2,1), size_hint=(1,0.06)))
        
        sc = ScrollView(size_hint=(1,0.78))
        box = BoxLayout(orientation='vertical', spacing=4, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        if total == 0:
            box.add_widget(Label(text='🎯 Henüz kupa yok!', font_size=20, color=(0.5,0.5,0.5,1), size_hint_y=None, height=60))
        else:
            counts = {}
            for t in self.dm.data['trophies']:
                counts[t] = counts.get(t, 0) + 1
            
            trophy_icons = {
                'Lig Şampiyonu': '🏆',
                'Kupa': '🏅',
                'Süper Kupa': '⭐'
            }
            
            for name, count in counts.items():
                row = RoundedBox(color=(0.1,0.1,0.2,1), radius=[5], size_hint_y=None, height=45)
                icon = trophy_icons.get(name, '🏆')
                row.add_widget(Label(text=f'{icon} {name}', font_size=18, color=(1,0.8,0.2,1), size_hint=(0.7,1)))
                row.add_widget(Label(text=f'x{count}', font_size=18, color=(0.8,0.8,0.9,1), size_hint=(0.3,1)))
                box.add_widget(row)
        
        sc.add_widget(box)
        main.add_widget(sc)
        self.add_widget(main)
    
    def on_enter(self):
        self.dm = DataManager()
        self.build()

# ============================================================
# ANA UYGULAMA
# ============================================================
class FootballManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SquadScreen(name='squad'))
        sm.add_widget(MatchScreen(name='match'))
        sm.add_widget(LeagueScreen(name='league'))
        sm.add_widget(TransferScreen(name='transfer'))
        sm.add_widget(TrainingScreen(name='training'))
        sm.add_widget(TrophiesScreen(name='trophies'))
        return sm
    
    def on_start(self):
        # Uygulama başlangıcında veri kontrolü
        dm = DataManager()
        dm.load()

if __name__ == '__main__':
    FootballManagerApp().run()
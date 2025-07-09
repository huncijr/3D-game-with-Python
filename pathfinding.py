from collections import deque
from functools import  lru_cache

class PathFinding:
    def __init__(self,game):
        self.game = game
        self.map = game.map.mini_map
        self.ways =[-1,0],[0,-1],[1,0],[0,1],[-1,-1],[1,-1],[1,1],[-1,1],
        self.graph = {}
        self.get_graph()

    @lru_cache()
    def get_path(self, start, goal):                # 🧭 Útvonal kiszámítása start -> goal között
        self.visited = self.bfs(start, goal,self.graph)  # 🧠 Lefuttatja a BFS algoritmust és elmenti a bejárt csomópontokat
        path = [goal]                               # 🧩 Kezdi az útvonalat a céllal (goal)
        step = self.visited.get(goal, start)        # 🔁 Visszafelé követi az útvonalat a start-ig
        while step and step != start:               # ↩️ Amíg nem ér el a start csomóponthoz
            path.append(step)                       # ➕ Hozzáadja az aktuális lépést az útvonalhoz
            step = self.visited[step]               # ⬅️ Következő lépés visszafelé
        return path[-1]                             # 🎯 Visszaadja az első lépést a start után (azaz: merre kell indulni)

    def bfs(self, start, goal, graph):              # 🧠 BFS algoritmus: szélességi bejárás start -> goal között
        queue = deque([start])                      #📥 Inicializál egy sort a starttal
        visited = {start: None}                     # 📌 Itt tároljuk, hogy ki honnan jött (útvonal visszakövetéshez)
        while queue:                                # 🔁 Amíg van elem a sorban
            cur_node = queue.popleft()              # ⬇️ Kivesz egy csomópontot a sor elejéről
            if cur_node == goal:                    # 🎯 Ha elértük a célt, kilépünk
                break
            next_nodes = graph[cur_node] # 🔄 Megnézzük az aktuális csomópont szomszédait
            for next_node in next_nodes:            # ♻️ Végigmegyünk a szomszédokon
                if next_node not in visited and next_node not in self.game.object_handler.npc_position:        # ✅ Ha még nem jártunk ott
                    queue.append(next_node)         # ➕ Hozzáadjuk a sorhoz
                    visited[next_node] = cur_node   # 🧩 Eltároljuk, hogy honnan jöttünk
        return visited                              # 🔙 Visszatér a bejárt útvonal információival

    def get_next_nodes(self,x,y):
        return[(x+dx,y+dy) for dx,dy in self.ways if (x+dx,y+dy) not in self.game.map.world_map]
    def get_graph(self):
        for y,row in enumerate(self.map):
            for x,col in enumerate(row):
                if not col:
                    self.graph[(x,y)] = self.graph.get((x,y),[]+ self.get_next_nodes(x,y))
        # print((8, 4) in self.graph)  # True vagy False
        print(sorted(self.graph.keys()))  # Kulcsok rendezve



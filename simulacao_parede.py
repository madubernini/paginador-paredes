import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import cv2

class DraggableWall:
    def __init__(self, ax, placas, imagens):
        self.ax = ax
        self.placas = placas
        self.imagens = imagens
        self.press = None

    def connect(self):
        self.cidpress = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata

    def on_motion(self, event):
        if self.press is None or event.xdata is None or event.ydata is None:
            return
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        for placa, img in zip(self.placas, self.imagens):
            x0, y0 = placa.xy
            placa.set_x(x0 + dx)
            placa.set_y(y0 + dy)
            img.set_extent((x0 + dx, x0 + dx + placa.get_width(), y0 + dy, y0 + dy + placa.get_height()))
        self.ax.figure.canvas.draw()
        self.press = event.xdata, event.ydata

    def on_release(self, event):
        self.press = None


def desenhar_parede_com_placas_e_objetos(largura_parede, altura_parede, tamanho_placa_largura=0.3,
                                         tamanho_placa_altura=0.3, imagem_placa=None, prumo_offset_esquerda=0,
                                         prumo_offset_direita=0, prumo_inicio_esquerda='cima', prumo_inicio_direita='cima',
                                         nivel_offset_cima=0, nivel_offset_baixo=0, nivel_inicio_cima='esquerda',
                                         nivel_inicio_baixo='esquerda'):
    fig, ax = plt.subplots()
    ax.set_xlim(0, largura_parede)
    ax.set_ylim(0, altura_parede)
    ax.set_aspect('equal')
    ax.set_title('Simulação de Instalação Placas')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    num_placas_x = int(largura_parede / tamanho_placa_largura) + 2
    num_placas_y = int(altura_parede / tamanho_placa_altura) + 2
    placas = []
    imagens = []

    for i in range(num_placas_x):
        for j in range(num_placas_y):
            x = (i - 1) * tamanho_placa_largura
            y = (j - 1) * tamanho_placa_altura
            placa = patches.Rectangle((x, y), tamanho_placa_largura, tamanho_placa_altura,
                                      linewidth=0.5, edgecolor='b', facecolor='none')
            ax.add_patch(placa)
            placas.append(placa)
            if imagem_placa:
                imagem_bgr = cv2.imread(imagem_placa)
                imagem_rgb = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2RGB)
                im = ax.imshow(imagem_rgb, extent=(x, x + tamanho_placa_largura, y, y + tamanho_placa_altura), zorder=1)
                imagens.append(im)

    objetos = [
        #patches.Rectangle((0.55, 0.80), 0.87, 2.03, linewidth=1, edgecolor='black', facecolor='lightgray', hatch='//', zorder=5),
        #patches.Rectangle((1.5, 0.80), 0.87, 2.03, linewidth=1, edgecolor='black', facecolor='lightgray', hatch='//', zorder=5)

    ]
    for objeto in objetos:
        ax.add_patch(objeto)

    if prumo_inicio_esquerda == 'cima':
        x_start_esquerda = 0
        y_start_esquerda = 0
        x_end_esquerda = x_start_esquerda + altura_parede * np.tan(np.radians(prumo_offset_esquerda))
        y_end_esquerda = altura_parede
    else:
        x_start_esquerda = 0
        y_start_esquerda = altura_parede
        x_end_esquerda = x_start_esquerda + altura_parede * np.tan(np.radians(prumo_offset_esquerda))
        y_end_esquerda = 0
    ax.plot([x_start_esquerda, x_end_esquerda], [y_start_esquerda, y_end_esquerda], color='black', linewidth=2, linestyle='--')
    hachura_esquerda = patches.Polygon([[0, altura_parede], [x_end_esquerda, y_end_esquerda], [0, 0]],
                                       closed=True, facecolor='lightgray', edgecolor='black', hatch='//', zorder=4)
    ax.add_patch(hachura_esquerda)

    if prumo_inicio_direita == 'cima':
        x_start_direita = largura_parede
        y_start_direita = 0
        x_end_direita = x_start_direita - altura_parede * np.tan(np.radians(prumo_offset_direita))
        y_end_direita = altura_parede
    else:
        x_start_direita = largura_parede
        y_start_direita = altura_parede
        x_end_direita = x_start_direita - altura_parede * np.tan(np.radians(prumo_offset_direita))
        y_end_direita = 0
    ax.plot([x_start_direita, x_end_direita], [y_start_direita, y_end_direita], color='black', linewidth=2, linestyle='--')
    hachura_direita = patches.Polygon([[largura_parede, altura_parede], [x_end_direita, y_end_direita], [largura_parede, 0]],
                                      closed=True, facecolor='lightgray', edgecolor='black', hatch='//', zorder=4)
    ax.add_patch(hachura_direita)

    if nivel_inicio_cima == 'esquerda':
        x_start_cima = 0
        y_start_cima = 0
        x_end_cima = largura_parede
        y_end_cima = y_start_cima + largura_parede * np.tan(np.radians(nivel_offset_cima))
    else:
        x_start_cima = largura_parede
        y_start_cima = 0
        x_end_cima = 0
        y_end_cima = y_start_cima + largura_parede * np.tan(np.radians(nivel_offset_cima))
    ax.plot([x_start_cima, x_end_cima], [y_start_cima, y_end_cima], color='green', linewidth=2, linestyle='--')
    
    hachura_cima = patches.Polygon([[0, 0], [x_end_cima, y_end_cima], [largura_parede, 0]] if nivel_inicio_cima == 'esquerda'
                                   else [[largura_parede, 0], [x_end_cima, y_end_cima], [0, 0]],
                                   closed=True, facecolor='lightgray', edgecolor='black', hatch='//', zorder=4)
    ax.add_patch(hachura_cima)

    if nivel_inicio_baixo == 'esquerda':
        x_start_baixo = 0
        y_start_baixo = altura_parede
        x_end_baixo = largura_parede
        y_end_baixo = y_start_baixo - largura_parede * np.tan(np.radians(nivel_offset_baixo))
    else:
        x_start_baixo = largura_parede
        y_start_baixo = altura_parede
        x_end_baixo = 0
        y_end_baixo = y_start_baixo - largura_parede * np.tan(np.radians(nivel_offset_baixo))
    ax.plot([x_start_baixo, x_end_baixo], [y_start_baixo, y_end_baixo], color='red', linewidth=2, linestyle='--')
    hachura_baixo = patches.Polygon([[0, altura_parede], [x_end_baixo, y_end_baixo], [largura_parede, altura_parede]] if nivel_inicio_baixo == 'esquerda'
                                    else [[largura_parede, altura_parede], [x_end_baixo, y_end_baixo], [0, altura_parede]],
                                    closed=True, facecolor='lightgray', edgecolor='black', hatch='//', zorder=4)
    ax.add_patch(hachura_baixo)

    draggable_wall = DraggableWall(ax, placas, imagens)
    draggable_wall.connect()

    plt.gca().invert_yaxis()
    plt.show()


largura_parede = 4.1
altura_parede = 2.66
imagem_placa = 'placa.png'
prumo_offset_esquerda = 2
prumo_offset_direita = 3
prumo_inicio_esquerda = 'baixo'
prumo_inicio_direita = 'cima'
nivel_offset_cima = 4
nivel_offset_baixo = 2
nivel_inicio_cima = 'direita'
nivel_inicio_baixo = 'esquerda'

desenhar_parede_com_placas_e_objetos(
    largura_parede, altura_parede,
    tamanho_placa_largura=0.30,
    tamanho_placa_altura=0.30,
    imagem_placa=imagem_placa,
    prumo_offset_esquerda=prumo_offset_esquerda,
    prumo_offset_direita=prumo_offset_direita,
    prumo_inicio_esquerda=prumo_inicio_esquerda,
    prumo_inicio_direita=prumo_inicio_direita,
    nivel_offset_cima=nivel_offset_cima,
    nivel_offset_baixo=nivel_offset_baixo,
    nivel_inicio_cima=nivel_inicio_cima,
    nivel_inicio_baixo=nivel_inicio_baixo
)

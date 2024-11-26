import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret = True
while ret:
    ret, frame = cap.read()
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(frame_cinza, 50, 200, None, 3)
    circulos = cv2.HoughCircles(bordas,
                                cv2.HOUGH_GRADIENT,
                                dp=1,
                                minDist=500,
                                param1=60,
                                param2=30,
                                minRadius=10,
                                maxRadius=1000)

    if circulos is not None:
        circulos_np = np.uint16(np.around(circulos))
        
        for circulos in circulos_np:
            for circle in circulos:
                x, y, r = circle
                
                maior_lado_recorte = int(r * np.sqrt(2)) + 30
                topo_x_recorte = x - maior_lado_recorte // 2
                topo_y_recorte = y - maior_lado_recorte // 2

                corte_quadrado = bordas[
                                    topo_y_recorte:topo_y_recorte + maior_lado_recorte, 
                                    topo_x_recorte:topo_x_recorte + maior_lado_recorte]
                
                linhas = cv2.HoughLines(corte_quadrado, 1, np.pi / 180, 145)
                
                coordenadas_linhas = []
                if linhas is not None and len(linhas) == 2:
                    for linha in linhas:
                        for rho, theta in linha:
                            a = np.cos(theta)
                            b = np.sin(theta)
                            x0 = a * rho
                            y0 = b * rho
                            
                            x1 = int(x0 + 1000 * (-b))
                            y1 = int(y0 + 1000 * (a))
                            x2 = int(x0 - 1000 * (-b))
                            y2 = int(y0 - 1000 * (a))           

                            min_x, min_y = 0, 0
                            max_x, max_y = corte_quadrado.shape[1], corte_quadrado.shape[0]

                            x1 = np.clip(x1 - topo_x_recorte, min_x, max_x - 1)
                            y1 = np.clip(y1 - topo_y_recorte, min_y, max_y - 1)
                            x2 = np.clip(x2 - topo_x_recorte, min_x, max_x - 1)
                            y2 = np.clip(y2 - topo_y_recorte, min_y, max_y - 1)

                            coordenadas_linhas.append([x1, y1, x2, y2])

                    x1, y1, x2, y2 = coordenadas_linhas[0]
                    x3, y3, y4, x4 = coordenadas_linhas[1]
                    
                    if y1 - y4 == 0 and x2 - x4 == 0:
                        cv2.line(frame, (x1 + topo_x_recorte, y1 + topo_y_recorte), (x2 + topo_x_recorte, y2 + topo_y_recorte), (0, 255, 0), 2)
                        cv2.line(frame, (x3 + topo_x_recorte, y3 + topo_y_recorte), (x4 + topo_x_recorte, y4 + topo_y_recorte), (0, 255, 0), 2)
                        
                        for i in circulos_np[0, :]:
                            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            
    cv2.imshow('Câmera', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

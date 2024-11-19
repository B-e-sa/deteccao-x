import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret = True
while ret:
    ret, frame = cap.read()

    corte_quadrado = None

    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bordas = cv2.Canny(gray_frame, 50, 200, None, 3)
        
        circles = cv2.HoughCircles(bordas,
                                   cv2.HOUGH_GRADIENT,
                                   dp=1,
                                   minDist=1000,
                                   param1=50,
                                   param2=30,
                                   minRadius=10,
                                   maxRadius=100)

        if circles is not None:
            circles_np = np.uint16(np.around(circles))
            
            for circles in circles_np:
                for circle in circles:
                    x, y, r = circle
                    
                    maior_lado_quadrado = int(r * np.sqrt(2))

                    quadrado_topo_x = x - maior_lado_quadrado // 2
                    quadrado_topo_y = y - maior_lado_quadrado // 2

                    corte_quadrado = gray_frame[quadrado_topo_y:quadrado_topo_y +
                                        maior_lado_quadrado, quadrado_topo_x:quadrado_topo_x + maior_lado_quadrado]

            for i in circles_np[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    if corte_quadrado is not None:
        cv2.imshow('Câmera', corte_quadrado)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

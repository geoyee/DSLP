# -- to test --
import cv2
from typing import List


WINDOW_WIDTH = 1920


def testShow(img_list: List, show_size: List[int]=[256, 256]) -> None:
    cols = WINDOW_WIDTH // show_size[0] - 1
    for i, img in enumerate(img_list):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, show_size)
        cv2.imshow(("im" + str(i)), img)
        cv2.moveWindow(("im" + str(i)), 256 * (i % cols), 256 * (i // cols))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
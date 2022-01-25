# -- to test --
import cv2
from typing import List


def testShow(img_list: List) -> None:
    for i, img in enumerate(img_list):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow(("im" + str(i)), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()